import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


async def stream_extract(audio_bytes, prompt):

    response = model.generate_content(
        [
            prompt,
            {
                "mime_type": "audio/wav",
                "data": audio_bytes
            }
        ],
        stream=True
    )

    for chunk in response:

        # skip empty chunks
        if not chunk.candidates:
            continue

        for candidate in chunk.candidates:

            if not candidate.content:
                continue

            for part in candidate.content.parts:

                if hasattr(part, "text"):
                    yield part.text