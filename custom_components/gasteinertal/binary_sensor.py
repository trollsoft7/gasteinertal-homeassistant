"""Weather warning binary sensors for Gasteinertal."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, WEATHER_WARNINGS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up weather warning entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        WeatherWarningSensor(coordinator, key, warning["name"])
        for key, warning in WEATHER_WARNINGS.items()
    )


class WeatherWarningSensor(CoordinatorEntity, BinarySensorEntity):
    """Today's maximum ZAMG warning state for one municipality."""

    entity_description: BinarySensorEntityDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, Any]],
        municipality: str,
        name: str,
    ) -> None:
        super().__init__(coordinator)
        self._warning_key = f"warning_{municipality}"
        self.entity_description = BinarySensorEntityDescription(
            key=self._warning_key,
            name=f"Wetterwarnung heute {name}",
            icon="mdi:weather-lightning-rainy",
        )
        self._attr_unique_id = f"gasteinertal_{self._warning_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "gasteinertal")},
            name="Gasteinertal",
            manufacturer="Land Salzburg / GeoSphere Austria",
        )
        self._attr_extra_state_attributes = {
            "quelle": WEATHER_WARNINGS[municipality]["url"],
            "hinweis": "Zeigt den höchsten Warnlevel für den heutigen Tag.",
        }

    @property
    def available(self) -> bool:
        """Only report a state when the source returned a valid warning response."""
        return (
            super().available
            and self.coordinator.data.get(self._warning_key, {}).get("available", True)
        )

    @property
    def is_on(self) -> bool:
        """Return whether a warning is issued at any time today."""
        return self.coordinator.data[self._warning_key]["active"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the warning severity details."""
        warning = self.coordinator.data[self._warning_key]
        return {
            **(self._attr_extra_state_attributes or {}),
            "warnstufe": warning["level"],
            "warnfarbe": warning["level_name"],
        }
