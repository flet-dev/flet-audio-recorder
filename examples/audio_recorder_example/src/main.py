import flet as ft

import flet_audio_recorder as far


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title=ft.Text("Audio Recorder"), center_title=True)

    path = "test-audio-file.wav"

    def show_snackbar(message):
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    async def handle_start_recording(e):
        show_snackbar(f"Starting recording...")
        await audio_rec.start_recording_async(output_path=path)

    async def handle_stop_recording(e):
        output_path = await audio_rec.stop_recording_async()
        show_snackbar(f"Stopped recording. Output Path: {output_path}")
        if page.web and output_path is not None:
            page.launch_url(output_path)

    async def handle_list_devices(e):
        o = await audio_rec.get_input_devices_async()
        show_snackbar(f"Input Devices: {', '.join([d.label for d in o])}")

    async def handle_has_permission(e):
        try:
            status = await audio_rec.has_permission_async()
            show_snackbar(f"Audio Recording Permission status: {status}")
        except Exception as e:
            show_snackbar(f"Error checking permission: {e}")

    async def handle_pause(e):
        print(f"isRecording: {await audio_rec.is_recording_async()}")
        if await audio_rec.is_recording_async():
            await audio_rec.pause_recording_async()

    async def handle_resume(e):
        print(f"isPaused: {await audio_rec.is_paused_async()}")
        if await audio_rec.is_paused_async():
            await audio_rec.resume_recording_async()

    async def handle_audio_encoder_test(e):
        supports_wav = await audio_rec.is_supported_encoder_async(far.AudioEncoder.WAV)

    audio_rec = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(encoder=far.AudioEncoder.WAV),
        on_state_change=lambda e: print(f"State Changed: {e.data}"),
    )
    page.services.append(audio_rec)

    page.add(
        ft.Button("Start Audio Recorder", on_click=handle_start_recording),
        ft.Button("Stop Audio Recorder", on_click=handle_stop_recording),
        ft.Button("List Devices", on_click=handle_list_devices),
        ft.Button("Pause Recording", on_click=handle_pause),
        ft.Button("Resume Recording", on_click=handle_resume),
        ft.Button("WAV Encoder Support", on_click=handle_audio_encoder_test),
        ft.Button(
            "Get Audio Recording Permission Status", on_click=handle_has_permission
        ),
    )


ft.run(main)
