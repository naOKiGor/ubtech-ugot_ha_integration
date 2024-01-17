"""Config flow for uGot USB Camera integration."""
from __future__ import annotations

from types import MappingProxyType
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import (
    CONF_NAME
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_UGOT_ADDRESS, DOMAIN, LOGGER


@callback
def async_get_schema(
    defaults: dict[str, Any] | MappingProxyType[str, Any], show_name: bool = False
) -> vol.Schema:
    """Return uGot USB Camera schema."""
    schema = {
        vol.Required(CONF_UGOT_ADDRESS, default=defaults.get(CONF_UGOT_ADDRESS)): str,
    }

    if show_name:
        schema = {
            vol.Optional(CONF_NAME, default=defaults.get(CONF_NAME)): str,
            **schema,
        }

    return vol.Schema(schema)


class ubtechUgotFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for UBTECH uGot Camera."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> ubtechUgotOptionsFlowHandler:
        """Get the options flow for this handler."""
        return ubtechUgotOptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Storing data in option, to allow for changing them later
            # using an options flow.
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, user_input[CONF_UGOT_ADDRESS]),
                data={},
                options={
                    CONF_UGOT_ADDRESS: user_input[CONF_UGOT_ADDRESS],
                },
            )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=async_get_schema(user_input, show_name=True),
            errors=errors,
        )


class ubtechUgotOptionsFlowHandler(OptionsFlow):
    """Handle UBTECH uGot options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize UBTECH uGot options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage UBTECH uGot options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, user_input[CONF_UGOT_ADDRESS]),
                data={
                    CONF_UGOT_ADDRESS: user_input[CONF_UGOT_ADDRESS],
                },
            )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="init",
            data_schema=async_get_schema(user_input or self.config_entry.options),
            errors=errors,
        )


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
