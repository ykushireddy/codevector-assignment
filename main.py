from fastapi import FastAPI

from .database import Base
from .database import engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "healthy"
    }