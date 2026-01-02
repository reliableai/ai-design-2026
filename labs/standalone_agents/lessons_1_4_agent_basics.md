# Lesson 1 — Software 1.0 → 2.0 → 3.0, and a First Line of Code

## 1. Goal of the lesson
Establish a shared mental model of **Software 3.0** and demystify LLMs as callable software components.

---

## 2. System we are building today

A minimal Python program that:
- calls an LLM via a hosted API (OpenRouter)
- sends a prompt
- receives a response

This is intentionally treated as a **function call**, not a chatbot.

---

## 3. New concepts introduced

- Software 1.0 vs 2.0 vs 3.0
- LLMs as external intelligence services
- Non-determinism in software behavior
- Latency and cost as first-class concerns

---

## 4. Live build / walkthrough

1. Minimal Python script calling an LLM
2. Change temperature → observe variability
3. Inspect latency and token usage
4. Re-run the same input → compare outputs

---

## 5. What breaks / tradeoffs observed

- Outputs are non-deterministic
- Traditional testing assumptions fail
- Latency is orders of magnitude higher than local code

---

## 6. Design discussion

Questions to discuss with students:
- In what sense is this still "software"?
- What assumptions from Software 1.0 break here?
- What would it mean to test this code?

---

## 7. Takeaway

> Software 3.0 looks like normal software — until you rely on it.

---


# Lesson 2 — From Function to Stateful Agent

## 1. Goal of the lesson
Move from a single LLM call to a **stateful agent**, and experience why state management becomes unavoidable.

---

## 2. System we are building today

A simple conversational agent that:
- reads user input
- calls an LLM
- returns a response
- maintains state across turns

The same system is evolved multiple times during the lesson.

---

## 3. New concepts introduced

- Agent as a control loop
- System boundary (backend vs UI)
- Context management strategies
- Memory as an explicit design choice

---

## 4. Live build / walkthrough

1. Basic agent loop (no memory)
2. Add a minimal web interface
3. Send full conversation history each turn
4. Measure prompt growth, cost, and latency
5. Truncate context to last N turns
6. Add a summary / memory of earlier turns

---

## 5. What breaks / tradeoffs observed

- Full history does not scale
- Truncated history loses important information
- Memory summaries are lossy and subjective

---

## 6. Design discussion

Questions to discuss with students:
- What information should be remembered?
- Who decides what is important?
- How does memory quality affect behavior?

---

## 7. Takeaway

> Memory is not a feature — it is a design decision.

---


# Lesson 3 — Tool Calling with a Single Agent

## 1. Goal of the lesson
Understand how **tools extend agent capabilities**, and why prompts alone are insufficient for building reliable AI systems.

---

## 2. System we are building today

A single AI agent:
- exposed via a local **FastAPI** service
- receiving user input via HTTP
- deciding whether to respond directly or call a tool

The agent remains:
- stateful
- long-lived across turns
- responsible for deciding *what to do next*

---

## 3. New concepts introduced

- Tool calling as capability extension
- Tool schemas as contracts
- Capability boundaries of LLMs
- Agent vs tool distinction

**Key framing:**
> Agents decide. Tools execute.

---

## 4. Live build / walkthrough

1. Define a minimal agent loop
   - input → decide → act → respond

2. Define tools
   - Calculator tool (pure function)
   - Memory store tool (simple persistence)
   - External API tool (dummy or real)

3. Expose the agent via FastAPI
   - `/chat` endpoint
   - tools invoked internally by the agent

4. Demonstrate tool usage
   - queries that fail without tools
   - same queries succeeding with tools

---

## 5. What breaks / tradeoffs observed

- Tool failures propagate to agent behavior
- Tool schemas constrain agent reasoning
- Latency increases with external calls
- Debugging becomes harder than pure prompting

---

## 6. Design discussion

Questions to discuss with students:
- Why is this a *tool* and not another agent?
- What guarantees should a tool provide?
- Should tools be deterministic?
- How do we test tools independently?

---

## 7. Takeaway

> Tools are how intelligence escapes the prompt.

---


# Lesson 4 — Multiple Agents as Independent Services

## 1. Goal of the lesson
Understand **when and why to modularize intelligence** into multiple agents — and when not to.

---

## 2. System we are building today

Two independent agents:
- each running as its own **FastAPI** service
- each with a clear responsibility
- communicating via HTTP

Example:
- Agent A: planner
- Agent B: executor

---

## 3. New concepts introduced

- Agents as services
- Explicit responsibility boundaries
- Coordination cost
- Failure propagation across agents

---

## 4. Live build / walkthrough

1. Stand up Agent A service
   - receives user intent
   - decides next action

2. Stand up Agent B service
   - executes a concrete task
   - returns result

3. Agent A calls Agent B
   - via HTTP
   - handles success and failure

4. Observe system behavior
   - latency
   - cascading failures
   - retries

---

## 5. What breaks / tradeoffs observed

- Increased latency
- Harder debugging
- Implicit coupling via prompts
- Partial failures are common

---

## 6. Design discussion: modularization — why or why not?

### Good reasons to split into multiple agents
- Different responsibilities
- Different memory requirements
- Different failure tolerance
- Organizational ownership
- Independent iteration

### Bad reasons to split
- "Because we can"
- Unclear boundaries
- Excessive coordination
- Hidden coupling
- Overhead without benefit

**Key question:**
> Could this have been one agent with tools?

---

## 7. Agent vs Tool (explicit clarification)

**Agent**
- Decides what to do next
- Maintains state
- Owns a control loop
- Can call tools or other agents

**Tool**
- Executes a specific capability
- Invoked by an agent
- Narrow contract
- No autonomy

---

## 8. Takeaway

> Modularity improves reasoning, but increases coordination cost.

