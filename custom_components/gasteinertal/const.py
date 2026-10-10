"""Constants for the Gasteinertal integration."""

from datetime import timedelta

DOMAIN = "gasteinertal"
PLATFORMS = ("sensor", "binary_sensor", "camera")
SCAN_INTERVAL = timedelta(minutes=10)

WATER_URL = "https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json"
STATION_URL = "https://www.salzburg.gv.at/lawine/Station.js"
GEOSPHERE_URL = (
    "https://dataset.api.hub.geosphere.at/v1/station/historical/"
    "klima-v2-10min"
)
GEOSPHERE_STATION_ID = "7"
WATER_STATION_NAME = "Bad Hofgastein"
MOUNTAIN_STATION_NAME = "badhofgastein_schlossalm"

WEATHER_WARNINGS = {
    "badgastein": {
        "name": "Bad Gastein",
        "url": (
            "http://warnungen.zamg.ac.at/html/de/heute/alle/at/salzburg/"
            "sankt_johann_im_pongau/badgastein/"
        ),
    },
    "badhofgastein": {
        "name": "Bad Hofgastein",
        "url": (
            "http://warnungen.zamg.ac.at/html/de/heute/alle/at/salzburg/"
            "sankt_johann_im_pongau/bad_hofgastein/"
        ),
    },
    "dorfgastein": {
        "name": "Dorfgastein",
        "url": (
            "http://warnungen.zamg.ac.at/html/de/heute/alle/at/salzburg/"
            "sankt_johann_im_pongau/dorfgastein/"
        ),
    },
}

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
    "sportgastein_siglitztal": {
        "name": "Sportgastein Siglitztal",
        "url": "https://www.gasteinertal.com/webcam/sportgastein2/current/1200.jpg",
    },
    "badgastein_zentrum": {
        "name": "Bad Gastein Zentrum",
        "url": "https://www.gasteinertal.com/webcam/badgastein2/current/1200.jpg",
    },
    "schlossalm_snowcam": {
        "name": "Schlossalm Snowcam",
        "url": "https://camhost1.gasteinertal.com/webcam/snowcam/current/1200.jpg",
    },
    "golfplatz": {
        "name": "Golfplatz Bad Gastein",
        "url": "https://www.gasteinertal.com/webcam/golfgastein/current/1200.jpg",
    },
    "wasserfall": {
        "name": "Wasserfall Bad Gastein",
        "url": "https://www.gasteinertal.com/webcam/wasserfall/current/816.jpg",
    },
    "jungeralm": {
        "name": "Jungeralm Stubnerkogel",
        "url": "https://www.gasteinertal.com/webcam/jungeralm.jpg",
    },
    "dorfgastein_talabfahrt": {
        "name": "Dorfgastein Talabfahrt",
        "url": "https://camhost1.gasteinertal.com/webcam/hauserbauer/current/1200.jpg",
    },
    "angertal": {
        "name": "Angertal Skizentrum",
        "url": "https://www.gasteinertal.com/webcam/angertal/current/1200.jpg",
    },
}
