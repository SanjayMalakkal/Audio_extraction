from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
import json
import asyncio

from prompt import build_prompt
from service import stream_extract

app = FastAPI()


@app.post("/extract")
async def extract_stream(
        audio: UploadFile = File(...),
        schema: str = Form(...)
):
    print(f"Received schema string: {repr(schema)}")
    # Parse schema
    try:
        schema_json = json.loads(schema)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        # Fallback: if it's just a comma/period-separated string without brackets
        schema = schema.replace(".", ",")
        if "," in schema and not schema.strip().startswith(("{", "[")):
            schema_json = [s.strip() for s in schema.split(",")]
        else:
            return JSONResponse(
                status_code=422,
                content={"detail": f"Invalid schema: must be valid JSON e.g. [\"field1\", \"field2\"]. Received: {schema}"}
            )

    if isinstance(schema_json, list):
        schema_json = {"fields": schema_json}

    # Build prompt and read audio concurrently
    prompt = build_prompt(schema_json)
    audio_bytes = await audio.read()

    async def generator():
        async for chunk in stream_extract(audio_bytes, prompt):
            yield chunk

    return StreamingResponse(
        generator(),
        media_type="text/plain",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        }
    )