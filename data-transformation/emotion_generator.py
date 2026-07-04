import logging
import pandas as pd

from emotion_model import (
    get_emotion_scores,
    GOEMOTIONS_LABELS
)
from append_data_lake import append_emotion_to_datalake


def generate_emotion_scores(
    df: pd.DataFrame,
    comment_id: str | None = None,
    batch_size: int = 1000
) -> None:

    logging.basicConfig(
        filename="logs.txt",
        level=logging.INFO,
        format="%(asctime)s | %(message)s"
    )

    if comment_id is not None:

        if comment_id not in df["comment_id"].values:
            raise ValueError(
                f"comment_id '{comment_id}' not found."
            )

        start_idx = (
            df.index[df["comment_id"] == comment_id][0] + 1
        )

        df = df.iloc[start_idx:].reset_index(drop=True)

        print(f"Resuming after comment_id={comment_id}")

    total = len(df)
    emotion_rows = []

    print(f"Processing {total} comments...")

    for i, (_, row) in enumerate(df.iterrows(), start=1):

        current_comment_id = row["comment_id"]
        comment = str(row["comment_text"])

        try:

            scores = get_emotion_scores(comment)

            emotion_rows.append({
                "comment_id": current_comment_id,
                "comment_text": comment,
                **scores
            })

            logging.info(f"{current_comment_id} | DONE")

        except Exception as e:

            logging.error(
                f"{current_comment_id} | FAILED | {e}"
            )

            continue

        if len(emotion_rows) >= batch_size:

            emotion_df = pd.DataFrame(emotion_rows)

            append_emotion_to_datalake(emotion_df)

            print(
                f"Uploaded batch "
                f"({i}/{total})"
            )

            emotion_rows = []

        if i % 100 == 0:

            print(
                f"Processed {i}/{total}"
            )

    if emotion_rows:

        emotion_df = pd.DataFrame(emotion_rows)

        append_emotion_to_datalake(emotion_df)

        print(
            f"Uploaded final batch "
            f"({len(emotion_df)} rows)"
        )

    print("Finished processing.")
