# Optimizing in the Dark:
Organizational Blindness in AI Evaluations

## Part 5: What To Do, and What Not To Do

*Practical solutions for visibility, action, and culture*

← [Part 4: Sources of Bias and Uncertainty](./part-4-sources-of-error.md) | [Series Index](./index.md)

---

Recall the three facets of the problem we identified:

1. **The visibility problem** (epistemic): People don't see the uncertainty. It's not reported, not computed, not surfaced.

2. **The culture problem** (organizational): Even when people could see uncertainty, the organization doesn't ask. There's no upside to surfacing it.

3. **The action problem** (methodological): Even when uncertainty is visible and the culture asks about it, people don't know what to do.

The solutions must address all three. But first, let's be clear about what doesn't work.

---

## What Doesn't Work

### Mandates

A common response to eval quality problems is to mandate process: "Every eval must have at least 100 ground truth examples." "Every team must use the standard rubric." "Every release must pass the evaluation checklist."

These mandates aren't wrong. The problem is what happens next.

Teams optimize for the mandate, not for the outcome. They produce 100 ground truth examples—but overfit to them. They use the standard rubric—but don't ask whether it captures what matters. They pass the checklist—and ship a system that fails in production.

The mandate becomes a shield: "We followed the process." Accountability shifts from *delivering reliable results* to *complying with requirements*. And compliance is much easier to game than reliability.

### Best Practices

Best practices have the same failure mode. A team follows the best practice guide, checks every box, and produces a number that looks rigorous. But they never asked: *is this number actually reliable?*

Best practices are useful as starting points. They become harmful when they replace judgment—when teams stop asking "is this right?" and start asking "did we follow the steps?"

### Why This Happens

Both mandates and best practices shift accountability in a subtle but important way:

| Approach | Accountability for | Leads to |
|----------|-------------------|----------|
| Mandates | Following the process | Gaming the process |
| Best practices | Checking the boxes | Box-checking without thinking |
| **Outcome ownership** | Reliability of the result | Actual rigor |

The fix isn't to abandon mandates or best practices. It's to make accountability explicit.

### Make RACI Clear

For every evaluation, someone must be **Accountable**—not for following the process, but for the *reliability of the number*. This person should be able to answer:

- Would you stake your reputation on this number?
- What range would you sign your name to?
- If this goes to production and fails, are you comfortable explaining why you believed it would work?

When accountability is clear, mandates become tools rather than shields. "We have 100 ground truth examples" becomes "We have 100 ground truth examples, and here's why I believe they're representative." The checklist becomes a starting point, not an endpoint.

**Mandate the questions, not the answers.** Require teams to answer "what's your confidence interval?" and "how do you know your data is representative?"—but let them own the answers.

---

## Addressing the Visibility Problem

The visibility problem has three parts: we are not **aware** of uncertainty, we don't **estimate** it, and we don't **report** it. Each must be addressed in turn.

### Awareness

Before we can estimate or report uncertainty, people must understand that it exists—and that it matters. This requires education on several fronts:

- The many sources of bias and variability
- The impact of each on the final uncertainty window
- The impact that this in turn has on our ability to iterate and take decisions

Several approaches can help:

**Ask teams to quantify it, even as ballpark.** This by itself will start creating awareness.

**Show, don't tell.** Let people see the variability in their own work. Take an existing eval. Run it with three reasonable variations of the eval prompt. Show the team the spread. If the scores are stable, that's reassuring. If they diverge by 15 points, that's a lesson no lecture can match. The same can be done with different samples from the same dataset, or with different judges. One demonstration on your own data is worth ten explanations of the theory.

**Use thinking tools.** Worksheets can act as "thinking" tools that confront questions they might otherwise skip: "How do you know your data is representative?" "What's your confidence interval?" "How many variants did you test on this dataset?" The act of answering—or discovering you cannot answer—creates awareness.

**Leverage AI assistants.** An AI "Center of Excellence" agent, grounded in evaluation best practices, can ask the probing questions that busy teams forget to ask themselves. "You're reporting 85% on 50 samples—are you comfortable that the true accuracy might be 75%?" This scales the function of a skeptical reviewer to every team.

**Make uncertainty visible by default.** When dashboards and reports show confidence intervals rather than point estimates, awareness becomes unavoidable. People cannot ignore what is in front of them. Changing the defaults changes the culture.

None of these require teams to become statisticians. They require only that teams see the variability that was always there but hidden—and that they see it often enough that it shapes how they think.

Awareness is a precondition for everything else. You cannot estimate what you don't know exists, and you will not report what you haven't estimated.

### Estimation

Once aware, the next step is to quantify—or at least bound—the uncertainty. For some sources, standard methods exist (confidence and credibility intervals, impact of noisy judges, bias created by multiple hypotheses testing...).

For other sources, precise quantification is harder. For example, **data representativeness**: How different is your test set from production? Often we cannot know precisely, but we can ask: Is this synthetic or real data? Does it cover the diversity of inputs we expect? Are there known gaps?

In these cases we often cannot produce a number. We can only probably go by experience and "ballpark it"—this is better than nothing and we will get better over time at estimating this.

### Reporting Uncertainty

Once uncertainty has been estimated—even approximately—it must be communicated.

The only exception is when the magnitude of uncertainty is irrelevant to the decision at hand. This is rare. For most ship/no-ship decisions, for most comparisons between system variants, uncertainty matters.

**A common objection is that "executives would not understand it."** This is not true. Executives routinely deal with uncertainty in financial forecasts, market projections, and risk assessments. They may ask hard questions—"Why is the range so wide?" or "What would it take to narrow it?"—but these are exactly the questions that should be asked. Discomfort with the questions is not a reason to hide the answers.

In fact, once one team begins reporting uncertainty, something important happens: decision-makers start asking why *other* teams aren't doing the same. Reporting uncertainty is contagious in a way that benefits everyone.

### What Should Reporting Look Like?

**Instead of this:**

| Metric | Score |
|--------|-------|
| Technical Accuracy | 89% ✓ |
| Completeness | 84% ✓ |
| Calling Correctness | 72% ⚠ |

**Consider this:**

| Metric | Estimated Range | Confidence Notes |
|--------|-----------------|------------------|
| Technical Accuracy | 80–94% | Based on 100 samples; prompt sensitivity adds ~5 pts |
| Completeness | 75–90% | Synthetic data may not reflect production diversity |
| Calling Correctness | 62–82% | Small sample (n=50); wide interval expected |

The second table says less with false precision and more with honest information. It invites the right conversations: "Can we get more data to narrow the Technical Accuracy range?" "What would it take to validate on real production samples?"

**Exposing uncertainty to decision-makers is one of the two easiest and fastest ways to improve the situation.** It requires no new tools, no new methods—only the willingness to show what we actually know.

---

## Addressing the Action Problem

### Reducing Uncertainty

Some uncertainty is actually avoidable. Before accepting bias and uncertainty, ask: can we reduce them? The answer is that in most cases—yes, we can.

**Eval at scale on customer data:** Uncertainty (and bias) in sample size and data representativeness can be reduced by running evaluations on customer data, and at scale. Sometimes this is not possible, but often this is not done as it may be time consuming, or due to the belief that we need human labelers to generate ground truth.

This is a false belief: I am yet to see a case where humans are consistently better than LLMs in assessing an <input, output> pair. When that happens, it is likely that eval guidelines are not well specified, or that the eval is subjective.

I am also yet to see a case where synthetic data is as nuanced as actual, production data. It may be—but that is a feat hard to achieve (not to mention that each use case, each domain, each customer is different).

Notice that if we eval at scale, we also greatly reduce the multiple hypotheses testing problem. If we have data at scale, we can have many holdout datasets, but in general a large and diverse test set by itself reduces the problem.

**Doing this takes effort—and if the impact of uncertainty and bias is recognized, then leadership can ask to put more resources on this.**

As another example, we can spend more cycles on **calibrating an LLM judge** so that the noise due to errors in the eval judge is reduced. This, again implies effort and dedicated, qualified resources.

None of these eliminate uncertainty. But they can reduce it meaningfully—and just as importantly, they help you understand *how much* uncertainty remains. The really important shift is to begin asking the question: **how can we reduce it?** And—the awareness for how important it is to do so.

### Develop Observability Concepts, Abstractions and Tools

We can borrow lessons from software engineering and apply them to AI systems to understand where low quality, unexpected behaviors occur.

This can be done by thinking from first principles and identifying concepts and abstractions that facilitate this. Here are some examples, based on needs emerged from actual production cases:

**Agentic Assertions on inputs and outputs:**
- Define expectations for what an agent or tool should receive and produce
- These can be structural (format, schema) or semantic (intent, purpose)
- When assertions fail, you learn something—either about your system or about your expectations

**Introduce the concept of desirable (vs undesirable) agentic execution paths:**
- For agent-based systems, some execution paths are expected, others are concerning
- Define these explicitly. Monitor which paths are taken in production
- Analyze at scale: in which cases do desirable paths get followed? What predicts failure?

**Exception handling:**
- What should happen when an agent encounters something unexpected?
- Define fallback behaviors. Make failures visible rather than silent.

This layer doesn't directly improve your eval scores. But it gives you ongoing visibility into whether your system is behaving as expected—and helps you catch problems that offline evaluation might miss. Based on this, we iterate and improve the system to reduce sources of undesired variability.

**Logging with appropriate granularity:**

Everything above depends on logging. For AI agents, capture inputs, decisions, tool interactions, outputs, and metadata. Consider log levels that reflect agent concerns:

- **TRACE**: Full chain-of-thought (debugging only)
- **EXECUTION**: Key decision points and tool calls (standard production)
- **OUTCOME**: Final result and assertion violations
- **EXCEPTION**: Errors, fallbacks, undesirable paths
- **AUDIT**: Security-relevant events

And respect access controls—AI agent logs are sensitive, containing user queries and business data.

### Use Worksheets as Thinking Tools

![](./images/image17.png)

Worksheets are great tools to help thinking. They do not shift accountability or responsibility, but they help teams think about how the evaluation has been done. I believe a good worksheet has three "columns": a question, an answer, and a request for evidence about the answer: **how do we know?**

It is ok to answer questions with an "I don't know" or "it's just my best guess"—but at least we know what we don't know.

This isn't about catching people out. It's about making the gaps visible—to yourself and to others.

*The worksheet can be easily filled automatically by an agent, given a report or a presentation.* Then PMs can be aware of which parts are missing and complete them.

![](./images/image18.png)

### AI "Center of Excellence" Agents

A Center of Excellence is valuable: experts who can review evaluation methodology, ask hard questions, and catch blind spots. But a small team of experts cannot review hundreds of evaluations across a large organization. The expertise becomes a bottleneck.

One approach: encode the function of the Center of Excellence into an AI assistant. An agent that:

- Knows the principles of rigorous evaluation
- Is aware of your organization's standards and practices
- Guides teams through the worksheet, asking probing questions
- Flags gaps and suggests improvements
- Helps fill in evidence or highlights where evidence is missing

This is not a replacement for human judgment. But it can scale the *questioning*—the part where someone asks "how do you know?" and "have you considered...?"

Think of it as a **Center of Excellence at your fingertips**. Not a rubber stamp, but a thinking partner that helps teams be more rigorous than they would be on their own.

---

## Addressing the Culture Problem

Everything above—the techniques, the tools, the processes—requires a cultural foundation.

Teams need to feel safe saying "we don't know." Executives need to accept that "82% ± 8 points" is more valuable than "82%"—even though it feels less confident.

This is perhaps the hardest part. Organizations prefer harmony. Point estimates feel decisive. Uncertainty feels like weakness.

**But uncertainty isn't weakness. Pretending certainty where none exists—*that's* weakness.** It leads to false belief, bad decisions, and eroded trust when reality catches up.

The goal isn't to eliminate uncertainty. It's to see it clearly, communicate it honestly, and make good decisions despite it.

### Three Things That Can Shift Culture Quickly

**1. Naming things right**

This is an *instant* way to address the issue. Naming always gets you a third of the way there. If we stop calling this "eval" and start calling it **"estimation of random variables"**, by itself this will create teams and execs to put the attention in the right place.

**2. Asking the questions**

Having executives asking the questions gets us another third of the way there. It instantly creates the right culture. **Instantly.**

**3. Make accountability explicit**

Every evaluation should have clear ownership—not for producing a good-looking number, but for the *reliability* of the number. Someone should be accountable for:

- Why these metrics matter
- Whether the methodology is sound
- What the uncertainty range is and why
- Whether the result is ready to inform decisions

---

## The Questions to Ask

The next time you see a scorecard with a green 89%, ask:

> *What range would you sign your name to?*

> *What would you tell a customer if they asked—and you had to stand behind the answer?*

> *What range would you be comfortable owning when this goes to production?*

**If the team can't answer, the number isn't ready. And neither is the decision.**

---

*Back to: [Series Index](./index.md)*

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering`
