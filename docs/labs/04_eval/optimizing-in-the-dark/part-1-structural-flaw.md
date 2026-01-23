# Optimizing in the Dark:
A Flaw in Human Judgement

## Part 1: A Structural Flaw in Judgment

*Iterating towards a random target*

---

![](./images/image1.png)

You have all been in this room. A slide goes up. There's a *metric*—"Technical Accuracy", a *number*: 89%, and a *color*—green.

Getting these metrics, numbers, and even the colors "right" are foundational to the success of a product.

They are the final output of a complex process of decisions and actions. This output is very consequential. Not only do they determine ship/no-ship decisions, but they tell engineers where to focus their energy, where to improve.
The metrics act like a *loss profile* and give us axes along which we need to improve our product. Unlike ML, this loss profile does not tell us how to improve, but it points us to what to work on.

![](../figs/loss_profile.jpg)

And as AI takes more of a leading role, they also tell AI where to improve—helping us make the "AI code generation → Evaluation" loop effective. Conversely, if we get these wrong, we iterate in the wrong directions, we ship things that make our customers lose trust in us, we hold back great features that could help us win deals.

![](./images/image3.png)

As I sit in the room at a customers' site and listen to presentation after presentation and report after report, I can't help but wonder: *how reliable are these numbers? Do the team reporting on the results know? And do we, and the executives sitting in the room, know? Do we grasp what that means for the decision we're about to make?*

---

Walter Lewin, the MIT physicist, in his first lecture of the course in basic Physics tells his students: "*Any measurement, without knowledge of the uncertainty, is meaningless.*" Not "less precise." Not "directionally useful." **Meaningless.** Then he adds: "*I want you to hear this at 3am tonight when you wake up.*" He says this *in the first lecture of the first course* on Physics, not at some random point.

And **he was talking to people who live in the science of measurement**. 
We are not in that world. In enterprise AI we evaluate and report "at scale" across many use cases and teams, with vastly diverse audiences ranging from engineers to scientists to executives. It is a duty of the presenter to make sure that they convey information in a manner that enables the listeners to take the right action. 

I posit that while the number in itself may be *meaningless*, the act of **reporting** without knowledge and indication of its uncertainty makes it **misleading**.


A common tendency in organizations is to wash this question away based on the idea that "*we are engineers, we are so cool because we approximate, and iterate. Dwelling on uncertainty is for theorists. A measure may not be perfect, we know, but it's a hint, and we will improve over time. We crawl, walk, run.*"
How many time have you heard this argument? Or how often do you hear that "yeah, it would be great to discuss uncertainty but executives won't understand, they need a simple number"?


But having a sense for how biased and noisy our measures can be is central to the notion of "engineering approximation". More specifically:

> *A measurement - and a report of a measurement - is harmful if it leads me to make the wrong decision, or take the wrong action on a system.*

Now, this is an issue only if it is true that 1. AI measures and reports are characterized by significant uncertainty, and 2. we don't communicate it or, even worse, we are not even aware that this is something to worry about.



---

## The Anthropic Paper and the Industry's Response


I started paying closer attention to this problem when Anthropic published a paper titled "[Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640)." I thought: "It's about time people in this industry begin making this point."


![](./images/image4.png)

But..... no, I was wrong. Social media were telling a different story.
Pedro Domingos said: "*Spectacular breakthrough in AI: Anthropic has discovered error bars!*" The sarcasm was widespread. "*What an unserious field*", people said, that needs to be told to add error bars.

![](./images/image5.png)


**The mockery proved the paper's point.** (the paper is on way more than "error bars" - and uncertainty is not synonymous with "error bars" - but it makes the point). 
If this was obvious and practiced, the paper wouldn't exist. The fact that a leading AI lab felt the need to write it—and the fact that the community's response was ridicule rather than embarrassment—tells us where we are.

---

# Kahneman's "Noise" and Organizational Blindness

Around the same time, I came across Kahneman, Sibony, and Sunstein's book "*Noise: A Flaw in Human Judgment*."

One of its central observations is that *organizations systematically underestimate—and resist acknowledging—variability* in judgment. We prefer consensus and harmony. We don't want to see the noise. The book focuses more on human judgment and assessment of human judgment, but the same applies to assessment of AI systems.

This book resonated well with my experience working with many companies and system integrators.

![](./images/image6.jpeg)

Even more insightful was the experience I had from discussing it with a friend working at an AI company in the Valley. His response after reading it was: "*Yeah, the book is pretty useless. We know there's a standard deviation.*" This is the same kind of response that the Anthropic article received.

The point the book is making is not that assessments are subject to errors. But that such errors are large, and largely ignored by organizations. The book dwell then some more on how orgs are especially insensitive to noise even more so than bias - for us, they are both relevant and need to be addressed.

So, yes, there's noise, and variance—and we don't know:

- How large it is,
- Where it comes from,
- How much it's costing us, 
- How to reduce it
- *Or even how to talk about it*

And - noise and variance are only part of the problem. In most of the companies I have worked with, Measurement processes can be—and typically are—*systematically* biased: consistently producing results that are too optimistic or simply measuring the wrong thing. 

What Kahneman helped me see is that this isn't just a skills gap. It's **structural**. Organizations have never had to rigorously measure the quality of machine judgment and have never had to deal with measurements that have so much uncertainty and this level of complexity. And to do so at scale.
The muscle doesn't exist—and it is unclear even if the right incentives to develop it are in place.

---

## Who bears responsibility?

We are building highly consequential AI systems, making decisions based on evaluation numbers, and we are systematically both *underestimating* and *ignoring* the uncertainty in those numbers.

This begs the question: who bears responsibility for this widespread flaw? Is it the person presenting? The person who designed the reporting template? The team that delivered evaluation tools? The instructors that prepared the training material? or, *The executive who doesn't ask? The culture that punishes uncertainty?* Or, the natural unwillingness of organizations to accept the existence of variability within a structured process?

The question is hard also because the "problem" landscape has three distinct facets:

1. **The visibility problem** (epistemic): People don't see the uncertainty. It's not reported, not computed, not surfaced. The green 89% on the screen looks solid. Decision-makers can't account for what they don't know exists.

2. **The culture problem** (organizational): The organization doesn't ask. We don't reward quantifying uncertainty. We don't penalize ignoring it. The question "how confident are we?" isn't part of the discussion process. Uncertainty stays invisible because making it visible has no upside and manypotential downsides (looking less confident, slowing things down, looking..... uncertain).

3. **The action problem** (methodological): Even when uncertainty is visible and the culture asks about it, people don't know what to do. How do you decide when the range is 77–95%? How do you reduce variance when you don't know which source dominates? The frameworks and practices are neither widely known nor well-established in modern AI.

To understand why evaluation practices erode as we move toward gen AI, we need to look at how engineering evolved across Software 1.0, 2.0, and 3.0. But first, let's understand the cost of inaction.

---

# The Cost of Inaction

It's easy to talk about noise as an abstract annoyance—"sure, the metric is a bit noisy, but directionally it's fine."

Every score is the output of a measurement pipeline—and that pipeline injects both **uncertainty** and **bias**. Whether we can wash away current eval imperfection as "engineering approximation" depends on how large they are.

---

## Every Score Has Two Error Terms: Bias and Uncertainty

For a given use case ***i***, the reported score is not just a function of system quality. It is an estimate:

> **reported_scoreᵢ = true_scoreᵢ + Bᵢ + εᵢ**

Where:

- **εᵢ** is ***noise*** (random error): sampling variance, stochastic judge variance, rater inconsistency, prompt sensitivity, rubric interpretation variance, etc. This is what produces **uncertainty (UNᵢ)**, typically visible as a confidence interval or run-to-run variability.

- **Bᵢ** is ***bias*** (systematic error): non-representative test sets, rubric misalignment with user value, proxy metrics that reward the wrong behavior, judge preference artifacts, contamination/leakage, over-representation of "easy" cases, and other consistent measurement distortions.

Two implications matter operationally:

1. **Uncertainty is often measurable. Bias often isn't.** You can estimate run-to-run variance. You can compute confidence intervals. But bias can hide behind stability. The most dangerous situation is a **tight error bar around the wrong number**.

2. **Bᵢ and UNᵢ vary by use case.** Some use cases are "measurement-friendly" (their eval pipeline is optimistic). Others are "measurement-hostile" (their eval pipeline is pessimistic). A portfolio that treats all scorecards as equally valid is not making a ranking—it's making a decision using unknown and uneven measurement error.

---

## Two Kinds of Cost: Random Mistakes and Systematic Mistakes

At scale, both noise and bias hurt—but they hurt differently.

- **Noise (variance)** creates ***random wrong turns***: you invest in the wrong variant, pause the wrong project, chase an improvement that wasn't real.

- **Bias** creates ***systematic wrong turns***: you consistently overestimate what's ready, consistently favor what's easy to score, consistently "prove" progress on the slide deck that won't show up in production.

**Selection turns noise into bias.**

Even if each individual evaluation were unbiased, the act of picking winners creates systematic optimism. The measurement process starts neutral. The decision process makes it lopsided. The math is real.

---

## The Single-Use-Case Cost: When One Scorecard Misleads You

A portfolio problem is made of many local problems. Even inside a single use case, bias and uncertainty create expensive failure modes.

### The Threshold Trap

Most decisions are threshold decisions: ship if score ≥ **T**.

But if **reported_score = true_score + B + ε**, then a small positive bias can dramatically increase the chance that an unready system crosses the threshold.

**Example:** T = 85, σ = 4 points, true = 80

| Bias B | What you're effectively measuring | Probability you ship even though true < T |
|--------|-----------------------------------|-------------------------------------------|
| 0 | 80 + noise | ~11% |
| +3 | 83 + noise | ~31% |
| +5 | 85 + noise | ~50% |

A few points of bias does not "nudge" the decision—it can **double or triple** the false-positive rate.

### The Directional Illusion

Within one use case, teams iterate quickly and celebrate small gains: +1, +2, +3 points.

But if those changes are within **UN**, what looks like progress is often just noise. That creates predictable waste:

- false wins ("we improved!"),
- false regressions ("we broke it!"),
- thrash between variants, and
- over-engineering to chase a moving number.

The waste is invisible because the work feels productive. Metrics fluctuate. Experiments complete. Sprints close. But a meaningful fraction of effort is spent climbing hills that don't exist.

### Bias Lock-In

Early evaluations are typically the most biased: weak rubrics, small or unrepresentative datasets, uncalibrated judge prompts, missing edge-case coverage.

Yet early evaluations drive the most irreversible choices: architecture, approach, tooling, and definitions of "good."

If early measurement is biased, you don't just waste one sprint—you build a system that is locally optimal for a flawed measurement process.

---

## The Portfolio Winner's Curse

Now scale up.

Suppose you have **U** use cases, each with a reported score:

> **reported_scoreᵢ = true_scoreᵢ + Bᵢ + εᵢ**

Even if εᵢ averages to zero across evaluations, the best-looking score among many will be "lucky." This is the same phenomenon as best-of-K selection inside one use case—except now it operates across your entire portfolio.

### Winner's curse from noise (ε): extremes are disproportionately luck

**Expected optimism from picking the best-looking item among many:**

| Candidates compared | Expected "winner's bonus" (E[max]/σ) | If σ = 4 points |
|---------------------|--------------------------------------|-----------------|
| 10 | ~1.54σ | +6.2 points |
| 50 | ~2.25σ | +9.0 points |
| 100 | ~2.51σ | +10.0 points |
| 500 | ~3.04σ | +12.1 points |

Interpretation: if your evaluation pipeline has **σ ≈ 4 points** (not unusual once you include sampling noise, judge noise, and rubric mapping), then in a portfolio of ~50 use cases, the "top" use case is expected to look ~9 points better than it truly is—even if all use cases had identical true quality.

### Winner's curse from bias (B): the portfolio selects measurement-friendly use cases

Noise is only half the story. In real portfolios, **Bᵢ varies**.

That means portfolio selection doesn't just surface the best *systems*. It systematically surfaces:

- use cases whose measurement pipeline is **optimistic** (high Bᵢ), and
- use cases with higher variance (high σᵢ), because they generate more extreme "wins."

This is how organizations drift toward "demo-friendly" and "metric-friendly" work. It's not because people are dishonest. It's because the system rewards what measures well.

### Selection happens repeatedly, so optimism accumulates

Organizations don't select once. They select repeatedly:

- Each team selects the best prompt or pipeline variant for their use case
- Leadership selects the best use cases across teams
- PMs select the best demos for executive review
- The organization selects the "reference implementation" everyone copies

Each selection step preferentially surfaces outcomes inflated by ε (luck) and, over time, biased toward use cases with favorable B.

By the time something becomes a showcase or a standard, it has survived multiple rounds of selection—which means it has accumulated multiple rounds of optimism.

---

## Misranking Is Not Rare—It's the Default When Differences Are Small

Portfolio decisions often hinge on small score differences: "Use case A is 84%, B is 88%—let's invest in B."

But if measurement noise is comparable to those differences, you are ranking with a randomizer.

If two use cases differ in true quality by Δ points, and evaluation noise has standard deviation σ, the probability you rank them incorrectly (due to noise alone) is approximately:

> **P(misrank) ≈ Φ( −Δ / (√2 · σ) )**

**Example (σ = 4 points):**

| True gap Δ | Chance you pick the wrong one |
|------------|-------------------------------|
| 4 points | ~24% |
| 6 points | ~14% |
| 8 points | ~8% |

And this is the optimistic case—because it ignores Bᵢ. If the two use cases have different bias terms (Bᵢ ≠ Bⱼ), then even "large" observed gaps can be artifacts of measurement. The ranking can be systematically wrong, not just occasionally wrong.

---

## What the Cost Looks Like in the Real Organization

### Wasted Engineering Cycles

Inside a single use case, noisy metrics cause false wins, false regressions, thrash, and over-engineering. Bias makes it worse: the team optimizes for what the measurement rewards, even when it doesn't translate to user value.

Multiply that by dozens of use cases, each running weekly evaluations, each making local optimizations. The organization pays a continuous tax: iteration budget spent on measurement artifacts rather than customer outcomes.

### Portfolio Misallocation

The largest cost isn't a wrong prompt tweak. It's when noisy or bias-inflated numbers determine which use cases get funded, which teams grow, and which product bets become strategic priorities.

When evaluation uncertainty is comparable to the actual differences between use cases, portfolio allocation becomes partly random. When bias differs across use cases, allocation becomes systematically distorted toward measurement-friendly work.

This is where measurement error becomes capital allocation error—the kind that burns quarters, not days.

### Incentive Distortion

Bias from selection means teams who run more experiments often report better numbers—not necessarily because they built better systems, but because they had more chances to get lucky and more opportunities to overfit the measurement.

Portfolio leadership then rewards the behavior that increases bias: more variants, more tuning on the same evaluation set, more aggressive metric chasing. The incentive structure selects for practices that make measurements less reliable, not more.

### Production Failures Are Predictable, Not Random

A false negative—delaying a feature that was actually ready—is expensive.

A false positive—shipping a feature that looked green but fails in production—is often catastrophic: customer trust erodes, escalations consume executive attention, emergency patches add complexity, and the narrative that "this AI thing is unreliable" damages unrelated use cases.

Here is the connection that matters: **false positives are not bad luck.** They are a predictable consequence of biased and uncertain measurement combined with selection. The systems that cross your "ready to ship" threshold are disproportionately the ones measured better than they truly are.

### Coordination Overhead and Argument Inflation

When metrics are unstable or non-comparable, the organization spends time arguing:

- which metric "counts,"
- whose judge prompt is correct,
- why two teams' numbers disagree,
- whether any dashboard can be trusted.

That debate is rational—but it is pure overhead created by non-credible measurement.

---

## The Compounding Problem

These costs compound over time.

Early evaluations—which are typically the noisiest and most biased, because you have the least data and the least-calibrated methodology—shape architectural choices, approach selection, and resource allocation. If those early evaluations mislead, you build on a flawed foundation.

Later iterations optimize within a suboptimal design space. You climb the wrong hill efficiently. By the time production feedback reveals the gap, you've invested months of engineering effort in the wrong direction.

The sunk cost creates pressure to explain away the gap rather than question the trajectory. "Production data is different." "Users behave unexpectedly." "Edge cases we didn't anticipate." The possibility that the evaluation was simply unreliable—that the direction was never right—is rarely the first hypothesis.

---

Noise is not just a statistical property of an evaluation. Bias is not just a theoretical concern.

In a portfolio organization, they become operating costs and strategy risks.

A single biased or noisy scorecard can waste a sprint. A portfolio of biased and noisy scorecards can waste a quarter—and systematically steer the organization toward the luckiest-looking, measurement-friendly bets rather than the truly best ones.

---

*Next: [Part 2: A Brief History of Evals](./part-2-history-of-evals.md) — How we got here, from Software 1.0 to 3.0*

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering`
