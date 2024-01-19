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

from .const import CONF_UGOT_ADDRESS, DOMAIN, LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a uGot camera,sensor based on a config entry."""
    LOGGER.debug(f"[{__name__}]----->>>>> async_setup_entry")
    async_add_entities(
        [
            uGotCamera(
                name=entry.title,
                ugot_address=entry.options[CONF_UGOT_ADDRESS],
                unique_id=f'uGotCamera-{entry.options[CONF_UGOT_ADDRESS]}',
                device_info=DeviceInfo(
                    name=f'{entry.title} USB Camera',
                    manufacturer="UBTECH",
                    identifiers={(DOMAIN, f'uGotCamera-{entry.options[CONF_UGOT_ADDRESS]}')},
                ),
            )
        ]
    )


class uGotCamera(Camera):
    """An implementation of uGot USB camera that is reachable by ugot sdk."""

    def __init__(
        self,
        *,
        name: str | None = None,
        ugot_address: str,
        unique_id: str | None = None,
        device_info: DeviceInfo | None = None,
    ) -> None:
        """Initialize a uGot USB camera."""

        super().__init__()
        self._attr_name = name
        self._ugot_address = ugot_address
        self._camera_opened = False

        self._got_sdk = ugot.UGOT()
        self._got_sdk.initialize(self._ugot_address)

        if unique_id is not None:
            self._attr_unique_id = unique_id
        if device_info is not None:
            self._attr_device_info = device_info

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""

        if not self._camera_opened:
            self._got_sdk.open_camera()
            self._camera_opened = True

        return self._got_sdk.read_camera_data()
