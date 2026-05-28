# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
import sys
from google import genai
from google.genai import types

# API Key will be loaded from environment
API_KEY = os.environ.get("GEMINI_API_KEY")

def load_env():
    """Simple helper to load GEMINI_API_KEY from .env.local if not in environment."""
    if os.environ.get("GEMINI_API_KEY"):
        return

    # Try to find .env.local relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # d:\Coders\gpus\.agent\skills\frontend-design\scripts -> d:\Coders\gpus
    env_path = os.path.abspath(os.path.join(script_dir, "../../../../.env.local"))

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    os.environ["GEMINI_API_KEY"] = key
                    break

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")

def generate(prompt, output_file_base="generated_image"):
    load_env()
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-pro-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
        image_config=types.ImageConfig(
            image_size="1K",
        ),
        tools=tools,
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        for part in chunk.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                inline_data = part.inline_data
                data_buffer = inline_data.data
                file_extension = mimetypes.guess_extension(inline_data.mime_type) or ".png"
                file_name = f"{output_file_base}_{file_index}{file_extension}"
                save_binary_file(file_name, data_buffer)
                file_index += 1
            elif part.text:
                print(part.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_images.py \"your prompt here\" [output_file_base]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    output_base = sys.argv[2] if len(sys.argv) > 2 else "generated_image"
    generate(user_prompt, output_base)
