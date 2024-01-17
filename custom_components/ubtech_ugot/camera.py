"""Support for IP Cameras."""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import suppress

from ugot import ugot

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_UGOT_ADDRESS, DOMAIN, LOGGER

TIMEOUT = 10
BUFFER_SIZE = 102400


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a MJPEG IP Camera based on a config entry."""
    async_add_entities(
        [
            uGotCamera(
                name=entry.title,
                ugot_address=entry.options[CONF_UGOT_ADDRESS],
                unique_id=entry.entry_id,
                device_info=DeviceInfo(
                    name=entry.title,
                    identifiers={(DOMAIN, entry.entry_id)},
                ),
            )
        ]
    )


class uGotCamera(Camera):
    """An implementation of an IP camera that is reachable over a URL."""

    def __init__(
        self,
        *,
        name: str | None = None,
        ugot_address: str,
        unique_id: str | None = None,
        device_info: DeviceInfo | None = None,
    ) -> None:
        """Initialize a MJPEG camera."""
        super().__init__()
        self._attr_name = name
        self._ugot_address = ugot_address
        self.got_sdk = ugot.UGOT()
        self.got_sdk.initialize(self._ugot_address)
        self.got_sdk.open_camera()

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""
        return self.got_sdk.read_camera_data()

