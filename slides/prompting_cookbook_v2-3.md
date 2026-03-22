# Prompting Cookbook (Oct 2025+) — Reusable Patterns for Modern LLMs

A practical **prompting cookbook** for a course on Designing AI Systems. Each "recipe" is a reusable pattern with **examples** for:
- **Chat UIs** (what you type — ChatGPT, Claude.ai, Gemini)
- **APIs** (what you send — OpenAI Responses API, Anthropic Messages API)

> **Focus:** post-Oct 2025 prompting norms — explicit reasoning controls, schema enforcement, eval-first prompting, and multi-model awareness.
>
> **Scope:** This lecture covers **prompting techniques only**. Tool use, memory/context management, and agentic architectures are covered in later lectures.

---

## Why multi-model?

This cookbook shows patterns for **OpenAI GPT-5.x** and **Anthropic Claude 4.x** (with notes on Google Gemini 3 where behavior diverges). The reason is pedagogical: prompting techniques are largely universal, but the details of *how* each model responds to them differ — and as designers of AI systems, you need to understand those differences. Where a recipe works identically across models, we show one example. Where behavior diverges, we flag it.

> **A note on model identifiers:** API examples below use specific model strings like `gpt-5.2` and `claude-sonnet-4-5-20250929`. These are current as of Feb 2026 but will change as new versions are released. Always check the vendor's model page for current identifiers. The *prompting patterns* are durable; the model strings are not.

---

## A key meta-insight (read this first)

A striking convergence across all vendor documentation (Anthropic, OpenAI, Google): **as models get smarter, prompts should get shorter and more direct.** Anthropic's context engineering guide describes seeking "the smallest possible set of high-signal tokens." Google's Gemini 3 guidance says prompts that were necessary for Gemini 2.x now feel bloated. OpenAI's GPT-5.2 guide says ambiguity, not insufficient prompting, is the primary cause of poor results.

This does *not* mean prompts should be vague. The art is **calibrating the right level of specificity** — the Goldilocks zone between brittle over-specification and vague under-specification. Anthropic's context engineering guide calls this finding the "right altitude." (See Sources section for links.)

Another way to say this: **modern models follow instructions literally.** Claude 4.x in particular will do exactly what you ask — no more, no less. If you want thoroughness, ask for it. If you want brevity, specify it. Don't rely on the model to infer your intent from vague prompts.

> ⚠️ **Common misreading:** "Shorter prompts" does not mean "drop your constraints." It means: remove *redundant* guardrails and over-explanation that the model doesn't need. You should still specify output format, constraints, audience, and verification criteria. The savings come from removing things like "Please note that you should be careful to..." — not from removing structure.

---

## How to use this cookbook

1. Pick the recipe that matches your task.
2. Copy the **UI prompt** or the **API payload**.
3. Adjust only the **ingredients** (constraints, schema, tools, evaluation bar).
4. Combine recipes freely — e.g., Recipe 4 (few-shot) + Recipe 5 (output clamp) + Recipe 12 (self-check).
5. If something isn't working as expected, check **Appendix D (FAQ)** — your question is probably there.

---

## UI vs API — what changes and what doesn't

Understanding the boundary between UI and API is essential for system designers. In principle, the underlying model family is the same — but in practice, UIs may route to different model variants, apply hidden system layers, or gate features in ways that make behavior diverge. The *interface* controls what you can see and enforce.

| Capability | Chat UI | API |
|---|---|---|
| **Core prompting** | Same — instructions, examples, roles all work | Same |
| **System prompt** | Set by the product (hidden); you can sometimes influence via Projects/Custom Instructions | Controlled by the developer |
| **Reasoning depth** | Model picker or "Thinking" toggle | `reasoning.effort` (OpenAI) or `budget_tokens` in extended thinking (Anthropic) |
| **Structured outputs** | Best-effort (ask for JSON and hope) | **Enforced** via JSON Schema (OpenAI `text.format`) or Anthropic tool-use schemas |
| **Response prefilling** | Not available | Anthropic API: you can prefill the start of the assistant response |
| **Tools** | Product-managed (web search, file upload, code interpreter) | Developer-defined (you declare tools, model decides when to call them) |
| **Memory** | Product-managed (ChatGPT Memory, Claude memory, Projects) | Developer-managed (you build the state store + retrieval) |
| **Hidden layers** | UI may apply product/system instructions not visible to you | Much more transparent — you control what you send, though platform-level safety policies and content filters may still operate invisibly |

**Teaching point:** When a prompt works in the UI but fails in the API (or vice versa), the cause is almost always in this table — hidden system prompts, model routing, tool availability, or output enforcement differences.

---

## Recipe index

### Core prompting (this lecture)
0. Migration / tuning loop
1. Universal prompt skeleton
2. Direct instruction (baseline)
3. Role prompting (expert stance)
4. Few-shot pattern induction
5. Output-shape clamp + response prefilling
6. Scope discipline
7. Structured formatting with delimiters
8. Schema extraction (UI) + strict schema (API)
9. Reasoning depth (fast vs. deliberate)
10. Long-context placement strategy
11. Self-check / revise loop
12. Evaluation-first prompting
13. Adversarial / red-team prompting
14. Decompose: plan → execute → verify
15. Prompt chaining (multi-call decomposition)
16. Multi-agent simulation

### Previews (future lectures)
17. Web research with citations *(→ tool-use lecture)*
18. File-grounded answers / RAG *(→ context lecture)*
19. Stateful work *(→ memory lecture)*
20. Memory-aware prompting *(→ memory lecture)*
21. Multimodal prompting *(→ vision lecture)*

---

# 0 · Migration / tuning loop

## Use when
You're moving a workflow to a newer model (or seeing regressions after a model update).

## Why this exists
Models change. A prompt optimized for GPT-4o or Claude 3.5 may behave differently on GPT-5.2 or Claude 4.x. Rather than guessing, you run controlled comparisons. This is the "eval your eval" mindset applied to prompts.

## UI example (manual A/B)
```text
Run this task twice:
- First: produce the answer quickly (minimal reasoning)
- Second: produce a more careful answer (step-by-step)

Then:
1) Compare outputs side by side
2) Identify what improved and what regressed
3) Propose 2 prompt changes that fix regressions without harming improvements
Task: [paste]
```

## API example — OpenAI (pin effort + iterate)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "none" },
  "input": "[your existing prompt]"
}
```
Re-run with `"effort": "low"`, `"medium"`, `"high"` while keeping the prompt identical.

## API example — Anthropic (extended thinking)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 8000,
  "messages": [{ "role": "user", "content": "[your existing prompt]" }]
}
```
Then compare with extended thinking enabled:
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 8000,
  "thinking": { "type": "enabled", "budget_tokens": 5000 },
  "messages": [{ "role": "user", "content": "[your existing prompt]" }]
}
```

## Cross-model note
Anthropic's Claude 4.x migration guide advises: **dial back emphatic language**. Prompts with "CRITICAL: You MUST..." that were needed for older models may now cause overtriggering on newer models. Their recommended fix: replace with normal phrasing like "Use this tool when..." (Source: [Anthropic prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices))

---

# 1 · Universal prompt skeleton

## Use when
You want a stable structure for almost any task.

## Ingredients
- Role (optional but helpful)
- Objective (one sentence)
- Context (facts, input data)
- Constraints (audience, length, inclusions/exclusions)
- Output format (exact structure)
- Verification rule (quality gate)

## UI prompt (works across all models)
```text
ROLE:
You are a [role].

OBJECTIVE:
[one sentence goal]

CONTEXT:
[bullets of facts, input data, pasted text]

CONSTRAINTS:
- Audience:
- Length:
- Must include / must not include:
- Tone:

OUTPUT FORMAT:
[exact headings / JSON / bullets]

VERIFY:
Before finalizing, check: correctness, missing edge cases, format compliance.
Return final answer only.
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "low" },
  "input": [
    { "role": "system", "content": "You are a [role]. Follow format exactly." },
    { "role": "user", "content": "OBJECTIVE: ...\nCONTEXT: ...\nCONSTRAINTS: ...\nOUTPUT FORMAT: ..." }
  ]
}
```

## API — Anthropic (XML variant)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 2000,
  "system": "You are a [role]. Follow the instructions precisely.",
  "messages": [{
    "role": "user",
    "content": "<objective>\n[one sentence goal]\n</objective>\n\n<context>\n[facts, input data]\n</context>\n\n<constraints>\n- Audience:\n- Length:\n- Must include / must not include:\n</constraints>\n\n<output_format>\n[exact structure]\n</output_format>"
  }]
}
```

## Cross-model note
Anthropic's recommended delimiter for Claude is **XML tags** (`<context>`, `<instructions>`, etc.) — Claude is trained to parse these with high fidelity. OpenAI works well with both `LABEL:` sections and XML. Google Gemini 3 responds best to short labeled sections. See Recipe 7 for a full comparison.

---

# 2 · Direct instruction (baseline)

## Use when
Simple transformations, quick explanations, short outputs. This is the "hello world" of prompting.

## Why it works
Modern models excel at following literal instructions. For straightforward tasks, a clear direct prompt is often all you need. Adding advanced techniques to a simple task just adds cost and latency.

## UI example
```text
Summarize the following for a VP:
- exactly 5 bullets
- include 1 risk + 1 recommendation
Text:
[paste]
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "none" },
  "input": "Summarize for a VP in exactly 5 bullets; include 1 risk and 1 recommendation:\n[paste]"
}
```

## API — Anthropic
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Summarize the following for a VP:\n- exactly 5 bullets\n- include 1 risk + 1 recommendation\n\nText:\n[paste]"
  }]
}
```

## Tip
If you see output drift (too long, inconsistent structure across runs), add Recipe 5 (output-shape clamp).

---

# 3 · Role prompting (expert stance)

## Use when
Reviews, critiques, domain voice, consistent judgment.

## What it does and doesn't do
- **Does:** Shape tone, vocabulary, depth, and framing. An "SRE reviewer" writes differently than a "product manager."
- **Does not:** Improve factual correctness. Practitioner research consistently shows role prompting helps with register and focus, not with getting facts right. Don't use personas as a substitute for grounding.

## UI example (SRE reviewer)
```text
Act as a senior SRE reviewing an incident postmortem.
Return:
1) Findings (major)
2) Missing evidence
3) Follow-ups (top 5, ranked by impact)
Postmortem:
[paste]
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "low" },
  "input": [
    { "role": "system", "content": "You are a senior SRE. Be strict, practical, concise." },
    { "role": "user", "content": "Review the postmortem:\n[paste]" }
  ]
}
```

## API — Anthropic (detailed persona with behavioral rules)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 2000,
  "system": "You are a senior SRE reviewing an incident postmortem. Behavioral rules:\n- Flag severity honestly: use CRITICAL / WARNING / SUGGESTION.\n- Be direct on CRITICAL issues; do not soften language.\n- If the postmortem is well-written, say so briefly. Do not invent issues to appear thorough.",
  "messages": [{
    "role": "user",
    "content": "Review the postmortem:\n[paste]"
  }]
}
```

## Cross-model note
**Google Gemini 3 (per Google's prompting guide):** Gemini takes assigned personas very seriously and may sometimes ignore other instructions to maintain persona adherence. Test carefully for conflicts between the persona and your task constraints.

**OpenAI GPT-5.x pattern:** Rather than a simple role label, OpenAI guides recommend detailed personality specs with behavioral rules for different situations — which is why the Anthropic API example above uses this pattern. It works well across models.

---

# 4 · Few-shot pattern induction

## Use when
Classification, style transfer, structured extraction, any task where "show, don't tell" works better than describing the rule.

## Why it's so effective
All vendors rank few-shot examples as the single most effective technique after clarity. Anthropic calls examples "the pictures worth a thousand words." Google recommends always including them. In practitioner benchmarks, few-shot has shown gains of up to ~80% over zero-shot on complex tasks (your mileage will vary — the benefit depends heavily on task complexity and example quality).

## Design principles (these matter)
- **Curate, don't accumulate.** 2–3 diverse, canonical examples beat 10 edge cases.
- **Keep format identical across examples.** If you mix formats, the model will too.
- **Show the pattern, not the anti-pattern.** Examples of correct behavior outperform "don't do this" examples.
- **Cover input diversity.** Include examples representing the range of inputs the model will encounter.
- **Start small, iterate.** Begin with 2–3 examples; add more only if the model fails to generalize.

## UI example (ticket routing)
```text
Label each ticket into: AUTH, NETWORK, BILLING, OTHER.

Examples:
Ticket: "VPN disconnects after 5 minutes." → NETWORK
Ticket: "Can't reset password; email never arrives." → AUTH
Ticket: "Charged twice last month." → BILLING

Now label:
1) "SSO login loops back to sign-in page."
2) "Packet loss to eu-west after 18:00."
3) "Invoice includes seats we removed."

Return JSON array: [{id, label, one_line_rationale}]
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "none" },
  "input": "[same prompt text as UI]"
}
```

## API — Anthropic (using XML to separate examples from task)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Label each ticket into: AUTH, NETWORK, BILLING, OTHER.\n\n<examples>\nTicket: \"VPN disconnects after 5 minutes.\" → NETWORK\nTicket: \"Can't reset password; email never arrives.\" → AUTH\nTicket: \"Charged twice last month.\" → BILLING\n</examples>\n\nNow label these tickets and return a JSON array [{id, label, one_line_rationale}]:\n1) \"SSO login loops back to sign-in page.\"\n2) \"Packet loss to eu-west after 18:00.\"\n3) \"Invoice includes seats we removed.\""
  }]
}
```

## Tip
If you need *guaranteed* JSON shape in production, combine with Recipe 8 (strict schema via API).

## Cross-model note
Anthropic warns: Claude 4.x pays **very close attention** to details in examples. If your example accidentally includes a behavior you don't want (a formatting quirk, an assumption), the model will reproduce it. Review examples carefully.

---

# 5 · Output-shape clamp + response prefilling

## Use when
You want consistent length, structure, and format across runs. Two complementary techniques.

### 5a. Output-shape clamp (all models)
Explicitly constrain the output structure so the model can't drift into "essay mode."

## UI example
```text
Answer with:
- 1 sentence overview
- then exactly 5 bullets labeled: What / Why / Risks / Next / Open questions
No other sections. No preamble.

Question: Propose a rollout plan for feature flags in a microservice platform.
```

## API — OpenAI (verbosity spec pattern from GPT-5.2 guide)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "low" },
  "input": [
    { "role": "system", "content": "Output rules:\n- Simple yes/no questions: 1–2 sentences\n- Typical questions: 3–6 sentences or up to 5 bullets\n- Complex multi-part analysis: 1 overview paragraph + up to 5 labeled bullets (What / Why / Risks / Next / Open Questions)\nDo not rephrase the user's request unless it changes semantics." },
    { "role": "user", "content": "Propose a rollout plan for feature flags in a microservice platform." }
  ]
}
```

### 5b. Response prefilling (Anthropic API only)
Instead of *describing* the format you want, **provide the start of the response** and let the model continue. This is one of the most reliable format-control techniques and is unique to the Anthropic API.

## API — Anthropic (prefilling)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "Compare PostgreSQL, MongoDB, and DynamoDB for a real-time analytics use case."
    },
    {
      "role": "assistant",
      "content": "| Feature | PostgreSQL | MongoDB | DynamoDB |\n|---------|-----------|---------|----------|\n| Query model |"
    }
  ]
}
```

**Effect:** The model is forced to continue the table format exactly. No preamble, no "Here's a comparison:" — it fills in the cells.

## Other prefilling uses
- **Force JSON:** Prefill with `{` to prevent any preamble
- **Skip pleasantries:** Prefill with the first content word
- **Lock into a framework:** Prefill with `## Analysis\n\n### 1.` to force a specific outline

## Cross-model note
Response prefilling is a **Claude-specific API feature**. OpenAI achieves similar effects through strong system prompt constraints or structured outputs (Recipe 8). Google's Gemini docs also highlight providing the start of output as a reliable format control pattern, though without API-level prefilling support.

---

# 6 · Scope discipline ("exactly this, nothing else")

## Use when
Coding diffs, UI changes, or any task that commonly triggers "helpful extras."

## Why this matters now
Modern models (especially Claude 4.x) will do exactly what you ask — but they can also be overly eager if you're vague. If you say "fix this function," a model might refactor the entire file. Scope discipline sets explicit boundaries.

## UI example (frontend change)
```text
Implement EXACTLY this and nothing else:
- Add a "Retry" button that re-calls fetchOrders()
- Show a spinner while loading
- No new components
- No styling changes

If anything is ambiguous, pick the simplest valid interpretation and state it in 1 line at the end.
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "medium" },
  "input": [
    { "role": "system", "content": "Do exactly what is requested. No embellishments." },
    { "role": "user", "content": "[requirements + code snippet]" }
  ]
}
```

## API — Anthropic
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 2000,
  "system": "Implement only what is explicitly requested. Do not add features, refactor surrounding code, or add comments unless asked.",
  "messages": [{
    "role": "user",
    "content": "Implement EXACTLY this in the attached code:\n- Add a \"Retry\" button that re-calls fetchOrders()\n- Show a spinner while loading\n\nIf anything is ambiguous, state the simplest interpretation in 1 line, then proceed.\n\n```javascript\n[paste code]\n```"
  }]
}
```

---

# 7 · Structured formatting with delimiters

## Use when
Complex prompts with multiple components (instructions, context, data, examples). Delimiters prevent the model from confusing your instructions with the content it's processing.

## Why this is a standalone recipe
Research and vendor testing shows that *how* you structure a prompt matters as much as *what* you say. Anthropic's documentation makes XML tags their primary recommendation. OpenAI uses them extensively in their guides too. Getting this right is a measurable quality improvement.

## Delimiter comparison

| Format | Example | Best for |
|---|---|---|
| **XML tags** | `<instructions>...</instructions>` | Claude (primary), OpenAI (works well) |
| **LABEL: sections** | `ROLE:\nCONSTRAINTS:` | Quick UI prompts, Gemini 3 |
| **Markdown headers** | `## Instructions` | General readability |
| **Triple quotes** | `"""content"""` | Separating data from instructions |

## Principles
- **Separate instructions from data.** If the model confuses your instructions with input content, stronger delimiters fix it.
- **Put long data first, instructions last.** For 20K+ token inputs, placing queries at the end can substantially improve quality. Anthropic's documentation reports up to 30% improvement in internal tests; Google's Gemini 3 guide makes the same structural recommendation.
- **Use anchor phrases.** After a large block of data, bridge with "Based on the information above..."
- **Don't over-format.** Formatting is becoming less important as models improve. Use it where it helps comprehension, not as decoration.

## Example: XML-structured prompt (Claude optimized)
```text
<context>
You are reviewing a services contract between Acme Corp and Beta Ltd,
signed January 2025, governing SaaS delivery with a 99.9% uptime SLA.
</context>

<document>
[full contract text here]
</document>

<instructions>
Identify all clauses that could expose Acme Corp to financial liability.
For each clause:
1. Quote the relevant language (max 15 words)
2. Explain the risk in plain English
3. Suggest a protective amendment
Return as a numbered list.
</instructions>
```

## Example: Long-context placement
```text
[10,000 words of research paper text here]

Based on the full paper above, answer:
1. What is the primary research question?
2. What methodology was used?
3. What are the three key findings?
Respond in 3 concise paragraphs.
```

**Teaching point:** Try the same prompt with instructions at the top vs. the bottom. On long inputs, the difference is measurable.

---

# 8 · Schema extraction (UI best-effort) + strict schema (API)

## Use when
Extraction, automation, pipelines — anywhere you need machine-readable output.

## The UI/API gap (important for system design)
This recipe shows the biggest practical difference between UI and API. In the UI, you *ask* for JSON and hope. Via API, you can *enforce* it.

## UI example (best effort — all models)
```text
Extract the following into JSON with exactly these keys:
party_name, jurisdiction, effective_date, termination_summary
Rules:
- If unknown, set null
- No extra keys
Text:
[paste]
```

## API — OpenAI (strict schema; enforced by the platform)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "none" },
  "text": {
    "format": {
      "type": "json_schema",
      "name": "contract_extract",
      "strict": true,
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "party_name": { "type": "string" },
          "jurisdiction": { "type": ["string", "null"] },
          "effective_date": { "type": ["string", "null"] },
          "termination_summary": { "type": ["string", "null"] }
        },
        "required": ["party_name","jurisdiction","effective_date","termination_summary"]
      }
    }
  },
  "input": "Extract the fields from the following text:\n[paste]"
}
```

## API — Anthropic (prefilling + strong instruction)
Anthropic doesn't have OpenAI's `strict` JSON Schema mode, but you can combine **prefilling** (Recipe 5b) with explicit instructions for reliable JSON:
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 500,
  "messages": [
    {
      "role": "user",
      "content": "Extract from the following text into JSON with exactly these keys: party_name, jurisdiction, effective_date, termination_summary. If unknown, use null. No extra keys.\n\nText:\n[paste]"
    },
    {
      "role": "assistant",
      "content": "{"
    }
  ]
}
```
Alternatively, Anthropic supports structured outputs via tool-use schemas — the model returns tool calls with enforced structure.

## Teaching point
This is a clear example of **why API access matters for production systems.** The UI can't guarantee output structure; the API can. If you're building a pipeline that parses model output, always use API-level enforcement.

---

# 9 · Reasoning depth (fast vs. deliberate)

## Use when
You need to trade off latency/cost vs. correctness. Not all tasks need deep reasoning.

## The calibration principle
This is the most commonly misused knob. Extended/deep reasoning is 10/10 for complex tasks (math, multi-step logic, code debugging) but 3/10 for simple queries (classification, translation, formatting). Using high reasoning effort on a simple task just adds cost and latency without improving quality.

## UI examples

### Fast answer
```text
Answer in 2 sentences max. No step-by-step explanation.
What's the difference between precision and recall?
```

### Deliberate answer
```text
Use a careful, step-by-step approach:
1) List 3 possible hypotheses
2) Test each against the evidence
3) Conclude, explaining why the other hypotheses fail
Problem: [paste]
```

## API — OpenAI
### Fast
```json
{ "model": "gpt-5.2", "reasoning": { "effort": "none" }, "input": "2 sentences max. Precision vs recall?" }
```

### Deep
```json
{ "model": "gpt-5.2", "reasoning": { "effort": "high", "summary": "concise" }, "input": "List 3 hypotheses, test, conclude:\n[paste]" }
```

## API — Anthropic
### Fast (no extended thinking)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 500,
  "messages": [{ "role": "user", "content": "In 2 sentences: what's the difference between precision and recall?" }]
}
```

### Deep (extended thinking enabled)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 8000,
  "thinking": { "type": "enabled", "budget_tokens": 5000 },
  "messages": [{ "role": "user", "content": "Analyze this problem step by step. List 3 hypotheses, test each, then conclude:\n[paste]" }]
}
```

## Cross-model notes

| | OpenAI | Anthropic | Google |
|---|---|---|---|
| **Knob** | `reasoning.effort` (none/low/medium/high) | `thinking.budget_tokens` (extended thinking) | Model selection (Flash vs Pro) |
| **Controls** | Single parameter scales reasoning depth | Token budget for thinking; thinking visible in response | Primarily model choice |
| **Sensitive words** | None noted | ⚠️ Per [Anthropic's docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices): Claude can be sensitive to "think" when extended thinking is off — use "consider," "evaluate," "analyze" instead | None noted |
| **Best for** | Granular effort tuning | Complex multi-step reasoning; interleaved thinking after tool use | — |

## Teaching point
**Interleaved thinking** (Anthropic-specific): Claude can be prompted to reflect *after receiving tool results* before proceeding. This is distinct from pre-answer reasoning and is useful in agentic workflows: "After receiving results, carefully evaluate their quality and determine optimal next steps before proceeding."

---

# 10 · Long-context placement strategy

## Use when
Working with large documents (20K+ tokens) — PDFs, policies, knowledge bases, multi-document inputs.

## The principle
Where you place instructions relative to data in a prompt significantly affects quality. This is backed by empirical testing across all three major vendors.

## The rule
**Long data first → instructions last → query at the very end.**

## Example: Poor placement
```text
Answer these questions about the document:
1. What is the log retention period?
2. What are the backup procedures?

Document:
[15,000 words of policy text]
```

## Example: Good placement
```text
<document>
[15,000 words of policy text]
</document>

Based on the document above, answer these questions:
1. What is the log retention period?
2. What are the backup procedures?

For each answer, cite the relevant section number.
```

## Multi-document pattern
```text
<document index="1" source="Security Policy v3.2">
[document 1 text]
</document>

<document index="2" source="Compliance Audit Report Q3">
[document 2 text]
</document>

<instructions>
Compare the two documents. Identify any contradictions between the
stated security policy and the audit findings. Return as a table:
| Finding | Policy says | Audit says | Contradiction? |
</instructions>
```

## Cross-model note
All three vendors converge on this principle. Anthropic's documentation reports up to 30% quality improvement in internal tests with queries placed at the end of long-context inputs. Google's Gemini 3 guide makes the same recommendation. This is one of the few techniques where vendor guidance is unanimous.

---

# 11 · Self-check / revise loop

## Use when
You want a quality boost without tools or multiple API calls. The model drafts, then critiques and revises its own output.

## Why it works
Self-revision forces the model to allocate compute to quality verification rather than generation alone. It's especially effective for factual accuracy, internal consistency, and format compliance.

## UI example (specific self-check criteria)
```text
Draft an answer to the question below.
Then self-check against these criteria:
- Factual accuracy: are all claims correct and verifiable?
- Internal consistency: do the parts of your answer agree?
- Edge cases: did you miss any important exceptions?
- Format: does the output match the requested structure?
Revise once based on your findings.
Return ONLY the revised answer (not the draft or the critique).

Question: Explain MAP vs MRR with a worked example for a 3-query ranking scenario.
```

## API — OpenAI
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "medium" },
  "input": "Draft, then self-check against: factual accuracy, internal consistency, edge cases, format compliance. Revise once. Return revised answer only.\n\nTopic: Explain MAP vs MRR with a worked example for a 3-query ranking scenario."
}
```

## API — Anthropic (critic persona variant)
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "<task>\nExplain MAP vs MRR with a worked example for a 3-query ranking scenario.\n</task>\n\n<process>\n1. Draft your answer.\n2. Then adopt the role of a strict peer reviewer. Check for:\n   - Mathematical correctness in the worked example\n   - Whether edge cases are covered (e.g., no relevant results)\n   - Clarity for a student audience\n3. Revise once based on the review.\n4. Return ONLY the revised answer.\n</process>"
  }]
}
```

## Connection to other recipes
Self-check is the lightweight version of Recipe 13 (adversarial). Use self-check for everyday quality; use adversarial prompting when you need systematic failure analysis.

---

# 12 · Evaluation-first prompting (metrics → baseline → intervention)

## Use when
Research, enterprise AI, "prove it works," KB quality improvements.

## Why this matters
Most people prompt LLMs to *generate solutions*. This recipe flips it: force the model to define success criteria *before* proposing anything. This is the prompting equivalent of test-driven development.

## UI example (KB retrieval)
```text
Before proposing solutions, do this:
1) Define success metrics (with formulas): Recall@k, MRR, citation precision, cost/latency
2) Define baseline + acceptance thresholds
3) Propose 3 interventions (ranked by expected ROI)
4) For each, predict impact and a validation plan (ablation + sample size)
Context: We want to improve KB retrieval quality for IT tickets.
```

## API — any model (high reasoning effort)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "high", "summary": "concise" },
  "input": "[same as UI]"
}
```

---

# 13 · Adversarial / red-team prompting

## Use when
You want robustness: "how does this fail in production?"

## UI example
```text
Propose a solution to: design a KB dedup pipeline.
Then attack it: list 7 failure modes (data, scaling, human process, eval bias).
Then redesign to address the top 3 failure modes.
```

## API — any model
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "high" },
  "input": "[same as UI]"
}
```

---

# 14 · Decompose: plan → execute → verify (single prompt)

## Use when
Complex tasks that benefit from explicit staging — but where you want everything in a single interaction.

## UI example
```text
Do this in 3 stages:

A) PLAN: write a short plan (≤8 bullets)
B) EXECUTE: produce the artifact
C) VERIFY: checklist against requirements; fix any violations

Task: Write a migration guide from REST to GraphQL for a team of backend developers.
Constraints: 1 page max; include code snippets for before/after.
```

## API — any model
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "high", "summary": "concise" },
  "input": "[same as UI]"
}
```

## When this isn't enough → Recipe 15 (prompt chaining)

---

# 15 · Prompt chaining (multi-call decomposition)

## Use when
The task is too complex for a single prompt, or you need to verify intermediate results before proceeding.

## How it differs from Recipe 14
Recipe 14 (plan/execute/verify) happens in **one prompt**. Prompt chaining uses **separate API calls**, where the output of each becomes the input for the next. This gives you control over each stage.

## Why this matters for system design
Prompt chaining is the bridge between "prompting" and "building an AI system." Once you chain prompts, you're designing a pipeline — and pipeline design (error handling, state management, intermediate validation) is engineering.

## Example: Research synthesis pipeline

### Call 1 — Extract
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "low" },
  "input": "Read these 5 paper abstracts. For each, extract:\n- Primary research question\n- Methodology\n- Key finding (one sentence)\nReturn as JSON array.\n\n[abstracts]"
}
```

### Call 2 — Analyze (receives Call 1 output)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "medium" },
  "input": "Given these extracted findings:\n{call_1_output}\n\nGroup by methodology. Identify agreements, contradictions, and gaps.\nReturn a structured comparison."
}
```

### Call 3 — Generate (receives Call 2 output)
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "high" },
  "input": "Based on this comparison:\n{call_2_output}\n\nWrite a 500-word literature review section. Academic tone. Highlight the key unaddressed gap."
}
```

## Why chain?
Each step is a different **capability** (extraction, analysis, generation). Separating them:
- Lets you verify intermediate results
- Prevents the model from cutting corners on early steps to save tokens for generation
- Lets you use different models or reasoning levels per step (e.g., fast extraction, deep analysis)
- Gives you a clear debugging surface when something goes wrong

## Cross-model note
Anthropic specifically recommends chaining for complex tasks. Their docs include a case study where a Fortune 500 company improved accuracy by chaining: list codes → identify sections → answer.

---

# 16 · Multi-agent simulation (single prompt)

## Use when
You want multiple perspectives without building a full multi-agent system.

## UI example
```text
Simulate 3 reviewers:

Reviewer A (Architect): propose design
Reviewer B (SRE): identify reliability risks
Reviewer C (Security): identify attack vectors

Then synthesize:
- 5 key decisions
- 5 key risks
- a recommended plan

Problem: Build a workflow that uses KB + ticket history to draft incident resolutions.
```

## API — any model
```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "high" },
  "input": "[same as UI]"
}
```

## Cross-model note
This is a combination of Recipe 3 (role prompting) and Recipe 13 (adversarial). It works across all models. **Field note:** In our testing, Google Gemini 3 takes personas especially seriously — if one simulated agent has a strong persona, it may dominate the synthesis. Worth testing for balance. (Google's Gemini 3 prompting guide warns that the model may prioritize persona adherence over other instructions.)

---

# Recipes 17–21: Previews (covered in future lectures)

These recipes involve tool use, memory, or context management — topics for later sessions. Brief descriptions for reference:

**17. Web research with citations** *(→ tool-use lecture)*
Prompting the model to use web search tools, cite sources, and resolve contradictions.

**18. File-grounded answers / RAG** *(→ context lecture)*
Grounding answers in uploaded documents. Key prompting pattern: "Use ONLY the uploaded document as ground truth. Quote exact lines."

**19. Stateful work** *(→ memory lecture)*
Maintaining conversational context across API calls. OpenAI uses `previous_response_id`; Anthropic requires explicitly re-sending context. Key gotcha: system instructions may not carry over automatically.

**20. Memory-aware prompting** *(→ memory lecture)*
Using project-level memory, custom instructions, or developer-managed state to maintain preferences across sessions.

**21. Multimodal prompting** *(→ vision lecture)*
Sending images, diagrams, or charts alongside text for analysis.

---

## Appendix A — Prompt modules library (copy/paste blocks)

These are reusable blocks you can insert into any recipe. They're the "spice rack" of the cookbook.

### A1 · Ambiguity guard (no back-and-forth)
```text
If ambiguous, do NOT ask clarifying questions.
Instead: provide 2–3 interpretations, label assumptions, then proceed with the most likely one.
```

### A2 · Extraction discipline
```text
If a field is missing or unknown, use null. Never invent values. No extra keys.
```

### A3 · Research bar
```text
Search until marginal value drops. Use at least 5 sources. Resolve contradictions. Cite sources.
```

### A4 · "No scope creep"
```text
Do exactly what is requested. Do not add features, sections, or commentary unless asked.
```

### A5 · "Show work" without verbosity explosion
```text
Do internal reasoning as needed, but keep the final answer short and structured.
```

### A6 · "When NOT to use" guard (⚠️ important)
This is arguably the most important module in the appendix. Advanced techniques (CoT, multi-agent, adversarial, self-check) are powerful but can become a crutch.
```text
Before applying an advanced technique, ask:
1. Is this task simple enough that a direct instruction (Recipe 2) would work?
2. Am I adding this technique because it genuinely helps, or because it feels more thorough?
3. What's the cost? (Extra tokens = extra latency + extra spend)
If the answer to #1 is yes, skip the technique. Simpler is better until it isn't.
```
**Rule of thumb for students:** Start with the simplest recipe that could work. Escalate only when you see concrete failures (wrong output, inconsistent format, missed edge cases). Don't pre-optimize.

---

## Appendix B — API knobs cheat sheet

### OpenAI (Responses API)
| Knob | Values | Purpose |
|---|---|---|
| `reasoning.effort` | none / low / medium / high | Controls depth of reasoning |
| `reasoning.summary` | concise | Short summary of reasoning chain |
| `tools` + `tool_choice` | web_search, file_search, etc. | Enable/force tool use |
| `text.format` | json_schema (with `strict: true`) | Enforce output schema |
| `previous_response_id` | response ID string | Maintain state across turns |

### Anthropic (Messages API)
| Knob | Values | Purpose |
|---|---|---|
| `thinking.type` | enabled / disabled | Extended thinking on/off |
| `thinking.budget_tokens` | integer | Token budget for thinking |
| `system` | string | System prompt (fully controlled by developer) |
| Assistant prefill | Partial assistant message | Force output format (see Recipe 5b) |
| Tool-use schemas | JSON Schema in tool definitions | Enforce structured outputs via tools |
| `max_tokens` | integer | Hard cap on output length |

### Key differences
- **Structured outputs:** OpenAI enforces via `text.format` with `strict: true`. Anthropic enforces via tool-use schemas or prefilling.
- **Reasoning control:** OpenAI has a simple effort dial. Anthropic gives a token budget for extended thinking.
- **Response prefilling:** Anthropic-only feature; OpenAI achieves similar with strong system prompts.
- **System prompt:** Both support it, but Anthropic's Claude 4.x is particularly responsive to system prompt instructions.

---

## Appendix C — Recipe combination cheat sheet

| Goal | Combine |
|---|---|
| Reliable extraction pipeline | Recipe 4 (few-shot) + Recipe 8 (strict schema) + Recipe 11 (self-check) |
| Deep analysis report | Recipe 3 (role) + Recipe 9 (high reasoning) + Recipe 14 (plan/execute/verify) |
| Production-grade classifier | Recipe 4 (few-shot) + Recipe 5 (output clamp) + Recipe 8 (strict schema) |
| Research synthesis | Recipe 15 (prompt chaining) + Recipe 12 (eval-first) |
| Stress-testing a design | Recipe 13 (adversarial) + Recipe 16 (multi-agent) |
| Simple task, fast | Recipe 2 (direct) + Recipe 9 (fast reasoning) — and nothing else |

---

## Appendix D — FAQ: Likely questions and honest answers

These are the pushbacks and confusions that come up most often. If you're reading this before class, treat them as a self-test.

---

### "Isn't prompt engineering mostly placebo now?"

Less than before — but structure, constraints, and schema enforcement still matter because they reduce ambiguity and output variance. The "just say what you want" approach works for simple tasks. For anything that needs consistency, measurability, or integration into a pipeline, you must specify format + constraints + verification. That's not magic; that's engineering.

---

### "You say prompts should get shorter — won't that make outputs worse?"

Shorter *after removing redundancy.* Keep the high-signal bits: output shape, constraints, success criteria, verification. Cut the low-signal bits: hedging language, over-explanation of things the model already knows, "please note that..." preambles. If you're not sure what's redundant, start minimal → test → add only what fixes observed failures (format drift, missing sections, wrong audience).

---

### "Roles and personas feel like cosplay. Do they actually help?"

They improve *style and focus*, not *factual truth.* Use roles for framing (tone, vocabulary, assumed reader knowledge). Use grounding, evals, and tools for correctness. Don't confuse a confident-sounding persona with an accurate one.

---

### "Why not always set reasoning to max?"

Cost + latency + diminishing returns. Deep reasoning is powerful for complex multi-step problems, but on simple tasks it can actually introduce overthinking or verbosity without improving quality. Calibrate to task complexity — that's what Recipe 9 is about.

---

### "Do we still need chain-of-thought prompting?"

Often not explicitly. Modern models reason internally when the task demands it. A better default pattern: ask for structured outputs + verification criteria, and only invoke explicit step-by-step reasoning when you're seeing errors that suggest the model is "jumping to conclusions." See also the reasoning effort knobs in Appendix B — these let you control thinking depth without CoT prompting.

---

### "If JSON schemas exist, why bother with few-shot examples?"

Schemas enforce *shape* (keys, types, nesting). Examples teach *semantics* — label boundaries, decision policy, edge-case handling, stylistic conventions. You often need both: the schema guarantees parseable output, the examples ensure the *content* of that output is what you want.

---

### "Can I replace examples with longer instructions?"

Sometimes, but examples are higher-signal and reduce misinterpretation — especially for classification, style transfer, and edge cases. The reason is simple: an example demonstrates a decision boundary implicitly; an instruction tries to describe it explicitly. The implicit version is often more reliable.

---

### "Response prefilling seems hacky. Why teach it?"

Because it's one of the most reliable format-control techniques where available. Think of it as a "format control primitive" — it removes ambiguity about output structure at the lowest possible level. It's not a hack; it's using the API as designed.

---

### "Does 'put instructions at the end' always win?"

Mostly for long contexts (10K+ tokens). For short inputs, placement rarely matters. Teach it as a default for long-document workflows and ignore it for quick queries.

---

### "What if the model ignores my constraints with long documents?"

Use stronger delimiters (XML tags, not just labels) + restate constraints immediately before the question + require citations or quotes from the source material. If it still fails, consider prompt chaining (Recipe 15) to break the task into focused steps.

---

### "Isn't evaluation-first overkill? I just want an answer."

For a one-off answer, yes — skip it. For a system you're shipping, it's the only way to avoid deploying "good-sounding" but unproven improvements. The eval-first pattern (Recipe 12) is the prompting equivalent of writing tests before code. It feels slow until it saves you from a bad deployment.

---

### "How do we evaluate subjective tasks like writing quality or helpfulness?"

Define rubrics, use pairwise preference tests, or set up human scoring with calibration. "Subjective" doesn't mean "unevaluable" — it means you need to be explicit about *what* you're measuring and *who* is the judge.

---

### "Why teach multi-model? We'll standardize on one vendor."

Even within one vendor, models change. Multi-model thinking builds robustness and forces you to separate the *pattern* (constraints, structure, examples, verification) from the *vendor knob* (reasoning.effort, budget_tokens, text.format). Patterns persist across model updates; knobs don't.

---

### "Won't vendor differences make this cookbook outdated?"

The knobs will age — that's inevitable (see the model identifier note at the top). The patterns won't, because they address fundamental properties of how language models process context: clarity reduces ambiguity, examples reduce misinterpretation, structure reduces output variance, and verification catches errors. These hold regardless of vendor.

---

---

## Sources and further reading

Vendor-specific behavioral claims in this cookbook are drawn from the following documentation (all accessed Feb 2026):

- **Anthropic** — [Prompting best practices (Claude 4.x)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) · [Migrating to Claude 4.5](https://docs.anthropic.com/en/docs/about-claude/models/migrating-to-claude-4) · [Extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) · [Context engineering for AI agents](https://www.anthropic.com/engineering/context-engineering) (Sep 2025)
- **OpenAI** — [GPT-5.1 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide) (Nov 2025) · [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide) (Dec 2025)
- **Google** — [Gemini 3 Prompting Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) (Nov 2025) · [Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

Practitioner sources:
- Giggs, D.R. — "Prompting and Prompt Engineering: A Comprehensive Guide" (Medium, Dec 2025)
- Ummareddy, N. — "Top 5 Prompt Engineering Techniques for LLMs in 2025" (Medium, Oct 2025)
- K2view — "Prompt Engineering Techniques: Top 6 for 2026" (Nov 2025)

---

*This cookbook accompanies the lecture on Prompting in the course "Designing AI Systems." Later lectures will cover context/memory management, tool use, agentic architectures, and evaluation.*
