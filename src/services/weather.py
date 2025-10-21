import httpx
import typing as tp
import os

class WeatherAPI:
    API_KEY = os.environ.get("OPEN_WEATHER_KEY")

    async def get_weather_by_loc(self,
                                 *,
                                 lat: float | None = None,
                                 lon: float | None = None,
                                 city: str | None = None) -> dict[str, tp.Any]:
        if lat is None and lon is None and city is None:
            raise ValueError(f"You should pass (lat, lon) or city")

        if lat is not None and lon is not None:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.get("https://api.openweathermap.org/data/2.5/weather", params={"lat": lat, "lon": lon, "appid": self.API_KEY, "units": "metric"})
        elif city is not None:
            async with httpx.AsyncClient(timeout=20) as client:
                lat, lon = await self._get_coords_by_city(city)
                resp = await client.get("https://api.openweathermap.org/data/2.5/weather", params={"lat": lat, "lon": lon, "appid": self.API_KEY, "units": "metric"})
        else:
            raise ValueError("You should pass both lat and lon")
        
        resp.raise_for_status()
        resp = resp.json()

        weather = {
            "weather_main": " ".join([x["main"] for x in resp["weather"]]),
            "temp": resp["main"]["temp"],
            "wind_speed": resp["wind"]["speed"]
        }

        return weather
        
                

    async def _get_coords_by_city(self, city: str) -> tuple[float, float]:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get("http://api.openweathermap.org/geo/1.0/direct", params={"q": city, "appid": self.API_KEY, "limit": 1})
            resp.raise_for_status()
            resp = resp.json()[0]

            return resp['lat'], resp['lon']
