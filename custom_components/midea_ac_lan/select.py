"""Select for Midea Lan."""  # noqa: A005

from typing import cast

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_SWITCHES, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from midealocal.device import MideaDevice

from .const import DEVICES, DOMAIN
from .midea_devices import MIDEA_DEVICES
from .midea_entity import MideaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up selects for device."""
    selects = []
    entry_data = hass.data[DOMAIN].get(config_entry.entry_id, {})
    for device_id, device in entry_data.get(DEVICES, {}).items():
        customize = config_entry.options.get(device_id) or {}
        extra_switches = customize.get(CONF_SWITCHES, []) or config_entry.options.get(CONF_SWITCHES, [])
        for entity_key, config in cast(
            "dict",
            MIDEA_DEVICES[device.device_type]["entities"],
        ).items():
            if config["type"] == Platform.SELECT and entity_key in extra_switches:
                dev = MideaSelect(device, entity_key)
                selects.append(dev)
    async_add_entities(selects)


class MideaSelect(MideaEntity, SelectEntity):
    """Represent a Midea select."""

    def __init__(self, device: MideaDevice, entity_key: str) -> None:
        """Midea select init."""
        super().__init__(device, entity_key)
        self._options_name = self._config.get("options")

    @property
    def options(self) -> list[str]:
        """Return entity options."""
        return cast("list", getattr(self._device, self._options_name))

    @property
    def current_option(self) -> str:
        """Return entity current option."""
        return cast("str", self._device.get_attribute(self._entity_key))

    def select_option(self, option: str) -> None:
        """Select entity option."""
        self._device.set_attribute(self._entity_key, option)
