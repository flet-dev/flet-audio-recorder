import json
from enum import Enum
from typing import Any, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.types import OptionalEventCallable
from flet.utils import deprecated


class AudioRecorderState(Enum):
    """
        The available AudioRecorder states are:

    - `STOPPED`
    - `RECORDING`
    - `PAUSED`
    """
    STOPPED = "stopped"
    RECORDING = "recording"
    PAUSED = "paused"


class AudioRecorderStateChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        """The current state of the audio recorder.

        Value is of type [AudioRecorderState](audiorecorderstate.md)."""
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.state: AudioRecorderState = AudioRecorderState(e.data)


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



class AudioRecorder(Control):
    """
    A control that allows you to record audio from your device.

    This control can record audio using different audio encoders and also allows configuration
    of various audio recording parameters such as noise suppression, echo cancellation, and more.
    """

    def __init__(
        self,
        audio_encoder: Optional[AudioEncoder] = None,
        suppress_noise: Optional[bool] = None,
        cancel_echo: Optional[bool] = None,
        auto_gain: Optional[bool] = None,
        channels_num: OptionalNumber = None,
        sample_rate: OptionalNumber = None,
        bit_rate: OptionalNumber = None,
        on_state_changed: OptionalEventCallable[AudioRecorderStateChangeEvent] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )
        self.__on_state_changed = EventHandler(
            lambda e: AudioRecorderStateChangeEvent(e)
        )
        self._add_event_handler("state_changed", self.__on_state_changed.get_handler())

        self.audio_encoder = audio_encoder
        self.suppress_noise = suppress_noise
        self.cancel_echo = cancel_echo
        self.auto_gain = auto_gain
        self.channels_num = channels_num
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.on_state_changed = on_state_changed

    def _get_control_name(self):
        return "audiorecorder"

    def start_recording(
        self, output_path: str = None, wait_timeout: Optional[float] = 10
    ) -> bool:
        """
        Starts recording audio and saves it to the specified output path.

        If not on the web, the `output_path` parameter must be provided.

        Args:
            output_path: The file path where the audio will be saved. It must be specified if not on web.
            wait_timeout: The time in seconds to wait for the recording to start. Default is 10.

        Returns:
            bool: `True` if recording was successfully started, `False` otherwise.
        """
        assert (
            self.page.web or output_path
        ), "output_path must be provided when not on web"
        started = self.invoke_method(
            "start_recording",
            {"outputPath": output_path},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return started == "true"

    def is_recording(self, wait_timeout: Optional[float] = 5) -> bool:
        """
        Checks whether the audio recorder is currently recording.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the recorder is currently recording, `False` otherwise.
        """
        recording = self.invoke_method(
            "is_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return recording == "true"

    async def is_recording_async(self, wait_timeout: Optional[float] = 5) -> bool:
        """
        Asynchronously checks whether the audio recorder is currently recording.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the recorder is currently recording, `False` otherwise.
        """
        recording = await self.invoke_method_async(
            "is_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return recording == "true"

    def stop_recording(self, wait_timeout: Optional[float] = 5) -> Optional[str]:
        """
        Stops the audio recording and optionally returns the path to the saved file.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            Optional[str]: The file path where the audio was saved or `None` if not applicable.
        """
        return self.invoke_method(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    async def stop_recording_async(
        self, wait_timeout: Optional[float] = 10
    ) -> Optional[str]:
        """
        Asynchronously stops the audio recording and optionally returns the path to the saved file.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 10.

        Returns:
            Optional[str]: The file path where the audio was saved or `None` if not applicable.
        """
        return await self.invoke_method_async(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def cancel_recording(self, wait_timeout: Optional[float] = 5) -> None:
        """
        Cancels the current audio recording.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.
        """
        self.invoke_method(
            "cancel_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def resume_recording(self):
        """
        Resumes a paused audio recording.
        """
        self.invoke_method("resume_recording")

    def pause_recording(self):
        """
        Pauses the ongoing audio recording.
        """
        self.invoke_method("pause_recording")

    def is_paused(self, wait_timeout: Optional[float] = 5) -> bool:
        """
        Checks whether the audio recorder is currently paused.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the recorder is paused, `False` otherwise.
        """
        paused = self.invoke_method(
            "is_paused",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return paused == "true"

    async def is_paused_async(self, wait_timeout: Optional[float] = 5) -> bool:
        """
        Asynchronously checks whether the audio recorder is currently paused.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the recorder is paused, `False` otherwise.
        """
        supported = await self.invoke_method_async(
            "is_paused",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    def is_supported_encoder(
        self, encoder: AudioEncoder, wait_timeout: Optional[float] = 5
    ) -> bool:
        """
        Checks if the given audio encoder is supported by the recorder.

        Args:
            encoder: The audio encoder to check.
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the encoder is supported, `False` otherwise.
        """
        supported = self.invoke_method(
            "is_supported_encoder",
            {
                "encoder": (
                    encoder.value if isinstance(encoder, AudioEncoder) else encoder
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    async def is_supported_encoder_async(
        self, encoder: AudioEncoder, wait_timeout: Optional[float] = 5
    ) -> bool:
        """
        Asynchronously checks if the given audio encoder is supported by the recorder.

        Args:
            encoder: The audio encoder to check.
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            bool: `True` if the encoder is supported, `False` otherwise.
        """
        supported = await self.invoke_method_async(
            "is_supported_encoder",
            {
                "encoder": (
                    encoder.value if isinstance(encoder, AudioEncoder) else encoder
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    def get_input_devices(self, wait_timeout: Optional[float] = 5) -> dict:
        """
        Retrieves the available input devices for recording.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            dict: A dictionary of available input devices.
        """
        devices = self.invoke_method(
            "get_input_devices",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return json.loads(devices)

    async def get_input_devices_async(self, wait_timeout: Optional[float] = 5) -> dict:
        """
        Asynchronously retrieves the available input devices for recording.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 5.

        Returns:
            dict: A dictionary of available input devices.
        """
        devices = await self.invoke_method_async(
            "get_input_devices",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return json.loads(devices)

    def has_permission(self, wait_timeout: Optional[float] = 10) -> bool:
        """
        Checks if the app has permission to record audio.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 10.

        Returns:
            bool: `True` if the app has permission, `False` otherwise.
        """
        p = self.invoke_method(
            "has_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return p == "true"

    async def has_permission_async(self, wait_timeout: Optional[float] = 10) -> bool:
        """
        Asynchronously checks if the app has permission to record audio.

        Args:
            wait_timeout: The time in seconds to wait for the result. Default is 10.

        Returns:
            bool: `True` if the app has permission, `False` otherwise.
        """
        p = await self.invoke_method_async(
            "has_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return p == "true"

    # audio_encoder
    @property
    def audio_encoder(self):
        """
        The audio encoder to be used for recording.

        Value is of type [`AudioEncoder`](audioencoder.md) 
        and defaults to `AudioEncoder.WAV`.
        """
        return self._get_attr("audioEncoder")

    @audio_encoder.setter
    def audio_encoder(self, value: Optional[AudioEncoder]):
        self._set_enum_attr("audioEncoder", value, AudioEncoder)

    # suppress_noise
    @property
    def suppress_noise(self) -> bool:
        """
        Whether to suppress noise during recording.

        Defaults to `False`.

        If `True`, it reduces the background noise while recording.
        """
        return self._get_attr("suppressNoise", data_type="bool", def_value=False)

    @suppress_noise.setter
    def suppress_noise(self, value: Optional[bool]):
        self._set_attr("suppressNoise", value)

    # cancel_echo
    @property
    def cancel_echo(self) -> bool:
        """
        Whether to cancel echo during recording.

        Defaults to `False`.

        If `True`, it reduces or cancels echo during recording.
        """
        return self._get_attr("cancelEcho", data_type="bool", def_value=False)

    @cancel_echo.setter
    def cancel_echo(self, value: Optional[bool]):
        self._set_attr("cancelEcho", value)

    # auto_gain
    @property
    def auto_gain(self) -> bool:
        """
        Whether to automatically adjust the audio gain during recording.

        Defaults to `False`.

        If `True`, the audio gain is automatically adjusted to avoid distortion or clipping.
        """
        return self._get_attr("autoGain", data_type="bool", def_value=False)

    @auto_gain.setter
    def auto_gain(self, value: Optional[bool]):
        self._set_attr("autoGain", value)

    # bit_rate
    @property
    def bit_rate(self) -> OptionalNumber:
        """
        The bit rate of the audio recording.

        This value is specified in kilobits per second (kbps). Defaults to `None`.
        """
        return self._get_attr("bitRate")

    @bit_rate.setter
    def bit_rate(self, value: OptionalNumber):
        self._set_attr("bitRate", value)

    # sample_rate
    @property
    def sample_rate(self) -> OptionalNumber:
        """
        The sample rate for the audio recording.

        This value is specified in Hertz (Hz). Defaults to `None`.
        """
        return self._get_attr("sampleRate")

    @sample_rate.setter
    def sample_rate(self, value: OptionalNumber):
        self._set_attr("sampleRate", value)

    # channels_num
    @property
    def channels_num(self) -> OptionalNumber:
        """
        The number of audio channels for the recording.

        Can be `1` (mono) or `2` (stereo). Defaults to `None`.
        """
        return self._get_attr("channels")

    @channels_num.setter
    def channels_num(self, value: OptionalNumber):
        if value is None or value in (1, 2):
            self._set_attr("channels", value)

    # on_state_changed
    @property
    def on_state_changed(self):
        """
        Event handler that is triggered when the recording state changes.

        This handler should accept an instance of [`AudioRecorderStateChangeEvent`](audiorecorderstatechangeevent.md).
        """
        return self.__on_state_changed.handler

    @on_state_changed.setter
    def on_state_changed(
        self, handler: OptionalEventCallable[AudioRecorderStateChangeEvent]
    ):
        self.__on_state_changed.handler = handler


