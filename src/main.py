from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager

from apps import weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan, docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition"],
)

app.include_router(weather_router)
