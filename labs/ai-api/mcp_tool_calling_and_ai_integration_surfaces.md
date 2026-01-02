# MCP, Tool Calling, and AI Integration Surfaces

*(Canonical reference document — replaces previous MCP notes)*

---

## 1. Why this document exists

As AI systems grow beyond a single script or demo, engineers face three **structurally different problems**:

1. **How do we build our own AI system internally?**
2. **How do we integrate external services and capabilities?**
3. **How do we expose our own capabilities so others (humans and AI systems) can build on them?**

Tool calling and the **Model Context Protocol (MCP)** address these problems at different layers.

This document provides a **clean mental model** for reasoning about when to use:
- local tool calling
- bespoke APIs
- MCP servers

---

## 2. What does it take to expose tools to an agent?

Before discussing MCP, it is useful to ask a more basic question:

> **What do we need in order to expose a capability so that an agent can actually use it?**

In practice, exposing a tool to an agent requires *much more* than just writing a function.

At minimum, we need:

1. **A clear capability description**
   - What does the tool do?
   - What problem does it solve?
   - When should it be used vs not used?

2. **A machine-readable interface**
   - Input schema
   - Output schema
   - Error conditions

3. **Invocation semantics**
   - How the tool is called
   - Whether it is synchronous or streaming
   - What happens on partial failure

4. **Context and preconditions**
   - What information the tool assumes
   - What state must already exist
   - What permissions are required

5. **Postconditions and side effects**
   - What changes in the system after invocation
   - What is guaranteed vs best-effort

6. **Discoverability**
   - How the agent learns that the tool exists
   - How it learns *when* the tool is appropriate

Historically, most of this information lived:
- in human-written documentation
- in ad-hoc prompt instructions
- or implicitly in the head of the developer

This does not scale well to many tools, many agents, or many hosts.

---

## 3. Why standardization helps

Standardization is not primarily about convenience — it is about **alignment**.

A standardized way of exposing tools helps because:

1. **Agents do not need to relearn semantics every time**
   - Consistent schemas
   - Consistent lifecycle
   - Consistent failure handling

2. **Hosts and tools can evolve independently**
   - Clear contracts reduce coupling
   - Fewer brittle, bespoke integrations

3. **Ecosystems become possible**
   - One tool can be reused by many hosts
   - One host can consume many tools

4. **Models understand the interface better**
   - Modern LLMs are trained on large amounts of data that include MCP-style tool descriptions and interactions
   - As a result, they often reason *better* when tools follow a known standard

This last point is subtle but important:

> **Standardization helps not only humans and systems, but also the models themselves.**

When a tool follows a familiar structure, the model is less likely to misuse it, hallucinate parameters, or ignore constraints.

---

## 4. Core definitions (non-negotiable)

### Agent
An **agent** is a system that:
- owns a control loop
- decides what to do next
- maintains state
- may call tools or other agents

> Agents decide.

---

### Tool
A **tool** is a capability that:
- executes a specific action
- is invoked by an agent
- has a narrow, testable contract
- has no autonomy

> Tools execute.

---

### MCP Server
An **MCP server**:
- exposes tools, resources, and prompts
- follows a standard lifecycle and discovery mechanism
- does *not* need to be an agent
- typically wraps existing systems or APIs

> MCP standardizes how tools and context are exposed to AI hosts.

---

### Tool
A **tool** is a capability that:
- executes a specific action
- is invoked by an agent
- has a narrow, testable contract
- has no autonomy

> Tools execute.

---

### MCP Server
An **MCP server**:
- exposes tools, resources, and prompts
- follows a standard lifecycle and discovery mechanism
- does *not* need to be an agent
- typically wraps existing systems or APIs

> MCP standardizes how tools and context are exposed to AI hosts.

---

## 3. The three perspectives: build, integrate, expose

A useful way to reason about AI system design is to separate **three perspectives**.

These are directional:
- **inward** (build)
- **outward** (integrate)
- **outward-facing** (expose)

---

## 3.1 Build: what we need to build our own system

This is the **internal architecture** view.

Typical elements:
- agents and control loops
- memory and summarization
- orchestration logic
- evaluation harnesses
- observability and logging

Here, tools are usually:
- local functions
- internal services
- internal HTTP endpoints

**Tool calling is sufficient** in this layer because:
- you control both sides
- iteration speed matters more than standardization

Tool calling here is an **implementation mechanism**, not an ecosystem contract.

---

## 3.2 Integrate: what we need from external services

This is the **consumer** view: your AI system depends on other providers.

Examples:
- GitHub (repositories, issues, pull requests)
- Render (deployments, logs)
- ServiceNow-like systems (tickets, workflows)
- external LLM providers
- third-party agents and services

There are two main integration strategies:

### Option A — Consume a normal API
- REST / SDK
- bespoke tool schemas
- manual discovery via documentation

### Option B — Consume an MCP server
- standardized discovery
- standardized invocation semantics
- reduced M×N integration cost

**Rule of thumb**:
- One host + one service → bespoke API wrappers are fine
- Many hosts + many services → MCP becomes attractive

---

## 3.3 Expose: what we offer others

This is the **platform/provider** view.

As a provider, you may expose:

### APIs (REST / SDK)
- for general-purpose, deterministic clients
- discovery is out-of-band
- semantics vary by service

### MCP servers
- for AI hosts and agent runtimes
- discovery is in-protocol
- semantics align with AI-specific primitives (tools, resources, prompts)

Important clarification:
> An MCP server usually wraps existing business APIs — it is a *different contract*, optimized for AI consumption.

---

## 4. Quick comparison table

| Perspective | Audience | What you expose | Typical choice | Why |
|---|---|---|---|---|
| Build | your own agent runtime | internal tools | tool calling | fastest iteration, full control |
| Integrate | your AI system | adapters / clients | REST/SDK or MCP client | MCP reduces bespoke glue |
| Expose | external devs & AI hosts | public contract | REST/SDK + MCP | REST for humans, MCP for AI |

Key sentence:
> Tool calling is the runtime act of invoking capabilities. MCP is how capabilities are packaged, discovered, and reused across hosts.

---

## 5. Why MCP exists (the M×N problem)

Without MCP:
- every host integrates every tool differently
- schemas, auth, streaming, retries are reinvented
- reuse across AI systems is limited

MCP addresses this by standardizing:
- roles (host, client, server)
- lifecycle (initialize → discover → invoke)
- primitives (tools, resources, prompts)

This is analogous to how LSP standardized language tooling.

---

## 6. MCP vs APIs and MCP vs REST

In the past, we exposed system capabilities primarily via **APIs**, and most commonly **REST APIs**.

We should still do that.

The right mental model is:
- **APIs/REST** are a general-purpose integration surface for deterministic clients (UIs, services, scripts).
- **MCP** is an AI-oriented integration surface for *AI hosts/agent runtimes* that need discovery, standardized invocation, and AI-native primitives.

They overlap, but they solve different parts of the problem.

---

### 6.1 MCP vs API (general)

**An API** (REST/SDK/RPC) gives you:
- a stable contract for software engineers
- clear versioning and compatibility strategies
- standard security patterns (OAuth, API keys, mTLS)
- mature tooling (gateways, rate limiting, WAF, monitoring)
- compatibility with every programming language and environment

**MCP** gives you:
- in-protocol **discovery** of tools/resources/prompts
- a standard lifecycle (initialize → discover → invoke)
- AI-native primitives:
  - **Tools** (callable functions)
  - **Resources** (context/data)
  - **Prompts** (reusable templates)
- interoperability across multiple AI hosts (reducing M×N bespoke integration)

Practical interpretation:
> MCP is often a *productized AI-facing facade* over underlying APIs.

---

### 6.2 MCP vs REST (more specific)

**REST** is one style of API design:
- resource-oriented endpoints
- stateless requests
- human-oriented documentation/discovery

**MCP** (even when transported over HTTP) is **not REST**:
- it assumes a stateful relationship (sessions/lifecycle)
- it supports discovery as part of the protocol
- it standardizes how an AI host learns what it can do and how to do it

So the relationship is not “REST vs MCP,” but typically:

- **Business REST APIs** (core service interface)
- **MCP server** wrapping those APIs (AI integration surface)

---

### 6.3 Should we still expose REST APIs?

Yes, in most real systems you should.

Reasons:
- Non-AI clients still exist (web/mobile apps, backend services, integrations).
- APIs are the stable foundation for governance, scalability, and operational maturity.
- Many organizations already have API management, security review processes, and SLOs built around REST/SDKs.

Think of it as layers:
1) **Core APIs** (REST/SDK/RPC) are the "source of truth" integration surface.
2) **MCP** is an additional surface optimized for AI hosts.

---

### 6.4 When MCP replaces a bespoke API wrapper (and when it doesn’t)

MCP helps most when:
- many AI hosts need the same capabilities
- you want consistent tool schemas across ecosystems
- you want discoverability and standard invocation semantics

A plain API wrapper is often enough when:
- you control the host and the service
- the integration is unique to one system
- you are still iterating on the product boundary

Rule of thumb:
> Build on APIs for stability; add MCP for AI interoperability.

---

## 7. MCP in the course narrative (Raise the Bar)

In *Raise the Bar*:

- **Early lessons** use tool calling to move fast
- **Mid-course** introduces multiple agents and integration pain
- **MCP appears naturally** when we want:
  - multiple AI hosts
  - clean role/permission boundaries
  - reusable integration surfaces

At that point, MCP is not trendy — it is a relief.

---

## 8. Common failure modes (to watch for)

- Using MCP everywhere too early
- Confusing tools with agents
- Treating MCP servers as autonomous agents
- Encoding policy only in prompts instead of at boundaries

---

## 9. Open design questions

- Should MCP servers ever be autonomous?
- How much intelligence belongs in the host vs the server?
- What guarantees should MCP tools provide?
- How does MCP affect evaluation and auditability?

These questions are intentionally left open.

