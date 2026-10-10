"""Sensors for Gasteinertal."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength, UnitOfTemperature
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
        coordinator: DataUpdateCoordinator[dict[str, float]],
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
    def native_value(self) -> float:
        """Return the latest measurement."""
        return self.coordinator.data[self.entity_description.key]
