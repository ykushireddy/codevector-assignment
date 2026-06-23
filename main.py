from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import Base
from database import engine
from routes import router

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
