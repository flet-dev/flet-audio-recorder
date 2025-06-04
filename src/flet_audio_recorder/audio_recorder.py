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
    """

    configuration: AudioRecorderConfiguration = field(
        default_factory=lambda: AudioRecorderConfiguration()
    )
    on_state_change: ft.OptionalEventCallable[AudioRecorderStateChangeEvent] = None

    async def start_recording_async(
        self,
        output_path: str = None,
        configuration: Optional[AudioRecorderConfiguration] = None,
    ) -> bool:
        """
        Starts recording audio and saves it to the specified output path.

        If not on the web, the `output_path` parameter must be provided.

        Args:
            output_path: The file path where the audio will be saved.
                It must be specified if not on web.
            configuration: The configuration for the audio recorder.
                If `None`, the `AudioRecorder.configuration` will be used.
        Returns:
            bool: `True` if recording was successfully started, `False` otherwise.
        """
        assert (
            self.page.web or output_path
        ), "output_path must be provided on platforms other than web"
        return await self._invoke_method_async(
            "start_recording",
            {
                "output_path": output_path,
                "configuration": configuration
                if configuration is not None
                else self.configuration,
            },
        )

    async def is_recording_async(self) -> bool:
        """
        Asynchronously checks whether the audio recorder is currently recording.

        Returns:
            bool: `True` if the recorder is currently recording, `False` otherwise.
        """
        return await self._invoke_method_async("is_recording")

    async def stop_recording_async(self) -> Optional[str]:
        """
        Asynchronously stops the audio recording and optionally returns the path to the saved file.

        Returns:
            Optional[str]: The file path where the audio was saved or `None` if not applicable.
        """
        return await self._invoke_method_async("stop_recording")

    async def cancel_recording_async(self):
        """
        Cancels the current audio recording.
        """
        await self._invoke_method_async("cancel_recording")

    def cancel_recording(self):
        """
        Cancels the current audio recording.
        """
        asyncio.create_task(self.cancel_recording_async())

    async def resume_recording_async(self):
        """
        Resumes a paused audio recording.
        """
        await self._invoke_method_async("resume_recording")

    def resume_recording(self):
        """
        Resumes a paused audio recording.
        """
        asyncio.create_task(self.resume_recording_async())

    async def pause_recording_async(self):
        """
        Pauses the ongoing audio recording.
        """
        await self._invoke_method_async("pause_recording")

    def pause_recording(self):
        """
        Pauses the ongoing audio recording.
        """
        asyncio.create_task(self.pause_recording_async())

    async def is_paused_async(self) -> bool:
        """
        Asynchronously checks whether the audio recorder is currently paused.

        Returns:
            bool: `True` if the recorder is paused, `False` otherwise.
        """
        return await self._invoke_method_async("is_paused")

    async def is_supported_encoder_async(self, encoder: AudioEncoder) -> bool:
        """
        Asynchronously checks if the given audio encoder is supported by the recorder.

        Args:
            encoder: The audio encoder to check.

        Returns:
            bool: `True` if the encoder is supported, `False` otherwise.
        """
        return await self._invoke_method_async(
            "is_supported_encoder", {"encoder": encoder}
        )

    async def get_input_devices_async(self) -> List[InputDevice]:
        """
        Asynchronously retrieves the available input devices for recording.

        Returns:
            dict: A dictionary of available input devices.
        """
        r = await self._invoke_method_async("get_input_devices")
        return [
            InputDevice(id=device_id, label=label) for device_id, label in r.items()
        ]

    async def has_permission_async(self) -> bool:
        """
        Asynchronously checks if the app has permission to record audio.

        Returns:
            bool: `True` if the app has permission, `False` otherwise.
        """
        return await self._invoke_method_async("has_permission")
