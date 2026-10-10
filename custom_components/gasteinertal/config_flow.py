"""Config flow for Gasteinertal."""

from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class GasteinertalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gasteinertal."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Add the integration without requiring user-provided settings."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="Gasteinertal", data={})
        return self.async_show_form(step_id="user")
