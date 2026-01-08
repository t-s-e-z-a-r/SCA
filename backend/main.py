from fastapi import FastAPI
from .database import engine, Base
from .routes import cats, missions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Cat Agency API",
    description="Management system for spy cats, missions, and targets",
    version="1.0.0"
)

app.include_router(cats.router)
app.include_router(missions.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Spy Cat Agency API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
