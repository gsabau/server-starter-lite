import json
import os

import httpx
from pydantic_ai import RunContext
from user_schema import Role


def users_api() -> str:
    return os.environ.get("USERS_API", "http://127.0.0.1:8000/api/v1")


async def read_users_api(path: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{users_api()}{path}", timeout=5.0)
    except httpx.HTTPError as e:
        return f"Users API unreachable: {e}"
    if res.status_code == 404:
        return "User not found"
    return res.text


def as_lines(text: str, role: str | None) -> str:
    """Turn a JSON list of users into one plain line per user. Optionally keep one role."""
    try:
        users = json.loads(text)
    except json.JSONDecodeError:
        return text
    if role:
        users = [u for u in users if u.get("role") == role]
    lines = [f"{len(users)} users" + (f" with role {role}" if role else "")]
    for user in users:
        lines.append(", ".join(f"{key}={value}" for key, value in user.items()))
    return "\n".join(lines)


async def list_users(ctx: RunContext, role: Role | None = None) -> str:
    """List users and count them. Use this for questions about several users, counts or groups.

    role: only users with this role. Leave empty for all users.
    """
    return as_lines(await read_users_api("/users"), role)


async def get_user(ctx: RunContext, user_id: int) -> str:
    """Get one user by id. Use this when the question names one id, for example user 3.

    user_id: the id of the user, a whole number.
    """
    # GET /api/v1/users/{user_id}
    return await read_users_api(f"/users/{user_id}")


def weather_word(code: int) -> str:
    if code == 0:
        return "clear"
    if code in (1, 2, 3):
        return "cloudy"
    if code in (45, 48):
        return "fog"
    if 51 <= code <= 67 or 80 <= code <= 82:
        return "rain"
    if 71 <= code <= 77 or 85 <= code <= 86:
        return "snow"
    if code >= 95:
        return "thunderstorm"
    return str(code)


async def get_weather(ctx: RunContext, city: str, days: int = 7) -> str:
    """Get the weather forecast for a city.

    city: city name, for example Vienna.
    days: number of forecast days, from 1 to 10. Default 7.
    """
    span = max(1, min(days, 10))
    try:
        async with httpx.AsyncClient() as client:
            found = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "de"},
                timeout=8.0,
            )
            found.raise_for_status()
            places = found.json().get("results") or []
            if not places:
                return "City not found."
            place = places[0]
            forecast = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
                    "timezone": "auto",
                    "forecast_days": span,
                },
                timeout=8.0,
            )
            forecast.raise_for_status()
    except httpx.HTTPError as e:
        return f"Weather API unreachable: {e}"

    daily = forecast.json()["daily"]
    lines = [f"{place['name']}, {place.get('country', '')}".rstrip(", ")]
    for i, day in enumerate(daily["time"]):
        low = daily["temperature_2m_min"][i]
        high = daily["temperature_2m_max"][i]
        rain = daily["precipitation_sum"][i]
        word = weather_word(int(daily["weather_code"][i]))
        lines.append(f"{day}: {low}–{high} °C, {rain} mm, {word}")
    return "\n".join(lines)
