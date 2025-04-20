from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

import flet as ft

__all__ = [
    "AudioRecorderState",
    "AudioEncoder",
    "AudioRecorderStateChangeEvent",
    "AudioRecorderConfiguration",
    "AndroidAudioSource",
    "AndroidRecordConfiguration",
    "InputDevice",
    "IosAudioCategoryOption",
    "IosRecordConfiguration",
]


class AudioRecorderState(Enum):
    STOPPED = "stopped"
    RECORDING = "recording"
    PAUSED = "paused"


@dataclass
class AudioRecorderStateChangeEvent(ft.ControlEvent):
    state: AudioRecorderState


class AudioEncoder(Enum):
    """
    The `AudioEncoder` enum represents the different audio encoders supported by the audio recorder.

    The available encoders are:

    - `AACLC`: Advanced Audio Codec Low Complexity. A commonly used encoder for streaming and general audio recording.
    - `AACELD`: Advanced Audio Codec Enhanced Low Delay. Suitable for low-latency applications like VoIP.
    - `AACHE`: Advanced Audio Codec High Efficiency. Optimized for high-quality audio at lower bit rates.
    - `AMRNB`: Adaptive Multi-Rate Narrow Band. Used for speech audio in mobile communication.
    - `AMRWB`: Adaptive Multi-Rate Wide Band. Used for higher-quality speech audio.
    - `OPUS`: A codec designed for both speech and audio applications, known for its versatility.
    - `FLAC`: Free Lossless Audio Codec. Provides high-quality lossless audio compression.
    - `WAV`: Standard audio format used for raw, uncompressed audio data.
    - `PCM16BITS`: Pulse Code Modulation with 16-bit depth, used for high-fidelity audio.
    """

    AACLC = "aacLc"
    AACELD = "aacEld"
    AACHE = "aacHe"
    AMRNB = "amrNb"
    AMRWB = "amrWb"
    OPUS = "opus"
    FLAC = "flac"
    WAV = "wav"
    PCM16BITS = "pcm16bits"


class AndroidAudioSource(Enum):
    DEFAULT_SOURCE = "defaultSource"
    MIC = "mic"
    VOICE_UPLINK = "voiceUplink"
    VOICE_DOWNLINK = "voiceDownlink"
    VOICE_CALL = "voiceCall"
    CAMCORDER = "camcorder"
    VOICE_RECOGNITION = "voiceRecognition"
    VOICE_COMMUNICATION = "voiceCommunication"
    REMOTE_SUBMIX = "remoteSubMix"
    UNPROCESSED = "unprocessed"
    VOICE_PERFORMANCE = "voicePerformance"


@dataclass
class AndroidRecordConfiguration:
    use_legacy: bool = False
    mute_audio: bool = False
    manage_bluetooth: bool = True
    audio_source: AndroidAudioSource = AndroidAudioSource.DEFAULT_SOURCE


class IosAudioCategoryOption(Enum):
    MIX_WITH_OTHERS = "mixWithOthers"
    DUCK_OTHERS = "duckOthers"
    ALLOW_BLUETOOTH = "allowBluetooth"
    DEFAULT_TO_SPEAKER = "defaultToSpeaker"
    INTERRUPT_SPOKEN_AUDIO_AND_MIX_WITH_OTHERS = "interruptSpokenAudioAndMixWithOthers"
    ALLOW_BLUETOOTH_A2DP = "allowBluetoothA2DP"
    ALLOW_AIRPLAY = "allowAirPlay"
    OVERRIDE_MUTED_MICROPHONE_INTERRUPTION = "overrideMutedMicrophoneInterruption"


@dataclass
class IosRecordConfiguration:
    options: List[IosAudioCategoryOption] = field(
        default_factory=lambda: [
            IosAudioCategoryOption.DEFAULT_TO_SPEAKER,
            IosAudioCategoryOption.ALLOW_BLUETOOTH,
            IosAudioCategoryOption.ALLOW_BLUETOOTH_A2DP,
        ]
    )
    manage_audio_session: bool = True


@dataclass
class InputDevice:
    id: str
    label: str


@dataclass
class AudioRecorderConfiguration:
    encoder: AudioEncoder = AudioEncoder.WAV
    suppress_noise: bool = False
    cancel_echo: bool = False
    auto_gain: bool = False
    channels: int = 2
    sample_rate: int = 44100
    bit_rate: ft.Number = 128000
    device: Optional[InputDevice] = None
    android_configuration: AndroidRecordConfiguration = field(
        default_factory=AndroidRecordConfiguration
    )
    ios_configuration: IosRecordConfiguration = field(
        default_factory=IosRecordConfiguration
    )

    def __post_init__(self):
        assert self.channels in (1, 2), "channels_num can either be 1 or 2"
