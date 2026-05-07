from pyspark.ml.recommendation import ALS
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, FloatType

from app.spark import get_spark
from app.config import settings

_als_model = None


def get_genre_stats():
    spark = get_spark()
    df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    df_exploded = (
        df.select("title", "genres", "vote_average")
        .withColumn("vote_average", F.col("vote_average").cast("float"))
        .filter((F.col("vote_average") > 0) & (F.col("vote_average") <= 10))
        .withColumn("genre", F.explode(F.from_json(F.col("genres"), "array<struct<id:int,name:string>>")))
        .withColumn("genre_name", F.col("genre.name"))
    )

    result = (
        df_exploded.groupBy("genre_name")
        .agg(
            F.round(F.avg("vote_average"), 2).alias("avg_rating"),
            F.count("title").alias("movie_count"),
        )
        .orderBy(F.desc("movie_count"))
        .collect()
    )

    return [row.asDict() for row in result]


def get_year_trend():
    spark = get_spark()
    df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    result = (
        df.select("release_date", "vote_average", "revenue")
        .withColumn("year", F.year(F.to_date(F.col("release_date"), "yyyy-MM-dd")))
        .withColumn("vote_average", F.col("vote_average").cast("float"))
        .withColumn("revenue", F.col("revenue").cast("long"))
        .filter(
            F.col("year").isNotNull()
            & (F.col("vote_average") > 0) & (F.col("vote_average") <= 10)
            & (F.col("revenue") > 0)
        )
        .groupBy("year")
        .agg(
            F.count("*").alias("movie_count"),
            F.round(F.avg("vote_average"), 2).alias("avg_rating"),
            F.round(F.avg("revenue"), 0).alias("avg_revenue"),
        )
        .orderBy("year")
        .collect()
    )

    return [row.asDict() for row in result]


def get_top_directors(limit: int = 10):
    spark = get_spark()
    credits_df = spark.read.csv(
        f"{settings.data_dir}/credits.csv",
        header=True,
        inferSchema=False,
    )
    movies_df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    directors = (
        credits_df
        .select("id", "crew")
        .withColumn("member", F.explode(F.from_json(F.col("crew"), "array<struct<job:string,name:string>>")))
        .filter(F.col("member.job") == "Director")
        .select(F.col("id"), F.col("member.name").alias("director"))
    )

    movies = (
        movies_df
        .select("id", "vote_average")
        .withColumn("vote_average", F.col("vote_average").cast("float"))
        .filter((F.col("vote_average") > 0) & (F.col("vote_average") <= 10))
    )

    result = (
        directors.join(movies, on="id")
        .groupBy("director")
        .agg(
            F.count("*").alias("movie_count"),
            F.round(F.avg("vote_average"), 2).alias("avg_rating"),
        )
        .filter(F.col("movie_count") >= 5)
        .orderBy(F.desc("avg_rating"))
        .limit(limit)
        .collect()
    )

    return [row.asDict() for row in result]


def get_top_actors(limit: int = 10):
    spark = get_spark()
    credits_df = spark.read.csv(
        f"{settings.data_dir}/credits.csv",
        header=True,
        inferSchema=False,
    )
    movies_df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    actors = (
        credits_df
        .select("id", "cast")
        .withColumn("member", F.explode(F.from_json(F.col("cast"), "array<struct<name:string,order:int>>")))
        .filter(F.col("member.order") < 3)
        .select(F.col("id"), F.col("member.name").alias("actor"))
    )

    movies = (
        movies_df
        .select("id", "vote_average")
        .withColumn("vote_average", F.col("vote_average").cast("float"))
        .filter((F.col("vote_average") > 0) & (F.col("vote_average") <= 10))
    )

    result = (
        actors.join(movies, on="id")
        .groupBy("actor")
        .agg(
            F.count("*").alias("movie_count"),
            F.round(F.avg("vote_average"), 2).alias("avg_rating"),
        )
        .filter(F.col("movie_count") >= 5)
        .orderBy(F.desc("avg_rating"))
        .limit(limit)
        .collect()
    )

    return [row.asDict() for row in result]


def get_roi_analysis(limit: int = 10):
    spark = get_spark()
    df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    result = (
        df.select("title", "budget", "revenue", "release_date")
        .withColumn("budget", F.col("budget").cast("long"))
        .withColumn("revenue", F.col("revenue").cast("long"))
        .withColumn("year", F.year(F.to_date(F.col("release_date"), "yyyy-MM-dd")))
        .filter(
            (F.col("budget") > 1_000_000)
            & (F.col("revenue") > 0)
        )
        .withColumn("roi", F.round((F.col("revenue") - F.col("budget")) / F.col("budget") * 100, 2))
        .select("title", "year", "budget", "revenue", "roi")
        .orderBy(F.desc("roi"))
        .limit(limit)
        .collect()
    )

    return [row.asDict() for row in result]


def get_similar_movies(movie_id:int, limit: int = 10):
    spark = get_spark()
    keywords_df = spark.read.csv(
        f"{settings.data_dir}/keywords.csv",
        header=True,
        inferSchema=False,
    )
    movies_df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    keywords = (
        keywords_df
        .withColumn("keyword", F.explode(F.from_json(F.col("keywords"), "array<struct<id:int,name:string>>")))
        .withColumn("keyword_name", F.col("keyword.name"))
        .groupBy("id")
        .agg(F.collect_set("keyword_name").alias("keywords"))
    )

    target = keywords.filter(F.col("id") == str(movie_id)).first()
    if not target:
        return []
    
    target_keywords = set(target["keywords"])

    candidates = keywords.filter(F.col("id") != str(movie_id)).collect()

    scores = []
    for row in candidates:
        other_keywords = set(row["keywords"])
        union = target_keywords | other_keywords
        if not union:
            continue
        score = len(target_keywords & other_keywords) / len(union)
        scores.append((row["id"], round(score, 4)))

    top_ids = [r[0] for r in sorted(scores, key=lambda x: -x[1])[:limit]]

    movies = (
        movies_df
        .select("id", "title", "vote_average", "release_date")
        .filter(F.col("id").isin(top_ids))
        .withColumn("vote_average", F.round(F.col("vote_average").cast("double"), 2))
        .filter(
            F.col("title").isNotNull()
            & F.col("vote_average").isNotNull()
            & F.col("release_date").rlike(r"^\d{4}-\d{2}-\d{2}$")
        )
        .collect()
    )

    return [row.asDict() for row in movies]


def _get_als_model():
    global _als_model
    if _als_model is not None:
        return _als_model
    
    spark = get_spark()
    df = spark.read.csv(
        f"{settings.data_dir}/ratings.csv",
        header=True,
        inferSchema=False,
    )

    ratings = (
        df.select(
            F.col("userId").cast(IntegerType()),
            F.col("movieId").cast(IntegerType()),
            F.col("rating").cast(FloatType()),
        )
        .filter(F.col("userId").isNotNull() & F.col("movieId").isNotNull())
        .sample(fraction=0.2, seed=42)
    )

    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="userId",
        itemCol="movieId",
        ratingCol="rating",
        coldStartStrategy="drop",
    )

    _als_model = als.fit(ratings)
    return _als_model


def get_user_recommendations(user_id: int, limit: int = 10):
    spark = get_spark()
    model = _get_als_model()

    movies_df = spark.read.csv(
        f"{settings.data_dir}/movies_metadata.csv",
        header=True,
        inferSchema=False,
    )

    user_df = spark.createDataFrame([(user_id,)], ["userId"])
    recs = model.recommendForUserSubset(user_df, limit)

    movie_ids = (
        recs.select(F.explode("recommendations").alias("rec"))
        .select(
            F.col("rec.movieId").alias("movieId"),
            F.round(F.col("rec.rating").cast("double"), 2).alias("predicted_rating"),
        )
    )

    movies = (
        movies_df
        .select(
            F.col("id").cast("integer").alias("id"),
            "title", "vote_average", "release_date"
        )
        .withColumn("vote_average", F.round(F.col("vote_average").cast("double"), 2))
        .filter(
            F.col("title").isNotNull()
            & F.col("release_date").rlike(r"^\d{4}-\d{2}-\d{2}$")
        )
    )

    result = (
        movie_ids.join(movies, movie_ids.movieId == movies.id)
        .select("title", "release_date", "vote_average", "predicted_rating")
        .collect()
    )

    return [row.asDict() for row in result]