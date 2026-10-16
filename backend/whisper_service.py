from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("✅ Whisper model loaded!")


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file and returns the transcript.
    """

    segments, info = model.transcribe(audio_path)

    transcript = ""

    for segment in segments:
        transcript += segment.text + "\n"

    return transcript