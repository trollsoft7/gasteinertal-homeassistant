"""Sensors for Gasteinertal."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

SENSORS = (
    SensorEntityDescription(
        key="water_level",
        name="Wasserstand Gasteiner Ache",
        icon="mdi:waves-arrow-up",
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="mountain_temperature",
        name="Temperatur Schlossalm",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="bad_gastein_temperature",
        name="Temperatur Bad Gastein",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="bad_gastein_precipitation",
        name="Niederschlag letzte 10 Min Bad Gastein",
        icon="mdi:weather-rainy",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="bad_gastein_precipitation_ytd",
        name="Niederschlag seit Jahresbeginn Bad Gastein",
        icon="mdi:weather-pouring",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gasteinertal sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GasteinertalSensor(coordinator, description) for description in SENSORS
    )


class GasteinertalSensor(CoordinatorEntity, SensorEntity):
    """A sensor backed by the Gasteinertal data coordinator."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, Any]],
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"gasteinertal_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "gasteinertal")},
            name="Gasteinertal",
            manufacturer="Land Salzburg / Gasteinertal.com",
        )

    @property
    def native_value(self) -> float | None:
        """Return the latest measurement, if its source is available."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Mark GeoSphere sensors unavailable when their optional source fails."""
        availability_key = {
            "bad_gastein_temperature": "bad_gastein_10min_available",
            "bad_gastein_precipitation": "bad_gastein_10min_available",
            "bad_gastein_precipitation_ytd": "bad_gastein_precipitation_ytd_available",
        }.get(self.entity_description.key)
        if availability_key is not None:
            return super().available and self.coordinator.data.get(
                availability_key, True
            )
        return super().available

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return data completeness metadata for the yearly sum."""
        if self.entity_description.key != "bad_gastein_precipitation_ytd":
            return {}
        attributes = {"jahr": self.coordinator.data["precipitation_year"]}
        is_available = self.coordinator.data.get(
            "bad_gastein_precipitation_ytd_available", True
        )
        attributes["daten_verfügbar"] = is_available
        if is_available:
            attributes["fehlende_tageswerte"] = self.coordinator.data[
                "bad_gastein_precipitation_ytd_missing_days"
            ]
        return attributes
