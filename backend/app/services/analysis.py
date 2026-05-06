from app.spark import get_spark

def get_genre_stats():
    spark = get_spark()
    # TODO: 실제 분석 로직
    return {"message": "genre stats"}