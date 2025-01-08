from homeassistant import config_entries, core
from homeassistant.helpers import discovery

DOMAIN = "bmas"

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Black Mesa Announcement System."""
    hass.data[DOMAIN] = {}
    # Load services
    hass.async_create_task(
        discovery.async_load_platform(hass, "tts", DOMAIN, {}, config)
    )
    return True