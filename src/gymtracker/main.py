from datetime import date
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Date, create_engine, func, select
from sqlalchemy.orm import Session

from src.db.models import Exercise, Set, Workout, WorkoutExercise

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/gym_db"
engine = create_engine(DATABASE_URL)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_db():
    with Session(engine) as session:
        yield session


# --- Schematy odpowiedzi ---


class ExerciseOut(BaseModel):
    id: int
    name: str


class VolumePoint(BaseModel):
    workout_date: date
    volume: float  # suma (reps × weight) dla danego treningu


# --- Endpointy ---


@app.get("/exercises", response_model=List[ExerciseOut])
def list_exercises(db: Session = Depends(get_db)):
    rows = db.execute(select(Exercise).order_by(Exercise.name)).scalars().all()
    return rows


@app.get("/exercises/{exercise_id}/volume", response_model=List[VolumePoint])
def exercise_volume(exercise_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(
            Workout.workout_date.cast(Date).label("workout_date"),
            func.sum(Set.reps * Set.weight).label("volume"),
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .join(Set, Set.workout_exercise_id == WorkoutExercise.id)
        .where(WorkoutExercise.exercise_id == exercise_id)
        .group_by(Workout.workout_date.cast(Date))
        .order_by(Workout.workout_date.cast(Date))
    )
    rows = db.execute(stmt).all()
    return [{"workout_date": r.workout_date, "volume": float(r.volume)} for r in rows]
