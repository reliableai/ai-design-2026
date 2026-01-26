# Better "Evals" Beats Better Dev

Part 3 of *Optimizing in the Dark:
Organizational Blindness in AI Evaluations*

*The value of knowing what you're measuring*

← [Part 2: The Cost of Ignorance](./part-2-cost-of-ignorance.md) | [Series Index](./index.md)

---

## Two Ways to Improve Quality

You're pouring engineering effort into making your agents better. More prompt tuning. More fine-tuning. More RAG improvements. More guardrails.

**Stop.**

Ask yourself first—*when you change from Prompt 1 to Prompt 2, do you actually know which one is better?*

Not "which one scored higher on your eval." Do you know which one is *actually* better? With enough confidence to ship it?

Because here's the minimum bar: you must be able to reliably detect *directional* improvement. If you can't confidently say "Prompt 2 is better than Prompt 1," then every iteration is a coin flip. You're not engineering. You're gambling.

Ideally, you'd know the *absolute* value—how much is this system worth to customers? But at bare minimum, you need *relative* comparison. Without that, you cannot iterate. You're optimizing in the dark.

There are two ways to improve quality:

1. **Better agents** — improve the system itself
2. **Better eval** — improve your knowledge of the system

Most companies focus exclusively on (1). This is the rookie mistake. Path 1 is almost trivial with AI—*if* you have Path 2. But without reliable measurement, you don't even know if Path 1 is working.

Let's understand what we're actually trying to measure.

---

## The M×C Matrix: What You're Actually Optimizing

When you deploy AI agents across an enterprise, you're not optimizing a single number. You're optimizing a *matrix*.

Consider: you have **M agents** (Incident Auto-Resolution, Incident Summarization, Knowledge Base Deduplication, Document Classification, ...) deployed across **C customers** (Customer A, Customer B, Customer C, ...). Each cell in this matrix has a *value distribution*: V<sub>m,c</sub>.

<figure class="mxc-matrix">
<!-- MxC Matrix visualization will go here -->
</figure>

**What's in each cell?** A distribution of value. Not a single number—a random variable. For Incident Auto-Resolution at Customer A, sometimes it saves 15 minutes, sometimes 5, sometimes it makes things worse and costs 10 minutes. The distribution captures this reality.

**The aggregates matter too:**
- **Row totals**: E[V<sub>m,*</sub>] = expected value of agent m across all customers
- **Column totals**: E[V<sub>*,c</sub>] = expected value for customer c across all agents

Each cell is *unknown*. We have *beliefs* about it, with varying degrees of uncertainty. And this is where things get interesting.

---

## Uncertainty vs. Variability: The Critical Distinction

When you see distributions or "bars" around a value, you need to be sure you understand what they represent. And you want to make sure the presenter knows what they represent.

If somebody says "We expect our incident resolution agent to have a value/cost savings of $12 per run, plus or minus $4," **you MUST ask what they mean**.

| What they might mean | Interpretation | Can we reduce it? |
|---------------------|----------------|-------------------|
| **Uncertainty** | "We believe the average is somewhere between $8 and $16, but we're not sure which" | **YES** — better measurement narrows the range |
| **Variability** | "We're confident the average is $12, but Customer A sees $8, Customer B sees $16" | **NO** — this is real-world difference, not measurement error |

This distinction is fundamental:

**Uncertainty** is about our *knowledge*. It reflects the fact that we haven't measured enough, or our measurements are noisy, or our judges are inconsistent. Uncertainty can be reduced by:
- Larger test sets
- Better sampling
- More consistent evaluation criteria
- Multiple judges with adjudication

**Variability** is about *reality*. It reflects the fact that different customers have different data quality, different languages, different processes. Variability across customers (the fact that E[V<sub>m,c1</sub>] ≠ E[V<sub>m,c2</sub>]) cannot be reduced via better measurement. It can only be addressed via:
- More adaptive agent implementations
- Selective deployment (only deploy where E[V] > 0)
- Better matching of agents to customer characteristics

**The questions you must ask:**
1. "Is that uncertainty or variability?"
2. "Does the presenter even know what they mean?"

When someone presents a range and can't answer these questions, the number is not just uncertain—it's *uninterpretable*.

---

## Better Eval Leads to Better Quality (Even Without Touching the System)

**Better eval improves realized customer value even if you never touch the agent itself.**

How? Through better *deployment decisions*.

Think about your current portfolio. You have agents in production. You have agents you held back. *How confident are you that you got those decisions right?*

If your eval has high uncertainty, some of your deployed agents are probably hurting customers. And some of your held agents are probably valuable. You just can't tell which.

Even without improving the agent, better eval lets you:
1. **Deploy where E[V] > 0 with confidence** — more good deploys
2. **Avoid deploying where E[V] < 0** — fewer harmful deploys
3. **Hold where uncertain until you know more** — avoid premature decisions

### A Worked Example

Suppose you have 10 agents and current eval quality. With your current measurements, you decide to deploy 8 of them.

**Reality (which you discover later):**
- 6 of the 8 deployed agents are genuinely valuable (✓)
- 2 of the 8 deployed agents are actually harmful (✗)
- 1 of the 2 held agents was actually valuable (missed opportunity)
- 1 of the 2 held agents was correctly held (✓)

Now suppose you invest in better eval. With improved measurement:
- You correctly identify and avoid the 2 harmful deploys
- You hold 1 uncertain agent for more data (turns out to be good, but you defer the decision)
- You deploy 1 agent that was being held back (turns out to be valuable)

**Let's quantify:**

| Outcome | Before (Poor Eval) | After (Better Eval) |
|---------|-------------------|---------------------|
| Good deploys | 6 × $10 = $60 | 7 × $10 = $70 |
| Harmful deploys | 2 × -$50 = -$100 | 0 × -$50 = $0 |
| Held (good) | 1 × $0 = $0 | 1 × $0 = $0 |
| Held (bad) | 1 × $0 = $0 | 1 × $0 = $0 |
| **Net value** | **-$40** | **+$70** |

The $110 improvement came entirely from better *decisions*, not better *agents*. The agents didn't change at all.

**Notice the asymmetry:** harmful deploys cost 5× more than the value of good deploys. This is typical in enterprise settings where trust, once lost, is hard to regain. This asymmetry makes the value of better eval even higher—avoiding one harmful deploy is worth more than making five good ones.

**If you have a team of 10 people working on AI, put 8 on evals and 2 on engineering, not the other way

The 2 engineers can iterate fast—AI helps them write code, test variants, try new approaches. But without the 8 people building reliable measurement, the 2 engineers have no idea if their iterations are improvements. They're spinning.

(Also, you probably shouldn't have teams of 10 people working on one thing. But that's a different article.)

---

## The Value of Reducing Uncertainty

In Part 2, we saw the value of *awareness*—knowing that uncertainty exists. But what happens when you invest in *reducing* that uncertainty?

**Continuing the example from Part 2:**

You held agents B, D, and G because their uncertainty was too high. Now you invest in better evaluation—more test cases, better judges, more representative data.

The systems don't change. But your knowledge improves:

| Agent | Before | After better measurement | True E[V] | Decision |
|-------|--------|--------------------------|-----------|----------|
| B | +3 [−8, +14] | −2 [−5, +1] | −4 | Don't deploy ✓ |
| D | +6 [−15, +27] | +9 [+6, +12] | +8 | Deploy ✓ |
| G | +1 [−12, +14] | −4 [−7, −1] | −6 | Don't deploy ✓ |

With better measurement:
- **Agent B:** The range narrowed and shifted. You now see it's likely negative. You confirm the hold—correct decision.
- **Agent D:** The range narrowed dramatically. You now see it's confidently positive. You can deploy—you've unlocked value that was always there.
- **Agent G:** The range narrowed and you see it's clearly negative. You confirm the hold—correct decision.

**What reducing uncertainty gives you:**

1. **Confident deploys:** Agent D was a good system all along. You just didn't know it. Better measurement gave you the confidence to ship.

2. **Confident rejects:** Agents B and G were bad systems. Better measurement confirmed you should hold back, and now you can stop investigating them.

3. **No wasted effort:** Without better measurement, you might have kept investigating all three forever—or eventually deployed them out of impatience.

The system didn't improve. Your *knowledge* improved. And that knowledge has direct business value: you shipped a good agent you were holding back, and you stopped wasting effort on bad ones.

**The investment case for better measurement:**

Traditional framing: "We need better evals to improve our systems."

Better framing: "We need better evals to *know which systems are already good enough to ship*—and which ones aren't worth further investment."

Reducing uncertainty doesn't just help you improve. It helps you *decide*—faster, with more confidence, and with fewer mistakes.

---

## From Value to Scorecard: Knowing Where to Improve

So far we've talked about V (value) as a single number. But in practice, value is composed of multiple factors.

Think back to the loss profile from Part 1:

<figure>
<img src="../figs/loss_profile.jpg" alt="Loss profile optimization landscape" />
<figcaption>The loss landscape has many dimensions—each representing a different quality axis</figcaption>
</figure>

This multi-dimensional surface maps to a *scorecard*—a breakdown of value into measurable components:

- **Latency**: How fast does the agent respond?
- **Accuracy**: Does it get the right answer?
- **Fluency (German)**: How natural is the German output?
- **Fluency (English)**: How natural is the English output?
- **Safety**: Does it avoid harmful outputs?
- **Cost**: How much does it cost to run?
- **Compliance**: Does it follow required procedures?

Each dimension is an axis along which we can improve. And critically, **if we can measure these dimensions reliably, we know where to focus engineering effort**.

This is the second way better eval leads to better quality: not just through better deployment decisions, but through **directed improvement**.

Consider two scenarios:

**Scenario A: Poor scorecard measurement**
- You know the agent is "not great" but not why
- Engineers try random improvements
- Some work, some don't, you're not sure which
- Progress is slow and uncertain

**Scenario B: Good scorecard measurement**
- You know German fluency is at 65%, English at 92%, accuracy at 88%
- Engineers focus specifically on German fluency
- You can measure whether each change helps
- Progress is fast and directed

Conversely, if we cannot measure scorecard metrics properly, we cannot understand where to act. We're flying blind—iterating toward a random target, as we discussed in Part 1.

---

## Finding What Matters: Correlation as a Shortcut

Here's a practical insight: sometimes it's hard to come up with a good scorecard from first principles. What dimensions actually matter to customers? Is latency more important than fluency? Does accuracy matter more than compliance?

There's an empirical shortcut:

1. **Build a rich scorecard** — many dimensions, even speculative ones
2. **Measure actual value** — ask customers directly, or observe outcomes (adoption, complaints, escalations)
3. **Identify correlations** — which scorecard dimensions predict customer value?
4. **Focus on what matters** — now you know which aspects of the scorecard are useful and which are secondary

**This is extremely powerful.** You don't need to know in advance what matters. You can discover it empirically.

For example, you might hypothesize that latency matters a lot. But after measuring, you discover that customers don't complain about latency until it exceeds 5 seconds—below that, they don't notice. Meanwhile, every 10% improvement in German fluency correlates with a 15% increase in adoption among German-speaking users.

Now you know: optimize German fluency, not latency. Without the correlation analysis, you might have spent months shaving milliseconds off response time while the real problem went unaddressed.

---

## Why This All Matters

Better eval gives you two things:

**1. Better decisions.** Deploy what works, hold what's uncertain, disable what harms. This improves value immediately, without touching the agents.

**2. Effective improvement cycles.** You know the gradient—which dimensions to optimize, which agents need work, which customers are underserved. Your iterations move in the right direction, and you waste fewer cycles on changes that don't matter.

This is analogous to knowing the gradient in ML: you can always iterate, but without the gradient you're doing random search.

And here's why this matters even more now: **AI can write the code.** The engineering bottleneck is dissolving. What remains is knowing *what* to build. The teams with better eval will compound improvements. The teams without it will spin, whether they have 2 engineers or 20.

---

## The Questions You Must Ask

In every presentation, every review, every decision, train yourself to ask:

1. **"Can you stand behind these numbers?"** — Not "are they good" but "would you bet on them?"

2. **"Are you giving me a number or a range?"** — A point estimate without uncertainty is not information.

3. **"How did you reduce uncertainty?"** — What did you do to make this measurement reliable? More samples? Better judges? Multiple evaluators?

4. **"What measures have you taken against bias?"** — How do you know your eval isn't systematically optimistic? Have you checked for overfitting? For multiple hypothesis testing—picking the best of many runs?

5. **"Is that range uncertainty or variability?"** — Are we unsure about the average, or certain that it varies across customers?

Today, most presenters cannot answer these questions. That's the problem.

The next part explains *why*—where the bias, overfitting, and noise come from. But you don't need to understand the sources to start asking. Start asking.

---

**And we haven't even started discussing why your evals are likely to be structurally wrong.** That's next.

---

*Next: [Part 4: Sources of Bias and Uncertainty](./part-4-sources-of-error.md) — Where evaluation uncertainty comes from*

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering` `Uncertainty`

