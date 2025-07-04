# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

### Added

- Deployed online documentation: https://flet-dev.github.io/flet-audiorecorder/
- `AudioRecorder` control new property: `configuration`
- New dataclasses:
    - `AudioRecorderConfiguration`
    - `AndroidRecorderConfiguration`
    - `IosRecorderConfiguration`
    - `InputDevice`
- New enums:
    - `AndroidAudioSource`
    - `IosAudioCategoryOption`

### Changed

- Refactored `AudioRecorder` control to use `@ft.control` dataclass-style definition and switched to `Service` control type

#### Breaking Changes

- `AudioRecorder` must now be added to `Page.services` instead of `Page.overlay`.
- Recording configuration properties (`audio_encoder`, `suppress_noise`, `cancel_echo`, `auto_gain`, `channels_num`, `sample_rate`, `bit_rate`) are now grouped under `configuration: AudioRecorderConfiguration`
- Event `on_state_changed` renamed to `on_state_change`
- In all methods, parameter `wait_timeout` was renamed to `timeout`.
- The following sync methods were removed from `AudioRecorder` (use corresponding async methods instead):
    - `is_recording` → `is_recording_async`
    - `stop_recording` → `stop_recording_async`
    - `cancel_recording` → `cancel_recording_async`
    - `resume_recording` → `resume_recording_async`
    - `pause_recording` → `pause_recording_async`
    - `is_paused` → `is_paused_async`
    - `is_supported_encoder` → `is_supported_encoder_async`
    - `get_input_devices` → `get_input_devices_async`
    - `has_permission` → `has_permission_async`

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-audio-recorder/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-audio-recorder/releases/tag/0.1.0