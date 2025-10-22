from fastapi import UploadFile
from fastapi.responses import JSONResponse

import uuid

from database.config import database_engine_async
# from backend.templates.responses import TemplateResponsesNamespace

from database.oop.database_worker import DatabaseWorkerAsync
from database.orm import WeatherRequests

from loguru import logger

database_worker = DatabaseWorkerAsync(database_engine_async)

async def post_weather_implementation(
    lat: float,
    lon: float,
    temp: float,
    weather_main: str,
    wind_speed: float
) -> JSONResponse:
    data_to_insert = {
        "lat": lat,
        "lon": lon,
        "temp": temp,
        "weather_main": weather_main,
        "wind_speed": wind_speed
    }
    request: WeatherRequests = await database_worker.custom_insert(
        cls_to=WeatherRequests, data=[data_to_insert], returning=WeatherRequests, return_unpacked=True
    )
    logger.info(f"{request}")

    return JSONResponse(
        content={
            "status": "success",
            "result": 
                request.as_dict(
                    transform_dates=True
                ),
        },
        status_code=200
    )
