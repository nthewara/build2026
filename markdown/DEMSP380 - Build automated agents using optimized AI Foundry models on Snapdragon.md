---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/snapdragon
  - topic/qualcomm
  - topic/on-device-ai
  - topic/agents
  - topic/npu
  - topic/ai-foundry
source: https://www.youtube.com/watch?v=vc4tADfTnYY
session_code: DEMSP380
event: Microsoft Build 2026
speakers: LLMware (Darren, demo lead) + Qualcomm/ISV presenter
duration_min: 25
aliases:
  - Build automated agents using optimized AI Foundry models on Snapdragon
---

# DEMSP380 — Build automated agents using optimized AI Foundry models on Snapdragon

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** LLMware presenter "Darren" (demo lead, drives the live build/SDK walkthrough) + a Qualcomm/ISV co-presenter (frames the enterprise problem and the Snapdragon NPU advantage)  
> **Duration:** ~25 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=vc4tADfTnYY)

## 🎯 TL;DR
A partner demo (LLMware + Qualcomm) showing how to build **fully automated, multi-step AI agents that run entirely on-device** on Snapdragon Copilot+ PCs — no cloud, no token charges, no prompting required. The agents are built in **LLMware Model HQ**, a no-code drag-and-drop designer, using **small language models pulled from Microsoft Foundry Local** and executed on the **Snapdragon X2 NPU** (via Windows ML API / ONNX Runtime with Qualcomm execution providers). The headline use case is an automated **Jira triage workflow**: pull issues from Jira → filter for the most critical/open ones → summarize each row with AI → emit a clean spreadsheet → email it out, all schedulable to run every morning. The session also shows how a no-code agent can be exposed as a **local Windows service / API + SDK** so it can be called programmatically, shared as a zip file like a PowerPoint, and pushed to a server for scaling — closing the prototype-to-production gap for local AI.

## 🔑 Key Takeaways
- **On-device, schedule-driven agents** are the thesis: instead of a human prompting a cloud chat model, you build a repetitive/complex/multi-step enterprise workflow once and let it run automatically on a schedule, locally.
- Four explicit learning goals: (1) build a multi-step AI workflow powered by small language models, (2) make it automated on a Snapdragon PC, (3) get optimized NPU performance by running the model locally, (4) implement a **scheduled run** of the agents.
- The stack is **LLMware Model HQ** (no-code app, sits in the middle) → **Microsoft Foundry Local** (model source) → **Windows ML API / ONNX Runtime** → **Qualcomm execution providers** → **Snapdragon X2 NPU**.
- **No-code build, drag-and-drop palette**: every step (Jira pull, filters, summarization, email) is a component dropped onto a canvas; usable by completely non-technical SMEs, yet extensible by sophisticated developers.
- The demo integrates **three external components**: a configured **Jira API**, **Windows/Foundry Local** model inference, and an **email client** (the workflow ends by emailing the result).
- **NPU = the "secret sauce"** of running AI locally — avoids cloud round-trips, token charges, and privacy risk, because the accelerator is already inside the laptop everyone is carrying.
- **Snapdragon X2 has 80 TOPS** of NPU compute, unlocking bigger/more models running faster; the chosen model was specifically optimized for Snapdragon X2.
- Outputs land in **business-ready formats** — CSV, Excel workbooks, PowerPoint — not raw model text, so the AI drives real productivity and the artifacts can be consumed/shared directly (email, Teams, Slack).
- The same no-code agent can be **flipped into a back-end Windows service** exposed over API (localhost by default, or an external port to turn a laptop into a mini server) — nothing has to leave the machine.
- An **SDK** wraps the agent: instantiate a `client` (carries credentials), then `call_agent` by name (runs **asynchronously**, returns an **execution ID / receipt**) and later `get_agent_outputs` to retrieve a zip of result files.
- **Hybrid cloud-burst is supported**: ~200 models in the catalog including cloud models; do text/extraction/summarization locally, then "punch out" to a cloud model (e.g. Gemini) for one hard reasoning/multimodal step — best of both worlds.
- **Sharing is trivial and credential-safe**: the whole agent distills to hundreds of lines of JSON config + custom data assets, wraps into a zip, and is shared like a PowerPoint/Excel file (over email or SharePoint). **No credentials are ever shared.**
- This is a **shipping commercial product**, not just a demo — they cited **15+ other industry scenarios** available at the Qualcomm booth, where attendees can build their first agent "in just a minute."
- The end-to-end Jira agent in the pre-recorded video was **built in ~15 minutes** in (near) real time, then compressed for showing.
- Closing message from the partners: **look into local AI** — cost, privacy, and the capabilities of next-gen AI PCs let you do almost anything a cloud model does, locally, without token charges or privacy concerns.

## 📚 Detailed Notes

### The problem: cloud chat apps vs. real enterprise workflows
Today most enterprise workflows are built as **chat applications against a cloud-hosted model** — you send a prompt, it fetches an answer, you read the result. That pattern breaks down when the workflow is:
- **Repetitive** (the same job runs over and over),
- **Complex / multi-step** (many stages, not a single Q&A),
- **Schedule-driven** (it should fire on a cadence, e.g. every morning), and/or
- **Security/privacy-sensitive** (an enterprise requirement that may *necessitate running the model locally*).

The provocative framing: **what if, without ever typing a prompt, you could run automated workflows that are schedule-driven and run entirely on the device?** That is exactly what the session demonstrates with LLMware Model HQ + Snapdragon PCs + Foundry-optimized models via the Windows ML API.

### The four things to walk away with
1. **Build a multi-step AI workflow powered by small language models (SLMs).** LLMware can build these automated workflows for many enterprise scenarios across industries; today's worked example is a **Jira** workflow.
2. **Make the workflow automated on a Snapdragon PC.**
3. **Get optimized performance on the NPU** by running the model locally on the NPU.
4. **Implement a scheduled run** of the automated agents.

### Why Jira (and the "data in silos" problem)
Jira was chosen as a representative enterprise system, with the acknowledgement that *many* enterprise software systems would need to be hooked in for real agentic workflows. In any large enterprise there are **multiple Jira databases** — product managers store user stories, feature requests, bug reports — so relevant data sits in **many silos**. The agent's job: **glean the relevant data across those sources and form a knowledge base**, then run the needed prompts/requests **locally on the PC**. The demo uses a **CSV file of structured data with thousands of rows** and shows how to gather the relevant information and extract just the important summary you actually need.

### The architecture (the single demo slide)
At the center sits **LLMware Model HQ** — the application and the **no-code drag-and-drop design interface**. It integrates:
- **Microsoft Foundry Local** (and other model repositories) for the models — via no-code integration in the software.
- On the back end, either the **Windows ML API** or the **ONNX Runtime APIs**.
- Underneath those, the **Qualcomm execution providers**, which deliver the best performance by **running the model locally on the NPU**.

So the conceptual flow is: **Model HQ (no-code) → Foundry Local model → Windows ML / ONNX Runtime → Qualcomm execution providers → Snapdragon NPU.**

### The pre-recorded overview (what the workflow does end-to-end)
A ~2-minute silent video (audio failed live due to the noisy room, so they re-narrated it) walked the build, which integrates **three components**: the **Jira API**, **Windows/Foundry Local** inference, and an **email client**. The steps:
1. **Select an NPU model from Foundry Local** optimized for performance on the **Snapdragon X2** (so it runs very fast).
2. **Compose the process entirely with no code** — drag-and-drop components define every step.
3. **Pull information from the Jira API.**
4. **Run basic filters** to find the most **important open and critical issues** with certain characteristics.
5. **Run a summarization** over all that activity.
6. **Produce the output**: instead of hundreds of Jira rows, you get just the rows you wanted, each with an **AI summary distilling that individual issue**.
7. **Email the result** to yourself/your team.

The payoff: put it on a **scheduling API** and run it every day, so when you/your team arrive in the morning your inbox already holds — **safely, securely, and without any token charges** — a distillation of the most critical Jira issues plus a summarization in a **common spreadsheet** everyone can work from. The whole thing in the video was created **in ~15 minutes** end-to-end, then compressed.

### The live demo — building & running locally
- **Model HQ is just a Windows application running entirely locally** on the device. The **only network dependency is the Jira pull** (everything else is on-device). They noted a **fully air-gapped version** exists they could pivot to if Wi-Fi/Jira failed ("the demo gods").
- The process canvas mirrors the video: **drag-and-drop elements onto a palette**, like a typical data-transformation / process-automator tool — very intuitive, usable by **completely non-technical people**, yet powerful enough to automate complex workflows.
- They ran it live; the **Jira API pull (the slowest part) succeeded**, and the inferences completed **very fast**, with the **NPU visibly active in Task Manager**. The speed of running through all those inferences was explicitly attributed to the NPU.
- **NPU as the "secret sauce" of local AI**: the accelerators are increasingly built into the kit every attendee is carrying; you don't have to send everything to the cloud, so you avoid **token charges** and **privacy risk** while getting a "really powerful accelerator" inside the laptop.

### Outputs in consumable formats
Outputs come out in the formats you'd actually want to consume: **CSV files, Excel workbooks, PowerPoints.** The AI thus drives **real productivity** by producing custom outputs already in a usable form — which can then be **emailed to someone, shared over Teams, or shared over Slack.**

### From no-code prototype → programmatic / production
The core developer message: people get stuck in **prototype/demo mode** ("that's cool, I'll show my boss") but then struggle to **move it into production**, share it, integrate it into an operational or custom application. LLMware's answer:
- In addition to being a UI app, **all functionality can be exposed as a back-end Windows service** — by **flipping a switch**, every feature becomes available over **API**.
- It runs on **localhost** by default (nothing leaves the machine), but you can **expose it over an external port** — effectively turning a laptop into a **mini server**.
- Once exposed, the **no-code agent can be accessed and extended programmatically**.

### The SDK pattern
They switched to code to "do some real work," reassuring the developer audience. The SDK mirrors familiar high-level model SDKs (e.g. the OpenAI SDK pattern): **instantiate a `client` object** that carries your credentials, then invoke methods on it. Two APIs were used:
- **`call_agent`** — the just-built agent is exposed over an endpoint and **called by name**. In this demo there were **no inputs** (everything comes from the API), but in other cases you can **pass inputs into the API call**.
- Running the agent **launches it asynchronously on the device** and returns a **receipt / execution ID**. You **come back after about a minute with that execution ID** and call **`get_agent_outputs`** to retrieve all the agent's outputs — delivered as a **zip folder** containing the same files produced in the interactive run.

Because it runs **asynchronously in the background as a Windows service**, you **don't need the app open**; it can run quietly in the background, **on a schedule** (every morning/night), as long as the Windows service is running — **even if someone closes the laptop**.

### Scaling to a server
Beyond point-to-point sharing among local colleagues, there is a **server component**: once an agent is built and working, it **can be exposed as an endpoint on that server**, letting you go from local development → point-to-point sharing → **pushing it up to a server for a much more scalable deployment**.

### Sharing an agent (credential-safe)
Sharing is "as easy as that": the entire agent — every component shown, including the **custom Jira integration service** and **custom data assets** — distills down to **hundreds of lines of JSON configuration** plus those data assets, wrapped into a **zip file**. **No credentials are ever shared or passed.** That zip is as easy to share as a PowerPoint or Excel spreadsheet — email it, post it to a **SharePoint** site, "Hey, I built this agent, go check it out." Collaboration becomes trivial, all **no-code** and all **powered by the Snapdragon X2 NPU**.

### Q&A — key points
- **"Small models are great, but what about tasks needing larger models?"** Supported. They have **~200 models** in the catalog **including cloud-based models**. For a step needing complex reasoning/analytics (e.g. "I need Gemini for this"), you **add a node** that calls out to that model — e.g. a complex multimodal/visual transformation. Pattern: do the other ~10 steps (extraction, summarization, text) **locally**, then for the **one critical step punch out to a cloud model** and bring the result back — **best of both worlds**.
- **"Does this only matter on Snapdragon, or any CPU? What's the advantage of a Snapdragon processor?"** The ISV answer plus Qualcomm confirmation: **it's fast — really, really fast.** The NPU is fully integrated on the device; the **latest X2 Snapdragon has 80 TOPS**, i.e. lots of capability to run **more and bigger models faster**. Ultimately a processor's value for models comes down to the **speed and the size of model** it unlocks, and this is a **state-of-the-art platform** for using the biggest/best models in the fastest way.
- **Booth pitch:** more use cases at the **Qualcomm booth** — they could only cover one use case in-session and have **15+ other scenarios** to show across different industries. Attendees can **build their first agent in ~a minute**, regardless of technical depth.

### Closing message
"**Look into local AI.**" Amid all the Build messaging over the next two days, the partners' core point: **cost, privacy, and the capabilities of next-generation AI PCs** unlock a lot. As an IC/hardware vendor, Qualcomm is committed to pushing innovation from the hardware level so you can do **almost anything you'd do with a cloud model — locally — without worrying about token charges or privacy concerns.**

## 🛠️ Products / Features / Technologies Mentioned
- **LLMware Model HQ** — the central Windows application: a **no-code, drag-and-drop** agent/workflow designer that runs entirely locally and orchestrates the whole pipeline.
- **Microsoft Foundry / Foundry Local** — the model source; provides models (incl. NPU-optimized ones) integrated into Model HQ with no-code wiring.
- **Windows ML API** — back-end inference API used to run the model on Windows.
- **ONNX Runtime APIs** — alternative back-end runtime for executing models.
- **Qualcomm execution providers** — the layer underneath Windows ML / ONNX Runtime that targets the NPU for best local performance.
- **Snapdragon X2 (NPU)** — the on-device accelerator the models are optimized for; **80 TOPS** of compute.
- **Small Language Models (SLMs)** — power the multi-step automated workflows locally.
- **Jira API** — enterprise data source integrated as a workflow node (pull issues/user stories/bugs).
- **Email client integration** — final node that emails the produced report.
- **LLMware SDK** — Python-style SDK: `client` object (holds credentials), `call_agent` (by name, async), `get_agent_outputs` (returns a zip of results).
- **Back-end Windows service / API mode** — flip a switch to expose all functionality over API (localhost or external port).
- **Server component** — exposes a built agent as a scalable server endpoint.
- **Scheduling API** — runs the agent on a cadence (e.g. daily) unattended.
- **Model catalog (~200 models)** — includes cloud models (e.g. **Gemini** cited) for hybrid cloud-burst steps.
- **Output formats** — CSV, Excel workbooks, PowerPoint.
- **Sharing/collaboration targets** — email, **Microsoft Teams**, **Slack**, **SharePoint**.
- **Air-gapped version** — a fully offline variant of the demo as a fallback.
- **Task Manager** — used to visibly show the NPU under load during inference.

## 🚀 Announcements / What's New
None explicitly announced. This was a **partner demo (DEMSP)** of an existing, **shipping commercial product** (LLMware Model HQ) integrated with Microsoft Foundry Local on Snapdragon X2 Copilot+ PCs — capabilities were demonstrated rather than newly launched. No GA/preview milestones, dates, or new SKUs were stated. (The newest hardware referenced — **Snapdragon X2 with 80 TOPS** — was cited as the platform, not announced here.)

## 💡 Demos
- **Pre-recorded ~2-min overview (silent, re-narrated live).** Walked the no-code build of the Jira agent: select NPU model from Foundry Local (Snapdragon X2-optimized) → drag-and-drop the process (Jira pull → filters → summarization) → run → clean per-row AI-summarized output → email it. Point proved: a complete, scheduleable on-device enterprise agent can be **built in ~15 minutes** with no code and deliver a tidy spreadsheet to your inbox with no token charges.
- **Live build & run in Model HQ.** Showed the actual drag-and-drop canvas, ran the agent live, **successfully pulled from the Jira API in real time**, and completed all inferences **very fast** with the **NPU visibly working in Task Manager**. Point proved: the on-device NPU pipeline is genuinely fast and real, not a canned recording.
- **Outputs demo.** Showed results emitted as **CSV/Excel/PowerPoint**, ready to email or share over Teams/Slack. Point proved: AI output is delivered in immediately consumable business artifacts.
- **Programmatic/SDK demo.** Flipped the app into a **back-end Windows service**, then used the **SDK** (`client` → `call_agent` → `get_agent_outputs`) to invoke the same agent **asynchronously** via API on localhost, get an **execution ID**, and retrieve a **zip of outputs**. Point proved: a no-code agent crosses cleanly into production/programmatic use and scheduled background execution.
- **Sharing demo.** Showed the agent **distilled to JSON config + data assets, zipped, and shared like a PowerPoint** — **no credentials passed**. Point proved: frictionless, secure collaboration on agents.

## 📊 Notable Stats / Quotes
- **80 TOPS** — NPU compute of the latest **Snapdragon X2**.
- **~200 models** in the LLMware model catalog (including cloud models).
- **15+ other industry scenarios** available to try at the Qualcomm booth.
- **~15 minutes** to build the full Jira agent end-to-end (in the video).
- **~20–25 minute** session framing for "we just created this over the course of a session — how do we share it?"
- **"This really is the secret sauce of running AI locally"** — on the Snapdragon NPU.
- **"You don't have to send everything up to the cloud. You don't have to incur token charges, privacy risk, because you have now inside your laptop this really powerful accelerator."**
- **"Look into local AI… Cost, privacy, and the kinds of capabilities that you're finding now in next-generation AI PCs unlock a lot."** — closing message.
- **"Unlike some demos, this actually is a commercial product."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up **Foundry Local** on a Snapdragon Copilot+ PC and pull an **NPU-optimized SLM**; confirm it offloads to the NPU (watch Task Manager) via Windows ML / ONNX Runtime + Qualcomm EP.
  - Prototype a **no-code multi-step agent** (data pull → filter → summarize → export to Excel → email) and put it on a **schedule** to land in the inbox each morning.
  - Test the **hybrid "cloud-burst" node** pattern: keep extraction/summarization local, route one hard step to a cloud model, measure latency/cost tradeoff.
  - Exercise the **SDK** flow end-to-end: `client` → `call_agent` (async) → poll **execution ID** → `get_agent_outputs` zip; then expose over a port to test the "laptop as mini server" claim.
  - Package an agent as a **zip** and verify **no credentials** travel; share via SharePoint and have a colleague run it locally.
- [ ] Questions:
  - Which **specific Foundry Local SLMs** are Snapdragon X2-optimized, and what accuracy/latency do they hit on the NPU vs CPU/GPU?
  - What are the **licensing/pricing** terms for LLMware Model HQ + the server component at production scale?
  - How is **secrets/credential management** handled for connectors (Jira, email) when an agent runs as a Windows service or on a shared server?
  - How robust are the **no-code connectors** beyond Jira (ServiceNow, GitHub, SharePoint, databases) for real enterprise silos?
  - What's the upper bound on workflow size/throughput on-device before you *must* burst to cloud or a server?
- [ ] Relevant to:
  - On-device / edge AI strategy for **privacy- and cost-sensitive** enterprise automation (no token charges, data stays local).
  - **Copilot+ PC / Snapdragon** developer enablement and NPU-optimized model deployment via **Foundry Local + Windows ML**.
  - Automating internal **Jira / issue-triage / reporting** pipelines into a daily inbox digest.
  - Closing the **prototype → production** gap for AI workflows built by non-technical SMEs but operationalized by developers.

## 🔗 Related
- [[DEM345 - From prompt to app build AI powered apps on Windows]] — sibling Windows/on-device app-building demo at the same event.
- [[Foundry Local]] — the model-hosting/runtime layer this session pulls NPU-optimized models from.
- [[Windows ML]] — the on-device inference API underpinning the Qualcomm execution-provider path.
- [[Snapdragon X2 NPU]] — the 80 TOPS accelerator the models are optimized for and run on.
- [[On-device AI]] — the broader theme (cost, privacy, local inference) this session champions.
- [[Small Language Models]] — the SLMs powering the multi-step local agent workflow.
- [[AI Agents]] — automated, scheduled, multi-step agent pattern demonstrated here.
- Source list: [[2026 Build Session List]]