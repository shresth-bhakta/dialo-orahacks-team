import asyncio
from edge_tts import Communicate

async def generate_sample_audio(text, output_file):
    """Generate audio for the given text using Edge TTS."""
    communicate = Communicate(text, "en-US-JennyNeural")  # Female voice
    await communicate.save(output_file)

# Generate the sample audio file
if __name__ == "__main__":
    text = "How many days in a week"
    output_file = "sample_audio.wav"
    asyncio.run(generate_sample_audio(text, output_file))
