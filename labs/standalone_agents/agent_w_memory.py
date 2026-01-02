import os
import time
import requests
from typing import List, Dict

# ----------------------------
# Config (keep minimal)
# ----------------------------
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
URL = "https://openrouter.ai/api/v1/chat/completions"

CHAT_MODEL = "openai/gpt-4.1-mini"
SUMMARY_MODEL = "openai/gpt-4.1-mini"

WINDOW_TURNS = 6  # keep last N turns (a turn = user + assistant)
TEMPERATURE = 0.7

# Choose how memory is summarized by changing only this:
# Options: "BULLETS", "JSON", "TLDR"
SUMMARY_STYLE = "BULLETS"


# ----------------------------
# OpenRouter call
# ----------------------------
def call_openrouter(model: str, messages: List[Dict], temperature: float = 0.0) -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    resp = requests.post(URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


# ----------------------------
# Memory summarization prompts
# ----------------------------
SUMMARY_PROMPTS = {
    "BULLETS": (
        "You are maintaining a long-term memory summary of a conversation.\n"
        "Update the MEMORY so it remains short, factual, and useful.\n\n"
        "Rules:\n"
        "- Keep at most 12 bullet points.\n"
        "- Prefer stable facts, preferences, goals, commitments, decisions.\n"
        "- Avoid quoting long text.\n"
        "- If something is corrected later, reflect the latest info.\n\n"
        "Return ONLY the updated MEMORY as bullet points.\n"
    ),
    "JSON": (
        "You are maintaining a long-term memory of a conversation.\n"
        "Update the MEMORY into a compact JSON object with keys:\n"
        "{\n"
        '  "facts": [..],\n'
        '  "preferences": [..],\n'
        '  "goals": [..],\n'
        '  "open_questions": [..]\n'
        "}\n\n"
        "Rules:\n"
        "- Each list should be <= 6 items.\n"
        "- Keep items short.\n"
        "- Reflect the latest corrections.\n\n"
        "Return ONLY valid JSON.\n"
    ),
    "TLDR": (
        "You are maintaining a long-term memory summary of a conversation.\n"
        "Update MEMORY into a very short paragraph (max 80 words).\n"
        "Focus on stable facts, decisions, and what matters for continuing.\n"
        "Return ONLY the updated MEMORY.\n"
    ),
}


def update_memory(existing_memory: str, transcript: List[Dict]) -> str:
    """
    Summarize the provided transcript into the long-term memory.
    We keep this simple: pass the existing memory + the transcript to a summarizer prompt.
    """
    style_prompt = SUMMARY_PROMPTS.get(SUMMARY_STYLE, SUMMARY_PROMPTS["BULLETS"])

    # Create a compact text transcript for summarization
    lines = []
    for m in transcript:
        role = m["role"]
        content = m["content"].strip()
        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")
    transcript_text = "\n".join(lines)

    messages = [
        {"role": "system", "content": style_prompt},
        {"role": "user", "content": f"EXISTING MEMORY:\n{existing_memory or '(empty)'}\n\nNEW TRANSCRIPT:\n{transcript_text}"},
    ]

    return call_openrouter(SUMMARY_MODEL, messages, temperature=0.0).strip()


def build_chat_messages(memory: str, window: List[Dict]) -> List[Dict]:
    """
    Build messages for the main chat call:
    - system instruction
    - memory (as context)
    - the recent windowed conversation
    """
    system = {
        "role": "system",
        "content": (
            "You are a helpful assistant.\n"
            "You may use the MEMORY section as long-term context.\n"
            "If MEMORY is irrelevant, ignore it.\n"
            "Be concise and accurate."
        ),
    }

    memory_msg = {
        "role": "system",
        "content": f"MEMORY (summary of earlier conversation):\n{memory or '(empty)'}",
    }

    return [system, memory_msg] + window


def trim_to_last_n_turns(conversation: List[Dict], n_turns: int) -> List[Dict]:
    """
    Keep only the last n turns (user+assistant pairs).
    Conversation format is alternating user/assistant, but we won't assume perfect alternation.
    We'll approximate turns by counting user messages from the end.
    """
    if n_turns <= 0:
        return []

    # Walk backwards, count user messages as turn boundaries
    kept = []
    user_count = 0
    for m in reversed(conversation):
        kept.append(m)
        if m["role"] == "user":
            user_count += 1
            if user_count >= n_turns:
                break

    return list(reversed(kept))


def main():
    print("Agent with window + memory summary. Type 'exit' to quit.\n")
    print(f"WINDOW_TURNS={WINDOW_TURNS} | SUMMARY_STYLE={SUMMARY_STYLE}\n")

    conversation: List[Dict] = []
    memory_summary: str = ""

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        conversation.append({"role": "user", "content": user_input})

        # If conversation is bigger than our window, summarize the older part into memory
        window = trim_to_last_n_turns(conversation, WINDOW_TURNS)
        older = conversation[: max(0, len(conversation) - len(window))]

        if older:
            # Only summarize when there's enough new older content to matter:
            # (You can tune this; keeping simple.)
            memory_summary = update_memory(memory_summary, older)
            # Drop the older part from the stored conversation (we've compressed it into memory)
            conversation = window

        # Call main model with memory + window
        messages = build_chat_messages(memory_summary, conversation)

        start = time.time()
        try:
            assistant_reply = call_openrouter(CHAT_MODEL, messages, temperature=TEMPERATURE)
        except requests.HTTPError as e:
            print(f"\n[HTTP error] {e}\n")
            continue
        except Exception as e:
            print(f"\n[Error] {e}\n")
            continue

        elapsed = time.time() - start

        conversation.append({"role": "assistant", "content": assistant_reply})

        print(f"\nAssistant ({elapsed:.2f}s):")
        print(assistant_reply.strip())
        print("\n---")
        print("Debug:")
        print(f"- memory chars: {len(memory_summary)}")
        print(f"- window msgs: {len(conversation)}")
        print("---\n")


if __name__ == "__main__":
    main()
