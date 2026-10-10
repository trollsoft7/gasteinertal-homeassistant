"""Webcam entities for Gasteinertal."""

from __future__ import annotations

from aiohttp import ClientError, ClientTimeout
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CAMERAS, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gasteinertal webcam entities."""
    async_add_entities(
        GasteinertalCamera(camera_id, camera_data)
        for camera_id, camera_data in CAMERAS.items()
    )


class GasteinertalCamera(Camera):
    """A webcam image fetched from gasteinertal.com."""

    _attr_content_type = "image/jpeg"

    def __init__(self, camera_id: str, data: dict) -> None:
        super().__init__()
        self._url = data["url"]
        self._attr_name = data["name"]
        self._attr_unique_id = f"gasteinertal_{camera_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "gasteinertal")},
            name="Gasteinertal",
            manufacturer="Land Salzburg / Gasteinertal.com",
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return the latest webcam image."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                self._url, timeout=ClientTimeout(total=20)
            ) as response:
                response.raise_for_status()
                return await response.read()
        except (ClientError, TimeoutError) as err:
            raise HomeAssistantError(
                f"Unable to fetch the {self._attr_name} webcam image"
            ) from err
