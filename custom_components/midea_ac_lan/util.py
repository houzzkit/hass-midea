from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from .const import DOMAIN

async def appliances_store(hass: HomeAssistant, uid: str, data=None):
    return await hass_store(hass, f"{uid}-appliances", data)

async def hass_store(hass: HomeAssistant, key: str, data=None):
    store = Store(hass, 1, f"{DOMAIN}/{key}.json")
    if data is not None:
        return await store.async_save(data)
    return await store.async_load()
