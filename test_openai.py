import os
from openai import OpenAI

# OpenAI კლიენტი
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# პატარა ტესტი ტექსტზე
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "გამარჯობა, მუშაობს თუ არა API?"}
    ]
)

print(resp.choices[0].message)

