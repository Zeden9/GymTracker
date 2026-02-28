import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

raw_df = pd.read_csv("data/processed/raw_notes.csv")

SET_PATTERN = re.compile(r"(?:(\d+)\s*x\s*)?(\d+)(?:\s*kg)?\s*x\s*(\d+)", re.IGNORECASE)


def normalize_entry(date: datetime, entry: str) -> List[Dict[str, Any]]:
    """
    Normalize single exercise entry into list of sets.
    Example:
        "dumbell curl 25xx10 30x8"
    """
    normalized_rows = []

    # 1. Dzielimy wejście na poszczególne ćwiczenia po przecinku
    exercises_blocks = entry.split(",")

    for block in exercises_blocks:
        block = block.strip()
        if not block:
            continue

        # 2. Wyciągamy nazwę ćwiczenia (wszystko do pierwszej cyfry w danym bloku)
        match_exercise = re.search(r"^([^0-9]+)", block)
        exercise_name = match_exercise.group(1).strip() if match_exercise else "Unknown"

        # 3. Szukamy wszystkich serii w obrębie tego jednego bloku
        sets = SET_PATTERN.finditer(block)

        exercise_set_counter = 1
        for m in sets:
            num_sets_str, weight_str, reps_str = m.groups()

            num_sets = int(num_sets_str) if num_sets_str else 1
            # Obsługa wag zmiennoprzecinkowych (np. 22.5)
            weight = float(weight_str) if "." in weight_str else int(weight_str)
            reps = int(reps_str)

            for _ in range(num_sets):
                normalized_rows.append(
                    {
                        "Date": date,
                        "Exercise": exercise_name,
                        "Set_Number": exercise_set_counter,  # Licznik wewnątrz ćwiczenia
                        "Weight": weight,
                        "Reps": reps,
                    }
                )
                exercise_set_counter += 1

    return normalized_rows


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    normalized_rows = []

    for _, row in df.iterrows():
        date = row["date"]
        entries = [e.strip() for e in row["data"].split(",") if e.strip()]

        for entry in entries:
            normalized_rows.extend(normalize_entry(date, entry))

    return pd.DataFrame(normalized_rows)


normalized_df = normalize_df(raw_df)

normalized_df.to_csv("data/processed/normalized_notes3.csv", index=False)
