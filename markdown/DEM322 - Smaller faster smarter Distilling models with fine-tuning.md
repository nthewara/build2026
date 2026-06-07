---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/fine-tuning
  - topic/distillation
  - topic/models
  - topic/ai
source: https://www.youtube.com/watch?v=EkZmVdfjPL0
session_code: DEM322
event: Microsoft Build 2026
speakers: William (Azure AI Foundry Fine-Tuning team)
duration_min: 25
aliases:
  - Smaller faster smarter Distilling models with fine-tuning
---

# DEM322 — Smaller, faster, smarter: Distilling models with fine-tuning

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** William — Azure AI Foundry Fine-Tuning team  
> **Duration:** ~25 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=EkZmVdfjPL0)

## 🎯 TL;DR
This demo session shows how to take a large, expensive "teacher" model (GPT-5.5) running in production as an agent, capture its real **agent traces**, and use those traces to **distill** its behaviour into a much smaller, cheaper "student" model (GPT-4.1 nano) via **supervised fine-tuning (SFT)** on Azure AI Foundry. The core insight is economic: as AI moves from frontier labs into enterprise workflows, intelligence has to become a cheap **utility rather than a luxury** — and agents are token-consumption machines that get very expensive at scale ("can I afford to run my agent a hundred million times?"). William demonstrates the full loop end-to-end: design a hard task set, simulate teacher conversations to generate traces, evaluate with a multi-dimensional rubric and a **pass@k** metric, fine-tune the student in Foundry directly from collected traces, and prove that the fine-tuned nano closes much of the gap to the teacher — sometimes matching or exceeding it on the narrow task. Crucially, distillation teaches not just the right *answer* but the right *trajectory*: correct tool order, correct argument values, and correct policy-checking behaviour.

## 🔑 Key Takeaways
- **The economics changed.** Six months ago the goal was "the fastest agent"; now the question is "can I afford to run my agent 100 million times?" Intelligence needs to become a cheap utility, not a luxury commodity.
- **Agents are token-consumption machines.** Every tool, context window, memory, and policy point you bake into an agent multiplies token usage — so running a frontier model (e.g. GPT-5.5) per request "breaks your budget."
- **Model distillation = an apprenticeship between two AI models.** A large capable **teacher** solves real tasks; you collect examples of how it behaves and **fine-tune a smaller, cheaper student** to imitate that behaviour at a fraction of the cost.
- **Learn from agent traces, not synthetic data.** Traces are *real* conversations capturing the messy, off-script questions users actually ask — plus the tool calls (which tool, what order, what argument values). This is real signal, not what you *imagine* users will ask.
- **Trajectory matters as much as the answer.** Like getting the right answer with the wrong method in school, an agent can reach the right outcome via the wrong path. Distillation teaches the correct trajectory: right tools, right order, right arguments, right policy checks.
- **Four wins from distillation:** (1) dramatically lower cost (models small enough to sometimes fit on-device), (2) faster responses, (3) teacher-level quality on the narrow task (sometimes outperforming the teacher), (4) more consistent behaviour from supervised fine-tuning.
- **Traces are free and self-improving on Foundry.** If you build agents on Foundry, trace collection runs automatically in the background — your agent gets smarter the more it's used, at no additional cost.
- **Evaluation is the key.** You can't improve what you can't measure. William scores full multi-turn conversations across four dimensions: **decision correctness, tool trajectory, financial accuracy, and communication.**
- **pass@k measures consistency.** Run the same task k times; count how often the model scores above an acceptable threshold. Each model (teacher / base student / fine-tuned student) is run 3× per task to gauge reliability, not just one lucky pass.
- **The headline result:** a large baseline gap between GPT-4.1 nano and GPT-5.5 was substantially closed by fine-tuning — the fine-tuned nano sometimes matched the teacher and "recovered more than half of the headroom," with a separate **holdout set** proving genuine imitation rather than memorisation.
- **Fine-tuning fixes real failure modes** demonstrated live: refusing unjustified refunds (defect vs. "I don't like it"), checking refund policy before acting, enforcing final-sale rules, and routing out-of-scope requests instead of calling tools it shouldn't.
- **The whole pipeline lives in Foundry.** A "Create dataset" button under Trace converts collected agent traces into an SFT dataset; you then launch a fine-tuning job on that dataset directly in the Fine-tuning tab — no separate data plumbing.
- **Distill what you already own.** The strategic message: stop treating frontier models as a luxury; use your existing production history and trajectories to embed cheaper, faster, smarter intelligence into your enterprise.

## 📚 Detailed Notes

### The motivation: intelligence as a utility, not a luxury
The session opens by reframing the goal of agent building. Six months ago the objective was to build the *fastest* agent. That goal now "looks a little different" because the real question is no longer *whether* your agent works — it's **whether you can afford to run it a hundred million times.** As AI moves from frontier labs into enterprise workflows, there is a pressing need for intelligence to become **dramatically cheaper**, so that intelligence behaves like a **utility** (always-on, affordable, embedded everywhere) rather than a **luxury** reserved for special cases.

William is from the **Azure AI Foundry fine-tuning team**. The promise of the session: learn everything needed to turn your **production agent traces** into **smaller models that run cheaper, faster, and smarter.**

### Why this matters now: agents are token-consumption machines
Enterprises are increasingly adopting **agentic AI**, and many teams already have agents in production today. The problem is that agents are **inherently token-consumption machines** — they consume far more tokens than a plain chatbot because of all the **tools, context, and memories** fed into them. Each of those inflates the per-request token cost, and at enterprise scale (millions of calls) that cost becomes the dominant constraint.

### What model distillation is (the apprenticeship analogy)
**Model distillation is like an apprenticeship between two AI models:**
- You start with a **large, capable model = the teacher** that solves real tasks well.
- You **collect many examples** of how the teacher behaves *in the real environment*.
- You use that data to **train (fine-tune) a smaller, cheaper model = the student** so it imitates the teacher's behaviour.
- After training, the **student handles the task at a fraction of the cost.**

This is positioned as the enterprise's **"secret weapon"**: turning frontier models into something **tailored for your business** at a fraction of the cost.

### Why learn from agent traces specifically
Agent traces are described as a **unique, emerging field** in agent building — extremely informative yet **not fully utilised** today. The reasons traces are the right training signal:

- **They are real conversations.** Traces capture the **messy, off-script questions** users *actually* ask — not the idealised inputs you imagine when designing the agent.
- **Tool use is included in the trace.** The student learns not just *what to say* but **which tools to call, in what order, with what argument values.** That is what makes an agent genuinely useful instead of "just a chatty chatbot."
- **They teach the right trajectory.** Analogy: in school, getting the right answer with the wrong method doesn't earn full marks. Likewise, an agent can reach a correct outcome via an incorrect path. Distillation aims to teach models to solve problems with the **correct trajectory** — the real order of tools and the real argument values the agent should fill when calling them.
- **They're easy (and free) to collect on Foundry.** If you build agents on Foundry, the platform already provides all the tooling to collect traces — they "come free to you at no [cost]."
- **They grow automatically.** Trace collection runs **in the background**, so your agent gets **smarter the more you and your users interact with it.**
- **They're more trustworthy than synthetic data.** Rather than training on synthetic data or data you *think* represents the real world, traces are **real signal** from actual usage — obtained at no additional cost just by running your agent on Foundry.

### The four wins from distillation
1. **Dramatically reduced cost** — you end up running very small models, sometimes small enough to **fit on devices**.
2. **Faster responses** — smaller models are quicker.
3. **Teacher-level quality on the narrow task** — when fine-tuned on real-world traces, the student can **closely mimic teacher quality**, with a **substantial performance lift** on the specific task it was trained for, **sometimes even outperforming the teacher** on some tasks.
4. **More consistent behaviour** — achieved specifically through **supervised fine-tuning (SFT)**, which is the technique demonstrated in this session.

### The end-to-end pipeline demonstrated today
The demo follows this sequence (a compressed, simulated stand-in for what would normally happen continuously in production):
1. **Pick hard tasks** — tasks so difficult that small base models (e.g. GPT-4.1 nano) can't handle them alone.
2. **Simulate conversations** between the **teacher model** and these tasks to **generate traces** (mimicking what a deployed agent would accumulate naturally over time; simulated here only to fit the session's time budget).
3. **Clean the traces** and use them to **fine-tune the student.**
4. **Evaluate** the result to see the benefit.

### Model choices and the task set
- **Student model:** GPT-4.1 nano — "very cheap, very fast, very nice to use." (William refers to it loosely as "4 nano" / "490" / "190" — all the GPT-4.1 nano student.)
- **Teacher model:** GPT-5.5 — the expensive frontier model many teams run in production ("breaking your budget a lot of the time").

The evaluation uses **100 tasks**, written to be **very challenging for base models**:
- **Split:** 80 tasks for **training**, 20 held out as a **holdout** test set (to verify generalisation, not memorisation).
- **Labelling per task:** each task has a **category** (e.g. a *late delivery* interaction) and a **tagged expected solution.**
- **Example task:** customer **Noah**, a **platinum-tier** customer who bought a **smartwatch**, wants a **refund** and believes he's also owed a **late-delivery credit**. Context: delivered ~50 days ago → check the policy → determine refund and/or credit eligibility. There are 100 such tasks simulating real production scenarios.

### Watching a live teacher conversation (the latency problem)
William runs one conversation live against the deployed GPT-5.5 agent. The key observation: because the agent has **so many tools, contexts, and policy points baked in**, it takes a **long time** — it has to go through the database, retrieve everything, synthesize results, and call tools again just to answer one question. He likens it to coding agents that "think" for so long you "go to bed and maybe next morning something comes out of it." This latency-and-cost pain is exactly what distillation is meant to fix.

### Designing the evaluation
**"Evaluation is the key."** You must understand how something performs before you can improve it. You are **free to design the evaluation however you want**; William chose **four scoring dimensions**, applied to **full multi-turn conversations**:
1. **Decision correctness** — is the agent calling the right tools / making the right decisions?
2. **Tool trajectory** — are the tool calls in the **right order**?
3. **Financial accuracy** — are the monetary calculations (refunds, credits, fees) correct?
4. **Communication** — does the agent say the right things? (e.g. include a **specific keyword** when denying or accepting a request.)

Each conversation is scored against these criteria; a baseline example checks that all tool calls are expected and in the right order, financial calculations are correct, and communication is correct.

### The pass@k metric
**pass@k** answers: *if you try k times, how many times do you succeed* (i.e. score above an acceptable threshold)? To measure **consistency** (not a single lucky run), William runs **each model — teacher, base student, fine-tuned student — three times per task** and collects summary statistics. Example interpretation: maybe you succeed 1/3, 2/3, or 3/3 times. This pass@k summary is the headline metric for the session.

### The headline result
The chart (hard to read on screen, but described) shows:
- A **very large gap** between the **base student (GPT-4.1 nano)** and the **teacher (GPT-5.5)** — two models very different in size perform very differently in capability.
- After **fine-tuning**, the **student's performance lifts a lot**, **sometimes matching the teacher.**
- The **holdout** results confirm the model isn't just **memorising** but is genuinely **imitating the teacher's reasoning capability.**
- The fine-tuned nano **recovers more than half of the available headroom** between base and teacher.

### Doing it in Foundry: from traces to a fine-tuning job
William switches to **Azure AI Foundry** to show the real workflow:
- He has an **agent already running** in Foundry and pastes in **Noah's** message (reusing the earlier simulated example).
- The **GPT-5.5 agent** again takes noticeable time — thinking, scanning all data, going over all contexts — then responds. At scale, many customers doing this produces **traces.**
- **What a trace is:** "a collection of everything that happens inside a request" — for each conversation turn: **all tool calls, all reading steps, all data flows** — captured and **visualised** for you.
- Because **Foundry collects traces automatically**, after running an agent for a while you accumulate the **full set of real customer conversations.**

**Converting traces → SFT dataset → fine-tuning job (the click-path):**
1. Under **Trace**, click **"Create dataset"** and choose **Supervised fine-tuning**. Foundry **automatically collects all traces** from a chosen time range (in the demo, ~**1,000+** traces).
2. **Name the dataset** (he names it **"Hi build" / "High bill"** — caption-garbled).
3. Go to the **Fine-tuning** tab and select **Supervised fine-tuning** for the model.
4. The newly created dataset appears as the **training data source** automatically.
5. **Submit the job** — it goes into the **queue.**

That's the whole loop: **pour agent traces into an SFT dataset and start a fine-tuning run entirely inside Foundry.**

### Real-world results — four failure modes fixed by fine-tuning
To show benchmark gains translate into real value, William compares the **base GPT-4.1 nano** against his **fine-tuned version** (trained on the teacher's traces) on concrete cases:

**1. Restocking-fee math (refusing manipulation).**
Customer **Diego** bought a **mechanical keyboard**, dislikes the keys, and argues it's a **defect** so he shouldn't pay a restocking fee. He is **standard tier**, so the **15% restocking fee applies** — the correct refund *includes* the fee. The **base nano gets manipulated:** "since you told me it's a defect… I guess it's a defect," and it **refunds the customer** (goes "into your bank account"). The **teacher (GPT-5.5) correctly rejects** this and can't be convinced so easily. The **fine-tuned nano** now makes all the right tool calls and **correctly applies the restocking fee**, recognising that "I don't like it" ≠ "it's a defect." Scaled across many orders, this **saves the company a lot of false refunds.**

**2. Right outcome, wrong method (skipping the policy check).**
Customer **Liam** wants to cancel an **unshipped order with two items**, both still processing — correct outcome is **cancel both and refund.** The agent is *supposed* to **check the refund/business-logic policy before submitting a resolution.** The **base nano skips that:** it gets order detail + fulfillment status, sees "unshipped," and **jumps straight to submitting a resolution.** No money leaves the account in this case (so evaluation might not flag it), but it's an **inherent risk** — the agent is **acting out of trajectory** relative to your business logic. The **fine-tuned nano** mimics the teacher **step-by-step**: check fulfillment status → confirm not shipped → **check the resolution policy** (calling the tool with the correct argument: reason = *change of mind*) → confirm applicability → calculate the resolution → refund → submit. Same right answer, but now with **confidence that the agent did the right thing in the right order.**

**3. Final-sale defect claim (enforcing policy under pressure).**
A customer bought a **water bottle**, a **final-sale item**, and complains it's **"not as advertised"** (doesn't keep water cold as marketed), arguing that makes it a **defect** deserving a refund despite final-sale rules. The **base nano caves:** it **issues a store credit**, deeming the item defective. The **fine-tuned nano** holds the line: gets order detail + fulfillment status, then says (in effect) "I understand you claim it differs from advertisement, but I **don't consider it a defect**; unless you can **show** it's a defect, **no refund**." This **improves consistency** of agent behaviour against unexpected real-world customer arguments.

**4. Out-of-scope request (correct routing instead of acting).**
The agent is designed for **post-order support**, but a customer asks it to do something **out of scope** — **place a new order.** The agent should **do nothing** (recognise the intent and **route it separately** per business policy). The **base nano tries anyway** — it even calls the **check-inventory tool** when it **shouldn't.** After fine-tuning, the model **correctly recognises the out-of-scope intent and routes** instead of calling tools it isn't supposed to.

### Closing message
The work's purpose is to motivate the idea that **intelligence should be embedded into your enterprise/organisation** rather than treated as a **luxury commodity** via always reaching for frontier models. The path: **use what you already own** — your **agent traces, production history, and trajectories** — to **optimise cost/performance** by **distilling agents, models, and traces into smaller models** that run **faster, cheaper, and smarter** for your organisation.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure AI Foundry** — the platform hosting the agents, automatic trace collection, dataset creation, and fine-tuning jobs; the entire distillation loop runs here.
- **Foundry agents** — agents built and run in Foundry (the deployed GPT-5.5 customer-support agent in the demo).
- **Agent traces / Tracing** — automatically captured record of everything inside each request: tool calls, reading steps, data flows, full multi-turn conversations; visualised in Foundry.
- **"Create dataset" (under Trace)** — one-click conversion of collected traces into a **Supervised fine-tuning** dataset for a chosen time range.
- **Supervised Fine-Tuning (SFT)** — the fine-tuning technique demonstrated; yields more consistent behaviour by training the student on teacher trajectories.
- **Fine-tuning tab (Foundry)** — where you select SFT, pick the trace-derived dataset as training source, and submit/queue the job.
- **GPT-5.5** — the **teacher** model (large, frontier, expensive) running the production agent.
- **GPT-4.1 nano** — the **student** model (very small, cheap, fast); the base vs. fine-tuned versions are compared throughout (spoken variously as "4.1 nano," "4 nano," "490," "190").
- **pass@k** — evaluation metric measuring success rate / consistency across k attempts (each model run 3× per task).
- **Holdout set** — 20 of 100 tasks reserved to verify generalisation (imitation) rather than memorisation.

## 🚀 Announcements / What's New
None explicitly announced. This is a demo/how-to session showing existing Azure AI Foundry capabilities (automatic agent tracing, trace-to-dataset creation, and supervised fine-tuning) rather than new product launches or previews. No GA/preview status was stated for any feature.

## 💡 Demos
- **Live teacher conversation (latency demo):** Ran a single task live against the deployed **GPT-5.5** agent to show how long a heavily-tooled, policy-laden frontier agent takes to retrieve data, synthesize, and call tools for **one** answer — making the cost/latency problem tangible.
- **Evaluation walkthrough:** Showed scoring a full multi-turn conversation across the **four dimensions** (decision correctness, tool trajectory, financial accuracy, communication), then aggregating across all 100 tasks into a **pass@k** summary comparing teacher vs. base student vs. fine-tuned student (3 runs each).
- **Results chart:** Visualised the large base-student↔teacher gap and the substantial lift after fine-tuning (sometimes matching the teacher; holdout confirming real imitation).
- **Foundry trace-to-fine-tune (the money demo):** In Foundry, pasted Noah's message into a running agent, watched the trace get captured/visualised, then used **Create dataset → Supervised fine-tuning** to pull ~1,000+ traces into a dataset ("Hi build"), selected it in the **Fine-tuning** tab, and **submitted/queued an SFT job** — all in-product.
- **Four failure-mode comparisons (base vs. fine-tuned nano):** (1) Diego/restocking-fee manipulation, (2) Liam/skipped policy check, (3) water-bottle final-sale defect claim, (4) out-of-scope "place a new order" request — each showing the base nano failing and the fine-tuned nano matching the teacher's correct behaviour.

## 📊 Notable Stats / Quotes
- **"The question is not just whether my agent works, it is about whether I can afford to run my agent a hundred million times."** — the framing for the whole session.
- **Intelligence should be "a utility rather than a luxury."** (Repeated as the closing thesis: don't treat frontier models as a luxury commodity.)
- **Model distillation = "an apprenticeship between two AI models"** — teacher solves real tasks, student imitates at a fraction of the cost.
- **"Evaluation is the key. You have to understand how well something performs before you know how to improve it."**
- **100 tasks** total → **80 train / 20 holdout**; each model run **3×** per task for pass@k.
- **~1,000+ traces** auto-collected in the Foundry demo for the fine-tuning dataset.
- Fine-tuned **GPT-4.1 nano** **"recovered more than half of the headroom"** to the teacher, **sometimes matching GPT-5.5** on the narrow task.
- **Four wins:** lower cost (sometimes on-device) · faster responses · teacher-level (sometimes teacher-beating) quality on the narrow task · more consistent behaviour.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up a small Foundry agent, run it enough to accumulate real traces, then use **Create dataset → Supervised fine-tuning** to distill a **GPT-4.1 nano** student from a **GPT-5.5** teacher and compare cost/latency.
  - Build a **pass@k** harness (run each candidate model ~3× per task) with a multi-dimensional rubric (decision correctness · tool trajectory · financial accuracy · communication) before and after fine-tuning.
  - Always reserve a **holdout split** (here 20/100) to confirm the student is *imitating reasoning*, not memorising.
  - Reproduce the four failure-mode tests (manipulation resistance, policy-check-before-action, final-sale enforcement, out-of-scope routing) as regression evals for any distilled support agent.
- [ ] Questions:
  - What are the actual **cost-per-1k-tokens** and **latency** deltas between fine-tuned GPT-4.1 nano and GPT-5.5 for this agent? (Not quantified in the talk.)
  - How many traces / training examples are needed before the lift plateaus? (Demo used ~1,000+ traces, 80 training tasks.)
  - Does Foundry's trace→dataset step handle **PII redaction / data governance** automatically, and how is sensitive customer data treated in SFT?
  - When does the fine-tuned student actually **outperform** the teacher vs. merely match it — and how brittle is that outside the narrow task?
  - Pricing/quota and supported base models for SFT in Foundry — which student models are eligible?
- [ ] Relevant to:
  - Cost optimisation for any production **agentic** workload where a frontier model is called at high volume.
  - Customer-support / refund-policy agents where **correct trajectory and policy enforcement** (not just the final answer) matter.
  - Teams already on **Azure AI Foundry** wanting to exploit automatically-collected traces as a free, self-improving training signal.

## 🔗 Related
- [[Azure AI Foundry]]
- [[Fine-tuning]]
- [[Model distillation]]
- [[Supervised fine-tuning (SFT)]]
- [[Agent traces]]
- [[Agentic AI]]
- [[Microsoft Build 2026]]