from dotenv import load_dotenv
import os, base64
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

print("Calling client.images.generate() ...")
resp = client.images.generate(
    model="gpt-image-1",
    prompt="A small modern house in a green field, photorealistic",
    size="512x512"
)

print("Response: ", resp.data[0].keys() if hasattr(resp.data[0], 'keys') else "no keys")
b64 = resp.data[0].b64_json if hasattr(resp.data[0], 'b64_json') else None
if not b64:
    print("No base64 found; trying URL")
    try:
        print("URL:", resp.data[0].url)
    except Exception as e:
        print("No URL either:", e)
else:
    img_bytes = base64.b64decode(b64)
    with open("test_house.png", "wb") as f:
        f.write(img_bytes)
    print("Saved test_house.png")
