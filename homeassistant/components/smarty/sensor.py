"""Support for Salda Smarty XP/XV Ventilation Unit Sensors."""
from __future__ import annotations

import datetime as dt
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.util.dt as dt_util

from . import DOMAIN, SIGNAL_UPDATE_SMARTY

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Smarty Sensor Platform."""
    smarty = hass.data[DOMAIN]["api"]
    name = hass.data[DOMAIN]["name"]

    sensors = [
        SupplyAirTemperatureSensor(name, smarty),
        ExtractAirTemperatureSensor(name, smarty),
        OutdoorAirTemperatureSensor(name, smarty),
        SupplyFanSpeedSensor(name, smarty),
        ExtractFanSpeedSensor(name, smarty),
        FilterDaysLeftSensor(name, smarty),
    ]

    async_add_entities(sensors, True)


class SmartySensor(SensorEntity):
    """Representation of a Smarty Sensor."""

    _attr_should_poll = False

    def __init__(
        self, name: str, device_class: str, smarty, unit_of_measurement: str = ""
    ):
        """Initialize the entity."""
        self._attr_name = name
        self._attr_native_value = None
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._smarty = smarty

    async def async_added_to_hass(self):
        """Call to update."""
        async_dispatcher_connect(self.hass, SIGNAL_UPDATE_SMARTY, self._update_callback)

    @callback
    def _update_callback(self):
        """Call update method."""
        self.async_schedule_update_ha_state(True)


class SupplyAirTemperatureSensor(SmartySensor):
    """Supply Air Temperature Sensor."""

    def __init__(self, name, smarty):
        """Supply Air Temperature Init."""
        super().__init__(
            name=f"{name} Supply Air Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit_of_measurement=TEMP_CELSIUS,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_native_value = self._smarty.supply_air_temperature


class ExtractAirTemperatureSensor(SmartySensor):
    """Extract Air Temperature Sensor."""

    def __init__(self, name, smarty):
        """Supply Air Temperature Init."""
        super().__init__(
            name=f"{name} Extract Air Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit_of_measurement=TEMP_CELSIUS,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_native_value = self._smarty.extract_air_temperature


class OutdoorAirTemperatureSensor(SmartySensor):
    """Extract Air Temperature Sensor."""

    def __init__(self, name, smarty):
        """Outdoor Air Temperature Init."""
        super().__init__(
            name=f"{name} Outdoor Air Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            unit_of_measurement=TEMP_CELSIUS,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_native_value = self._smarty.outdoor_air_temperature


class SupplyFanSpeedSensor(SmartySensor):
    """Supply Fan Speed RPM."""

    def __init__(self, name, smarty):
        """Supply Fan Speed RPM Init."""
        super().__init__(
            name=f"{name} Supply Fan Speed",
            device_class=None,
            unit_of_measurement=None,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_native_value = self._smarty.supply_fan_speed


class ExtractFanSpeedSensor(SmartySensor):
    """Extract Fan Speed RPM."""

    def __init__(self, name, smarty):
        """Extract Fan Speed RPM Init."""
        super().__init__(
            name=f"{name} Extract Fan Speed",
            device_class=None,
            unit_of_measurement=None,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_native_value = self._smarty.extract_fan_speed


class FilterDaysLeftSensor(SmartySensor):
    """Filter Days Left."""

    def __init__(self, name, smarty):
        """Filter Days Left Init."""
        super().__init__(
            name=f"{name} Filter Days Left",
            device_class=SensorDeviceClass.TIMESTAMP,
            unit_of_measurement=None,
            smarty=smarty,
        )
        self._days_left = 91

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        days_left = self._smarty.filter_timer
        if days_left is not None and days_left != self._days_left:
            self._attr_native_value = dt_util.now() + dt.timedelta(days=days_left)
            self._days_left = days_left
