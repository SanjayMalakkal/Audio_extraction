def build_prompt(schema: dict):

    fields = schema.get("fields", [])

    field_list = "\n".join([f"- {f}" for f in fields])

    prompt = f"""
You are an information extraction system.

Extract the following fields from the audio conversation.

Fields:
{field_list}

Rules:
- Ignore filler words like um, ah, etc.
- If not found return null
- Return valid JSON

Example output:

{{
  "customer_name": "",
  "phone_number": "",
  "product": "",
  "complaint": "",
  "resolution": ""
}}
"""

    return prompt