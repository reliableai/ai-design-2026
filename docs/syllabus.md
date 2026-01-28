## 5. Weekly Schedule (12 Weeks, 24 Lessons)

Each week has **two 90-minute lessons**.
The course has **three phases**:

- **Phase 1 (Lessons 1–6):** Building & Evaluating AI Apps (agents, tools, memory, monitoring, quality estimation, iteration).
- **Phase 2 (Lessons 7–10):** Complex AI Systems (councils of agents, complex systems, middleware, project structuring).
- **Phase 3 (Lessons 11–24):** Project-driven work (reviews, meetings, presentations).

---

### Week 1 – Hello World & Stateful Clients

**Lesson 1 – Hello World**
Connecting to AI via API: chat, streaming, voice, and image.

**Lesson 2 – Stateful Clients**
Managing context and session memory, cost and latency tradeoffs.

---

### Week 2 – Tools & Monitoring

**Lesson 3 – Tools & The Agentic Loop**
Tool calling, orchestration, AI controlling UX.

**Lesson 4 – Monitoring & Business Assertions**
Observability, runtime checks, evaluating executions.

---

### Week 3 – Quality Estimation & Iteration

**Lesson 5 – Quality & Performance Estimation**
Metrics, golden datasets, LLM-as-judge, "Optimizing in the Dark" case study.

**Lesson 6 – Iterating on Clients, Agents & Prompts**
Systematic improvement cycles, experiment design, error analysis.

---

### Week 4 – Councils & Complex Systems

**Lesson 7 – Councils of Agents**
Eliciting diversity of opinions, ensemble approaches, consensus mechanisms.

**Lesson 8 – Building Complex Systems**
Divide et impera, testability, separation of concerns, APIs vs interfaces.

---

### Week 5 – Middleware & Project Structuring

**Lesson 9 – Middleware, Abstractions & Interfaces**
MCP protocol, guardrails, long-term memory, privacy.

**Lesson 10 – Structuring Complex Projects**
Approaching and maintaining large AI systems, multi-version considerations.

---

### Week 6 – Frameworks & Project Kick-off

**Lesson 11 – AI Frameworks**
When and why to use frameworks; LangChain as a case study.

**Lesson 12 – Project Specification**
Track selection, requirements, team formation. **Project Spec v1** due.

---

### Week 7 – Midterm & First Project Review

> From this week on, **all contact hours are project-focused**: exams, project reviews, working sessions, and presentations.

**Lesson 13 – Midterm Written Exam (Individual)**
- Written exam on material from Lessons 1–10:
  - Phase 1: Hello world, stateful clients, tools, monitoring, quality estimation, iteration.
  - Phase 2: Councils of agents, complex systems, middleware, project structuring.

**Lesson 14 – Project Review Meeting #1 (Teams)**  
- Per-team review (Track A & B mixed):
  - Revisit problem statement & scope.  
  - Present refined architecture diagram.  
  - Present current evaluation plan and golden dataset status.  
- You and peers give feedback on:
  - Feasibility and focus.  
  - Evaluation coverage and realism.  
- Teams leave with a concrete **milestone plan** for Weeks 8–10.

---

### Week 8 – Deep Project Working Sessions

**Lesson 15 – Project Working Session #2 (Implementation Focus)**  
- Hands-on coding in class:
  - Integrate missing components (tools, memory, logging, safety modules).  
  - Ensure there is at least one end-to-end flow runnable.  
- Short 5-minute **stand-ups** per team:
  - What we did since last week.  
  - Blockers.  
  - Plan until next class.

**Lesson 16 – Project Working Session #3 (Evaluation Focus)**  
- Each team:
  - Finalizes first full **evaluation run** on the golden dataset.  
  - Debugs the evaluation harness as needed.  
- Mini “round-robin” reviews:
  - Teams pair up and quickly review each other’s eval setups & metrics.

---

### Week 9 – Mid-Project Presentations & Design Clinic

**Lesson 17 – Mid-Project Presentations (Internal Demo)**  
- 10–12 minutes per team:
  - Live or recorded demo of current system.  
  - Architecture overview.  
  - Current evaluation design and early results.  
  - Biggest open risks / unknowns.
- Feedback from instructor + peers on:
  - Clarity of design narrative.  
  - Strength of evaluation strategy.  
  - Suggestions for final stretch.

**Lesson 18 – Design & Evaluation Clinic #2 (Breakout Meetings)**  
- Breakout tables:
  - Table A: architecture & scalability questions.  
  - Table B: evaluation & golden dataset questions.  
  - Table C: safety/guardrails & memory behavior.  
- Teams rotate or camp at the table most relevant to their blockers.  
- Goal: unblock design/eval decisions for the final two weeks.

---

### Week 10 – Final Implementation Push

**Lesson 19 – Project Working Session #4 (Integration & Hardening)**  
- Focus on:
  - Integration between components (tools, memory, UI, eval harness).  
  - Error handling, logging, and basic observability.  
- Instructor circulates for 1:1 technical coaching.

**Lesson 20 – Project Working Session #5 (Final Evaluation Runs)**  
- Run **final evaluation suites**:
  - Golden dataset + main metrics.  
  - Key experiments/ablations (as defined in project spec).  
- Start drafting **results tables and plots** for the report.

---

### Week 11 – Final Reports & Presentation Prep

**Lesson 21 – Project Review Meeting #3 (Results & Storytelling)**  
- Each team brings:
  - Draft results section (tables/figures).  
  - Draft error taxonomy & key examples.  
- In-class:
  - You focus on sharpening the **narrative**:
    - What did we really learn?  
    - Which experiments mattered?  
    - How did evaluation change design?

**Lesson 22 – Presentation Rehearsals (Dry Runs)**  
- Teams rehearse their final presentation (~10–12 minutes).  
- Peer feedback on:
  - Clarity of slides/demos.  
  - Balance between design explanation and evaluation findings.  
  - Time management.

---

### Week 12 – Final Presentations & Retrospective

**Lesson 23 – Final Presentations (Graded)**  
- Each team presents:
  - System demo.  
  - Design choices & non-obvious alternatives considered.  
  - Evaluation framework and main results.  
  - Limitations & future work.
- Q&A after each presentation.

**Lesson 24 – Final Project Meeting & Course Retrospective**  
- Final project check-in:
  - Any last clarifications on reports (if due after class).  
- Whole-class retrospective:
  - What worked / didn’t in your system and process.  
  - How evaluation affected design decisions.  
  - How you would approach a **new** large-scale AI system differently after this course.
