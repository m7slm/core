"""Describe mobile_app logbook events."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.const import ATTR_FRIENDLY_NAME, ATTR_ICON
from homeassistant.core import Event, HomeAssistant, callback

from .const import DOMAIN

IOS_EVENT_ZONE_ENTERED = "ios.zone_entered"
IOS_EVENT_ZONE_EXITED = "ios.zone_exited"

ATTR_ZONE = "zone"
ATTR_SOURCE_DEVICE_NAME = "sourceDeviceName"
ATTR_SOURCE_DEVICE_ID = "sourceDeviceID"
EVENT_TO_DESCRIPTION = {
    IOS_EVENT_ZONE_ENTERED: "entered zone",
    IOS_EVENT_ZONE_EXITED: "exited zone",
}


@callback
def async_describe_events(
    hass: HomeAssistant,
    async_describe_event: Callable[[str, str, Callable[[Event], dict[str, str]]], None],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_zone_event(event: Event) -> dict[str, str]:
        """Describe mobile_app logbook event."""
        data = event.data
        event_description = EVENT_TO_DESCRIPTION[event.event_type]
        zone_entity_id = data.get(ATTR_ZONE)
        source_device_name = data.get(
            ATTR_SOURCE_DEVICE_NAME, data.get(ATTR_SOURCE_DEVICE_ID)
        )
        zone_name = None
        zone_icon = None
        if zone_entity_id and (zone_state := hass.states.get(zone_entity_id)):
            zone_name = zone_state.attributes.get(ATTR_FRIENDLY_NAME)
            zone_icon = zone_state.attributes.get(ATTR_ICON)
        description = {
            "name": source_device_name,
            "message": f"{event_description} {zone_name or zone_entity_id}",
            "icon": zone_icon or "mdi:crosshairs-gps",
        }
        if zone_entity_id:
            description["entity_id"] = zone_entity_id
        return description

    async_describe_event(DOMAIN, IOS_EVENT_ZONE_ENTERED, async_describe_zone_event)
    async_describe_event(DOMAIN, IOS_EVENT_ZONE_EXITED, async_describe_zone_event)
