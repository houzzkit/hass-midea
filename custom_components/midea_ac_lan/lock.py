"""Lock entities for Midea Lan."""

from typing import Any, cast

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_SWITCHES, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICES, DOMAIN
from .midea_devices import MIDEA_DEVICES
from .midea_entity import MideaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities for device."""
    locks = []
    entry_data = hass.data[DOMAIN].get(config_entry.entry_id, {})
    for device_id, device in entry_data.get(DEVICES, {}).items():
        customize = config_entry.options.get(device_id) or {}
        extra_switches = customize.get(CONF_SWITCHES, []) or config_entry.options.get(CONF_SWITCHES, [])
        for entity_key, config in cast(
            "dict",
            MIDEA_DEVICES[device.device_type]["entities"],
        ).items():
            if config["type"] == Platform.LOCK and entity_key in extra_switches:
                dev = MideaLock(device, entity_key)
                locks.append(dev)
    async_add_entities(locks)


class MideaLock(MideaEntity, LockEntity):
    """Represent a Midea lock entity."""

    @property
    def is_locked(self) -> bool:
        """Return true if state is locked."""
        return cast("bool", self._device.get_attribute(self._entity_key))

    def lock(self, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Lock the lock."""
        self._device.set_attribute(attr=self._entity_key, value=True)

    def unlock(self, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Unlock the lock."""
        self._device.set_attribute(attr=self._entity_key, value=False)

    def open(self, **kwargs: Any) -> None:  # noqa: ANN401, ARG002
        """Open the lock."""
        self.unlock()
