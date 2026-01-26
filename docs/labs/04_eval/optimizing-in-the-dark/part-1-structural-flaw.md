# A Structural Flaw in Judgment

Part 1 of *Optimizing in the Dark:
Organizational Blindness in AI Evaluations*

*Iterating towards a random target*

[Series Index](./index.md) | [Part 2 →](./part-2-cost-of-ignorance.md)

---

![](./images/image1.png)

You have all been in this room. A slide goes up. There's a *metric*—"Technical Accuracy", a *number*: 89%, and a *color*—green.

Getting these metrics, numbers, and even the colors "right" are foundational to the success of a product.
These numbers - and colors - are the final output of a complex process of decisions and actions.

 This output is very consequential. Not only does it determine ship/no-ship decisions, but it tells engineers where to focus their energy, where to improve.
The metrics act like a *loss profile* and give us axes along which we need to improve our product. 

![](../figs/loss_profile.jpg)

And as AI takes more of a leading role in development, getting the right metrics and the right measures is central to effective product improvement iterations - poissibly even automating the entire process. Conversely, if we get these wrong, we iterate in the wrong directions, we ship things that make our customers lose trust in us, we hold back great features that could help us win deals.

![](./images/image3.png)

As I sit in the room at a customers' site and listen to presentation after presentation and report after report, I can't help but wonder: *how reliable are these numbers? Do the team reporting on the results know? And do we, and the executives sitting in the room with me, know? Do we grasp what that means for the decision we're about to make?*

---

Walter Lewin, the MIT physicist, in his first lecture of the course in basic Physics tells his students: "*Any measurement, without knowledge of the uncertainty, is meaningless.*" Not "less precise." Not "directionally useful." **Meaningless.** 

Then he adds: "*I want you to hear this at 3am tonight when you wake up.*" He says this *in the first lecture of the first course* on Physics, not at some random point.

And **he was talking to people who live in the science of measurement**. 
We are not in that world. In enterprise AI we evaluate and report "at scale" across many use cases and teams, with vastly diverse audiences ranging from engineers to scientists to executives. *It is the duty of the presenter to make sure that they convey information in a manner that enables the listeners to take the right action.* 


I posit that while the number in itself may be *meaningless*, the act of **reporting** without knowledge and indication of its uncertainty makes it **misleading**.


A common tendency in organizations is to wash this question away based on the idea that "*we are engineers, we are so cool because we approximate, and iterate. Dwelling on uncertainty is for theorists. A measure may not be perfect, we know, but it's a hint, and we will improve over time. We crawl, walk, run.*"
How many time have you heard this argument? Or how often do you hear that "yeah, it would be great to discuss uncertainty but executives won't understand, they need a simple number"?

These are scarily naive and dangerous arguments. 
Having a sense for how biased and noisy our measures can be is central to the notion of "engineering approximation". More specifically:

> *A measurement - and a report of a measurement - is harmful if it leads me to make the wrong decision, or take the wrong action on a system.*

There are only two conditions under which ignoring and not reporting on uncertainty is not a problem:

1. The measurement is so precise that it is not subject to any meaningful uncertainty
2. The measurement doesnt matter that much

If the second condition is true, then stop reading - and stop measuring. 
If metrics matter, then reporting without knowledge of uncertainty should be a fireable offense. Maybe we need one more "[Jeff Bezos memo](https://github.com/victorvalentee/bezos_api_mandate)" moment...



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

## Kahneman's "Noise" and Organizational Blindness

Around the same time, I came across Kahneman, Sibony, and Sunstein's book "*Noise: A Flaw in Human Judgment*."

One of its central observations is that *organizations systematically underestimate—and resist acknowledging—variability* in judgment. We prefer consensus and harmony. We don't want to see the noise. The book focuses more on human judgment and assessment of human judgment, but the same applies to assessment of AI systems.

This book resonated well with my experience working with many companies and system integrators.

![](./images/image6.jpeg)

I've had this conversation a dozen times with engineers at AI companies. The response is remarkably consistent: "*Yeah, we know there's variance. Big deal.*" 

But the point the book is making is not that assessments are subject to errors and variability, but that such errors are *large*, and *largely ignored* by organizations. The book dwells on how orgs are especially insensitive to noise even more so than bias. For us, both are present, relevant, and need to be addressed.

So yes, there's noise and variance—and we don't know:

- How large it is,
- Where it comes from,
- How much it's costing us, 
- How to reduce it
- *Or even how to talk about it*

And - noise and variance are only part of the problem. In most of the customers I have worked with, measurement processes can be—and typically are—*systematically* biased: consistently producing results that are too optimistic or simply measuring the wrong thing. 

What Kahneman helped me see is that this isn't just a skills gap. It's **structural**. Organizations have never had to rigorously measure the quality of machine judgment and have never had to deal with measurements that have so much uncertainty and this level of complexity. And to do so at scale.

The muscle doesn't exist—and it is unclear even if the right incentives to develop it are in place.

---

# What's the core of the proglem, and who bears responsibility?

We are building highly consequential AI systems, making decisions based on evaluation numbers, and we are systematically both *underestimating* and *ignoring* the uncertainty in those numbers.

This begs the question: who bears responsibility for this widespread flaw? Is it the person presenting? The person who designed the reporting template? The team that delivered evaluation tools? The instructors that prepared the training material? or, *The executive who doesn't ask? The culture that punishes uncertainty?* Or, the natural unwillingness of organizations to accept the existence of variability within a structured process?

The question is hard also because the "problem" landscape has three distinct facets:

1. **The visibility problem** (epistemic): People don't see the uncertainty. It's not reported, not computed, not surfaced. The green 89% on the screen looks solid. Decision-makers can't account for what they don't know exists.

2. **The culture problem** (organizational): The organization doesn't ask. We don't reward quantifying uncertainty. We don't penalize ignoring it. The question "how confident are we?" isn't part of the discussion process. Uncertainty stays invisible because making it visible has no upside and many potential downsides (looking less confident, slowing things down, looking..... uncertain).

3. **The action problem** (methodological): Even when uncertainty is visible and the culture asks about it, people don't know what to do. How do you decide when the range is 77–95%? How do you reduce variance when you don't know which source dominates? The frameworks and practices are neither widely known nor well-established in modern AI.

Let's understand the cost of inaction—and then what to do about it.

---

*Next: [Part 2: The Cost of Ignorance](./part-2-cost-of-ignorance.md) — Why ignoring uncertainty is expensive*

---

**Tags:** `AI` `Machine Learning` `Evaluation` `MLOps` `AI Engineering`
