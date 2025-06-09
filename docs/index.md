# flet-audio-recorder

Adds audio recording support to Flet apps.

It is based on the [record](https://pub.dev/packages/record) Flutter package.

## Platform Support

This package supports the following platforms:

| Platform | Supported |
|----------|:---------:|
| Windows  |     ✅     |
| macOS    |     ✅     |
| Linux    |     ✅     |
| iOS      |     ✅     |
| Android  |     ✅     |
| Web      |     ✅     |

## Installation

Add `flet-audio-recorder` as dependency to `pyproject.toml` of your Flet app:

```
dependencies = [
  "flet-audio-recorder",
  "flet",
]
```

???+ note
    On Linux, encoding is provided by [fmedia](https://stsaz.github.io/fmedia/) which must be installed separately.

## Example

```python title="main.py"
--8<-- "examples/audio_recorder_example/src/main.py"
```
