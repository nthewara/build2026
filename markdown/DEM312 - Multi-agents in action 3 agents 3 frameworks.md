---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/multi-agent
  - topic/frameworks
  - topic/ai
source: https://www.youtube.com/watch?v=27FNddH0g7o
session_code: DEM312
event: Microsoft Build 2026
speakers: Jan (Azure Container Apps team), Vinnie (Azure Container Apps team)
duration_min: 22
aliases:
  - Multi-agents in action 3 agents 3 frameworks
---

# DEM312 — Multi-agents in action with 3 AI agents, 3 frameworks, tools & models

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jan & Vinnie — both from the Azure Container Apps team  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=27FNddH0g7o)

## 🎯 TL;DR
Two engineers from the Azure Container Apps (ACA) team build a live multi-agent "content factory" using **three different agents, three different agent frameworks (LangChain Python, Microsoft Agent Framework in C#, GitHub Copilot SDK), and Foundry models**, all orchestrated together and observable through a single management plane. The core announcement is **Azure Container Apps Sandboxes** (private preview at `sandboxes.azure.com`) — fast, isolated, stateful, on-demand infrastructure that lets agents securely execute untrusted AI-generated code, snapshot memory + filesystem, resume sub-second, and enforce network egress controls. The demo shows agents dynamically provisioning one sandbox per tool call to run a Mexico-vs-Czechia football match simulator, then highlights security pitfalls (API keys leaking into agent code) and the fix (managed identity + an out-of-band egress gateway that injects secrets the code never sees).

## 🔑 Key Takeaways
- **Agentic infrastructure is the missing layer:** Gartner predicts ~40% of agentic projects will be canceled (cited as "by 2025") — not because LLMs/agents fail, but due to **high risk, lack of governance, and breaking runtimes**.
- **Four runtime challenges** for agents today: (1) resources running unattended / no lifecycle, (2) running untrusted AI-generated code next to apps, (3) slow cold starts on tool calls, (4) no state preservation for long-running tasks.
- **Azure Container Apps Sandboxes** (private preview) = fast, isolated, stateful infrastructure on demand; executes code securely, resumes instantly, snapshots **disk AND memory**, and can burst to hyperscale.
- **Sandboxes are already powering internal Microsoft workloads:** Microsoft Foundry hosted agents, GitHub Sandboxes, and Azure Container Apps Express all use the same technology.
- **Mix-and-match frameworks by design:** researcher = LangChain (Python), creator = Microsoft Agent Framework (C#), podcast/narrator = GitHub Copilot SDK — reflecting how real orgs adopt tech bottom-up ("grassroots").
- **One management plane:** three diverse models/agents are brought into **Microsoft Foundry** for management, observation, continuous evaluation, and registration (as long as they speak A2A or share a contract).
- **Observability via OpenTelemetry (OTel):** every agent *and* the orchestrator emits detailed OTel telemetry → OTel collector → Application Insights → visible in both Azure Portal and Foundry.
- **One tool call ≈ one sandbox:** the simulator agent writes Python, and each query (lineups, news, injury reports) fires a brand-new sandbox dynamically at runtime — not pre-provisioned at deploy time.
- **Sandboxes go idle automatically** by snapshotting memory + filesystem, so you **don't pay for idle compute**, and **resume is sub-second** from snapshot.
- **Egress policy** lets you control outbound traffic per sandbox: default-deny + allowlist, or allow + denylist specific destinations (demoed blocking certain sports URLs).
- **Don't hand secrets to agent code:** putting an API key in an environment variable means the AI-written code can read your secret — a real risk demoed live.
- **The secure fix:** use **managed identity** (sandboxes run inside Azure) for Azure services; for non-Azure services, use the **egress "transform" policy** where an out-of-band egress gateway injects the secret as a header on outbound calls — the sandbox code never sees the key.
- **GitHub Copilot SDK supports "bring your own model"** — here it's used as the agent harness while calling a Foundry model instead of the default Copilot LLM.
- **GitHub repo provided:** `aka.ms/aca-build2026-demo312` (full code for both demos available).

## 📚 Detailed Notes

### Who & What
Jan and Vinnie, both from the **Azure Container Apps team**, present a session on "multi-agents in action." Their goal: demonstrate **three different agents, three different agent frameworks**, how to call tools, and how to run infrastructure at scale — all stitched into a working "agentic content factory" whose code is published to a GitHub repo for the audience to run immediately.

### The Problem: Modern Agentic Infrastructure & Why It Matters
They open with a provocative stat: **Gartner predicts ~40% of agentic projects will be canceled** (stated in the talk as "by 2025"). The cause isn't model/agent capability — it's **high risk, lack of governance, and runtimes that break**.

They enumerate the concrete **challenges of today's runtime**:
1. **Unattended resources / no lifecycle** — you spin up an Azure resource and forget it; you deploy something 10 times and end up with 10 stray resources. There's no built-in lifecycle for agentic compute. ("It's happening to me all the time.")
2. **Running untrusted code** — i.e., AI-generated code running next to your applications. Audience confirms nobody does this today. The takeaway: you must **separate those boundaries**.
3. **Cold start** — when an agent makes a tool call (run a script, swarm to other agents), it shouldn't take a minute per agent just to wait on infrastructure to come up.
4. **Long-running tasks & state** — agentic infra isn't just for short "run code then disappear" tasks. Long-running work needs **state preservation** via **snapshots** and the ability to **restore to a previous point**.
5. **Hand-stitched tooling** — because the space evolves so fast, tooling is often manually glued together.

### The Announcement: Azure Container Apps Sandboxes
**Azure Container Apps Sandboxes** — a **private preview** of **fast, isolated, and stateful infrastructure on demand**. Available now at **`sandboxes.azure.com`** (sign in and create a sandbox today).

Core properties:
- **Executes your code securely** (isolated from your application).
- **Resumes instantly** from snapshot.
- **Snapshots not just disk, but also memory.**
- **Burst to hyperscale.**

**Already in production internally:**
- **Microsoft Foundry** hosts its **hosted agents** on ACA Sandboxes.
- **GitHub Sandboxes** use the same technology.
- **Azure Container Apps Express** — an agent-first technology introduced recently that provisions in a couple of seconds and **scales from zero to one in ~a second**.

### The Demo Architecture: The "Content Factory" (Three Agents, Three Frameworks)
The promised three agents:
1. **Researcher agent** — researches a specific topic. Built with **LangChain (Python)**.
2. **Creator agent** — takes the researcher's output and **creates content**: a blog, an article, social posts. Built with **Microsoft Agent Framework**, coded in **C#**.
3. **Podcast/Narrator agent** — creates an **engaging podcast** from the content. Built with the **GitHub Copilot SDK**.

Why three different frameworks? Because that's how projects really happen in orgs — **from the grassroots**, with people using different technologies.

**Note on GitHub Copilot SDK:** the speakers recommend trying it as the **harness layer** — "very easy to get started." Importantly, they use **bring-your-own AI model**: they are **not** using the LLM behind GitHub Copilot, but **one of the Foundry models** instead.

**Higher-level topology:**
- On the left, an **orchestrator** manages the workflow between the three agents — this is the component the user interacts with.
- The three agents connect to **Microsoft Foundry** because they use Foundry models.
- Goal #2 of the demo: show how to bring **three diverse models into one management plane** — manage and observe them from **Foundry + Application Insights**.

**How observability works:** **OTel (OpenTelemetry)** is the key. All three agents **and** the orchestrator emit **detailed OTel telemetry**, so you always know what's going on. **All components run on Container Apps.**

**Repo / QR code:** `aka.ms/aca-build2026-demo312` (shown throughout the session).

### Demo Twist: Football (not "Soccer") Match Simulator
Rather than a boring "what is Container Apps?" demo, the presenters — football fans, Vinnie "made in Mexico," Jan "made in Czechia" — build a **competitive game simulator: a Mexico vs. Czechia football match simulator** (corrected from "soccer" to "proper football" after an audience heckle).

**The simulator UI** has **four built-in prompts** plus custom prompt support:
- A default prompt (already started).
- "What if this player plays and this other doesn't?"
- "What if it turns out to be a defensive battle?"
- "What if this Czechia player is in the best form of his life?"
- Or write your own.

### How It Works Behind the Scenes (Dynamic Sandbox-per-Call)
- There are three agents; the **researcher/simulator agent** decides to fire a number of **web searches** to gather info.
- For this demo, the agent **writes Python code** to fetch information: **lineups, latest news, injury reports**, etc.
- **That code runs in sandboxes.** Each query **fires up a new sandbox**, sends the Python code, runs it, retrieves the result — then **fires another sandbox to run the simulation**.
- The **simulation** takes all gathered info, passes it to an **LLM** (another LLM call), and that produces how the match went.

**Critical point (recap):** these sandboxes were **NOT provisioned during deployment**. It runs on Azure (you can `azd up` it), but the **simulator agent dynamically creates these resources / infrastructure at runtime** and keeps them up **as long as needed**.

The first live run returns a (boring/"wrong") **2–2** result; pre-cooked resources are used in the interest of time. They note simulation results "should be reviewed by an expert."

### Sandbox Lifecycle, Idle Snapshots & Sub-Second Resume
- In the sandbox UI, each **blue line item = one sandbox** that fired with a **specific purpose** → **one [goal] ≈ one sandbox ≈ one piece of infrastructure** running code from the main agent.
- Example shown: a very simple sandbox that **fetches the roster for Czechia**.
- Sandboxes **have no name** because they're **managed by code / by the agent** — you search by purpose/identifier.
- A shown sandbox is already **idle**, meaning it **automatically took a snapshot and is sleeping** → **you're not paying for compute** while idle.
- **Lifecycle policy:** you decide how long sandboxes stick around, and — more importantly — you can **resume** them. When idle, there's a **persistent snapshot** (per your snapshot policy; in this case **memory + filesystem**). **Resume is sub-second** ("definitely sub-second").

### Security Feature 1: Egress Policy (Network Control)
- One of the sandboxes ran web research. A key feature is the **egress policy** — controlling outbound network traffic **per sandbox**.
- Demoed: **blocking certain URLs** (e.g., `skysports.com` — "nothing against" it, just for the demo) and a **deny** list of three sites.
- You can configure egress either way:
  - **Deny-all + whitelist** specific destinations, OR
  - **Allow + denylist** specific destinations.
- "All the features you'd expect from a sort of egress policy."

### Security Problem: Don't Give Secrets to Agent Code
- When a sandbox **runs the simulation**, it runs an **agent inside the sandbox**, which must **call the LLM**.
- **Naïve approach:** put the API key in an **environment variable**. Demoed as a trap: the code logs the request, and inspecting the log shows the **API key was visible to the AI-written code**. "This is not very good." / "Why would you give your secrets to the LLM?"

### Security Fix: Managed Identity + Egress "Transform"
Two complementary fixes:
1. **Managed identity** — because all sandboxes **run within Azure**, you can use **managed identity** to securely access Azure services (**Cosmos, Foundry, Azure OpenAI**) **without** handing an API key to the agent code.
2. **Egress "transform" policy** (for non-Azure services that still need a secret/API key):
   - A second simulation used a **"secure egress"** checkbox.
   - The **same code** ran, but **the API key was NOT present / not available** to the agent-written code — yet the simulation **still succeeded**.
   - **Why it worked:** the **transform** egress policy. A **secret is defined for the sandbox**, and the egress policy is configured to **inject that API key as a header on outgoing calls to a particular endpoint**.
   - **Architecture:** the **egress gateway lives OUTSIDE the sandbox infrastructure** — it's a *different* piece of the platform than the part that runs your code. The egress component has the **final say** on outbound calls. Before the request leaves, the **egress gateway intercepts and modifies the call** (injecting the secret). The sandbox code **literally has no access** to the secret.

### Content Output: Blog + Narration
- After the simulation, the other agents run:
  - The **blog agent** wrote a **blog post about the match**.
  - The **narration agent** produced an **AI-generated audio narration**. Because **Mexico won** this run, they play the **full narration** (excited play-by-play featuring Jorge Sánchez, a cross, Orbelín Pineda, and a goal by Santiago Giménez; "the Aztec drums are thundering... but Czechia is not here to roll over").
- Point: this showcases what's achievable with **Foundry TTS models** — it's **all AI-generated** — "just how big you can dream" to augment your applications.

### Observability Deep Dive (Foundry + App Insights)
- Not shown how it's configured live, but: because they use **OpenTelemetry to instrument all agent calls**, they use the **built-in OTel collector**.
- **Pipeline:** different container apps **stream telemetry → OTel collector → Application Insights → visible in Azure Portal AND in Foundry.**
- In **AI Foundry**, you can **register all these agents** regardless of technology — as long as they **talk A2A** or share **some contract** between them. Then you can **manage them, run continuous evaluations, and observe insights.**

### Recap & Where to Learn More
What was shown: the **workflow across three different agents**, **secure code execution in ACA Sandboxes**, **Azure OpenAI API keys stored securely outside the running sandbox**, **idle/snapshotted sandboxes brought back fast**, and **end-to-end observability + management in Foundry**.

Takeaways emphasized:
- **Sandboxes run code safely** — not next to your application, but in **physically different infrastructure**.
- **API keys live outside the sandbox** (the sandbox code has no access).
- **Idle sandboxes snapshot** and come back to life quickly.

**Calls to action / pointers:**
- Meet the ACA team at **booth #44** (other pavilion).
- **All ACA announcements:** `aka.ms/aca/build`.
- **Breakout session at 2:45** — more demos (their colleague **Simon** talks to an agent) plus a **customer use case**.
- **Get started today:** go to **`sandboxes.azure.com`**, create a sandbox (e.g., with **Copilot**), and start writing **right from your browser immediately**.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Container Apps (ACA)** — the platform all components run on.
- **Azure Container Apps Sandboxes** *(private preview)* — fast, isolated, stateful, on-demand infra at `sandboxes.azure.com`.
- **Azure Container Apps Express** — agent-first tech; provision in seconds, scale 0→1 in ~1 second.
- **Microsoft Foundry / AI Foundry** — model hosting, management plane, agent registration, continuous evaluation, observability; also **Foundry models** and **Foundry TTS models**.
- **Microsoft Agent Framework** — used (in **C#**) for the creator agent.
- **LangChain (Python)** — used for the researcher agent.
- **GitHub Copilot SDK** — used as the harness for the narrator agent; supports **bring-your-own-model**.
- **GitHub Sandboxes** — internal consumer of the same sandbox technology.
- **OpenTelemetry (OTel)** + **built-in OTel collector** — telemetry instrumentation.
- **Azure Application Insights** — telemetry sink, visible in Azure Portal + Foundry.
- **Managed Identity** — secure, keyless access to Azure services (Cosmos, Foundry, Azure OpenAI).
- **Azure OpenAI** — LLM endpoint called from sandboxes.
- **Azure Cosmos DB** — example service accessible via managed identity.
- **A2A (agent-to-agent)** — interoperability contract enabling cross-framework agent registration in Foundry.
- **Egress policy** (allow/deny lists) and **egress "transform"** (header/secret injection via egress gateway).
- **`azd` (`azd up`)** — used to deploy the demo to Azure.
- **Snapshots** — memory + filesystem; enable idle suspend and sub-second resume.

## 🚀 Announcements / What's New
- **Azure Container Apps Sandboxes — Private Preview.** Fast, isolated, and stateful infrastructure on demand. Securely executes code, resumes instantly, snapshots **disk + memory**, and bursts to hyperscale. Available at **`sandboxes.azure.com`** today. Already used internally by **Microsoft Foundry hosted agents**, **GitHub Sandboxes**, and **Azure Container Apps Express**.
- **Egress controls for sandboxes:** per-sandbox **egress policy** (deny-all+allowlist or allow+denylist) and an **egress "transform"** capability that injects secrets as headers via an out-of-band egress gateway, keeping API keys out of agent-written code.
- **Demo source code released:** `aka.ms/aca-build2026-demo312`.
- **Aggregated ACA Build announcements:** `aka.ms/aca/build`.

## 💡 Demos
- **The Agentic Content Factory (orchestrated 3-agent pipeline):** researcher (LangChain/Python) → content creator (Microsoft Agent Framework/C#) → podcast narrator (GitHub Copilot SDK), coordinated by an orchestrator, all wired to Foundry models and emitting OTel telemetry.
- **Mexico vs. Czechia football match simulator** (the headline live demo):
  - UI with 4 built-in prompts + custom prompts.
  - Simulator agent **writes Python**, fires **one sandbox per web query** (lineups, news, injury reports), then a **separate sandbox runs the simulation** via an LLM call.
  - Sandboxes are **created dynamically at runtime** (not at deploy), kept alive only as needed.
  - First run returned **2–2**; a pre-cooked run produced the "proper" simulation.
- **Sandbox lifecycle demo:** show idle sandboxes (auto-snapshotted, not billed) and **sub-second resume** from a memory+filesystem snapshot.
- **Egress policy demo:** blocking specific URLs (e.g., `skysports.com`) per sandbox with deny lists.
- **Secret-leak demo + fix:** show API key visible in agent code via env var (bad), then show **secure egress / transform** making the key invisible to code while the call still succeeds.
- **AI-generated narration playback:** full play-by-play audio of the match (Santiago Giménez goal for Mexico) generated by **Foundry TTS models**.
- **(Referenced, not configured live):** observability pipeline streaming OTel → collector → App Insights → Azure Portal + Foundry, with agent registration/management in Foundry.

## 📊 Notable Stats / Quotes
- **"Gartner is predicting that 40% of agentic projects will be canceled by 2025... not because the agents or the LLM cannot keep up [but] because of high risk, lack of governance, and that the runtime is breaking."**
- **Scale-from-zero:** ACA Express provisions in "a couple seconds" and scales **"from zero to one [in] around a second."**
- **Resume speed:** snapshot resume is **"definitely sub-second."**
- **Match result:** first (incorrect) run **2–2**; "proper" pre-cooked simulation → **Mexico won**.
- **"One [goal] equals to one sandbox... equals to one infrastructure that runs the code from the main agent."**
- **"Why would you give your secrets to the LLM?"** — on the API-key-in-env-var anti-pattern.
- **"The egress gateway lives outside of the sandbox infrastructure"** — the code "literally has no access" to the secret.
- **Narration:** *"The stage is set. Mexico against Czechia. Two prideful nations clash... Santiago Giménez. Mexico rises. The crowd is enraptured. The Aztec drums are thundering. But Czechia is not here to roll over."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Sign in at `sandboxes.azure.com` and spin up a Copilot-enabled sandbox from the browser.
  - Clone and run the demo: `aka.ms/aca-build2026-demo312` (`azd up`).
  - Build a sandbox that calls an LLM **without** an API key in code — first via **managed identity** (Azure OpenAI), then via **egress transform** (non-Azure endpoint).
  - Try **GitHub Copilot SDK** as an agent harness with **bring-your-own Foundry model**.
  - Wire up OTel → collector → App Insights and register cross-framework agents in **Foundry** via A2A.
- [ ] Questions:
  - Pricing/billing model for idle (snapshotted) vs. active sandboxes — exactly what's metered?
  - What are the snapshot size/retention limits, and how granular is the lifecycle/snapshot policy?
  - GA timeline and region availability for ACA Sandboxes beyond private preview.
  - Egress "transform" — which auth schemes/header formats are supported beyond simple header injection?
  - How does cold-start latency compare for the *first* sandbox of a call chain vs. a resumed one?
  - What isolation guarantees (kernel/VM-level?) back the "physically different infrastructure" claim?
- [ ] Relevant to:
  - Any project running **AI-generated / untrusted code** that needs strong isolation + lifecycle controls.
  - **Multi-agent orchestration** efforts mixing frameworks (LangChain, Agent Framework, Copilot SDK) under one Foundry management plane.
  - **Cost governance** for agentic workloads (idle snapshot → no compute billing).
  - **Secrets management / zero-secret-in-code** patterns (managed identity + egress transform).
  - **Observability** standardization on OpenTelemetry → App Insights → Foundry.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[Azure Container Apps]]
- [[Microsoft Foundry]]
- [[Multi-agent systems]]
- [[Microsoft Agent Framework]]
- [[LangChain]]
- [[GitHub Copilot SDK]]
- [[OpenTelemetry]]
- [[Managed Identity]]
- Demo repo: `aka.ms/aca-build2026-demo312`
- ACA Build announcements: `aka.ms/aca/build`
- Sandboxes: `sandboxes.azure.com`