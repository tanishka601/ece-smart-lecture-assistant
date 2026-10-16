from whisper_service import transcribe_audio

audio_file = "uploads/sample.mp3"

print("Starting transcription...\n")

transcript = transcribe_audio(audio_file)

print("Transcript:\n")
print(transcript)