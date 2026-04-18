# seed.py
import csv
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.db.models import Exercise, Set, Workout, WorkoutExercise

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/gym_db"
engine = create_engine(DATABASE_URL)


def seed(csv_path: str):
    with Session(engine) as session:
        workout_cache = {}  # date_str -> Workout
        exercise_cache = {}  # name -> Exercise

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                date = datetime.strptime(row["Date"], "%Y-%m-%d")
                exercise_name = row["Exercise"].strip()
                set_number = int(row["Set_Number"])
                weight = float(row["Weight"])
                reps = int(row["Reps"])

                # --- Workout (jeden per dzień) ---
                date_key = date.date().isoformat()
                if date_key not in workout_cache:
                    workout = Workout(workout_date=date, created_at=datetime.now())
                    session.add(workout)
                    session.flush()
                    workout_cache[date_key] = workout
                workout = workout_cache[date_key]

                # --- Exercise ---
                if exercise_name not in exercise_cache:
                    existing = session.execute(
                        select(Exercise).where(Exercise.name == exercise_name)
                    ).scalar_one_or_none()
                    if not existing:
                        existing = Exercise(name=exercise_name)
                        session.add(existing)
                        session.flush()
                    exercise_cache[exercise_name] = existing
                exercise = exercise_cache[exercise_name]

                # --- WorkoutExercise (jeden per trening + ćwiczenie) ---
                we_key = (date_key, exercise_name)
                if not hasattr(seed, "_we_cache"):
                    seed._we_cache = {}
                if we_key not in seed._we_cache:
                    we = WorkoutExercise(
                        workout_id=workout.id,
                        exercise_id=exercise.id,
                    )
                    session.add(we)
                    session.flush()
                    seed._we_cache[we_key] = we
                we = seed._we_cache[we_key]

                # --- Set ---
                s = Set(
                    workout_exercise_id=we.id,
                    set_number=set_number,
                    reps=reps,
                    weight=weight,
                )
                session.add(s)

        session.commit()
        print("Import zakończony.")


if __name__ == "__main__":
    seed("data/processed/normalized_notes.csv")  # podaj ścieżkę do swojego pliku
