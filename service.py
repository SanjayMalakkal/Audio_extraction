import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
import asyncio
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


async def stream_extract(audio_bytes, prompt):

    response = await model.generate_content_async(
        [
            prompt,
            {
                "mime_type": "audio/wav",
                "data": audio_bytes
            }
        ],
        stream=True,
        generation_config={
            "temperature":0,
            "max_output_tokens":8192,
            "top_p":0.9,
            "top_k":40,
            "response_mime_type":"application/json"
        }
    )

    async for chunk in response:

        # skip empty chunks
        if not chunk.candidates:
            continue

        for candidate in chunk.candidates:

            if not candidate.content:
                continue

            for part in candidate.content.parts:

                if hasattr(part, "text"):
                    yield part.text