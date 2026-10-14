import json
from pathlib import Path

HIGH_SCORE_FILE = Path(__file__).parent / "highscore.json"

def load_high_score():
    if not HIGH_SCORE_FILE.exists():
        return 0

    try:
        with HIGH_SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return max(0, int(data.get("high_score", 0)))

    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return 0

def save_high_score(score):
    data = {"high_score": score}

    with HIGH_SCORE_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)