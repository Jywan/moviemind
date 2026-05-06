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
