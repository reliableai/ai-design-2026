import argparse
import json
import random
import time
from pathlib import Path

import jinja2
from datasets import load_dataset
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load OPENAI_API_KEY from .env

client = OpenAI()  # Automatically uses OPENAI_API_KEY env var

GENERATOR_MODEL = "gpt-4.1-mini"
JUDGE_MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.7
ROW_INDEX = 42  # None = random row
TEXT_FIELD = "body"  # Field in the dataset to use as input text (it may vary by dataset, e.g. "text" or "body")
DATASET = "Tobi-Bueck/customer-support-tickets"


def render_template(env: jinja2.Environment, name: str, context: dict) -> str:
    template = env.get_template(name)
    return template.render(**context)


def call_model(prompt: str, model: str, temperature: float) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content


def run_external_judge_only(
    env: jinja2.Environment,
    request_text: str,
    generator_model: str,
    judge_model: str,
    temperature: float,
) -> tuple[str, str]:
    gen_prompt = render_template(env, "generation_only.j2", {"request": request_text})
    extraction = call_model(gen_prompt, generator_model, temperature)

    judge_prompt = render_template(
        env,
        "external_judge.j2",
        {"request": request_text, "extraction": extraction},
    )
    review = call_model(judge_prompt, judge_model, temperature)
    return extraction, review


def run_external_judge_with_correction(
    env: jinja2.Environment,
    request_text: str,
    generator_model: str,
    judge_model: str,
    temperature: float,
) -> tuple[str, str, str]:
    gen_prompt = render_template(env, "generation_only.j2", {"request": request_text})
    extraction = call_model(gen_prompt, generator_model, temperature)

    judge_prompt = render_template(
        env,
        "external_judge_correction.j2",
        {"request": request_text, "extraction": extraction},
    )
    review_and_fix = call_model(judge_prompt, judge_model, temperature)
    payload = json.loads(review_and_fix)
    corrected_extraction = {
        "intent": payload.get("corrected_intent"),
        "symptoms": payload.get("corrected_symptoms"),
    }
    second_judge_prompt = render_template(
        env,
        "external_judge.j2",
        {"request": request_text, "extraction": corrected_extraction},
    )
    second_review = call_model(second_judge_prompt, judge_model, temperature)
    return extraction, review_and_fix, second_review


def run_internal_judge(
    env: jinja2.Environment,
    request_text: str,
    model: str,
    temperature: float,
) -> str:
    prompt = render_template(
        env, "internal_judge_correction.j2", {"request": request_text}
    )
    return call_model(prompt, model, temperature)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run extraction/judging tests using Jinja templates."
    )
    parser.add_argument(
        "--test",
        choices=["external", "external-revise", "internal"],
        default="external-revise",
        help="Which test to run: external, external-revise, or internal",
    )
    args = parser.parse_args()

    ds = load_dataset(DATASET, split="train")

    if ROW_INDEX is None:
        row = random.choice(ds)
    else:
        if ROW_INDEX < 0 or ROW_INDEX >= len(ds):
            raise IndexError(f"Row index out of range: {ROW_INDEX} (0..{len(ds)-1})")
        row = ds[int(ROW_INDEX)]
    print("=== DATASET ROW ===")
    print(row)
    request_text = row[TEXT_FIELD]

    template_dir = Path(__file__).resolve().parent
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    start = time.time()

    if args.test == "external":
        extraction, review = run_external_judge_only(
            env,
            request_text,
            GENERATOR_MODEL,
            JUDGE_MODEL,
            TEMPERATURE,
        )
        print("\n=== REQUEST ===")
        print(request_text)
        print("\n=== EXTRACTION ===")
        print(extraction)
        print("\n=== EXTERNAL JUDGE REVIEW ===")
        print(review)
    elif args.test == "external-revise":
        extraction, review_and_fix, second_review = run_external_judge_with_correction(
            env,
            request_text,
            GENERATOR_MODEL,
            JUDGE_MODEL,
            TEMPERATURE,
        )
        print("\n=== REQUEST ===")
        print(request_text)
        print("\n=== EXTRACTION ===")
        print(extraction)
        print("\n=== EXTERNAL JUDGE REVIEW + CORRECTION ===")
        print(review_and_fix)
        print("\n=== EXTERNAL JUDGE REVIEW (ON CORRECTED OUTPUT) ===")
        print(second_review)
    else:
        internal_result = run_internal_judge(
            env,
            request_text,
            JUDGE_MODEL,
            TEMPERATURE,
        )
        print("\n=== REQUEST ===")
        print(request_text)
        print("\n=== EXTRACTION AND INTERNAL JUDGE REVIEW ===")
        print(internal_result)

    elapsed = time.time() - start
    print(f"\n⏱ {elapsed:.2f}s")


if __name__ == "__main__":
    main()
