import requests
import time

OPENROUTER_API_KEY = "<read from env in real code>"
URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

print("Stateless agent. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    payload = {
        "model": "openai/gpt-4.1-mini",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
    }

    start = time.time()
    response = requests.post(URL, headers=headers, json=payload)
    elapsed = time.time() - start

    data = response.json()
    assistant_reply = data["choices"][0]["message"]["content"]

    print(f"\nAssistant ({elapsed:.2f}s):")
    print(assistant_reply)
    print()
