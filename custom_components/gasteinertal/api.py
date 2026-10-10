"""API client and response parsing for Gasteinertal."""

from __future__ import annotations

import json
import math
import re
from typing import Any

from aiohttp import ClientSession

from .const import (
    MOUNTAIN_STATION_NAME,
    STATION_URL,
    WATER_STATION_NAME,
    WATER_URL,
)


async def async_fetch_data(session: ClientSession) -> dict[str, float]:
    """Fetch and parse both Gasteinertal measurements."""
    async with session.get(WATER_URL) as response:
        response.raise_for_status()
        water_data = await response.json(content_type=None)

    async with session.get(STATION_URL) as response:
        response.raise_for_status()
        station_text = await response.text()

    return {
        "water_level": parse_water_level(water_data),
        "mountain_temperature": parse_mountain_temperature(station_text),
    }


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


def _numeric_value(value: Any, description: str) -> float:
    """Return an API measurement as a finite numeric value."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise ValueError(f"Invalid {description}: {value!r}")
    return float(value)
