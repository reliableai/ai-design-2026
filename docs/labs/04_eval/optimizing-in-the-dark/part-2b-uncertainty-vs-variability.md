# Uncertainty vs Variability

Part 2b of *Optimizing in the Dark:
Organizational Blindness in AI Evaluations*

*When you see a range, what does it mean?*

← [Part 2: The Cost of Ignorance](./part-2-cost-of-ignorance.md) | [Series Index](./index.md)

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

## One Agent, Many Customers

So far in Part 2 we discussed M agents for one customer. But there's another dimension: deploying one agent across N customers.

This introduces a different kind of uncertainty — one that better measurement can *reveal* but cannot *reduce*.

You have one agent — say, Incident Auto-Resolution — and 10 customers considering deployment. You've evaluated thoroughly and you're confident: E[V] = +8, range [+5, +11].

Should you deploy to all 10 customers?

Your evaluation was done on some dataset — maybe a mix of data from several customers, maybe synthetic data, maybe data from your most engaged pilot customer.

But each customer's data is different:
- Customer A has clean, well-structured tickets with consistent formatting
- Customer B has messy tickets with lots of jargon and abbreviations
- Customer C has tickets in multiple languages
- Customer D has a ticket system that truncates long descriptions

The agent might perform very differently across these environments. Your confident E[V] = +8 might actually be:

| Customer | True E[V] |
|----------|-----------|
| A | +15 |
| B | +2 |
| C | −5 |
| D | +12 |
| E | +8 |
| F | −3 |
| G | +10 |
| H | +6 |
| I | +1 |
| J | −8 |

Your aggregate evaluation gave you confidence, but the reality is: 3 out of 10 customers would be harmed.

---

**This uncertainty is different**

With measurement uncertainty, better evaluation narrows your range. You become more confident about the true E[V].

With cross-customer variability:
- Better measurement makes you *more confident about the variance* — you learn precisely how much performance differs across customers
- But better measurement *doesn't reduce* the variance — it's real variability in the world, not measurement error

If you evaluate on Customer C's data, you don't make the agent work better for Customer C. You just learn that it doesn't work well there.

---

**What can you do?**

1. **Improve the system:** Make the agent more robust to different data distributions. This actually reduces the variance.

2. **Deploy selectively:** Learn which customers (or which data characteristics) predict success, and only deploy where you expect E[V] > 0.

3. **Set expectations:** If you deploy broadly, communicate that results will vary. Some customers will see great results; some won't.

The key point: this is not a measurement problem. It's a real-world variability problem. Recognizing the difference matters for deciding where to invest effort.

---

*Next: [Part 3: Better "Evals" Beats Better Dev](./part-3-value-of-better-measurement.md) — The value of knowing what you're measuring*

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering`
