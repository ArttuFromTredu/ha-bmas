from homeassistant.components.tts import Provider
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import os
import logging
from pydub import AudioSegment

_LOGGER = logging.getLogger(__name__)

DOMAIN = "bmas"
WAV_FILES_DIR = os.path.join(os.path.dirname(__file__), 'wav_files')
TTS_DIR = os.path.join(os.path.dirname(__file__), '../../tts')

async def async_setup_platform(hass: HomeAssistant, config: ConfigType, async_add_entities, discovery_info=None):
    async_add_entities([BmasProvider(hass)])

def get_engine(hass: HomeAssistant, config: ConfigType, discovery_info: DiscoveryInfoType = None):
    return BmasProvider(hass)

class BmasProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.name = "Black Mesa Announcement System TTS"

    @property
    def default_language(self):
        return "en"

    @property
    def supported_languages(self):
        return ["en"]

    @property
    def supported_options(self):
        return []

    @property
    def default_options(self):
        return {}

    async def async_get_tts_audio(self, message, language, options=None):
        return await self.hass.async_add_executor_job(self.get_tts_audio, message)

    def get_tts_audio(self, message):
        words = message.split()
        wav_files = [os.path.join(WAV_FILES_DIR, f"{word.lower()}.wav") for word in words]
        combined_file = os.path.join(TTS_DIR, "combined.wav")

        _LOGGER.debug("Combining WAV files: %s", wav_files)

        combined = AudioSegment.empty()
        for wav_file in wav_files:
            if os.path.exists(wav_file):
                audio_segment = AudioSegment.from_wav(wav_file)
                combined += audio_segment
                _LOGGER.debug("Added %s to combined file", wav_file)
            else:
                _LOGGER.warning("WAV file %s does not exist", wav_file)

        combined.export(combined_file, format="wav")
        _LOGGER.debug("Combined WAV file created at %s", combined_file)

        with open(combined_file, 'rb') as f:
            return "wav", f.read()