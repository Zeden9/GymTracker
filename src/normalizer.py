import re

import pandas as pd

raw_df = pd.read_csv("data/processed/raw_notes.csv")


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    SET_PATTERN = re.compile(
        r"(?:(\d+)(?:\s*kg)?\s*x\s*)?(\d+)\s*x\s*(\d+)(?:\s*-\s*(\d+))?"
    )
    normalized_rows = []

    for _, row in df.iterrows():
        date = row["date"]
        entries = [e.strip() for e in row["data"].split(",") if e.strip()]

        for entry in entries:
            match_exercise = re.search(r"^[^\d]+", entry)
            exercise_name = (
                match_exercise.group(0).strip() if match_exercise else "Unknown"
            )

            sets = SET_PATTERN.finditer(entry)

            for i, m in enumerate(sets, 1):
                res = m.groups()
                # Group 1: Set, 2: reps, 3: weight
                reps = int(res[1]) if res[1] else None
                weight = int(res[2]) if res[2] else None

                normalized_rows.append(
                    {
                        "Date": date,
                        "Exercise": exercise_name,
                        "Set_Number": i,
                        "Reps": reps,
                        "Weight": weight,
                    }
                )

    return pd.DataFrame(normalized_rows)


normalized_df = normalize_df(raw_df)

normalized_df.to_csv("data/processed/normalized_notes.csv", index=False)
