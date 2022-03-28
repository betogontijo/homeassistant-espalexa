"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION


class IntegrationBlueprintEntity(CoordinatorEntity):
    def __init__(self, unique_id, name, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._unique_id = unique_id
        self._name = name

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self._name,
            "model": VERSION,
            "manufacturer": 'EspAlexa',
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data),
            "integration": DOMAIN,
        }
