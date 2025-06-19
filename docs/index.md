# flet-audio-recorder

[![pypi](https://img.shields.io/pypi/v/flet-audio-recorder.svg)](https://pypi.python.org/pypi/flet-audio-recorder)
[![downloads](https://static.pepy.tech/badge/flet-audio-recorder/month)](https://pepy.tech/project/flet-audio-recorder)
[![license](https://img.shields.io/github/license/flet-dev/flet-audio-recorder.svg)](https://github.com/flet-dev/flet-audio-recorder/blob/main/LICENSE)

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

## Usage

### Installation

To install the `flet-audio-recorder` package and add it to your project dependencies:

=== "uv"
    ```bash
    uv add flet-audio-recorder
    ```

=== "pip"
    ```bash
    pip install flet-audio-recorder  # (1)!
    ```

=== "poetry"
    ```bash
    poetry add flet-audio-recorder
    ```

???+ warning
    On Linux, encoding is provided by [fmedia](https://stsaz.github.io/fmedia/) which must be installed separately.

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

## Example

```python title="main.py"
--8<-- "examples/audio_recorder_example/src/main.py"
```
