"""Config flow for UBTECH uGot integration."""
from __future__ import annotations

from types import MappingProxyType
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow, SOURCE_ZEROCONF
from homeassistant.const import (
    CONF_NAME
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_UGOT_ADDRESS, DOMAIN, LOGGER


@callback
def async_get_schema(
    defaults: dict[str, Any] | MappingProxyType[str, Any], show_name: bool = False
) -> vol.Schema:
    """Return UBTECH uGot schema."""

    schema = {
        vol.Required(CONF_UGOT_ADDRESS, msg="uGot IP Address", default=defaults.get(CONF_UGOT_ADDRESS)): cv.string,
    }

    if show_name:
        schema = {
            vol.Optional(CONF_NAME, msg="Device Name", default=defaults.get(CONF_NAME)): cv.string,
            **schema,
        }

    return vol.Schema(schema)


class ubtechUgotFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for UBTECH uGot."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        errors: dict[str, str] = {}

        if user_input is not None:
            # Storing data in option, to allow for changing them later
            # using an options flow.
            LOGGER.debug(f"user_input={user_input}")
            await self.async_set_unique_id(f'uGotLight-{user_input[CONF_UGOT_ADDRESS]}')  # using uGotLight to detect if already configured
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, user_input[CONF_UGOT_ADDRESS]),
                data={},
                options={
                    CONF_UGOT_ADDRESS: user_input[CONF_UGOT_ADDRESS],
                },
            )
        else:
            if self.context.get("source") == SOURCE_ZEROCONF:
                user_input = {
                    CONF_NAME: self.context.get(f'ZEROCONF-{CONF_NAME}'),
                    CONF_UGOT_ADDRESS: self.context.get(f'ZEROCONF-{CONF_UGOT_ADDRESS}')
                }
            else:
                user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=async_get_schema(user_input, show_name=True),
            errors=errors,
        )

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> Dict[str, Any]:
        """Handle zeroconf discovery."""
        
        if discovery_info is not None:
            hostname = discovery_info.hostname
            if hostname[4] == '_':
                prefix = hostname[0:4]
                subfix = hostname[5:9]
            else:
                prefix = hostname[0:4]
                subfix = hostname[4:8]

            matched = all(map(lambda x: ('0' <= x <= '9') or ('A' <= x <= 'F'), subfix))
            if prefix != 'UGOT' or not matched:
                return self.async_abort(reason="device_not_supported")
            
            self.context.update(
                {
                    f'ZEROCONF-{CONF_NAME}': f"{prefix}_{subfix}",
                    f'ZEROCONF-{CONF_UGOT_ADDRESS}': discovery_info.host,
                }
            )

        await self.async_set_unique_id(f'uGotLight-{discovery_info.host}')
        self._abort_if_unique_id_configured()

        return await self.async_step_user()
