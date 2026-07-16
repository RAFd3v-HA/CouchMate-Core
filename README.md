# CouchMate Core

Home Assistant custom integration for the CouchMate Apple TV app.

## Highlights

- Select areas, devices and individual entities through the Home Assistant UI.
- Exclude individual entities from selected areas or devices.
- Filtered REST and WebSocket APIs for the CouchMate client.
- New local Apple TV pairing API with short-lived codes such as `CM-A7KD-P4XM`.
- Paired-client credentials are stored as SHA-256 hashes in Home Assistant storage.
- German and English translations.

> The technical domain remains `couch_control` for compatibility with the existing alpha integration.

## Installation

1. Upload this repository to GitHub.
2. Add the repository to HACS as a custom **Integration** repository.
3. Install **CouchMate Core** and restart Home Assistant.
4. Add CouchMate Core under **Settings → Devices & services**.

## Pairing API (alpha)

The Apple TV client can create a request without a Home Assistant token:

- `POST /api/couch_control/pairing/create`
- `GET /api/couch_control/pairing/status?session_id=...`
- `POST /api/couch_control/pairing/exchange`

Approve the displayed code in Home Assistant via **Developer tools → Actions**:

- Action: `couch_control.approve_pairing`
- Code: `CM-XXXX-XXXX`

An authenticated approval endpoint is also available:

- `POST /api/couch_control/pairing/approve`

Pairing sessions expire after five minutes and can only be exchanged once.

## Existing client APIs

- `GET /api/couch_control/entities`
- `GET /api/couch_control/info`
- WebSocket `couch_control/get_entities`
- WebSocket `couch_control/subscribe_filtered`

## Version

`1.1.0-alpha.1`
