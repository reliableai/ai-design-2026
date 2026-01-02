

import requests
import json
import time

OPENROUTER_API_KEY = "<read from env in real code>"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "openai/gpt-4.1-mini",
    "messages": [
        {"role": "user", "content": "Explain Software 3.0 in one sentence."}
    ],
    "temperature": 0.7,
}

start = time.time()
response = requests.post(url, headers=headers, json=payload)
elapsed = time.time() - start

data = response.json()
text = data["choices"][0]["message"]["content"]

print("Response:")
print(text)
print(f"\nLatency: {elapsed:.2f}s")


# varoations: change temperature and see
# change prompt and see

