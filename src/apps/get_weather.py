from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from templates.schemas.weather_responses import Weather
from services.weather import WeatherAPI
from database.core.post_weather_core import post_weather_implementation
from loguru import logger

weather_router = APIRouter()

@weather_router.get("/weather", summary="Погода по городу или координатам", response_model=Weather)
async def get_weather(city: Annotated[str | None, Query(description="Название города")] = None,
                      lat: Annotated[float | None, Query(ge=-90, le=90, description="Широта")] = None,
                      lon: Annotated[float | None, Query(ge=-180, le=180, description="Долгота")] = None):
    """
    Input:
    - Должен быть указан "city" ИЛИ *оба* "lat" и "lon".
    - Если указаны и город, и координаты — используются координаты.
    Output:
    temperature: float, температура в Цельсиях.
    wind_speed: float, скорость ветра в м/с.
    weather_main: str, обшая характеристика погоды.
    """
    has_coords = lat is not None and lon is not None
    has_city = city is not None and city.strip() != ""
    if not (has_coords or has_city):
        raise HTTPException(
            400,
            detail="Укажите либо city, либо пару lat+lon.",
        )
    
    logger.info(f"Query parameters: {city=}, {lat=}, {lon=}")
    external_api = WeatherAPI()

    try:
        cur_weather = await external_api.get_weather_by_loc(lat=lat, lon=lon, city=city)
        logger.info(f"Response from core {cur_weather}")
        await post_weather_implementation(
            lat=cur_weather["lat"],
            lon=cur_weather["lon"],
            temp=cur_weather["temp"],
            wind_speed=cur_weather["wind_speed"],
            weather_main=cur_weather["weather_main"]
        )

        return Weather(
            temperature=cur_weather["temp"],
            wind_speed=cur_weather["wind_speed"],
            weather_main=cur_weather["weather_main"]
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            500,
            detail=str(e),
        )       
