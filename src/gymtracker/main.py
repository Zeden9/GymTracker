from fastapi import FastAPI

from gymtracker.api.routes import router

app = FastAPI(title="Gym Tracker API")

app.include_router(router)
