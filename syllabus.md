# Designing Large Scale AI Systems
**Course Syllabus (v1 – living document)**

## Course Overview

This course focuses on the **design, implementation, and evaluation of large-scale AI systems**.  
Rather than training models, students will learn how to **build AI-powered software systems** using modern LLMs as components: agents, tools, memory, orchestration, and evaluation pipelines.

The emphasis is on **systems thinking**:
- how AI components interact,
- how design decisions affect reliability and scalability,
- and how to evaluate AI systems rigorously under uncertainty.

---

## Target Audience & Prerequisites

**Audience**
- Master’s level or advanced undergraduate students
- Professionals with software engineering background

**Prerequisites**
- Solid Python proficiency
- Familiarity with APIs and basic software architecture
- No prior ML training required

---

## Learning Objectives

By the end of the course, students will be able to:

1. Design AI-powered systems using agents, tools, and memory
2. Build working LLM-based applications using modern APIs
3. Reason about orchestration, control flow, and failure modes
4. Design meaningful evaluation strategies for AI systems
5. Understand bias, noise, uncertainty, and measurement error
6. Critically assess AI system performance claims
7. Iterate on system design using empirical evidence

---

## Course Structure

- **Duration:** 12 weeks  
- **Sessions:** 24 lectures × 2 hours  
- **Format:**  
  - Weeks 1–6: lectures + applied exercises  
  - Weeks 7–12: project-driven reviews and presentations

---

## Weekly Outline

### **Weeks 1–2: Foundations — From Software 3.0 to Stateful Agents**

**Goal:** Students move from conceptual understanding to a working, stateful AI system.

#### **Lesson 1: Software 1.0 → 2.0 → 3.0, and a First Line of Code**

**Topics**
- Software 1.0, 2.0, and 3.0
- LLMs as software components (not models to train)
- Limits of determinism, testing, and traditional abstractions
- Hello-world example: Python calling an LLM via OpenRouter
- Observing latency, tokens, and non-determinism

**Outcomes**
- Conceptual grounding in Software 3.0
- Ability to call an LLM from Python using a modern API

---

#### **Lesson 2: From Function to Stateful Agent**

**Topics**
- Simple agent control loop
- Minimal web interface calling the agent
- Naive context management (full conversation history)
- Cost, latency, and prompt growth
- Truncated context windows
- Maintaining memory via summaries
- Failure cases and tradeoffs

**Outcomes**
- A working AI agent with memory
- First-hand experience of scaling and state-management issues

---

### **Weeks 4–6: Evaluation & Measurement**

**Goal:** Students understand why evaluating AI systems is fundamentally hard.

**Topics**
- What does it mean for an AI system to “work”?
- Metrics vs proxy metrics
- Task success vs user value
- Bias and systematic error
- Noise and variability
- Uncertainty in small datasets
- Golden datasets and test set construction
- LLM judges and prompt sensitivity
- Multiple hypothesis testing and hidden bias
- Cost of wrong measurements

**Outcomes**
- Ability to critique evaluation setups
- Design of a basic evaluation plan for an AI system

---

### **Week 7: Midterm Evaluation**

- **Format:** Written exam
- **Focus:**
  - System design reasoning
  - Evaluation critique
  - Conceptual understanding (not math-heavy)

---

### **Weeks 7–12: Project Phase (Studio Format)**

**Goal:** Design, iterate, and defend a complete AI system.

**Format**
- No traditional lectures
- Project reviews
- Design critiques
- Evaluation reviews
- Iterative refinement
- Final presentations

**Activities**
- Architecture walkthroughs
- Failure analysis
- Evaluation plan stress-testing
- Design tradeoff discussions

---

## Assessment & Grading

| Component | Weight |
|---------|--------|
| Midterm written exam | 30% |
| Final project | 70% |

**Final project evaluation will consider:**
- System design quality
- Correct use of agents, tools, and memory
- Evaluation rigor and honesty
- Ability to reason about limitations and uncertainty
- Clarity of communication

---

## Teaching Philosophy

- Build first, theorize after
- Systems > prompts
- Evaluation before optimization
- Evidence over intuition
- Uncertainty is unavoidable — ignoring it is a choice

---

## Notes

- This syllabus is a **living document**.
- Project details, constraints, and deliverables will be defined iteratively.
- The course emphasizes **thinking clearly about AI systems**, not maximizing benchmark scores.

