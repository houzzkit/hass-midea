from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from midealocal.cloud import get_midea_cloud
from .const import DOMAIN


async def appliances_store(hass: HomeAssistant, uid: str, data=None):
    return await hass_store(hass, f"{uid}-appliances", data)

async def appliance_store(hass: HomeAssistant, aid, data=None):
    return await hass_store(hass, f"{aid}", data)

async def hass_store(hass: HomeAssistant, key: str, data=None):
    store = Store(hass, 1, f"{DOMAIN}/{key}.json")
    if data is not None:
        return await store.async_save(data)
    return await store.async_load()

async def get_preset_cloud(hass: HomeAssistant):
    this_data = hass.data.setdefault(DOMAIN, {})
    preset_data = this_data.setdefault('preset_account', {})
    if preset_cloud := preset_data.get('cloud'):
        return preset_cloud

    from .config_flow import BaseFlow
    preset_cloud = get_midea_cloud(
        BaseFlow.preset_cloud_name,
        async_get_clientsession(hass),
        BaseFlow.preset_account,
        BaseFlow.preset_password,
    )
    await preset_cloud.login()
    preset_data['cloud'] = preset_cloud
    return preset_cloud