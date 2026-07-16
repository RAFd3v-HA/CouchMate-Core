# Changelog

## 1.1.0-alpha.3

- Added a CouchMate management menu under the integration options.
- Pairing requests can now be approved or rejected directly in the Home Assistant UI.
- Paired CouchMate clients can be revoked from the integration options.
- Added pairing cancellation endpoint.
- Added client-authenticated info and entity endpoints for the tvOS app.
- Pairing notifications are dismissed automatically after approval, rejection, or cancellation.
- Added `couchmate.reject_pairing` service.

## 1.1.0-alpha.2

- Renamed the technical integration domain from `couch_control` to `couchmate`.
- Updated REST paths, WebSocket commands, services, storage keys, translations, and documentation.

## 1.1.0-alpha.1

- Initial Apple TV pairing prototype.
