from read_parquet_from_blob import read_parquet_from_blob
from emotion_generator import generate_emotion_scores

DATASET_NAME = "Anxiety"

RESUME_COMMENT_ID = None

BATCH_SIZE = 1000


def main():

    df = read_parquet_from_blob(DATASET_NAME)

    generate_emotion_scores(
        df=df,
        comment_id=RESUME_COMMENT_ID,
        batch_size=BATCH_SIZE,
        dataset_name=DATASET_NAME
    )


if __name__ == "__main__":
    main()