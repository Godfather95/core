"""Support for Salda Smarty XP/XV Ventilation Unit Binary Sensors."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import DOMAIN, SIGNAL_UPDATE_SMARTY

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Smarty Binary Sensor Platform."""
    smarty = hass.data[DOMAIN]["api"]
    name = hass.data[DOMAIN]["name"]

    sensors = [
        AlarmSensor(name, smarty),
        WarningSensor(name, smarty),
        BoostSensor(name, smarty),
    ]

    async_add_entities(sensors, True)


class SmartyBinarySensor(BinarySensorEntity):
    """Representation of a Smarty Binary Sensor."""

    _attr_should_poll = False

    def __init__(self, name, device_class, smarty):
        """Initialize the entity."""
        self._attr_name = name
        self._attr_device_class = device_class
        self._smarty = smarty

    async def async_added_to_hass(self):
        """Call to update."""
        async_dispatcher_connect(self.hass, SIGNAL_UPDATE_SMARTY, self._update_callback)

    @callback
    def _update_callback(self):
        """Call update method."""
        self.async_schedule_update_ha_state(True)


class BoostSensor(SmartyBinarySensor):
    """Boost State Binary Sensor."""

    def __init__(self, name, smarty):
        """Alarm Sensor Init."""
        super().__init__(name=f"{name} Boost State", device_class=None, smarty=smarty)

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_is_on = self._smarty.boost


class AlarmSensor(SmartyBinarySensor):
    """Alarm Binary Sensor."""

    def __init__(self, name, smarty):
        """Alarm Sensor Init."""
        super().__init__(
            name=f"{name} Alarm",
            device_class=BinarySensorDeviceClass.PROBLEM,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_is_on = self._smarty.alarm


class WarningSensor(SmartyBinarySensor):
    """Warning Sensor."""

    def __init__(self, name, smarty):
        """Warning Sensor Init."""
        super().__init__(
            name=f"{name} Warning",
            device_class=BinarySensorDeviceClass.PROBLEM,
            smarty=smarty,
        )

    def update(self) -> None:
        """Update state."""
        _LOGGER.debug("Updating sensor %s", self._attr_name)
        self._attr_is_on = self._smarty.warning
