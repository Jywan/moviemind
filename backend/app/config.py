from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    data_dir: str = "data"
    spark_master: str = "local[*]"
    spark_partitions: int = 4

    class Config:
        env_file = ".env"

settings = Settings()