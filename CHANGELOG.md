# Superdesk Server Changelog

## [1.4.4] 2016-12-05

### Fixed

- Use default language if no language is set on desk.

## [1.4.3] 2016-11-30

### Fixed

- Allow tables in NITF output.

## [1.4.2] 2016-11-29

### Added

- Add support for desk language

### Fixed

- Fix validation in case of error in list field

## [1.4.1] 2016-11-22

### Fixed

- Fix missing validation error for embedded items.

## [1.4] 2016-11-15

### Added

- Add option to generate short item ids.
- Add support for translate item action.

### Fixed

- Set celery version <4.
- Allow email formatter for publishing.
- Improve word counting.
- Ignore dateline when validating correction.
- Fix online users info when doing sessions gc.
- Fix rss ingest when missing last updated date.
- Prevent rss ingested items to have timestamps in future.

## [1.3] 2016-10-14

### Added

- Add `superdesk.cache` module.
- Add htm2nitf method to NITF formatter
- Add basic curation function for text archive
- Add embargo privilege

### Fixed

- PA NITF ingest fixes
- Set ingest default values only of not set via profile
- Fix image cropping after updating image crop size vocabulary
- Preserve language on update/rewrite actions
- Update word count on save and publish action
- Allow duplicating items to different desks
- Update `versioncreated` of duplicated item

## [1.2] 2016-10-04

### Added

- Add spike expiry config setting
- Implement removing of content profiles
- Add `NO_TAKES` (default: `False`) config to be able to turn off takes packages.

### Fixed

- Fix scheduled items should not block publishing of normal items.
- Fix the query for genre in content filters
- Fix upload after changes to crop sizes vocabulary
- Fix saved search endpoint to return proper hateoas links
- Fix deleting of routed ingest items
- Use timezone for highlights queries
- Fix publishing of package items when those should be just included
- Fix only showing 25 desks
- Fixes for NITF formatter
- Fix fetching of media items - should not use content profiles
- Fix associated items validation - refresh before validation
- Fix query to return items for generating highlights

## [1.1] 2016-08-29

### Added

- Add destination picker for unspike action.
- Highlight matching terms in search results.

### Fixed

- Add missing associations data to HTTP PUSH publishing.
- Fix select area of interest func for embedded pictures.
- Fix uploading/editing of dictionaries.
- Filter out inactive search providers.
- Fix error when setting default value for cv field.
- Fix publishing of stories with feature image.
- Fix `LDAP_SERVER_PORT` setting not being integer.
- Fix duplicate subject codes parsing for nitf.
- Strip markup while matching content filters
- Make newly created items invisible, show it only after saving.


## [1.0] 2016-08-17

### Fixed

- Fix the handling of `anpa_take_key` for null values.

## [1.0-beta1] 2016-04-25

- initial release
