from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from midealocal.cloud import get_midea_cloud
from .const import DOMAIN, CONF_SERVER, CONF_ACCOUNT, CONF_PASSWORD


async def appliances_store(hass: HomeAssistant, uid: str, data=None):
    return await hass_store(hass, f"{uid}-appliances", data)

async def appliance_store(hass: HomeAssistant, aid, data=None):
    return await hass_store(hass, f"{aid}", data)

async def hass_store(hass: HomeAssistant, key: str, data=None):
    store = Store(hass, 1, f"{DOMAIN}/{key}.json")
    if data is not None:
        return await store.async_save(data)
    return await store.async_load()

async def get_entry_cloud(hass: HomeAssistant, config_entry, login=None):
    this_data = hass.data.setdefault(DOMAIN, {})
    entry_data = this_data.setdefault(config_entry.entry_id, {})
    if not (cloud := entry_data.get('cloud')):
        cloud = get_midea_cloud(
            config_entry.data[CONF_SERVER],
            async_get_clientsession(hass),
            config_entry.data[CONF_ACCOUNT],
            config_entry.data[CONF_PASSWORD],
        )
        cloud._access_token = config_entry.data.get('access_token')
        cloud._security._aes_key = config_entry.data.get('security_key', '0').encode()
        entry_data['cloud'] = cloud
        if not cloud._access_token:
            login = True
    if login:
        await cloud.login()
    return cloud

async def get_preset_cloud(hass: HomeAssistant, login=None):
    this_data = hass.data.setdefault(DOMAIN, {})
    preset_data = this_data.setdefault('preset_account', {})
    if not (cloud := preset_data.get('cloud')):
        from .config_flow import BaseFlow
        cloud = get_midea_cloud(
            BaseFlow.preset_cloud_name,
            async_get_clientsession(hass),
            BaseFlow.preset_account,
            BaseFlow.preset_password,
        )
        preset_data['cloud'] = cloud
        login = True
    if login:
        await cloud.login()
    return cloud
