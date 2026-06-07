---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
source: https://www.youtube.com/watch?v=ynxh3ujRIKk
session_code: SEG01
event: Microsoft Build 2026
speakers: Microsoft (product segment)
duration_min: 5
aliases:
  - Frontier Tuning
---

# SEG01 — Frontier Tuning

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Microsoft product segment (presenter unnamed; hands back to Satya at the end)  
> **Duration:** ~5 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ynxh3ujRIKk)

## 🎯 TL;DR
Frontier Tuning lets enterprises create their *own* enterprise AI by tuning both the model and the surrounding "harness" on their own data and workflows. The presenter demos fine-tuning via reinforcement learning (RL) in Foundry — uploading a dataset, adding a grader, and watching the model "hill climb" to higher accuracy through rollouts and scoring — and reveals a low-level training API for full control over the RL loop. The headline customer story is Land O'Lakes (a major US agribusiness), whose complex "butter report generation" workflow is codified into an RL environment of skills, knowledge, and tools, pushing accuracy past 90% with a model estimated to be 10x more efficient than baseline. The big idea: your agent continuously improves inside a compliant RL environment that encodes the way *you* work — "frontier tuning as smooth as butter."

## 🔑 Key Takeaways
- **Frontier Tuning = tune the model *and* the harness** on your own enterprise data and workflows to build a bespoke "hill climbing machine."
- A new model, **"M AI Thinking 1"** (caption-uncertain name), is in **private preview in the Foundry Model Catalog** — deployable as-is or fine-tunable.
- Fine-tuning flow is deliberately simple in the UI: **add dataset → add grader → submit job**; within a couple of hours you can watch the model generate rollouts, score them, and hill climb.
- A **low-level training API** gives full control over the RL loop: choose the model, configure rollout strategy + hyperparameters, and bring your own **RL gym** by defining the tools the model interacts with.
- For **M365 customers, you're "never starting from scratch"** — Copilot can build **RL environments from your existing data and workflows**.
- An RL environment = **skills + knowledge + tools**, backed by a full **RL gym** where agents continuously learn how you work.
- Microsoft is **extending the industry definition of "skills" to include rubrics** ("what good looks like") because for precision-heavy tasks even **80% accuracy isn't good enough**.
- Skills and rubrics can be **auto-suggested from M365 signals** (Teams, Outlook, Word, Excel, PowerPoint) to codify how you work at scale.
- **Grounding knowledge** can be pulled from OneDrive / SharePoint; environments ship with **built-in Microsoft tools** plus support for **custom tools**.
- Tools are **virtualized to simulate execution**, so the model can learn from real workflows **without impacting live business state**.
- Generalizing learnings into both the **main model and the embedding model** drove Land O'Lakes tasks to **>90% accuracy** with an estimated **10x efficiency** vs baseline.
- At inference, the tuned environment acts as an **inferencing harness**; the agent uses **test-time pre-search across multiple models** (including a fine-tuned one) and **continuously retrospects and self-evaluates**.

## 📚 Detailed Notes

### What Frontier Tuning is
Frontier Tuning is positioned as a way to **create your own enterprise AI**, where *both* the model and the surrounding harness are tuned on **your data and your workflows**. The framing metaphor throughout is building your own **"hill climbing machine"** — i.e., an RL-driven system that iteratively improves toward higher accuracy.

### The model: M AI Thinking 1 in Foundry
- A thinking model — captioned **"M AI Thinking 1"** (name caption-uncertain; likely a Microsoft "MAI"-family model) — is **now available in private preview** in the **Foundry Model Catalog**.
- Two paths: **deploy as-is**, or click **fine-tune** to start your own "hill climbing journey."

### Fine-tuning in the UI (RL workflow)
- In the fine-tuning UI: first **add the dataset**, then **add a grader**, then **submit the job** — presented as that simple ("and that's it").
- **A couple of hours in**, you can observe learning: the model **generates rollouts**, **scores them**, and begins to **hill climb** (the RL improvement loop).

### Low-level training API (full control)
For teams wanting full control over the RL training loop, there's a **sneak peek at a low-level training API**:
- Select the model (the **M AI Thinking** model shown).
- **Configure rollout strategy** and **hyperparameters** to define exactly how the training algorithm works.
- **Incorporate your own RL gym** by **defining the tools** the model interacts with.

### From code to M365: building RL environments from your work
Pivoting from raw code, the presenter notes **M365 customers never start from scratch** and switches to **Copilot**. As part of Frontier Tuning, Microsoft introduces a **new way to build RL environments based on your data and workflows**.

**Customer: Land O'Lakes** — described as one of the largest agribusinesses in the US — is using this to "perfect that butter on your morning toast." Their environment is walked through as the running example.

### Anatomy of an RL environment
- **High level:** an environment consists of **skills, knowledge, and tools**.
- **Back end:** Microsoft creates an **entire RL gym** so agents **continuously learn the way you work**.

**Example skill — "butter report generation":**
- These tasks are **very complex**, with **many manual steps** and a **high degree of precision**.
- For such tasks, **even 80% accuracy isn't good enough**.
- To reach higher accuracy, Microsoft is **extending the industry definition of skills to include rubrics** — explicit definitions of **"what good looks like."**

### Scaling skills across the enterprise
To codify *all* enterprise tasks (not just one):
- Leverage the **time you spend in M365** — **Teams, Outlook, Word, Excel, PowerPoint** — using those **signals to suggest skills and rubrics** that define how you work.
- Add **organizational knowledge for grounding** from sources like **OneDrive** and **SharePoint**.
- Environments come **built in with Microsoft tools**, and you can **add custom tools**.

### Virtualized tools (safe learning)
Because these tools **tap into real workflows**, Microsoft **virtualizes them to simulate execution** — letting the model **learn without actually impacting the live state of the business**.

### "The science" — generalization + results
The presenter's "favorite part" is the science:
- Learnings are **generalized into both the main model and the embedding model**, helping clients on **high-accuracy tasks**.
- For **Land O'Lakes tasks**, they **hill climb to >90% accuracy** using the **"MEI" model** (caption-uncertain — possibly "MAI"; flagged).
- The model is **estimated to be 10x more efficient than baseline models**.

### Inference with the tuned environment
Back to butter reporting, now running the task **using the tuned environment as an inferencing harness**:
- The task **normally takes a couple of minutes**, so a **cached response** is shown.
- The agent **leveraged test-time pre-search with multiple models, including a fine-tuned model**.
- The resulting **summary doesn't feel generic — it feels "undoubtedly Land O'Lakes."**
- The task **holds itself to high standards** and **continuously retrospects and evaluates itself**.

**Closing:** With Frontier Tuning, your agent **continuously improves** within a **compliant RL environment** built **on your data**, encoding the way you work — "frontier tuning as smooth as butter." Microsoft is eager to see the environments customers build, then hands back to **Satya**.

## 🛠️ Products / Features / Technologies Mentioned
- **Frontier Tuning** — Microsoft's offering to build your own enterprise AI by RL-tuning the model + harness on your data and workflows.
- **M AI Thinking 1** *(caption-uncertain name; likely a Microsoft "MAI" thinking model)* — thinking model in private preview, deployable or fine-tunable.
- **Foundry Model Catalog** — where M AI Thinking 1 is available; entry point to deploy or fine-tune.
- **Fine-tuning UI** — add dataset + grader, submit RL job, watch rollouts/scoring/hill-climbing.
- **Grader** — scoring component added during fine-tuning to drive RL improvement.
- **Low-level training API** — full control over the RL loop: model, rollout strategy, hyperparameters, custom RL gym/tools.
- **RL gym / RL environment** — backend simulation where agents continuously learn your workflows; composed of skills, knowledge, tools.
- **Microsoft 365 Copilot** — surface used to build RL environments from M365 data/workflows.
- **Skills (with rubrics)** — extended skill definition including rubrics defining "what good looks like."
- **M365 apps as signal sources** — Teams, Outlook, Word, Excel, PowerPoint signals used to suggest skills/rubrics.
- **Knowledge grounding** — organizational knowledge from OneDrive / SharePoint.
- **Built-in + custom tools** — Microsoft tools shipped with the environment, plus customer-added tools.
- **Tool virtualization** — simulates tool execution so the model learns without affecting live business state.
- **Embedding model + main model generalization** — learnings generalized into both for high-accuracy tasks.
- **"MEI" model** *(caption-uncertain; possibly "MAI")* — the tuned model achieving >90% accuracy on Land O'Lakes tasks.
- **Inferencing harness** — the tuned environment used at inference time.
- **Test-time pre-search** — inference-time search across multiple models (incl. a fine-tuned model) used by the agent.

## 🚀 Announcements / What's New
- **M AI Thinking 1** *(name caption-uncertain)* — **now available in private preview** in the **Foundry Model Catalog**. *(Status: Private preview)*
- **Frontier Tuning** — introduced as a way to create enterprise AI by tuning model + harness on your data/workflows. *(Status: Introduced this segment; preview-stage)*
- **Low-level training API** — shown as a **"sneak peek"** for full RL-loop control. *(Status: Sneak peek / preview)*
- **New way to build RL environments in Copilot** — based on your M365 data and workflows. *(Status: Introduced as part of Frontier Tuning)*
- **Extended definition of "skills" to include rubrics** — expanding the industry definition. *(Status: Newly introduced concept)*

## 💡 Demos
- **Fine-tuning UI walkthrough** — Proved how simple the RL fine-tuning flow is (dataset → grader → submit) and showed real learning via rollouts + scoring + hill climbing within a couple of hours.
- **Low-level training API sneak peek** — Proved that advanced users get full control: configurable rollout strategy, hyperparameters, and a bring-your-own RL gym via tool definitions.
- **Land O'Lakes RL environment (butter report generation)** — Proved Frontier Tuning works on a real, complex, precision-heavy enterprise workflow; showed environment anatomy (skills/knowledge/tools), rubrics, M365 signal-driven skill suggestions, OneDrive/SharePoint grounding, and virtualized tools.
- **Tuned-environment inference (cached butter report)** — Proved the end result: a non-generic, "undoubtedly Land O'Lakes" summary produced via test-time pre-search across multiple models, with the agent self-retrospecting and self-evaluating to high standards.

## 📊 Notable Stats / Quotes
- **>90% accuracy** achieved on Land O'Lakes tasks with the tuned ("MEI"/MAI) model.
- **~10x more efficient** than baseline models (estimated).
- **"even 80% accuracy isn't good enough"** — on precision-heavy enterprise tasks.
- **"a couple of hours in"** — time to start seeing the model learn during fine-tuning.
- Land O'Lakes described as **"one amongst the largest agribusinesses in the United States."**
- **"a summary that doesn't feel generic… it feels undoubtedly Land O'Lakes."**
- **"frontier tuning as smooth as butter."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Find M AI Thinking 1 in the Foundry Model Catalog (private preview) and test the dataset → grader → submit RL fine-tuning flow.
- [ ] Things to try: Explore building an RL environment from M365 Copilot (skills + rubrics suggested from Teams/Outlook/Office signals) on a real internal workflow.
- [ ] Questions: What's the exact/official model name? ("M AI Thinking 1" / "MEI" are caption-garbled — confirm if these are MAI-family models.)
- [ ] Questions: How does the low-level training API expose rollout strategy + hyperparameters (SDK? config schema?), and how is the custom RL gym defined?
- [ ] Questions: What does "compliant RL environment" entail re: data residency/governance, and how is tool virtualization implemented to guarantee no live-state impact?
- [ ] Questions: How is "10x more efficient than baseline" measured (cost? tokens? latency?), and against which baseline?
- [ ] Relevant to: Foundry fine-tuning, M365 Copilot extensibility, enterprise agent accuracy/RL, internal high-precision workflow automation.

## 🔗 Related
- [[2026 Build Session List]]
