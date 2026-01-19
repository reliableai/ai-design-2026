# Components, Services, Tools and AI

*Abstractions and Middleware for Agentic AI*


## 1. From monolithic software to modules and classes
In the beginning, software was a monolith.
We had code written on punching cards.

Then, with storage and data transfer we could write programs that consist of many lines of code and run them repeatedly.

Computers got bigger, programs got bigger too also because we could now handle more complex functionality.
With that we had to organize the code - even if it was written by one programmer. Why?
Because we need to manage complexity, and as Julius Ceasar teaches us, we do so by divide and conquer.

As complexty grows, we need teams to write software. Therefore we naturally need to divide the work and we do so using modules and packages and objects and classes and other abstractions.

What these abstractions have in common ia a desire to encapsulate logic, minimize coupling across components so that it was possible to evolve each component while keeping the overall code working.

With multi-person teams classes and modules also allow to divide responsibility while keping a clear and clean "contract" across teams.

Internally, communication about features and interfaces was provided via documentation, oriented to developers.

**Versions** were managed somewhat ad hoc from a conceptual perspective and, in practice, by working on a shared repo via some variations of git.
The layer of "standardization" was mostly defined by the programming language: all components were in C++, or in Java, and the compiler knew how to put pieces together.




## 2. Services
With the internet it becomes possible to offer functionality over the net (internally, as an intranet - but also externally).
People started building more and more complex "stuff" - and by stuff here I mean also databases and all sorts of resources - and providing access to them on the fly, without the need of packaging and releasing software.

![Integration wild west - many protocols, no standards](figs/integration_wild_west.png)
*Fig: Before standardization: every integration required custom protocols and middleware.*

![Web services enabling B2B integration across organizational boundaries](figs/5.5.1_web_services.png)
*Fig: Web services standardize protocols, eliminating the need for many different middleware infrastructures. Internal functionality becomes available as a service.*

Initially the ability to access resources created massive confusion. Teams built point-to-point integrations, shared databases directly, and created tight coupling that made systems brittle and change expensive.

![B2B integration with message brokers and adapters](figs/5.5.2_manual.png)
*Fig: While B2B integration via message brokers is conceptually possible, it rarely happens in practice due to lack of trust, autonomy, and confidentiality.*

### The Bezos API Mandate (circa 2002)

This chaos led to dictats such as the famous Jeff Bezos memo at Amazon:

> 1. All teams will henceforth expose their data and functionality through service interfaces.
> 2. Teams must communicate with each other through these interfaces.
> 3. There will be no other form of interprocess communication allowed: no direct linking, no direct reads of another team's data store, no shared-memory model, no back-doors whatsoever. The only communication allowed is via service interface calls over the network.
> 4. It doesn't matter what technology they use. HTTP, Corba, Pubsub, custom protocols — doesn't matter.
> 5. All service interfaces, without exception, must be designed from the ground up to be externalizable. That is to say, the team must plan and design to be able to expose the interface to developers in the outside world. No exceptions.
> 6. Anyone who doesn't do this will be fired.

This memo crystallized the notion of **service** and the importance of providing access to data and functionality via a relatively stable interface that provides a "contract" between service providers and consumers.

The key insight was not technical — it was organizational: **treat every consumer as if they were external**, even internal teams. This forces clean boundaries and explicit contracts.

At this time we also have the birth and rise of SaaS applications and vendors — which appeared like magic to many customers. Simple things, such as the ability to rename a column on an ITSM application, felt incredible to customers used to packaged software upgrade cycles.

While components were managed by the same org, now services are priovided both internally and externally.
This proliferation of service gave rise to the notion of Service-Oriented Architectures. The core idea here was to deliver functions via some sort of "stable" interface (people used horrible terms such as "well-defined").
The opportunity was for service providers to offer access to their services over the web and for consumer to use such services.
Correspondingly, this opportunity gave rise to the question: how do we facilitate exposing services? how do we facilitate consuming services?

As we move across the net, and away from the notion of one compiler bundling code together, the question becomes
1. how do we describe services so that other people can use them,
2. how does the communication take place
3. how do we even become aware of the existance of services

![Service description and discovery stack](figs/5.5.8.png)
*Fig: The layers needed for service interoperability: common base language, interfaces, business protocols, properties and semantics — plus directories for discovery.*

the problems applies both to machines and humans. First, it was "solved" for humans.
Humans can access services via html sent over http. They become aware of the service via ads or web search. And they consume it based on their own intelligence, or lack thereof.
The HTML page desrcibes to a human how to use the service.
A new version simply meant a new web pages, which is served via reload of the page.
Because the consumer is a human, changes are ok as long as they are not too confusing for humans. A/B testing was also used to understand which human interface was more condusive of higher usage, hence the orange-colored buttons we now see.

The question is - what if we want to offer a service to be consumed by a program, or, what if we want to consume such a service.
With programmatic access we have both opportunities and problems. A problem is that our client sofwtware may not be able to understand the HTML and how to use the service. An opportunity is that in theory we could, as a client, scan for services automatically (eg airline reservation services), identify at run time the one that best fits our need, and call it. At scale.
To solve the problems and capture the opportunities companies came up with "standards", or, specifications that they hoped would become standards.
Prime examples of such specifications were SOAP, WSDL, and UDDI and it is very informative to think and study what they were trying to specify, why, and why they failed.


### SOAP, WSDL, and UDDI: The First Attempt at Machine-to-Machine Services

![The SOAP/WSDL/UDDI triangle](figs/uddi.webp)
*Fig: The classic web services triangle — Service Registry (UDDI) for discovery, WSDL for description, SOAP for communication.*

**[SOAP](https://www.w3.org/TR/soap12/)** (Simple Object Access Protocol) addressed the communication problem: how do two programs talk over the network in a language-agnostic way? SOAP defined a message format using XML. The idea was that regardless of whether your service was written in Java or C# or Perl, you could send and receive SOAP messages and understand each other. ([see example](https://www.w3schools.com/xml/xml_soap.asp))

**[WSDL](https://www.w3.org/TR/wsdl20/)** (Web Services Description Language) addressed the description problem: how does a client program know what operations a service offers, what parameters they take, and what they return? WSDL was an XML document that described the service interface - essentially, machine-readable API documentation. In theory, a client could read the WSDL and automatically generate the code needed to call the service. ([see example](https://www.w3.org/2001/03/14-annotated-WSDL-examples.html))

**[UDDI](https://www.oasis-open.org/committees/uddi-spec/doc/spec/v3/uddi-v3.0.2-20041019.htm)** (Universal Description, Discovery, and Integration) addressed the discovery problem: how do you find services in the first place? UDDI was meant to be a global registry - a kind of yellow pages for web services. Companies would publish their services to UDDI, and clients would query UDDI to find services that matched their needs. ([see example](https://www.tutorialspoint.com/uddi/uddi_usage_example.htm))

![External architecture of Web services](figs/5.13.external_arch.png)
*Fig: The external architecture of web services — providers publish descriptions to a registry, requesters find and then interact with providers.*

The vision was compelling: a world where software could automatically discover services, understand how to call them, and integrate on the fly. Dynamic, loosely coupled, language-agnostic integration.

For a comprehensive treatment of these technologies and the era they defined, see the timeless masterpiece that defines the standards even Dante aspires to: [Web Services: Concepts, Architectures and Applications](https://link.springer.com/book/10.1007/978-3-662-10876-5) (Alonso, Casati et al - Springer, 2004).


These specifications did not fail technically - they failed practically.

The main aspect to keep in mind is that average developers are average. One is almost tempted to say that average programmers are below average, and we wrestle with math and statistics on this one. But the fact is that if a "standard" (horrible name - there is no such thing - there are specifications and adoption of specifications) is intedned for humans, it has to be simple. Nobody can hope that millions of humans read complex specs and understand them - correctly, and in the same way.
Even if we "just" hope that developers will imnplement clients to simplify work for humans, simplicity matters and facilitates adoption.


**Complexity killed adoption.** SOAP messages were verbose. WSDL files were notoriously difficult to read and write. The tooling was fragile. What was supposed to simplify integration often made it harder. Developers found themselves debugging XML namespaces instead of building features.

**The discovery dream never materialized.** UDDI assumed that services would be published to public registries and discovered dynamically. In practice, companies did not want to advertise their internal services publicly, and the trust model for dynamic discovery was never solved. You do not just call an airline reservation service you discovered in a registry - you negotiate a contract, agree on SLAs, exchange credentials. The business reality did not match the technical abstraction.


Part of the problem was also XML: reading XML is a nightmare and maybe if JSON were a thing back then, they would have been more successful.

What happens in the end is that developers did not really adopt these specs. instead, they "used REST"
**REST won by being simpler.** While the enterprise world debated WS-* specifications (WS-Security, WS-ReliableMessaging, WS-AtomicTransaction...), developers started building APIs with plain HTTP and JSON. REST had no formal specification - just conventions. You could understand it by looking at examples. It was good enough, and good enough won.


In fact, REST is a non standard. or, a non spec. using REST means using nothing, pretty much. It's HTTP.
Somehow people felt cool becuause they then found some consistency on when to use GET vs POST vs DELETE and maybe PUT, but nobody cared too much about that, too.


The lesson here is important for AI integration: **standards succeed when they reduce friction, not when they maximize expressiveness.** A protocol that is easy to adopt beats a protocol that is theoretically complete. Or at least that was the case in the past.


So what we have instead of WSDL is web pages that describe APIs. Yes, there are attempts to "standardize" but they never went that far or be that useful. in the end you have developers (that is, humans) reading specs on web pages and implementing clients that call the service.

**Versioning** was handled a bit in ad hoc way, sometimes by adding version numbers to APIs. SaaS vendors grew increasingly allergic to maintaining many versions and developed a tendency to push clients on the latest versions rather than maintaining loads of versions active.



## 3. How Gen AI changes things

The above remained true also during the first wave of AI, where services exposed ML models such as classification or regression. Things start to change when we bring to the mix AI that is capable of understanding text — and more.

**What's different with intelligent clients?**

- AI can read imperfect, informal descriptions and figure out intent
- AI can handle variations in API formats without brittle parsing
- AI can reason about *when* to use a tool, not just *how*
- We can move from procedural (script every step) to declarative (describe goals, let AI figure out the steps)

This is a significant shift. The SOAP/WSDL/UDDI dream of automatic integration might actually be achievable — not because we finally wrote the perfect spec, but because the client got smarter.

But this also introduces new challenges:

- **Ambiguity**: when interfaces are "forgiving," there's room for misinterpretation
- **Autonomy**: who decides what the AI can do?
- **Non-determinism**: the same input might produce different outputs
- **New attack surfaces**: prompt injection, data exfiltration via tools

We still have the same *kind* of questions from the services era — how do we describe, discover, invoke, manage access — but now we have new potential usages, so it all becomes richer, more flexible, and also trickier.


## 4. What do we need to standardize?

Before looking at what exists, let's ask: **if we were designing the infrastructure for AI+tools from scratch, what abstractions would we need?**

This is the design space. Some of these problems are well-addressed today; others are wide open.


### 4.1 Describing tools

The AI needs to know what tools exist and how to use them. This requires:

**What the tool does** — a clear description of functionality, when to use it, when *not* to use it.

**Input schema** — what parameters does it take? What types? What constraints? What are valid values?

**Output schema** — what does it return? How should the AI interpret the result?

**Error conditions** — what can go wrong? How should the AI respond?

This is analogous to the WSDL problem, but with a twist: the consumer is an AI that can tolerate imperfect descriptions. We don't need perfect machine-readable specs — we need *good enough* descriptions that an LLM can understand.

**What exists:** JSON Schema for input/output. Docstrings and natural language descriptions. Tools like [FastMCP](https://github.com/jlowin/fastmcp) that auto-generate schemas from Python function signatures.

**What's missing:** Standards for "when to use" vs "when not to use." Semantic versioning for tool behavior. Ways to express preconditions and side effects.

**Example — minimal vs better descriptions:**

Minimal (works, but LLM may guess wrong):
```python
@mcp.tool()
def search_tickets(status: str, date: str) -> list[dict]:
    """Search support tickets."""
    ...
```

Better (explicit about formats, constraints, and intent):
```python
@mcp.tool()
def search_tickets(
    status: Literal["open", "closed", "pending"],
    created_after: str,
    assignee: str | None = None,
    limit: int = 50
) -> list[dict]:
    """Search support tickets in the helpdesk system.

    Use this tool when the user asks about support tickets, customer issues,
    or wants to find cases matching certain criteria. Do NOT use this for
    searching knowledge base articles (use search_kb instead).

    Args:
        status: Filter by ticket status. Use "open" for active issues,
                "closed" for resolved ones, "pending" for awaiting response.
        created_after: ISO 8601 date (e.g., "2024-01-15"). Only returns
                       tickets created on or after this date.
        assignee: Email of the assigned agent. If None, returns tickets
                  assigned to anyone. Use "unassigned" for tickets with
                  no assignee.
        limit: Maximum number of tickets to return (1-200). Default 50.

    Returns:
        List of ticket objects with id, subject, status, created_at, assignee.
        Empty list if no matches found (not an error).
    """
    ...
```

The key improvements:
- **Type hints with Literal**: The LLM sees exactly which values are valid
- **When to use (and when not to)**: Prevents the LLM from picking the wrong tool
- **Format examples**: "ISO 8601 date (e.g., '2024-01-15')" removes ambiguity
- **Edge cases explained**: What does `None` mean? What does an empty result mean?

This is documentation for a non-human reader. Write it like you're explaining to a capable but literal-minded colleague who has never seen your codebase.


### 4.2 Discovering tools

The AI needs to learn what tools are available. This requires:

**Listing available tools** — an endpoint or mechanism to enumerate tools.

**Dynamic updates** — if tools change, the AI should be notified.

**Filtering/search** — with many tools, the AI may need to search rather than list all.

This is analogous to the UDDI problem, but scoped differently. UDDI imagined global registries across organizations; for AI+tools, discovery is usually within a session or a configured set of servers.

**What exists:** Protocol-level discovery (e.g., `tools/list` in MCP). Configuration files listing available tools.

**What's missing:** Semantic search over tools ("find me a tool that can send emails"). Hierarchical organization. Federation across tool providers.


### 4.3 Invoking tools (communication protocol)

Once the AI decides to use a tool, how does the call happen?

**Wire format** — how is the request encoded? JSON? XML? Binary?

**Transport** — HTTP? WebSockets? stdin/stdout for local tools?

**Synchronous vs streaming** — does the tool return all at once or stream results?

**Error handling** — how are errors communicated? Retries?

This is analogous to SOAP, but much simpler. The modern answer is JSON over HTTP (or stdio for local tools), with JSON-RPC as a thin layer for request/response correlation.

**What exists:** [JSON-RPC 2.0](https://www.jsonrpc.org/specification) provides a minimal, transport-agnostic protocol:

```json
// Request
{"jsonrpc": "2.0", "method": "get_weather", "params": {"location": "NYC"}, "id": 1}

// Response
{"jsonrpc": "2.0", "result": {"temp": 72, "conditions": "sunny"}, "id": 1}
```

**What's missing:** Streaming is ad-hoc. Long-running operations need polling or callbacks. No standard for partial results.


### 4.4 Managing autonomy

This is **new** — we didn't have this problem with SOAP/WSDL because clients were deterministic. If you called a SOAP service, it did exactly what you programmed it to do.

AI clients are different: they interpret, reason, and sometimes surprise you. The question becomes: **how much can the AI do without asking?**

![Autonomy spectrum](figs/autonomy-spectrum.svg)
*Fig: The autonomy slider — from full human control (approve every action) to full AI autonomy (AI acts freely). Most real systems live somewhere in the middle.*

```
Full human control                                    Full AI autonomy
|-------------------------------------------------------|
  Human approves       AI suggests,        AI acts,        AI acts
  every action         human confirms      human can       freely
                                           intervene
```

Where you land depends on:
- **Stakes**: reading a file vs. sending an email vs. transferring money
- **Reversibility**: can you undo the action?
- **Trust**: how well-tested is the AI's judgment for this task?
- **Context**: is this a demo, a personal assistant, or a production system?

**The "Click" problem**

Remember the movie *[Click](https://en.wikipedia.org/wiki/Click_(2006_film))* (2006) with Adam Sandler.

![Click (2006) movie poster](figs/click_film_poster.jpg)
*Click (2006) — a cautionary tale about automation that learns your preferences.*

In the film, Sandler's character gets a universal remote control that can fast-forward through boring parts of his life. Convenient! But the remote starts *learning* his preferences and auto-piloting his life — skipping arguments with his wife, fast-forwarding through his kids growing up, missing moments he would have wanted to experience.

This is a cautionary tale for AI autonomy:
- **Learning preferences is not the same as understanding intent.** The remote learned "he skips arguments" but not "he values his family."
- **Defaults compound.** One shortcut becomes a pattern; a pattern becomes autopilot.
- **You can't unlive skipped moments.** Some actions are irreversible.

When we design AI systems that "learn from user preferences" to reduce confirmation prompts, we risk building a Click remote.

**What exists:** Guidelines like "human in the loop." Confirmation prompts. Allowlists/blocklists.

**What's missing:** Policy frameworks. Permission systems with fine-grained control. Audit infrastructure. Ways to express "the AI can do X but not Y" declaratively. Middleware that enforces autonomy policies.

**Patterns for managing autonomy:**

1. **Confirmation prompts** — ask before executing
2. **Allowlists/blocklists** — restrict which tools can be called
3. **Sandboxing** — run tools in isolated environments
4. **Audit logging** — record every invocation for review
5. **Rate limiting** — prevent runaway AI
6. **Capability escalation** — start limited, expand with trust
7. **Semantic guardrails** — use another AI to review proposed actions


### 4.5 Testing

Testing is another area where **we lack mature abstractions**.

Traditional software testing has well-established patterns: unit tests, integration tests, end-to-end tests. For AI systems with tool access? We're mostly flying blind.

**What makes testing AI+tools hard?**

1. **Non-determinism**: The same input may produce different outputs.
2. **Combinatorial explosion**: 20 tools × 5 parameters each = enormous test space.
3. **Context sensitivity**: Behavior depends on conversation history, phrasing.
4. **Emergent behavior**: The AI might use tools in unanticipated ways.
5. **No ground truth**: For many tasks, there's no single "correct" answer.

**What exists:** Manual probing. Adversarial testing. Eval frameworks like [promptfoo](https://github.com/promptfoo/promptfoo), [Braintrust](https://www.braintrust.dev/).

**What's missing:**
- **Behavioral specifications**: "the AI should never call `delete_file` without confirmation"
- **Coverage metrics**: Did we exercise all tools? All parameter combinations?
- **Regression detection**: Did this prompt change cause different behavior?
- **Simulation environments**: Mock tools that look real but aren't
- **Middleware for test harnesses**: Intercept calls, inject failures, record/replay


### 4.6 Tool proliferation

If you expose 500 tools to an LLM, it will struggle. Context windows are finite, and more tools mean more tokens spent on descriptions rather than reasoning.

**What exists:** Flat tool lists. Manual curation.

**What's missing:**
- **Hierarchical organization**: Group tools into categories
- **Dynamic loading**: Only expose tools relevant to the current task
- **Semantic search**: Let the AI search for tools by description
- **Agent delegation**: Instead of one agent with 500 tools, have specialized agents


### 4.7 Other gaps

| Area | What we have | What we need |
|------|--------------|--------------|
| **Observability** | Basic logging | Standardized traces, anomaly detection, cost attribution |
| **Security** | Transport-level auth | Fine-grained permissions, prompt injection defense |
| **Versioning** | Nothing standard | Tool version negotiation, deprecation policies |
| **Streaming** | Ad-hoc implementations | Standard protocol for partial results |


### 4.8 Summary: the design space

| Need | Analogous to | Status |
|------|--------------|--------|
| Describing tools | WSDL | Partially solved (JSON Schema + natural language) |
| Discovering tools | UDDI | Partially solved (protocol-level listing) |
| Invoking tools | SOAP | Mostly solved (JSON-RPC over HTTP/stdio) |
| Managing autonomy | *New* | Wide open |
| Testing | *New* | Wide open |
| Tool proliferation | *New* | Wide open |

The first three are the "classic" problems from the services era — and they're reasonably well-addressed today, though not perfectly.

The last three are **genuinely new** problems introduced by AI clients. This is where we need more experience, more abstractions, and eventually middleware.



## 5. What exists today: MCP as an example

The **Model Context Protocol (MCP)** is one attempt to standardize some of these needs. It's worth understanding what MCP covers and what it doesn't.

MCP is developed by Anthropic and is designed for AI hosts (like Claude) to interact with external tools and data sources.


### 5.1 What MCP standardizes

**Describing tools** — Tools are described with JSON Schema for inputs, plus natural language descriptions:

```json
{
  "name": "get_weather",
  "description": "Get current weather information for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "City name or zip code"}
    },
    "required": ["location"]
  }
}
```

**Discovering tools** — Clients can call `tools/list` to enumerate available tools:

```json
// Request
{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}

// Response
{"jsonrpc": "2.0", "id": 1, "result": {"tools": [...]}}
```

**Invoking tools** — Clients call `tools/call` with the tool name and arguments:

```json
// Request
{"jsonrpc": "2.0", "id": 2, "method": "tools/call",
 "params": {"name": "get_weather", "arguments": {"location": "NYC"}}}

// Response
{"jsonrpc": "2.0", "id": 2, "result": {"content": [{"type": "text", "text": "72°F, sunny"}]}}
```

**Lifecycle** — MCP defines initialization, capability negotiation, and notifications (e.g., `tools/list_changed`).

**Transport** — MCP works over stdio (for local tools) or HTTP with Server-Sent Events (for remote tools).

![MCP message flow: Discovery, Tool Selection, Invocation, Updates](figs/message-flow-diagram.svg)
*Fig: MCP message flow — the client discovers tools from the server, the LLM selects which tool to use, the client invokes it, and the server can notify of changes.*


### 5.2 What MCP doesn't standardize

MCP is a **wire protocol**. It tells you how to describe, discover, and invoke tools. It does *not* tell you:

- **Autonomy policies**: Who can call what? When should the user be asked?
- **Testing infrastructure**: How do you test AI+tool behavior?
- **Tool proliferation**: How do you organize 500 tools?
- **Observability**: How do you trace and debug tool invocations?
- **Fine-grained security**: Beyond transport-level auth

MCP gives you the primitives; you build the governance layer.


### 5.3 MCP vs REST APIs

You should still expose REST APIs. MCP doesn't replace them.

Think of it as layers:
1. **Core APIs** (REST/SDK) are the stable foundation for all clients
2. **MCP** is an additional surface optimized for AI hosts

An MCP server usually *wraps* existing REST APIs — it's a different contract, optimized for AI consumption.


### 5.4 When to use MCP

MCP helps most when:
- Many AI hosts need the same capabilities
- You want consistent tool schemas across ecosystems
- You want discoverability and standard invocation semantics

A plain API wrapper is often enough when:
- You control both the host and the service
- The integration is unique to one system
- You're still iterating on the product boundary

Rule of thumb:
> Build on APIs for stability; add MCP for AI interoperability.


### 5.5 Other resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp) — Python library for building MCP servers
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)



## 6. Conclusion: where we are

We've come full circle from the services era:

| Era | Problem | Solution attempted | Outcome |
|-----|---------|-------------------|---------|
| 2000s | Machine-to-machine services | SOAP/WSDL/UDDI | Failed (too complex) |
| 2010s | API integration | REST + documentation | Succeeded (good enough) |
| 2020s | AI+tools | MCP + ??? | In progress |

The "classic" problems (description, discovery, invocation) are reasonably solved. MCP and similar protocols address them adequately.

The **new** problems (autonomy, testing, tool proliferation) are wide open. This is where the next generation of infrastructure will emerge.

For now:
- Use MCP (or similar) for the wire protocol
- Build custom solutions for autonomy, testing, observability
- Design for replaceability — your solutions will be superseded

The lesson from history: **standards succeed when they reduce friction, not when they maximize expressiveness.** Whatever emerges for autonomy and testing will need to be simple enough for average developers to adopt.
