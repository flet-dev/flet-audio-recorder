# AudioRecorder

Audio recorder from microphone to a given file path. Works on macOS, Linux, Windows, iOS, Android and web.
Based on the [record](https://pub.dev/packages/record) Dart/Flutter package.

**NOTE:** On Linux, encoding is provided by [fmedia](https://stsaz.github.io/fmedia/) which must be installed separately.

AudioRecorder control is non-visual and should be added to `page.overlay` list.

## Installation

Add `flet-audio-recorder` as dependency to `pyproject.toml` of your Flet app:

```
dependencies = [
  "flet-audio-recorder",
  "flet>=0.27.4",
]
```

## Documentation

https://flet-dev.github.io/flet-audio-recorder/