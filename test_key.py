from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
k = os.getenv("OPENAI_API_KEY")
print("KEY present?", bool(k))
if not k:
    raise SystemExit("Set OPENAI_API_KEY in .env first")

c = OpenAI(api_key=k)
print("Calling a tiny image test (this may cost credits)...")

r = c.images.generate(
    model="gpt-image-1",
    prompt="Tiny test: red dot on white",
    size="1024x1024",   # შეცვალე აქ
)

print("Response object:", r)

# შენახვა სურათად
import base64
img_data = r.data[0].b64_json
img_bytes = base64.b64decode(img_data)
with open("test_output.png", "wb") as f:
    f.write(img_bytes)

print("Saved test_output.png ✅")

