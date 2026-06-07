---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-foundry
  - topic/production
  - topic/agents
  - topic/open-source-models
  - topic/inference
  - topic/evaluations
source: https://www.youtube.com/watch?v=KLmRDETMCog
session_code: DEMSP383
event: Microsoft Build 2026
speakers: Vignesh (Applied AI, Fireworks AI)
duration_min: 15
aliases:
  - Move AI workflows from test to production on Microsoft Foundry
---

# DEMSP383 — Move AI workflows from test to production on Microsoft Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Vignesh — Applied AI team, Fireworks AI  
> **Duration:** ~15 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=KLmRDETMCog)

## 🎯 TL;DR
A partner demo from **Fireworks AI** showing how to take **open-source models** from initial testing all the way to **production-grade inference** on **Microsoft Foundry**. Fireworks AI provides high-performance, day-zero inference for open models (Kimi, GLM, MiniMax, etc.) via a first-party Azure integration, with workload-aware optimization, their own **Fire Attention** inference engine, adaptive caching, and quantization. The walkthrough demonstrates the full lifecycle inside Foundry: discovering Fireworks models, choosing deployment types (multi-tenant serverless → single-tenant provisioned throughput / PTUs), testing in the playground, A/B comparing two models side-by-side, saving the winner as an agent, running custom + benchmark **evaluations** against the full agent harness, iterating on versions, and finally publishing as a web app or pulling code snippets into Python workflows. For cases where out-of-the-box quality isn't enough, you can **bring your own weights** after post-training (SFT/RFT) and serve them through the Fireworks serving stack.

## 🔑 Key Takeaways
- **Fireworks AI** is a high-performance inference platform for **open-source models**, with a founding team from **PyTorch @ Meta** and **Vortex @ GCP**.
- Scale claims: **~13 trillion tokens/day** and **180,000 requests/second** served.
- **Day-zero support** for nearly all major open-source model providers (Kimi → GLM 5.1 and beyond) — they enable new models on launch day.
- Available as a **first-party Azure integration** on Microsoft Foundry; bill via your **MACC (Azure consumption commitment)** or build directly through Azure.
- The **Fireworks serving stack** does workload-aware optimization: adaptive caching, quantization, a proprietary inference engine called **Fire Attention**, and right-sized hardware selection for low latency or high throughput.
- Foundry exposes Fireworks models as **multi-tenant serverless endpoints** (infra already provisioned) — ideal for cheap experimentation and running evals.
- **Data Zone Standard** = multi-tenant serverless (shared endpoint, set TPM rate limits per account) for testing, not heavy production load.
- **Global / Data Zone Provisioned Throughput** = single-tenant dedicated deployment for production, sized via a **PTU calculator**.
- PTU example: 80,000 input tokens + 500 output tokens at 300–3,000 RPM → calculated **61,500 PTUs** needed (max scale shown ~1,160 in the UI demo).
- The **Playground** lets you chat with a deployed model and **compare two models side-by-side** (same prompt, simultaneous outputs) to weigh latency vs. quality vs. token count.
- **Save as Agent** turns a chosen model + system prompt + tools into a reusable agent inside Foundry.
- **Evaluations** run against the **entire agent harness** (system prompt + tool calls), not just the raw model — using custom datasets, open-source benchmarks, or synthetic data.
- Eval setup: pick metrics (intent resolution, coherence, fluency, relevance, groundedness), choose a **judge model** (demo used **GPT-4 mini**), use ground-truth data, and run across all rows (demo: 50-row code-review eval dataset).
- Iterate the agent harness across versions, re-run evals until metrics hit your benchmark (demo showed **90% task completion**), then promote to production.
- **Publishing options**: Foundry web app preview (front-end) OR a **Call Agent** tab with code snippets + project endpoint/API key to embed in external **Python** workflows.
- **Bring Your Own Weights (BYOW)**: post-train with any framework (or Fireworks' native **SFT/RFT**), register the custom model in Foundry, create a deployment, and route inference through the Fireworks stack.

## 📚 Detailed Notes

### Who Fireworks AI is
Fireworks AI positions itself as **high-performance open-source inference for open-source models**. The team has deep systems pedigree — founders came from the **PyTorch team at Meta** and from **Vortex at GCP**. Their differentiation is serving open models fast and at scale, with **day-zero support** for almost every major open-source model provider as new models drop (examples cited span from **Kimi** through **GLM 5.1**). Operating scale was given as **~13 trillion tokens per day** and **180,000 requests per second**.

### The Fireworks serving stack (how the speed happens)
The serving stack performs **workload-aware optimization** per model. The flow: once you find an open-source model that meets your evaluation bar, Fireworks "tunes different knobs" to optimize it for your specific workload. Components mentioned:
- **Adaptive caching** to reduce repeated compute.
- **Quantization** of the model to shrink/accelerate it.
- A proprietary inference engine called **Fire Attention** (their own serving stack).
- **Right-sized hardware selection** — choosing the correct hardware setup to hit either high throughput or ultra-low latency for the target workload.

The result is abstracted away and handed back to the customer as a **production-ready endpoint** they can use immediately.

### How Fireworks operates on Microsoft Foundry
Key properties of the Foundry integration:
- Access to **state-of-the-art open models on day zero** inside Foundry; new models are enabled as they roll out.
- **Optimized inference** tuned for specific workloads (as above).
- **Enterprise scale** — scale up without breaking the workflow.
- **First-party Azure integration** — bill via **MACC** or build via Azure directly.
- **Bring your own custom models / weights** after fine-tuning and upload to Foundry for serving.

**Post-training / BYOW workflow:** finish post-training your weights → **register the custom model** in Microsoft Foundry → **create a deployment** → inference requests get **routed through the Fireworks serving stack** → you get optimized inference on your own custom weights.

### Common use cases
Patterns Fireworks sees across customers:
- **Code completion**
- **Code review bots**
- **Customized chatbots**
- **Transcription and summarization**
- **A/B testing across open-source models** — start by comparing models, pick the best, build an agent, and serve it via Foundry endpoints.

### Walkthrough Step 1 — Discover Fireworks models in Foundry
From the Foundry landing page → **Discover** → **Models** page, which lists all providers and the large catalog of available models. Searching **"Fireworks"** surfaces all the **multi-tenant models that are already enabled** — meaning the infrastructure is already provisioned and ready to use. The demo selects a **Kimi K2.6** model to test for a use case, clicking through to **Deploy**.

### Walkthrough Step 2 — Deployment types
Two broad deployment paths were explained:

**Data Zone Standard (multi-tenant serverless):**
- A shared, serverless endpoint to start testing (e.g., Kimi K2.6).
- Set **tokens-per-minute (TPM) rate limits** across different accounts to manage consumption per user.
- One common endpoint shared across multiple users — good for running **evals** and experimentation, **not** for a massive production workload.

**Global / Data Zone Provisioned Throughput (single-tenant, dedicated):**
- Used once benchmarks/evals look good and you want a dedicated, single-tenant deployment for production.
- Surfaces a **PTU (Provisioned Throughput Unit) calculator**.
- **Worked example:** input token size **80,000**, output **500 tokens**, **300 → 3,000 requests per minute** → calculator returns **61,500 PTUs** required. The UI's max scale at demo time was ~**1,160**, so the workload must fit within the PTU calculation before clicking **Deploy**, which provisions a single-tenant deployment.

### Walkthrough Step 3 — Test in the Playground
Before committing to a dedicated deployment, validate model performance for your use case. The demo switches to already-deployed models — a **Kimi 2.5** and a **MiniMax** model — and opens the **Playground** to chat. Example task: a **code review agent** asked to catch **SQL injection issues** and **hard-coded secrets**. Observations: **very low latency** and a high-quality response out of the box.

### Walkthrough Step 4 — Compare two models head-to-head
The Playground supports **pitting two models against each other**. The demo compares the **MiniMax** model with a **Kimi 2.6** model via the **Compare models** UI: the same input is sent and outputs generate **simultaneously**. Findings in the demo:
- **MiniMax** had little traffic → answered very quickly.
- **Kimi** produced a **more detailed, "thinking"-heavy answer** with multiple deployment-to-production options.
- The choice depends on how you weight **latency vs. quality vs. tokens generated**. You then pick a model and click **Save as Agent** (either the MiniMax or the Kimi model).

### Walkthrough Step 5 — Run evaluations against the agent harness
With a saved agent (e.g., the code-review agent), run **evaluations** via the Playground's **metrics configurator**:
- Use agents already configured in Foundry with **your own custom evaluation datasets**.
- Demo target: a **50-row** dataset, evaluating **intent resolution, coherence, fluency, relevance**.
- Critically, evaluate the **entire agent harness** — not just the model — because it may include **multiple tool calls** and a **detailed system prompt**. Pick the agent → **Next**.
- Choose dataset source: **existing dataset** vs. **synthetic generation** (demo used an uploaded **code-review eval dataset**, 50 rows, with a **ground-truth** column for comparison).
- Optionally run against **pre-uploaded open-source benchmarks** for basic coding agents.
- **Automated field mapping** is provided.
- **Judge model:** demo used **GPT-4 mini** as the LLM judge.
- A set of **auto-suggested criteria** appears; you can narrow to a subset (e.g., **relevance, groundedness, coherence**) → name it → **Submit**.
- The full evaluation suite runs against all rows, producing **percentage scores per metric**.

### Walkthrough Step 6 — Read results and iterate
The demo showed a **pre-existing completed run** for the code-review agent with **task completion at 90%**. If metrics fall short, **tweak the harness**, create **multiple iterations/versions** of the agent, and **re-run** the eval metrics until it hits the benchmark and is ready to push to production.

### Walkthrough Step 7 — Publish to production
Once satisfied, several publishing paths exist:
- **Web app preview** — see how the agent looks on the front end if publishing through Foundry; it's the same agent without the playground, and you can test prompts there.
- **Call Agent tab** — get **code snippets** to use the agent as a workflow in code; use the **project endpoint** with your account's **API key** and incorporate it into **Python workflows outside the Foundry UI**.

This closes the loop: test → compare models → save as agent → evaluate → iterate → publish (web UI or code snippet → Python).

### Walkthrough Step 8 — Bring Your Own Weights (when OOTB isn't enough)
If out-of-the-box open-source quality is insufficient, move to a **post-training** workflow:
- Take the **base model as-is**.
- Fine-tune with **any framework** (outside Foundry or on Foundry); the **Fireworks AI native platform** also supports fine-tuning via its **SFT** (supervised fine-tuning) or **RFT** (reinforcement fine-tuning) frameworks.
- **Upload the tuned weights** and run them through the **same serve workflow** to get optimized inference on the Fireworks tech stack.

### Closing
Vignesh framed the whole flow as an **intuitive, easy, end-to-end** way to adopt open-source models on Foundry. The session ended with an MC thanking the presenter and noting another session was starting immediately afterward (attendees asked to stay seated).

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — host platform for model discovery, deployment, playground, evals, and publishing.
- **Fireworks AI** — high-performance open-source inference partner (first-party Azure integration).
- **Fire Attention** — Fireworks' proprietary inference engine within their serving stack.
- **Fireworks serving stack** — workload-aware optimization, adaptive caching, quantization, hardware right-sizing.
- **Open-source models referenced:** Kimi K2.6, Kimi 2.5, MiniMax, GLM 5.1.
- **Deployment types:** Data Zone Standard (multi-tenant serverless), Global Provisioned Throughput, Data Zone Provisioned Throughput (single-tenant).
- **PTU (Provisioned Throughput Units)** + **PTU calculator**.
- **Foundry Playground** — chat, model comparison, metrics configurator.
- **Save as Agent** — package model + prompt + tools as a reusable agent.
- **Evaluations** — custom datasets, open-source benchmarks, synthetic generation, automated field mapping, LLM-as-judge.
- **GPT-4 mini** — used as the eval **judge model**.
- **Eval metrics:** intent resolution, coherence, fluency, relevance, groundedness, task completion.
- **Publishing:** Web app preview, Call Agent tab (code snippets, project endpoint + API key, Python).
- **Fine-tuning:** Fireworks native **SFT** and **RFT** frameworks; Bring Your Own Weights (BYOW).
- **MACC** (Microsoft Azure Consumption Commitment) — billing path.
- **Founding-team lineage:** PyTorch @ Meta, Vortex @ GCP.

## 🚀 Announcements / What's New
- **None explicitly announced as new GA/preview.** This was a **partner demo (DEMSP)** showcasing Fireworks AI's existing capabilities on Microsoft Foundry rather than launching a product. The Foundry integration, multi-tenant serverless endpoints, provisioned-throughput deployments, in-Foundry evaluations, agent publishing, and BYOW are presented as currently available functionality. GA-vs-preview status of individual features was not stated in the session.

## 💡 Demos
A single continuous, end-to-end live demo inside the Microsoft Foundry UI:
1. **Discover** Fireworks models (search "Fireworks" → multi-tenant models already enabled) and select **Kimi K2.6**.
2. Walk through **deployment options**: Data Zone Standard (serverless, TPM limits) vs. Provisioned Throughput with the **PTU calculator** (80k input / 500 output / 300–3,000 RPM → **61,500 PTUs**).
3. **Playground test** of a **code-review agent** on a MiniMax model — catching **SQL injection** + **hard-coded secrets** with low latency.
4. **Side-by-side comparison** MiniMax vs. Kimi 2.6 on the same prompt (MiniMax faster, Kimi more detailed/"thinking").
5. **Save as Agent** from the chosen model.
6. **Run evaluations** via the metrics configurator — 50-row code-review dataset, ground truth, **GPT-4 mini** judge, metrics including relevance/groundedness/coherence, against the **full agent harness**.
7. **Review a completed eval run** showing **90% task completion**, with guidance to iterate versions until benchmarks pass.
8. **Publish** — web app preview and the **Call Agent** code snippet for **Python** workflows.
9. Mentioned **BYOW** post-training path (SFT/RFT) to upload custom weights through the same serve flow.

## 📊 Notable Stats / Quotes
- **~13 trillion tokens/day** served by Fireworks AI.
- **180,000 requests/second** served.
- **Day-zero** model enablement for major open-source providers.
- PTU worked example: **80,000 input tokens**, **500 output tokens**, **300–3,000 RPM** → **61,500 PTUs** required (UI max scale ~**1,160** at demo time).
- Eval dataset: **50 rows**; demo eval run hit **90% task completion**.
- Founding team from **PyTorch @ Meta** and **Vortex @ GCP**.
- Presentation framed as a **~5-minute** intro deck followed by the live Foundry demo.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Search "Fireworks" in Foundry → Discover → Models and deploy a **Kimi K2.6** or **MiniMax** model on a **Data Zone Standard** serverless endpoint for cheap eval runs.
  - Build a small **code-review agent** and use the **Compare models** UI to weigh latency vs. quality (MiniMax vs. Kimi).
  - Stand up a **50-row eval dataset** with ground truth and run a full-harness eval using **GPT-4 mini** as judge; check intent resolution / groundedness / coherence.
  - Use the **PTU calculator** with realistic token + RPM numbers to size a production single-tenant deployment.
  - Try the **Call Agent** code snippet path to embed a Foundry agent into an external **Python** workflow.
- [ ] Questions:
  - What is the actual GA vs. preview status of Fireworks provisioned-throughput deployments and in-Foundry evals?
  - How does Fireworks PTU pricing compare to first-party Azure OpenAI PTUs for equivalent throughput?
  - Does BYOW (custom weights) work with **Global Provisioned Throughput**, or only specific deployment types?
  - What governance/observability (logging, monitoring, drift) ships for production Fireworks endpoints on Foundry?
- [ ] Relevant to:
  - Teams standardizing on **open-source models** but needing enterprise-grade, low-latency serving on Azure.
  - Anyone building an **eval-driven path to production** for agents (test → compare → eval → iterate → publish).
  - Cost/capacity planning for **provisioned throughput** vs. serverless on Foundry.

## 🔗 Related
- [[DEM320 - Hugging Face open-source models to production on Foundry]]
- [[BRKSP91 - Turn foundation models into production AI on Foundry]]
- [[BRK241 - From prototype to production build and run agents at scale]]
- [[BRK231 - Deploy Observe Learn Reinforcement learning for production agents]]
- [[BRK230 - Build smarter AI systems in Foundry as models and costs evolve]]
- [[DEM361 - Understand and fix Agent Framework apps with observability and evals]]
- Source list: [[2026 Build Session List]]
