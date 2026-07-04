import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "duelker/samo-goemotions-deberta-v3-large"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.to(device)
model.eval()

GOEMOTIONS_LABELS = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral"
]

emotion_labels = {
    i: GOEMOTIONS_LABELS[i]
    for i in range(len(GOEMOTIONS_LABELS))
}


def get_emotion_scores(text: str) -> dict:

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    scores = torch.sigmoid(outputs.logits)[0]

    return {
        emotion_labels[i]: float(scores[i])
        for i in range(len(scores))
    }