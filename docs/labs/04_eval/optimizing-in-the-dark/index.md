# Optimizing in the Dark:
A Flaw in Human Judgement

---

*A four-part series on the hidden uncertainty in AI evaluation metrics*

---

You've been in this room. A slide goes up. There's a metric—"Technical Accuracy", a number: 89%, and a color—green. The decision feels obvious.

![](../figs/metric_meeting.png)

But how reliable is that number? What if the true accuracy could be anywhere from 74% to 95%? What if the act of selecting the "best" system has systematically inflated your expectations? What if you're iterating toward a random target?

This series explores a structural problem in how organizations evaluate AI systems: we are building highly consequential systems, making decisions based on evaluation numbers, and systematically both *underestimating* and *ignoring* the bias and uncertainty in those numbers.

---

## The Series

### [Part 1: A Structural Flaw in Judgment](./part-1-structural-flaw.md)

The problem statement. Why "89% accuracy" might be meaningless—or worse, misleading. The three facets of the problem: visibility, culture, and action. And the real costs of ignoring uncertainty: wasted cycles, misallocated portfolios, and production failures that were predictable all along.

### [Part 2: A Brief History of Evals](./part-2-history-of-evals.md)

How we got here. A journey through Software 1.0 (deterministic code), Software 2.0 (ML models), and Software 3.0 (Gen AI applications)—tracing how our evaluation muscles weakened as systems became more complex, more open-ended, and harder to pin down.

### [Part 3: Sources of Bias and Uncertainty](./part-3-sources-of-error.md)

The technical deep dive. From sample size effects to multiple hypothesis testing, from developer-induced overfitting to noisy LLM judges, from rubric mapping artifacts to prompt sensitivity. Each source alone can flip your decisions. Together, they compound.

### [Part 4: What To Do About It](./part-4-what-to-do.md)

The path forward. Addressing visibility (awareness, estimation, reporting), action (reducing uncertainty, building observability), and culture (naming things right, asking the questions, making accountability explicit). Practical tools including evaluation worksheets and AI-powered methodology assistants.

---

## Key Themes

- **Every score has two error terms**: bias (systematic) and uncertainty (random). Bias is harder to see but often more dangerous.

- **Selection turns noise into bias**: Even unbiased evaluations become optimistic when you pick winners. The math is real.

- **Small differences are noise**: If your evaluation noise is ±4 points, a 4-point gap between systems gives you a ~24% chance of picking the wrong one.

- **The uncertainty is larger than you think**: Sample size alone gives you a 16-point confidence interval on 100 examples at 82% accuracy. And that's the *optimistic* case.

- **Culture matters**: Organizations prefer harmony. Point estimates feel decisive. Uncertainty feels like weakness. But pretending certainty where none exists—*that's* weakness.

---

## Who This Is For

- **Engineering leaders** making ship/no-ship decisions based on evaluation metrics
- **ML/AI practitioners** designing and running evaluation pipelines
- **Product managers** interpreting and reporting quality numbers
- **Executives** who see scorecards and need to know what questions to ask

---

*"Any measurement, without knowledge of the uncertainty, is meaningless."*
— Walter Lewin, MIT

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering` `Quality Assurance`
