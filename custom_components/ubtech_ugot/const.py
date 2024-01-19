"""Constants for the UBTECH uGot integration."""

import logging
from typing import Final

from homeassistant.const import (
    CONF_HOST,
    Platform
)

DOMAIN: Final = "ubtech_ugot"
PLATFORMS: Final = [
    Platform.CAMERA, 
    # Platform.TTS, 
    # Platform.MEDIA_PLAYER,
    # Platform.SENSOR,
    Platform.LIGHT,
]

LOGGER = logging.getLogger(__package__)

CONF_UGOT_ADDRESS: Final = CONF_HOST
