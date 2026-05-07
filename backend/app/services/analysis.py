from pyspark.sql import functions as F
from app.spark import get_spark
from app.config import settings


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