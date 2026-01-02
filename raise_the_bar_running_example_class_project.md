# Raise the Bar — Running Example & Class Project

*(Living project specification — to be refined iteratively during the course)*

---

## 1. Purpose of the running example

**Raise the Bar** is the canonical running example and class project for *Designing Large Scale AI Systems*.

It can be instantiated in multiple, equivalent contexts:
- a **conference management system** (academic or industry)
- a **class / course management system** (peer review, feedback, advising)
- an **internal industry conference or review process**

Across all instantiations, the core goal is the same:

> Combine **human judgment** and **AI assistance** to improve the *quality of work and feedback*, not merely to assess or rank.

Raise the Bar is intentionally chosen because it:
- involves multi-party review workflows
- blends assessment with advice and improvement
- requires careful handling of tone, fairness, and authority
- naturally creates conversations between authors, reviewers, and organizers
- benefits from AI assistance without full automation

---

## 2. Two perspectives we will study

This project is used from **two complementary perspectives**.

### 2.1 Service provider perspective

Think: *conference platform / class management system / internal review system*

Key question:
> How does a platform expose its services so that AI systems can safely and productively assist reviewers, authors, and organizers?

From this perspective, Raise the Bar acts as:
- a **platform** that owns workflows, data, and permissions
- a system coordinating reviews, feedback, and conversations
- a provider of MCP servers exposing tools, resources, and prompts

---

### 2.2 AI system developer perspective

Think: *developer building an AI-powered assistant for reviewing and improvement*

Key question:
> How do I build an AI system that helps humans review, advise, and improve work — while respecting boundaries and authority?

From this perspective, Raise the Bar acts as:
- a **host application** or agent runtime
- a consumer of MCP servers provided by the platform
- an orchestrator of agents, tools, and conversations

---

### 2.2 AI system developer perspective

Think: *developer building an AI-powered assistant or workflow*

Key question:
> How do I build an AI system that consumes MCP servers, orchestrates agents and tools, and delivers real value to users?

From this perspective, Raise the Bar acts as:
- a **host application**
- an agent runtime
- a consumer (and sometimes provider) of MCP servers

---

## 3. Product vision (high level)

Raise the Bar is a **review management system** oriented toward improvement rather than scoring.

Core idea:
- AI provides **early, actionable feedback** to help authors/students revise before human review.
- After human reviewers submit their review, the AI:
  - shows its own review to the reviewer (post-submission) so the reviewer can revise,
  - gives **feedback on the review itself** (clarity, tone, specificity, actionability).
- The AI can help **drive structured conversations** between authors and reviewers to ensure discussion points are surfaced and resolved.

Non-goals (explicit):
- automated final decisions without human oversight
- ranking people

The AI’s role is to:
- assist, not decide
- suggest, not mandate
- improve clarity, fairness, and actionability

---

## 4. Core domain objects (initial draft)

*(To be refined)*

Suggested entities:
- **Submission** (paper, project, report)
- **Author** / **Student**
- **Reviewer** / **Peer**
- **Organizer** / **Instructor**
- **ReviewCycle**
- **Review**
- **FeedbackItem** (issue, suggestion, question)
- **DiscussionThread** (author–reviewer conversation)
- **Revision** (versioned updates of the submission)
- **AIReview** (AI-generated feedback artifact)

Each entity exists both:
- as a **business object** (platform perspective)
- as **context** consumed or produced by AI systems

---

## 5. Example AI-assisted capabilities

*(Illustrative, shared across conference / class / industry settings)*

### Author/student assistance (pre-human review)
- Generate initial feedback to help revise a submission
- Suggest concrete improvements (structure, clarity, argumentation)
- Ask reflective questions (“what evidence supports claim X?”)

### Reviewer assistance (post-submission)
- Show AI’s review **after** reviewer submits, so reviewer can revise
- Give feedback to reviewers on their review (tone, specificity, actionability)
- Highlight missing considerations, unclear reasoning, or overly vague feedback

### Facilitating resolution
- Drive a structured conversation between authors and reviewers
- Ensure key discussion points are addressed and resolved
- Summarize agreements, remaining concerns, and next actions

Important constraints (initial):
- AI does **not** make final accept/reject decisions.
- AI outputs are clearly labeled as AI-generated.
- Human users remain accountable for submitted reviews and final outcomes.

---

## 6. MCP mapping (to be filled)

This section will explicitly map Raise the Bar concepts to MCP primitives.

### From the service provider side:
- MCP servers exposing:
  - tools (e.g., create feedback draft)
  - resources (e.g., review documents)
  - prompts (e.g., coaching templates)

### From the AI system side:
- MCP clients consuming those servers
- agents orchestrating workflows
- optional MCP servers exposing new derived capabilities

---

## 7. Design challenges (intentionally unresolved)

These challenges are **part of the running example** and will be revisited as the course progresses. We will not fully resolve them upfront.

1) **Facilitation vs authority**
- If the AI “drives” a conversation and summarizes outcomes, it may accidentally become a de facto authority.
- Design question: how do we ensure the AI is a facilitator (proposes) rather than an adjudicator (declares)?

2) **Anchoring and conformity effects**
- Even if the AI review is revealed *after* a human review is submitted, it may still bias revisions toward the AI’s perspective.
- Design question: should AI feedback be framed as a checklist/questions rather than a reference evaluation?

3) **Reviewer coaching social risk**
- AI feedback to reviewers (tone, specificity, actionability) can improve quality, but can also cause defensiveness or “write-to-the-AI” gaming.
- Design question: what should be private vs shared, and how do we keep feedback concrete and actionable?

4) **State + permissions as first-class system design**
- The workflow naturally implies phases (draft, under review, discussion, final) and role-based visibility.
- Design question: what can each role see/do at each phase, and how do we enforce this at the system boundary (not just in prompts)?

---

## 8. Scale considerations

"Large scale" in Raise the Bar may include:
- many users
- many review cycles
- many AI-assisted interactions
- governance and auditability
- evaluation of AI impact over time

We will deliberately reason about scale **without** focusing on cloud infrastructure.

---

## 9. Open questions (to resolve together)

- Which roles do we model explicitly? (author, reviewer, organizer/instructor)
- What is the minimal canonical workflow and state machine?
- What actions are AI-assisted vs AI-prohibited (writes vs suggestions)?
- What failure modes matter most (privacy leaks, tone harm, unfairness, hallucinated critique)?
- What is the human override model for AI-driven conversations?
- How do we evaluate whether Raise the Bar actually improves outcomes?

These questions are part of the course.

---

## 9. Relationship to course lessons

Raise the Bar will be revisited across the course:
- early lessons: single-agent assistance
- mid lessons: tools, multiple agents, MCP
- later lessons: evaluation, bias, uncertainty, impact

This document will evolve alongside the lesson notes and MCP design notes.

