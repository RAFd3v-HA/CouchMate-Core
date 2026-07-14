# CouchMate Core

![CouchMate Core](assets/couchmate-banner.png)

**CouchMate Core** is a Home Assistant custom integration for selecting the areas, devices, and entities exposed to the compatible Apple TV client.

> Alpha release: the visible product name is CouchMate Core, while the technical Home Assistant domain and legacy API identifiers intentionally remain `couch_control` for compatibility.

## Features

- Select complete Home Assistant areas
- Select complete devices
- Add individual entities
- Exclude individual entities
- Review and change the selection through **Configure**
- Diagnostic entities show the selected and resolved totals
- Existing REST and WebSocket interfaces remain available

## Installation through HACS

1. Add `https://github.com/RAFd3v-HA/CouchMate-Core` as a custom **Integration** repository in HACS.
2. Install **CouchMate Core**.
3. Restart Home Assistant.
4. Add **CouchMate Core** under **Settings → Devices & services**.

The original integration and CouchMate Core cannot be installed at the same time because both intentionally use the technical domain `couch_control`.

## Updating from the previous test build

Replace the repository files, download the update in HACS, and restart Home Assistant. Your stored selection should remain available. The active version is shown on the CouchMate Core device page.

## Compatibility promise for this alpha

This release is deliberately based on the already tested Beta 6 flow. It does not replace the selector implementation, domain, storage key, REST paths, or WebSocket command names.

## License and attribution

CouchMate Core is derived from the MIT-licensed CouchControlHACS project by Lucas Franz. The original copyright and MIT license are retained in `LICENSE`.
