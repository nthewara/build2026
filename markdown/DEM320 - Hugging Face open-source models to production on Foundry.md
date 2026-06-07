---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/hugging-face
  - topic/open-source
  - topic/foundry
  - topic/ai
source: https://www.youtube.com/watch?v=5lB9Bk4KEF8
session_code: DEM320
event: Microsoft Build 2026
speakers: Vaidya (Microsoft Foundry team), Jeff (Hugging Face), OC Kadu (Microsoft Foundry PM)
duration_min: 26
aliases:
  - Hugging Face open-source models to production on Foundry
---

# DEM320 — Hugging Face open-source models to production on Microsoft Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Vaidya (Microsoft Foundry team), Jeff (Hugging Face), OC Kadu (PM, Microsoft Foundry)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=5lB9Bk4KEF8)

## 🎯 TL;DR
This session shows how to take open-source models all the way from the Hugging Face catalog into production on **Microsoft Foundry**, using the newly announced **Foundry Managed Compute** — a managed PaaS where you just pick the model and the GPU, and Foundry handles all the infrastructure, runtimes, GPU topology, patching, and maintenance. Foundry now hosts **11,000+ models**, **10,000+ of which come from Hugging Face**, curated and security-screened daily so trending models land in Foundry the same day they're published. The headline message: open models are now on par with frontier closed models, you can customize/own/version-control them, and (for the first time at Build) you can deploy them from Foundry, use them in the **Playground**, call them from **VS Code**, and wire them into **Foundry Agents** with tools like web search and agentic RAG — all under Foundry's enterprise security (RBAC, identities, private tenant, supply-chain guarantees).

## 🔑 Key Takeaways
- **Foundry Managed Compute** is a new managed Platform-as-a-Service for open-source and custom models: you pick the GPU, Foundry handles infrastructure, GPU topology, runtimes, patching, and maintenance — "pick the model parameters, then boom, deploy."
- It's part of the Foundry resource, so it shares the **same endpoint, same SDK, same authentication, and same billing construct** as the rest of Foundry — no separate plumbing.
- Foundry now offers **11,000+ models**, and **over 10,000 of them come from Hugging Face** — the result of a long-running Microsoft × Hugging Face partnership.
- Hugging Face and Microsoft **monitor trending/most-liked/most-downloaded models daily** (across providers like Nvidia) so new models become available in Foundry **the same day they land on the Hub** ("day-zero access").
- **Five reasons enterprises should use open models:** (1) baseline performance is on par with frontier closed models, (2) you can customize/fine-tune/post-train/distill them, (3) hosting the weights means you own the experience, (4) the open community makes them cheaper to run, (5) you can version-control them.
- The pipeline that gets a model into Foundry includes **curation, license screening (commercially permissible only), remote-code filtering, security scanning, and validated deployment** — only enterprise-ready models land in the catalog.
- With Managed Compute the **model weights are uploaded into Microsoft Foundry/Azure** (not pulled live from the Hugging Face Hub at runtime), giving full **supply-chain security and robustness**.
- A deployed Hugging Face model from the Foundry collection is guaranteed **not to make network calls outside your own secure tenant** — a key enterprise guarantee.
- **Deployment templates** pre-configure the right runtime + GPU config (e.g. single/dual H100s, single/dual A100s); H100 templates can exploit **Blackwell NVFP4** data types (e.g. for the latest NeMo/Triton models), and you can prioritize for **larger context windows** (agentic use cases) or **lower latency**.
- The right **runtime depends on the model**: vLLM and SGLang for LLMs, Text Embeddings Inference for embeddings/RAG, llama.cpp for quantized CPU models, Nvidia NIM (TensorRT-LLM) for Nvidia models, and the new **HF Serve** SDK for speech/vision/multimodal tasks.
- **First-at-Build firsts:** you can now deploy open models directly from Foundry, use them in the **Playground**, call them from **VS Code**, and integrate them with **Foundry Agents**.
- Foundry Agents built on open models inherit Foundry's tooling (e.g. **web search**) and full multi-turn/context-aware behavior — the demo showed live NBA Finals results (data outside the model's training) plus agentic RAG remembering a user's "favorite country."
- A **week ago** this workflow would have required hopping between Foundry → Azure Machine Learning → quota requests → guessing runtimes/parameters; Managed Compute collapses it into a near one-click experience.
- All of it runs under **Foundry's enterprise security**: role-based access control, identities, and permissions are built in automatically.
- **Call to action / homework:** (1) start building with Foundry, (2) sign up for the Managed Compute preview, (3) suggest Hugging Face models to onboard via the new **Microsoft feedback portal**.

## 📚 Detailed Notes

### Speakers & structure
Three presenters split the talk:
- **Vaidya** (Microsoft Foundry team) — platform improvements for open-source consumption (intro + Managed Compute).
- **Jeff** (Hugging Face) — the partnership, why open models matter, and how models get from Hugging Face into Foundry.
- **OC Kadu** (PM, Microsoft Foundry) — the live code demos.

The session was scoped tightly to ~20 minutes and framed against the prior day's Foundry keynote sessions (referenced as presented by "Ena and Tina"). Foundry was positioned throughout as **the agent-hosting platform**, with this talk focused specifically on the **open-source model ecosystem**.

### The platform problem and Foundry Managed Compute
Foundry is fundamentally an **agent-hosting platform** with access to both proprietary frontier models and open-source models — **10,000+ models from Hugging Face**.

How you consume models differs by type:
- **Proprietary frontier models** come in multiple form factors:
  - **PAYGO / per-token (PTOK)** — easy access, "PRC go"-style quick setup.
  - **PTUs (Provisioned Throughput Units)** — for production-like environments needing control over latency.
- **Open-source and custom models** — the new construct introduced here is **Foundry Managed Compute**.

**What Managed Compute is:** a managed Platform-as-a-Service where you simply **pick the GPUs** and don't worry about the underlying infrastructure — "it works out of the box." Crucially it's part of the Foundry resource, so:
- the **endpoint is the same**,
- the **SDK is the same**,
- the **authentication and billing constructs are the same**.

**What Foundry handles for you:** when you deploy a model there are normally many concerns — GPU topology, runtimes (vLLM, SGLang, etc.), maintenance, and patching. With Managed Compute, **all of that maintenance and patchwork is handled by Foundry**. The developer just picks the **model parameters**, hits deploy, and it's live.

### Why Managed Compute needs the open-source funnel
Compute alone isn't enough — you also need a constant inflow of the latest open models. New models arrive on Hugging Face constantly (Qwen, MiniMax, and many **Nvidia** partner models such as the **NeMoTron** family were called out as just-released). Keeping up with all of this in real time is "super tough" — which is exactly where the Hugging Face partnership and **day-zero access** come in.

### Why open models matter — Jeff's five reasons
Jeff (Hugging Face) opened by thanking Microsoft for the partnership, noting they've worked together a long time to make Hugging Face models easy for Azure customers. He reiterated the keynote stat: **11,000 models in Foundry today, 10,000+ from Hugging Face**. He then gave five reasons enterprises should work with open models:

1. **Performance / baseline is on par with the frontier.** Open models have been on par with closed frontier models for over a year. In the **Artificial Analysis Intelligence Index**, roughly **half of the top 20 models are open**. This is just the baseline, though.
2. **You can build on, customize, and adapt them.** Base open models can be **fine-tuned, post-trained, and distilled** to improve them for a specific use case. Example: **Phi-2** (a popular open model from Microsoft) has **~1,500 derivatives**. This is *why* there are so many models on Hugging Face — enterprises customize base models to their own data/use case for far better task performance.
3. **Hosting the weights = owning the experience.** If you don't host the weights, you don't really control the experience. Microsoft + Hugging Face make it easy to host on Azure right from the Hugging Face model page, with **two options**:
   - Deploy on **your own Azure account/tenant** via Microsoft Foundry.
   - Use **Hugging Face Inference Endpoints** to deploy on Azure using the **Hugging Face tenant**.
4. **Cost — the community optimizes for cheaper inference.** The whole open-source community focuses on making models cheaper to run (e.g. multiple techniques exist for running Stable Diffusion more cheaply). For specific tasks, small models can be state-of-the-art: **Granite-Docling from IBM** (~250 **million**, not billion, parameters) is state-of-the-art for **batch inference on documents**.
5. **Version control.** Because you host them, you can pin versions. Developers have been burned by a **closed model behind an API changing overnight**, silently altering behavior for customers. On Hugging Face **every model repository is fully version-controlled**, and you can **tag a specific version ID in code**.

Summary of the five: baseline performance on par → improve via customization → host weights to own the experience → control costs → control behavior via version control.

### What Hugging Face is today (scale)
Jeff gave a quick state-of-Hugging-Face update:
- **16 million** AI builders signed up (he corrected "over 15 million" to 16 million).
- **400,000+ organizations** set up for private work and access control; **Microsoft** is one of the enterprise organizations.
- **3 million+ public/open models** covering every imaginable task.
- **1 million+ public datasets** to use with them.
- Open-source tooling: the **Transformers** library plus a whole ecosystem for **inference, post-training, reinforcement learning**, etc.

But: open source and the model only take you so far. To **build an app and scale it to production**, many more challenges arise — and that's where the Foundry partnership comes in.

### How models get from Hugging Face into Foundry (the pipeline)
Jeff detailed the collaboration pipeline that turns "3 million models on the Hub" into "11,000 enterprise-ready models in Foundry":

1. **Daily curation / trending monitoring.** They monitor the trending, most-liked, and most-downloaded models daily across the most important tasks and providers (e.g. Nvidia), so models become available in Foundry **the same day they land on Hugging Face**. That's how the count reached 11,000.
2. **Coverage of all ML tasks, not just LLMs.** Document processing, speech recognition, image detection, embeddings, etc. — all selectable via **easy-to-use filters directly in Foundry**.
3. **Runtime optimization for scaled usage.** Open source alone won't scale; you must pick a runtime/config tuned for best throughput or smallest latency. Foundry works this out so it's a **one-click experience**.
4. **Enterprise-readiness screening.** Before a model reaches Foundry:
   - **License screening** — only **commercially permissible** models are offered.
   - **Remote-code filtering** — models containing remote code that the runtime would inject/execute are filtered out.
   - **Security scanning** of models so everything in Foundry is enterprise-ready.
5. **Supply-chain security.** With Managed Compute, the **weights are uploaded into Microsoft Foundry/Azure**, giving complete robustness and supply-chain security (not pulling from the Hub at runtime).
6. **Validated deployment experience.** They validate the actual deployment: which **runtime**, what **configuration parameters**, what **context window** to enable per model.
7. **Network isolation guarantee.** Every Hugging Face model picked from the Foundry collection, once deployed, **will not make network calls outside your own secure tenant** — an important enterprise guarantee.

### Runtimes — one size does not fit all
Jeff stressed that the optimal runtime depends on the model/task:
- **vLLM** — some providers optimize their LLMs for vLLM.
- **SGLang (SG Lang)** — other providers optimize their LLM deployment for SGLang.
- **Text Embeddings Inference (TEI)** — for **embedding models** used to build **RAG pipelines**.
- **llama.cpp** — the C++ runtime for **quantized** models that run efficiently/super-efficiently on **CPU**.
- **Nvidia NIM** — for Nvidia models, powered by **TensorRT-LLM**.
- **HF Serve** — a **new framework/SDK** to optimize deployment of **speech, vision, and other multimodal ML tasks**.

Foundry provides **containers and deployment templates** for these.

### The demo — discovering, deploying, and using an open model
OC Kadu ran the live demo (with the obligatory "demo effect" Wi-Fi gremlins — he fell back to a phone hotspot). Flow:

**1. Discover / catalog.**
- Go to **Discover** in Foundry → the model catalog with different collections.
- Left sidebar → **Models** page; filter by **provider** (filter to the **Hugging Face** collection).
- Filters also let you select the **machine-learning task** (embeddings, vision, speech, etc.) to quickly find the right kind of model.
- Alongside Microsoft AI, Anthropic, and OpenAI, there are **11,000+ open models**.

**2. Pick a model + Managed Compute.**
- On the Models catalog page, scroll to **deployment options** and choose **Managed Compute** (the focus of the talk).
- These models are **hosted on Azure** — *not* pulled from the Hugging Face Hub at deploy/runtime.
- The demo searched for and selected a **Qwen 3 32B** parameter model (caption rendered it "plan three 32" / "Quant 3 32B" / "10 3 32B" — all the same **Qwen3-32B** model).

**3. Deployment page + templates.**
- The deployment page has an **acknowledgements** step, then **deployment templates** (four shown).
- Templates included a base config (single **H100** / **A100**) plus pre-built configs for **two H100s** and **two A100s** — everything **pre-configured and customized**; nothing else to set up.
- Choosing the **two-H100** template let you exploit the latest **Blackwell data types** — e.g. an **NVFP4** variant (as exists for the latest **NeMo/Triton** models). You can also prioritize for **larger context window** (agentic use cases) or **lower latency**.
- Concrete numbers from the templates: **two H100s → max context length 131,000 tokens**; a **single H100 → ~41,000 tokens**. Selecting **Accelerators** is just clicking "H100" — no low-level infra details to manage.
- "The magic of managed compute": no more hunting in the console for whether you have **quota** for the right accelerator type — it's a simple dropdown. **A100s and H100s** are available now, with **AMD Instinct GPUs coming**.

**4. Use a deployed model.**
- Under **Build → Models** there's a dedicated **Managed Compute** tab listing **managed compute deployments**.
- OC selected the already-deployed **Qwen3-32B** and used the **Playground** integration: a simple "Hello" returned "Hello, how can I help?" after a couple of seconds. (Noted as a **first** — deploying open models from Foundry and using them in the Playground before a Build audience.)

**5. Call from VS Code.**
- Since "developers don't live in playgrounds," OC opened the **Call Model** screen, copied the code snippet, and pasted it into a **pre-configured VS Code** project.
- Asked "What is the capital of Nigeria?" → after running (slow on the hotspot) it correctly answered **Abuja** (not Lagos). This demonstrated the **one-stop-shop loop**: search → find → access GPUs → deploy → integrate into code, all in the same UI.

### The demo — Foundry Agents on open models
- **First-ever agent integration with open models** in Foundry. From the deployment screen → **Build → Models → Qwen3-32B**, then **add to agent**.
- Create a resource (named **build 2026**) → **Agents → new agent** → build a new agent (with a fun "Thing One / Dr. Seuss" persona).
- **Why it's a big deal:** a week ago this required jumping from Foundry → **Azure Machine Learning** → getting quota → guessing the right runtime → guessing deployment parameters → figuring out how to plug it into agent creation. Now it's all in one place.
- **Tool integration — web search.** Agents integrate with tools, including a **web search tool** for live web results. Demo: asked about the **NBA Finals** — it returned "**Wednesday, June 3rd**, NBA Finals tonight at **8:30 p.m. Eastern**, **New York Knicks vs San Antonio [Spurs]**." Since that data **isn't in the model's training data**, it proved the web-search integration was working live.
- **Call the agent from code.** Via the **Call Agent** screen, copy the snippet into the editor and run it ("who do you have for the NBA Finals?") — showing agents are callable from **VS Code**, not just the Playground. (Aside banter: both presenters rooting for "Wemby"/the Spurs.)
- **Agentic RAG + multi-turn / context-awareness.** A small RAG script: telling the agent "my favorite country is Nigeria," then later asking "what did I tell you my favorite country was?" → it correctly recalled **Nigeria**, demonstrating **multi-turn, context-aware** behavior on open models in Foundry. Final query: "what city should I visit in Nigeria?" for travel suggestions (OC mentioned an upcoming December trip).
- **Enterprise security is built in.** While networking lagged, the presenters underlined that all the work you'd have to do anyway when building agents — **role-based access control, identities, permissions** — is **built into Foundry**, so all of Foundry's security automatically applies to your open-model usage.

### Wrap-up
Recap from the presenters: yesterday Microsoft announced **Managed Compute** in Foundry — "the easiest way to build with open models," bringing **all Hugging Face open models** into the new experience so you can deploy with **security, performance, and GPUs** without going through "all of the hoops." Closing homework:
1. **Start building** with Foundry (referred to as "AI Foundry").
2. **Sign up for the Managed Compute preview.**
3. Use the **new Microsoft feedback portal** to **suggest Hugging Face models** to onboard to Foundry.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — Microsoft's agent-hosting / AI platform with access to proprietary frontier and open-source models; the hub for everything in this session. (Also referred to as "AI Foundry.")
- **Foundry Managed Compute** — new managed PaaS for deploying open-source/custom models: pick the GPU, Foundry handles infra/topology/runtimes/patching; same endpoint, SDK, auth, and billing as Foundry.
- **Hugging Face** — open-model platform/community supplying 10,000+ of Foundry's models; partner in the curation/security/deployment pipeline.
- **Hugging Face Hub / model repositories** — fully version-controlled model repos; tag a specific version ID in code.
- **Hugging Face Inference Endpoints** — deploy Hugging Face models on Azure using the Hugging Face tenant (alternative to deploying in your own Azure tenant).
- **Transformers (library)** — Hugging Face's open-source library; part of its inference / post-training / RL ecosystem.
- **PAYGO / per-token & PTUs (Provisioned Throughput Units)** — the form factors for consuming proprietary frontier models in Foundry (quick access vs. production-grade controlled latency).
- **Deployment templates** — pre-configured runtime + GPU configs in Foundry (e.g. single/dual H100, single/dual A100) optimized for context window or latency.
- **vLLM** — high-throughput LLM serving runtime.
- **SGLang** — alternative optimized LLM serving runtime.
- **Text Embeddings Inference (TEI)** — optimized runtime for embedding models / RAG pipelines.
- **llama.cpp** — C++ runtime for quantized models running efficiently on CPU.
- **Nvidia NIM** — Nvidia's inference microservices for Nvidia models, powered by TensorRT-LLM.
- **TensorRT-LLM** — Nvidia's optimized LLM inference engine underpinning NIM.
- **HF Serve** — new Hugging Face framework/SDK to optimize deployment of speech, vision, and multimodal ML tasks.
- **Foundry Playground** — in-portal chat UI to interact with deployed models.
- **Foundry Agents** — agent-building experience in Foundry now integrated with open models, including tools like web search.
- **Web search tool (Foundry Agents)** — gives agents live web results beyond training data.
- **VS Code integration** — "Call Model" / "Call Agent" code snippets to invoke deployed models/agents from code.
- **GPUs: Nvidia A100, Nvidia H100 (Blackwell), AMD Instinct** — accelerators; A100/H100 available, AMD Instinct "coming." H100 templates can use Blackwell NVFP4 data types.
- **NVFP4** — Blackwell low-precision (FP4) data type usable on H100 templates (e.g. for latest NeMo/Triton models).
- **Artificial Analysis Intelligence Index** — third-party model leaderboard cited (≈half of top 20 are open models).
- **Microsoft feedback portal** — new portal to suggest Hugging Face models for onboarding into Foundry.

### Models referenced
- **Qwen3-32B** — the 32B-parameter open model deployed/used throughout the demo (caption-garbled as "plan/Quant/10 3 32B").
- **Phi-2** — Microsoft open model with ~1,500 derivatives (example of customizability).
- **Granite-Docling (IBM)** — ~250M-parameter model, state-of-the-art for batch document inference (caption: "Duckling Granite").
- **NeMoTron / NeMo (Nvidia)** — recently released Nvidia open models cited as examples landing on Hugging Face; latest NeMo/Triton variants can use NVFP4 on H100 templates.
- **Qwen, MiniMax** — examples of providers continually pushing new open models to Hugging Face.
- **Stable Diffusion** — image model referenced as an example of community cost-optimization efforts.

## 🚀 Announcements / What's New
- **Foundry Managed Compute** — announced the day before this session (Build 2026 keynote) and demoed here; a managed PaaS for deploying open-source/custom models on Foundry where you pick the GPU and Foundry manages infra, GPU topology, runtimes, patching, and maintenance. **In preview** — the closing CTA explicitly says to *sign up for the Managed Compute preview*.
- **All Hugging Face open models brought into Managed Compute** — the full Hugging Face catalog (10,000+ models already in Foundry) is being made deployable through the new Managed Compute experience.
- **First-at-Build firsts (stated live):** for the first time you can (a) **deploy open models directly from Foundry**, (b) use them in the **Foundry Playground**, (c) **call them from VS Code**, and (d) **integrate them with Foundry Agents** (including tools like web search and agentic RAG / multi-turn memory).
- **AMD Instinct GPUs "coming"** to Managed Compute (A100 and H100 available now) — roadmap item, not yet GA.
- **Microsoft feedback portal for Hugging Face model onboarding** — new portal where users can suggest Hugging Face models to onboard into Foundry.
- **HF Serve** — presented as a new Hugging Face framework/SDK for optimized deployment of speech/vision/multimodal tasks.

## 💡 Demos
A single continuous live demo by **OC Kadu** (plagued by "demo effect" Wi-Fi, run over a phone hotspot) proved the end-to-end open-model-to-production workflow:

1. **Discover & filter the catalog** — navigated Foundry **Discover → Models**, filtered by **provider → Hugging Face collection**, and showed task-based filters (embeddings/vision/speech). Point proved: open models live alongside Microsoft AI / Anthropic / OpenAI, 11,000+ of them, easy to find.
2. **Deploy via Managed Compute** — selected **Qwen3-32B**, chose **Managed Compute**, acknowledged terms, and picked a **deployment template** (two H100s → **131K-token** context; single H100 → ~**41K**). Point proved: zero infra/quota wrangling — just pick model + GPU template; H100 templates unlock Blackwell **NVFP4**.
3. **Playground chat** — sent "Hello" to the deployed model, got a reply in seconds. Point proved: open models are usable in the Foundry Playground out of the box (a first).
4. **Call from VS Code** — copied the **Call Model** snippet into pre-configured VS Code, asked "capital of Nigeria?" → correctly answered **Abuja**. Point proved: the same UI takes you from search → deploy → code integration (one-stop shop).
5. **Build a Foundry Agent on the open model** — added Qwen3-32B to a new agent (resource "build 2026"). Point proved: agent creation on open models is now native to Foundry (previously required hopping to Azure ML + quota + parameter-guessing).
6. **Web search tool** — asked the agent about the **NBA Finals**; it returned live details (June 3rd, 8:30pm ET, Knicks vs Spurs) that **aren't in the model's training data**. Point proved: live tool/web-search integration works.
7. **Call the agent from VS Code** — ran the **Call Agent** snippet ("who do you have for the NBA Finals?"). Point proved: agents are callable from code, not just the Playground.
8. **Agentic RAG / multi-turn memory** — told the agent "my favorite country is Nigeria," then later asked "what did I tell you my favorite country was?" → correctly recalled **Nigeria**; followed up with "what city should I visit in Nigeria?". Point proved: multi-turn, context-aware agentic behavior on open models in Foundry.

Throughout, the presenters emphasized that **Foundry's enterprise security (RBAC, identities, permissions)** applies automatically to all of the above.

## 📊 Notable Stats / Quotes
- **11,000+ models** in Microsoft Foundry today; **10,000+ from Hugging Face**.
- **16 million** AI builders signed up on Hugging Face; **400,000+ organizations**; **3 million+ public models**; **1 million+ public datasets**.
- **~half of the top 20 models** in the Artificial Analysis Intelligence Index are **open** (true for over a year).
- **Phi-2** has **~1,500 derivatives** on Hugging Face.
- **Granite-Docling (IBM)** is **~250 million** parameters — "not billion" — and state-of-the-art for batch document inference.
- Deployment template context windows: **two H100s → 131,000 tokens**, **single H100 → ~41,000 tokens**.
- *"Over 10,000 of those come from Hugging Face."* — Jeff, on Foundry's 11,000 models.
- *"Pick the model parameters and then boom, deploy."* — Vaidya, on Managed Compute simplicity.
- *"That's the magic of managed compute… you don't have to go into the console [and ask] do I have the quota for the right accelerator type."* — Jeff.
- *"A week ago, in order to do all of this, you would have had to jump through a lot of hoops."* — Jeff, on the pre-Managed-Compute workflow.
- *"Every model repository is fully version controlled, and you can tag to a specific version ID in code."* — Jeff, on version control.
- Closing homework: *"One, start building with AI Foundry. Two, sign up for the preview for managed compute. Three… suggest Hugging Face models to onboard to Foundry."* — OC Kadu.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Sign up for the **Foundry Managed Compute preview** and deploy a Hugging Face model (e.g. Qwen3-32B) end-to-end.
  - Try a deployment template on **2× H100** to see the 131K context window vs. a single H100 (~41K).
  - Wire a deployed open model into a **Foundry Agent** with the **web search** tool and test multi-turn/agentic RAG.
  - Test the **VS Code** "Call Model" / "Call Agent" snippets against a managed-compute endpoint.
  - Explore non-LLM tasks (embeddings via TEI, a quantized CPU model via llama.cpp, a speech/vision model via HF Serve).
  - Suggest a model via the new **Microsoft feedback portal**.
- [ ] Questions:
  - Pricing model for Managed Compute — is it pure GPU-hours, and how does billing roll into the existing Foundry billing construct?
  - When do **AMD Instinct** GPUs land, and which runtimes/data types will they support?
  - What's the SLA / autoscaling story for Managed Compute endpoints (scale-to-zero, cold starts)?
  - Region availability for the preview (relevant for `australiaeast`)?
  - How does the "no network calls outside your tenant" guarantee interact with agent tools like web search (which clearly do egress)?
  - Fine-tuning/post-training path: can you bring a customized/derivative model's weights into Managed Compute the same way?
- [ ] Relevant to:
  - Productionizing open-source models on Azure under enterprise security/compliance.
  - Building agents on cost-controlled, version-pinned open models instead of closed APIs.
  - Any RAG/embeddings or multimodal workload needing optimized, managed GPU serving.

## 🔗 Related
- [[BRK243 - Claw and agent harness in Microsoft Foundry]]
- [[BRK246 - Foundry IQ Fuel agents with enterprise knowledge]]
- [[BRK240 - Build context-aware agents]]
- [[BRK242 - Turn your agents into action Connect tools APIs documents]]
- [[DEM340 - Build work-ready agents with Foundry and Work IQ]]
- [[DEM331 - Turn APIs tools and data into real agent velocity]]
- [[DEMSP387 - Secure agent workflows in GitHub Copilot with NVIDIA]]
- [[DEMSP388 - Ship faster with Claude Code and Cowork in Microsoft Foundry]]
