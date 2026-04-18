# ML Gym Tracker

End-to-end data pipeline for strength training analytics and machine learning.
This project transforms raw workout data (CSV) into a normalized relational database, enabling performance analysis and visualization via a FastAPI + React web interface.

---

## Project Goals

- [x] Parse raw workout data (TXT format)
- [x] Normalize and store structured data in CSV
- [x] Load normalized data from csv into Postgres database
- [x] Expose data via REST API (FastAPI)
- [x] Visualize training volume per exercise (React + Chart.js)
- [ ] Web interface to log new sessions
- [ ] Progressive Overload Forecasting using ML
- [ ] LLM-based adaptive workout plan generation
- [ ] Containerize and deploy as a production-ready service

---

## Architecture Overview

TXT → CSV → ETL → PostgreSQL → SQLAlchemy ORM → FastAPI → React

The system follows a normalized relational design to ensure scalability and analytical flexibility.

---

## Project Structure

GymTracker/
├── src/
│ ├── db/
│ │ ├── models.py # SQLAlchemy ORM models
│ ├── etl/
│ │ ├── parser.py # Unstructured txt → Serialized CSV
│ │ ├── normalizer.py # Serialized CSV → Normalized CSV
│ │ └── seed.py # CSV import into database
│ ├── gymtracker/
│ │ ├── config.py
│ │ └── main.py # FastAPI app
├── frontend/ # React + Vite
│ └── src/
│ └── App.jsx
├── docker-compose.yml
└── README.md

---

## Database Schema

![Database Diagram](docs/db_diagram.png)

### Tables

#### `workouts`

| Column       | Type         |
| ------------ | ------------ |
| id           | integer (PK) |
| workout_date | timestamp    |
| created_at   | timestamp    |

#### `exercises`

| Column      | Type             |
| ----------- | ---------------- |
| id          | integer (PK)     |
| name        | varchar (unique) |
| description | varchar          |

#### `workout_exercises`

| Column      | Type               |
| ----------- | ------------------ |
| id          | integer (PK)       |
| workout_id  | integer (FK)       |
| exercise_id | integer (FK)       |
| notes       | varchar (optional) |

#### `sets`

| Column              | Type         |
| ------------------- | ------------ |
| id                  | integer (PK) |
| workout_exercise_id | integer (FK) |
| set_number          | integer      |
| reps                | integer      |
| weight              | float        |

---

## API Endpoints

| Method | Endpoint                 | Opis                         |
| ------ | ------------------------ | ---------------------------- |
| GET    | `/exercises`             | Lista wszystkich ćwiczeń     |
| GET    | `/exercises/{id}/volume` | Objętość treningowa w czasie |

---

## Running the Project

### 1. Start the database

```bash
docker compose up -d
```

### 2. Import data from CSV

CSV format: `Date,Exercise,Set_Number,Weight,Reps`

```bash
python src/etl/seed.py
```

### 3. Start the backend

```bash
uvicorn src.gymtracker.main:app --reload
```

API available at: `http://localhost:8000`  
Docs at: `http://localhost:8000/docs`

### 4. Start the frontend

```bash
cd frontend
npm install   # first time only
npm run dev
```

App available at: `http://localhost:5173`

---

## Why This Design?

- Fully normalized (3NF)
- Atomic training data (1 set = 1 row)
- Scalable to multiple users
- Ready for analytics and ML
- Backend/API friendly
