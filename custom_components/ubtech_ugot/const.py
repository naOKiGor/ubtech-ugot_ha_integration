"""Constants for the uGot USB Camera integration."""

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "ubtech_ugot"
PLATFORMS: Final = [Platform.CAMERA]

LOGGER = logging.getLogger(__package__)

CONF_UGOT_ADDRESS: Final = "ugot_address"
