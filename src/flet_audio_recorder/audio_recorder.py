import asyncio
from dataclasses import field
from typing import List, Optional

import flet as ft

from .types import (
    AudioEncoder,
    AudioRecorderConfiguration,
    AudioRecorderStateChangeEvent,
    InputDevice,
)

__all__ = ["AudioRecorder"]


@ft.control("AudioRecorder")
class AudioRecorder(ft.Service):
    """
    A control that allows you to record audio from your device.

    This control can record audio using different audio encoders and also allows configuration
    of various audio recording parameters such as noise suppression, echo cancellation, and more.

    Note:
        This control is non-visual and should be added to `Page.services` list before it can be used.
    """

    configuration: AudioRecorderConfiguration = field(
        default_factory=lambda: AudioRecorderConfiguration()
    )
    """
    The default configuration of the audio recorder.
    """

    on_state_change: ft.OptionalEventHandler[
        AudioRecorderStateChangeEvent["AudioRecorder"]
    ] = None
    """
    Event handler that is called when the state of the audio recorder changes.
    
    Event handler argument is of type [`AudioRecorderStateChangeEvent`][(p).].
    """

    async def start_recording_async(
        self,
        output_path: Optional[str] = None,
        configuration: Optional[AudioRecorderConfiguration] = None,
        timeout: Optional[float] = 10,
    ) -> bool:
        """
        Starts recording audio and saves it to the specified output path.

        If not on the web, the `output_path` parameter must be provided.

        Args:
            output_path: The file path where the audio will be saved.
                It must be specified if not on web.
            configuration: The configuration for the audio recorder.
                If `None`, the `AudioRecorder.configuration` will be used.
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if recording was successfully started, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        assert (
            self.page.web or output_path
        ), "output_path must be provided on platforms other than web"
        return await self._invoke_method_async(
            method_name="start_recording",
            arguments={
                "output_path": output_path,
                "configuration": configuration
                if configuration is not None
                else self.configuration,
            },
            timeout=timeout,
        )

    async def is_recording_async(self, timeout: Optional[float] = 10) -> bool:
        """
        Checks whether the audio recorder is currently recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the recorder is currently recording, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async("is_recording", timeout=timeout)

    async def stop_recording_async(self, timeout: Optional[float] = 10) -> Optional[str]:
        """
        Stops the audio recording and optionally returns the path to the saved file.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            The file path where the audio was saved or `None` if not applicable.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async("stop_recording", timeout=timeout)

    async def cancel_recording_async(self, timeout: Optional[float] = 10):
        """
        Cancels the current audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        await self._invoke_method_async("cancel_recording", timeout=timeout)

    def cancel_recording(self, timeout: Optional[float] = 10):
        """
        Cancels the current audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        asyncio.create_task(self.cancel_recording_async(timeout=timeout))

    async def resume_recording_async(self, timeout: Optional[float] = 10):
        """
        Resumes a paused audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        await self._invoke_method_async("resume_recording", timeout=timeout)

    def resume_recording(self, timeout: Optional[float] = 10):
        """
        Resumes a paused audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        asyncio.create_task(self.resume_recording_async(timeout=timeout))

    async def pause_recording_async(self, timeout: Optional[float] = 10):
        """
        Pauses the ongoing audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        await self._invoke_method_async("pause_recording", timeout=timeout)

    def pause_recording(self, timeout: Optional[float] = 10):
        """
        Pauses the ongoing audio recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Raises:
            TimeoutError: If the request times out.
        """
        asyncio.create_task(self.pause_recording_async(timeout=timeout))

    async def is_paused_async(self, timeout: Optional[float] = 10) -> bool:
        """
        Checks whether the audio recorder is currently paused.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the recorder is paused, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async("is_paused", timeout=timeout)

    async def is_supported_encoder_async(self, encoder: AudioEncoder, timeout: Optional[float] = 10) -> bool:
        """
        Checks if the given audio encoder is supported by the recorder.

        Args:
            encoder: The audio encoder to check.
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the encoder is supported, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async(
            "is_supported_encoder", {"encoder": encoder}, timeout=timeout
        )

    async def get_input_devices_async(self, timeout: Optional[float] = 10) -> List[InputDevice]:
        """
        Retrieves the available input devices for recording.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            A list of available input devices.
        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method_async("get_input_devices", timeout=timeout)
        return [
            InputDevice(id=device_id, label=label) for device_id, label in r.items()
        ]

    async def has_permission_async(self, timeout: Optional[float] = 10) -> bool:
        """
        Checks if the app has permission to record audio.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the app has permission, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async("has_permission", timeout=timeout)
