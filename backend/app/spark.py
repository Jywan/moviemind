from pyspark.sql import SparkSession
from app.config import settings

_spark = None


def get_spark() -> SparkSession:
    global _spark
    if _spark is None:
        _spark = (
            SparkSession.builder
            .appName("MovieAnalysis")
            .master(settings.spark_master)
            .config("spark.sql.shuffle.partitions", settings.spark_partitions)
            .config("spark.sql.ansi.enabled", "false")
            .config("spark.driver.memory", "4g")
            .config("spark.executor.memory", "4g")
            .getOrCreate()
        )
        _spark.sparkContext.setLogLevel("WARN")
    return _spark