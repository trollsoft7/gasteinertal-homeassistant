"""API client and response parsing for Gasteinertal."""

from __future__ import annotations

import asyncio
import json
import logging
import math
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from aiohttp import ClientSession

from .const import (
    GEOSPHERE_STATION_ID,
    GEOSPHERE_DAILY_URL,
    GEOSPHERE_URL,
    MOUNTAIN_STATION_NAME,
    STATION_URL,
    WATER_STATION_NAME,
    WATER_URL,
    WEATHER_WARNINGS,
)

_LOGGER = logging.getLogger(__name__)


async def async_fetch_data(session: ClientSession) -> dict[str, Any]:
    """Fetch and parse Gasteinertal measurements and weather warnings."""
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
    end = now.strftime("%Y-%m-%dT%H:%M")
    geosphere_params = {
        "parameters": "tl,rr",
        "start": start,
        "end": end,
        "station_ids": GEOSPHERE_STATION_ID,
    }
    year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    daily_params = {
        "parameters": "rr",
        "start": year_start.strftime("%Y-%m-%dT%H:%M"),
        "end": end,
        "station_ids": GEOSPHERE_STATION_ID,
    }

    water_data, station_text, warning_data = await asyncio.gather(
        _async_fetch_json(session, WATER_URL),
        _async_fetch_text(session, STATION_URL),
        _async_fetch_warnings(session),
    )

    async def fetch_10min_data() -> dict[str, Any]:
        """Fetch GeoSphere's 10-minute measurements without blocking other data."""
        try:
            data = await asyncio.wait_for(
                _async_fetch_json(session, GEOSPHERE_URL, params=geosphere_params),
                timeout=20,
            )
            return {
                **parse_geosphere_data(data),
                "bad_gastein_10min_available": True,
            }
        except (ClientError, TimeoutError, ValueError) as err:
            _LOGGER.warning("Unable to fetch 10-minute GeoSphere data: %s", err)
            return {
                "bad_gastein_temperature": None,
                "bad_gastein_precipitation": None,
                "bad_gastein_10min_available": False,
            }

    async def fetch_yearly_precipitation() -> dict[str, Any]:
        """Fetch the optional year-to-date precipitation total."""
        try:
            data = await asyncio.wait_for(
                _async_fetch_json(session, GEOSPHERE_DAILY_URL, params=daily_params),
                timeout=20,
            )
            return {
                **parse_yearly_precipitation(data),
                "bad_gastein_precipitation_ytd_available": True,
            }
        except (ClientError, TimeoutError, ValueError) as err:
            _LOGGER.warning("Unable to fetch yearly precipitation from GeoSphere: %s", err)
            return {
                "bad_gastein_precipitation_ytd": None,
                "bad_gastein_precipitation_ytd_missing_days": None,
                "bad_gastein_precipitation_ytd_available": False,
            }

    weather_data, yearly_precipitation = await asyncio.gather(
        fetch_10min_data(), fetch_yearly_precipitation()
    )

    return {
        "water_level": parse_water_level(water_data),
        "mountain_temperature": parse_mountain_temperature(station_text),
        "precipitation_year": now.year,
        **weather_data,
        **yearly_precipitation,
        **warning_data,
    }


async def _async_fetch_json(
    session: ClientSession, url: str, *, params: dict[str, str] | None = None
) -> Any:
    """Fetch a JSON response."""
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json(content_type=None)


async def _async_fetch_text(session: ClientSession, url: str) -> str:
    """Fetch a text response."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def _async_fetch_warnings(session: ClientSession) -> dict[str, dict[str, Any]]:
    """Fetch today's warning level for each Gasteinertal municipality."""

    async def fetch_warning(key: str, url: str) -> tuple[str, dict[str, Any]]:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
            parsed = parse_warning_level(text)
            parsed["available"] = True
            return key, parsed
        except Exception as err:
            # A changed warning page must not take down unrelated sensors.
            return key, {
                "active": False,
                "level": None,
                "level_name": "unavailable",
                "available": False,
                "error": str(err),
            }

    results = await asyncio.gather(
        *(
            fetch_warning(key, warning["url"])
            for key, warning in WEATHER_WARNINGS.items()
        )
    )
    return {f"warning_{key}": warning for key, warning in results}


def parse_water_level(data: Any) -> float:
    """Extract the Bad Hofgastein water level in centimetres."""
    if not isinstance(data, list):
        raise ValueError("Water data must be a list")

    station = next(
        (
            item
            for item in data
            if isinstance(item, dict) and item.get("name") == WATER_STATION_NAME
        ),
        None,
    )
    if station is None:
        raise ValueError(f"Water station {WATER_STATION_NAME!r} was not found")

    try:
        value = station["values"]["W"]["15m.Cmd.WiskiWeb"]["v"]
    except (KeyError, TypeError) as err:
        raise ValueError("Water level is missing from the response") from err

    return _numeric_value(value, "water level")


def parse_mountain_temperature(text: str) -> float:
    """Extract the Schlossalm air temperature in degrees Celsius."""
    json_text = re.sub(r"^\s*stationData\s*=\s*", "", text, count=1)
    json_text = json_text.strip().removesuffix(";").strip()
    try:
        station_data = json.loads(json_text)
    except json.JSONDecodeError as err:
        raise ValueError("Station.js did not contain valid JSON") from err

    if not isinstance(station_data, dict):
        raise ValueError("Station data must be an object")

    for stations in station_data.values():
        if not isinstance(stations, list):
            continue
        for station in stations:
            if (
                isinstance(station, dict)
                and station.get("name") == MOUNTAIN_STATION_NAME
            ):
                try:
                    value = station["measuredData"]["values"]["LT"]
                except (KeyError, TypeError) as err:
                    raise ValueError("Mountain temperature is missing") from err
                return _numeric_value(value, "mountain temperature")

    raise ValueError(f"Mountain station {MOUNTAIN_STATION_NAME!r} was not found")


def parse_geosphere_data(data: Any) -> dict[str, float]:
    """Extract the latest temperature and precipitation from GeoSphere data."""
    if not isinstance(data, dict) or not isinstance(data.get("features"), list):
        raise ValueError("GeoSphere data must contain a features list")

    properties = next(
        (
            item["properties"]
            for item in data["features"]
            if isinstance(item, dict)
            and isinstance(item.get("properties"), dict)
            and item["properties"].get("station") == int(GEOSPHERE_STATION_ID)
        ),
        None,
    )
    if properties is None:
        raise ValueError("GeoSphere station Bad Gastein was not found")

    parameters = properties.get("parameters", {})
    return {
        "bad_gastein_temperature": _latest_numeric_value(
            parameters, "tl", "Bad Gastein temperature"
        ),
        "bad_gastein_precipitation": _latest_numeric_value(
            parameters, "rr", "Bad Gastein precipitation"
        ),
    }


def parse_yearly_precipitation(data: Any) -> dict[str, int | float]:
    """Sum valid daily precipitation values from the start of the year."""
    if not isinstance(data, dict) or not isinstance(data.get("features"), list):
        raise ValueError("GeoSphere daily data must contain a features list")

    properties = next(
        (
            item["properties"]
            for item in data["features"]
            if isinstance(item, dict)
            and isinstance(item.get("properties"), dict)
            and item["properties"].get("station") == int(GEOSPHERE_STATION_ID)
        ),
        None,
    )
    if properties is None:
        raise ValueError("GeoSphere station Bad Gastein was not found in daily data")

    try:
        values = properties["parameters"]["rr"]["data"]
    except (KeyError, TypeError) as err:
        raise ValueError("Yearly precipitation is missing from the response") from err
    if not isinstance(values, list):
        raise ValueError("Invalid daily precipitation series")

    valid_values = []
    for value in values:
        if value is None or (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and value < 0
        ):
            continue
        valid_values.append(_numeric_value(value, "daily precipitation"))
    if not valid_values:
        raise ValueError("No valid daily precipitation values in the response")

    return {
        "bad_gastein_precipitation_ytd": math.fsum(valid_values),
        "bad_gastein_precipitation_ytd_missing_days": len(values) - len(valid_values),
    }


def _latest_numeric_value(
    parameters: dict[str, Any], key: str, description: str
) -> float:
    """Return the most recent numeric value from a GeoSphere time series."""
    try:
        values = parameters[key]["data"]
    except (KeyError, TypeError) as err:
        raise ValueError(f"{description} is missing from the response") from err
    if not isinstance(values, list):
        raise ValueError(f"Invalid {description} series")

    for value in reversed(values):
        if value is not None:
            return _numeric_value(value, description)
    raise ValueError(f"No valid {description} value in the response")


def parse_warning_level(text: str) -> dict[str, Any]:
    """Parse the maximum warning level shown for today on a ZAMG page."""
    table_match = re.search(
        r"<table\b[^>]*\bid=[\"']daymax[\"'][^>]*>(.*?)</table>",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if table_match is None:
        raise ValueError("ZAMG warning page did not contain the day-level table")

    row_match = re.search(
        r"<tr\b[^>]*\bclass=[\"'][^\"']*\bwarnlevels\b[^\"']*[\"'][^>]*>(.*?)</tr>",
        table_match.group(1),
        re.IGNORECASE | re.DOTALL,
    )
    if row_match is None:
        raise ValueError("ZAMG warning page did not contain today's warning level")

    cell_match = re.search(
        r"<td\b[^>]*\bclass=[\"']([^\"']*)[\"'][^>]*>",
        row_match.group(1),
        re.IGNORECASE | re.DOTALL,
    )
    if cell_match is None:
        raise ValueError("ZAMG warning level is missing")

    classes = cell_match.group(1).lower().split()
    level_by_color = {"green": 0, "yellow": 1, "orange": 2, "red": 3}
    color = next((name for name in level_by_color if name in classes), None)
    if color is None:
        raise ValueError(f"Unknown ZAMG warning level classes: {classes}")

    return {
        "active": level_by_color[color] > 0,
        "level": level_by_color[color],
        "level_name": color,
    }


def _numeric_value(value: Any, description: str) -> float:
    """Return an API measurement as a finite numeric value."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise ValueError(f"Invalid {description}: {value!r}")
    return float(value)
