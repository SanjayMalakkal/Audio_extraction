from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import json

from prompt import build_prompt
from service import stream_extract

app = FastAPI()


@app.post("/extract")

async def extract_stream(
        audio: UploadFile = File(...),
        schema: str = Form(...)
):

    schema_json = json.loads(schema)

    audio_bytes = await audio.read()

    prompt = build_prompt(schema_json)

    async def generator():

        async for chunk in stream_extract(audio_bytes, prompt):

            yield chunk

    return StreamingResponse(
        generator(),
        media_type="text/plain"
    )