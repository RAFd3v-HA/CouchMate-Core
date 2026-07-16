"""REST API for CouchMate Core."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import web
import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, PAIRING_MANAGER
from .pairing import PairingManager, PairingStatus
from .storage import async_save_entities

_LOGGER = logging.getLogger(__name__)


def _manager(hass: HomeAssistant) -> PairingManager:
    return hass.data[DOMAIN][PAIRING_MANAGER]


class CouchMateEntitiesView(HomeAssistantView):
    url = "/api/couchmate/entities"
    name = "api:couchmate:entities"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        hass = request.app["hass"]
        if DOMAIN not in hass.data:
            return web.json_response({"error": "CouchMate Core not configured"}, status=400)
        entities = hass.data[DOMAIN].get("entities", [])
        ent_reg = er.async_get(hass)
        detailed_entities: list[dict[str, Any]] = []
        for entity_id in entities:
            state = hass.states.get(entity_id)
            entry = ent_reg.async_get(entity_id)
            entity_data: dict[str, Any] = {
                "entity_id": entity_id,
                "state": state.state if state else None,
                "attributes": dict(state.attributes) if state else {},
                "last_changed": state.last_changed.isoformat() if state else None,
                "last_updated": state.last_updated.isoformat() if state else None,
            }
            if entry:
                entity_data.update({
                    "name": entry.name or entry.original_name,
                    "icon": entry.icon or entry.original_icon,
                    "device_class": entry.device_class,
                    "unit_of_measurement": entry.unit_of_measurement,
                    "area_id": entry.area_id,
                    "device_id": entry.device_id,
                })
            detailed_entities.append(entity_data)
        return web.json_response({"entities": detailed_entities, "count": len(detailed_entities)})

    async def post(self, request: web.Request) -> web.Response:
        hass = request.app["hass"]
        try:
            data = vol.Schema({vol.Required("entities"): [str]})(await request.json())
        except (ValueError, vol.Invalid) as err:
            return web.json_response({"error": f"Invalid data: {err}"}, status=400)
        valid = [entity_id for entity_id in data["entities"] if hass.states.get(entity_id)]
        hass.data[DOMAIN]["entities"] = valid
        await async_save_entities(hass, {"entities": valid})
        return web.json_response({"success": True, "entities": valid, "count": len(valid)})


class CouchMateInfoView(HomeAssistantView):
    url = "/api/couchmate/info"
    name = "api:couchmate:info"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        hass = request.app["hass"]
        return web.json_response({
            "integration": "CouchMate Core",
            "version": "1.1.0-alpha.2",
            "domain": DOMAIN,
            "filtered_entities_count": len(hass.data.get(DOMAIN, {}).get("entities", [])),
            "pairing": True,
            "status": "active",
        })


class PairingCreateView(HomeAssistantView):
    url = "/api/couchmate/pairing/create"
    name = "api:couchmate:pairing:create"
    requires_auth = False

    async def post(self, request: web.Request) -> web.Response:
        hass = request.app["hass"]
        if DOMAIN not in hass.data:
            return web.json_response({"error": "not_configured"}, status=503)
        try:
            data = await request.json()
        except Exception:
            data = {}
        session = _manager(hass).create_session(str(data.get("device_name", "Apple TV")))
        persistent_notification.async_create(
            hass,
            f"Ein Apple TV namens **{session.device_name}** möchte sich mit CouchMate verbinden. "
            f"Kopplungscode: **{session.code}**. Bestätige ihn über den Dienst "
            f"`couchmate.approve_pairing`.",
            title="CouchMate Kopplungsanfrage",
            notification_id=f"{DOMAIN}_pairing_{session.session_id}",
        )
        return web.json_response(session.public_dict())


class PairingStatusView(HomeAssistantView):
    url = "/api/couchmate/pairing/status"
    name = "api:couchmate:pairing:status"
    requires_auth = False

    async def get(self, request: web.Request) -> web.Response:
        session_id = request.query.get("session_id", "")
        session = _manager(request.app["hass"]).get_by_session_id(session_id)
        if not session:
            return web.json_response({"error": "session_not_found"}, status=404)
        payload = session.public_dict()
        if session.status == PairingStatus.APPROVED:
            payload["exchange_token"] = session.exchange_token
        return web.json_response(payload)


class PairingApproveView(HomeAssistantView):
    url = "/api/couchmate/pairing/approve"
    name = "api:couchmate:pairing:approve"
    requires_auth = True

    async def post(self, request: web.Request) -> web.Response:
        data = await request.json()
        session = _manager(request.app["hass"]).approve(str(data.get("code", "")))
        if not session:
            return web.json_response({"error": "code_not_found"}, status=404)
        return web.json_response(session.public_dict())


class PairingExchangeView(HomeAssistantView):
    url = "/api/couchmate/pairing/exchange"
    name = "api:couchmate:pairing:exchange"
    requires_auth = False

    async def post(self, request: web.Request) -> web.Response:
        data = await request.json()
        credentials = await _manager(request.app["hass"]).async_exchange(
            str(data.get("session_id", "")), str(data.get("exchange_token", ""))
        )
        if not credentials:
            return web.json_response({"error": "exchange_denied"}, status=403)
        return web.json_response(credentials)


async def async_setup_api(hass: HomeAssistant) -> None:
    for view in (
        CouchMateEntitiesView(),
        CouchMateInfoView(),
        PairingCreateView(),
        PairingStatusView(),
        PairingApproveView(),
        PairingExchangeView(),
    ):
        hass.http.register_view(view)
    _LOGGER.info("CouchMate Core REST and pairing API endpoints registered")
