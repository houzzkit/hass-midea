"""Switch for Midea Lan."""

from typing import Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_SWITCHES, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICES, DOMAIN
from .midea_devices import MIDEA_DEVICES
from .midea_entity import MideaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switches for device."""
    switches = []
    entry_data = hass.data[DOMAIN].get(config_entry.entry_id, {})
    for device_id, device in entry_data.get(DEVICES, {}).items():
        extra_switches = config_entry.options.get(CONF_SWITCHES, [])
        for entity_key, config in cast(
            "dict",
            MIDEA_DEVICES[device.device_type]["entities"],
        ).items():
            if config["type"] == Platform.SWITCH and entity_key in extra_switches:
                dev = MideaSwitch(device, entity_key)
                switches.append(dev)
    async_add_entities(switches)


class MideaSwitch(MideaEntity, ToggleEntity):
    """Represent a Midea switch."""

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return cast("bool", self._device.get_attribute(self._entity_key))

    def turn_on(self, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Turn on switch."""
        self._device.set_attribute(attr=self._entity_key, value=True)

    def turn_off(self, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Turn off switch."""
        self._device.set_attribute(attr=self._entity_key, value=False)
