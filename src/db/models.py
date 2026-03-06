from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    workout_date = Column(DateTime)

    exercises = relationship("WorkoutExercise", back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name_normalized = Column(String, unique=True)
    muscle_group = Column(String)

    workouts = relationship("WorkoutExercise", back_populates="exercise")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    notes = Column(String)

    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workouts")

    sets = relationship("Set", back_populates="workout_exercise")


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    workout_exercise_id = Column(Integer, ForeignKey("workout_exercises.id"))

    set_number = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)

    workout_exercise = relationship("WorkoutExercise", back_populates="sets")
