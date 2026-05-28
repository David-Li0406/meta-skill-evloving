---
name: ha-integration-maintainer
description: Home Assistant + HACS maintenance for the Heat Pump Predictor integration. Use when adding or updating config flow, coordinator, entities, services, translations, recorder/statistics compatibility, dashboards, or HACS release assets. Trigger for any HA/HACS changes to custom_components/heat_pump_predictor/.
---

# Home Assistant Integration Maintainer (Heat Pump Predictor)

Use this skill whenever modifying or validating the Heat Pump Predictor integration for Home Assistant (HACS-compatible). Keep outputs concise; prefer checklists and ready snippets.

## Scope and Triggers
- Changes to config flow, coordinator, entities, services, translations, recorder/statistics, dashboards, or HACS packaging.
- Debugging UpdateFailed, missing entities, translation or manifest issues, recorder/state_class warnings, or HACS validation.
- Preparing releases (version bumps, docs alignment) for heat_pump_predictor.

## Quick Checklist (per change)
- Config flow: async_step_user with voluptuous; validate 3 inputs (energy total_increasing, running binary, temperature sensor); surface errors via errors dict.
- Coordinator: DataUpdateCoordinator with 5m interval; call async_config_entry_first_refresh; raise UpdateFailed on API/state errors.
- Entities: subclass CoordinatorEntity + platform class; set _attr_has_entity_name = True; main feature entities set _attr_name = None; use translation_key; unique_id per entry + key; device_info from coordinator.
- Translations: add/align strings.json keys (flow, options, entities); no hard-coded English in code.
- Recorder/Statistics: correct device_class, unit, state_class (energy = total_increasing, power = measurement, duty = measurement, precision per metric); avoid unavailable/unknown math.
- Services: register calculate_energy with schema; validate entry id + temperature; async-only I/O.
- Manifest/HACS: manifest fields (domain, name, version SemVer, codeowners, documentation, issue_tracker, config_flow true, integration_type, iot_class); hacs.json present; README aligned; bump version on release.
- Logging/diagnostics: lazy formatting; log once per failure path; do not swallow exceptions.
- Tests: use MockConfigEntry + hass.config_entries.async_setup; assert hass.states.get; avoid direct module import; snapshot complex outputs when needed.

## Core Patterns and Snippets
- **Config Flow (user step)**
  - async_step_user: schema requires energy_sensor, running_sensor, temperature_sensor; validate entity domains/types; return self.async_create_entry on success; set errors["base"] for CannotConnect/InvalidAuth/unknown.
  - Use voluptuous selectors if extending; keep async for entity lookups.

- **Coordinator Setup**
  - Create DataUpdateCoordinator(hass, LOGGER, name=DOMAIN, update_interval=timedelta(minutes=5), update_method=_async_update_data).
  - Call await coordinator.async_config_entry_first_refresh() before forwarding platforms.
  - In _async_update_data, raise UpdateFailed on network/parse/state issues; never block.

- **Entity Template**
  - class MyEntity(CoordinatorEntity, SensorEntity): _attr_has_entity_name = True; _attr_name = None for main feature entities; translation_key for additional ones; unique_id f"{entry.entry_id}_{description.key}".
  - Use entity_description with value_fn; in available, rely on coordinator.last_update_success.

- **Translations**
  - Use translation_key matching strings.json; avoid hard-coded English names; strings.json holds entity/device/flow text.

- **Recorder/Statistics**
  - Energy: device_class=energy, unit=kWh, state_class=total_increasing.
  - Power: device_class=power, unit=W, state_class=measurement.
  - Duty cycle: unit=%, state_class=measurement; round sensibly.
  - Guard against None/unavailable before math; return None when data missing.

- **Services**
  - calculate_energy: validate temperature bucket and config_entry_id; async handler using coordinator/data manager; catch and log predictable errors, re-raise HomeAssistantError for user-facing issues.

- **Dashboards (ApexCharts helpers)**
  - Curve sensors expose attributes.data with entries like {temp, power_overall, power_running} or {temp, duty_cycle} or {temp, energy}; data_generator maps to [temp, value].
  - Recommend enabling only relevant bucket sensors (disabled by default) to reduce entity load.

## Common Pitfalls
- Missing _attr_has_entity_name = True or hard-coded English names; fix via translation_key and _attr_name = None for main entities.
- Forgetting async_config_entry_first_refresh leading to None data on startup.
- Swallowing exceptions in update_method; always raise UpdateFailed.
- Incorrect state_class/unit/device_class causing recorder warnings.
- Unique_id collisions; ensure entry-scoped unique_id.
- Not bumping manifest version for releases; HACS will complain.

## Release and Validation Steps
- Update manifest version (SemVer) and ensure documentation/issue_tracker URLs are present.
- Confirm hacs.json name set; README matches behavior.
- Run tests (pytest) if available; lint if configured.
- Validate strings.json is valid JSON and covers translation_keys used.
- Tag/release per repo workflow; ensure assets in custom_components/heat_pump_predictor/ only.

## References (read as needed)
- Project README for sensor expectations and ApexCharts examples.
- custom_components/heat_pump_predictor/const.py for domain, keys, and intervals.
- copilot/python-ha-integration.md for coding conventions (imports, async, logging, entities, constants).
