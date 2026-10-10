"""Constants for the Gasteinertal integration."""

from datetime import timedelta

DOMAIN = "gasteinertal"
PLATFORMS = ("sensor", "camera")
SCAN_INTERVAL = timedelta(minutes=10)

WATER_URL = "https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json"
STATION_URL = "https://www.salzburg.gv.at/lawine/Station.js"
WATER_STATION_NAME = "Bad Hofgastein"
MOUNTAIN_STATION_NAME = "badhofgastein_schlossalm"

CAMERAS = {
    "badhofgastein": {
        "name": "Bad Hofgastein",
        "url": "https://www.gasteinertal.com/webcam/badhofgastein/current/1200.jpg",
    },
    "haitzingalm": {
        "name": "Haitzingalm",
        "url": "https://www.gasteinertal.com/webcam/haitzingalm/current/1200.jpg",
    },
    "kuehhager": {
        "name": "Kühhager",
        "url": "https://www.gasteinertal.com/webcam/kuehhager/current/1200.jpg",
    },
    "badgastein": {
        "name": "Bad Gastein",
        "url": "https://www.gasteinertal.com/webcam/badgastein/current/1200.jpg",
    },
    "sportgastein": {
        "name": "Sportgastein",
        "url": "https://www.gasteinertal.com/webcam/sportgastein/current/1200.jpg",
    },
}
