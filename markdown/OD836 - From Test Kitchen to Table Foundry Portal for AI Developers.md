---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/foundry
  - topic/ai-portal
  - topic/ai
  - topic/agents
  - topic/models
  - topic/evaluation
source: https://www.youtube.com/watch?v=vcBF4XPE6I8
session_code: OD836
event: Microsoft Build 2026
speakers: Carlotta Castelluccio, Nitya Narasimhan
duration_min: 79
aliases:
  - From Test Kitchen to Table Foundry Portal for AI Developers
---

# OD836 — From Test Kitchen to Table: A Demo-driven Tour of Foundry Portal for AI Developers

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Carlotta Castelluccio (Senior AI Advocate, Microsoft — Core AI DevRel, based in Lecce, Italy) & Nitya Narasimhan, PhD (Senior AI Advocate, Microsoft — Core AI DevRel)  
> **Duration:** ~79 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=vcBF4XPE6I8)

## 🎯 TL;DR
A 79-minute, almost entirely live-demo session that walks through the **Microsoft Foundry portal** (`ai.azure.com`) as a "test kitchen" for building agentic AI apps **without writing a single line of code** in the browser. Using a fictitious DIY retailer **Zava** and a shopping-assistant agent called **Kora**, the speakers build an agent from scratch and iteratively improve it: create a Foundry project → spin up a default agent (GPT-4.1 + web search) → add tracing/observability via App Insights → compare 11,000+ catalog models with the **leaderboard / trade-off chart** and swap to a cheaper-but-better **GPT-5.4 Nano** → use **model router** for automatic model selection → improve **instructions** (with a prompt optimizer) → **ground** the agent in Zava product manuals via file upload/vector index → write **custom evaluators** (prompt-based LLM-as-judge + code-based) → run **batch evaluations** on synthetic test data → run a **red teaming** adversarial scan → and **monitor** the fleet via the operate tab. The core message: agents are like **microservices**; Foundry portal is the **low-code inner-loop** where you rapidly prototype, evaluate and govern before graduating ("test kitchen → table") to a **pro-code** path in VS Code with the Foundry SDK + Foundry toolkit + GitHub Copilot for Azure.

## 🔑 Key Takeaways
- **Foundry portal = low-code "test kitchen."** You can author, configure, test, evaluate, red-team and monitor a production-shaped agent end-to-end in the browser at `ai.azure.com` before ever touching code.
- **Agentic AI is a microservices mindset.** Each agent is a single, independently-evolvable unit of work, so you can update one agent without re-deploying the whole monolithic application.
- The portal mirrors a **three-phase development journey** — **Design** (use case, model exploration, prototype with tools+knowledge, tracing) → **Optimize / Build** (move to code, dev container, evaluate behaviour, publish) → **Govern / Operate** (safety, integration, monitoring/regression). It's an **iterative loop**, not linear; you frequently move right-to-left.
- A new Foundry project **auto-provisions** sensible defaults: a **GPT-4.1** model deployment, a **text-embedding-3-large** deployment (for future RAG), and a starter agent with a **web search** tool — guided, click-through creation of resource group → Foundry resource → Foundry project → agent.
- **Tracing requires App Insights.** Connecting an Application Insights + Log Analytics workspace (one click) lights up traces/responses, evaluation scores per response, tool-call inspection, and input/output metadata — and you can still see traces logged *before* you connected it.
- **Evaluation-driven development:** use traces + per-response evaluation scores (quality + safety metrics, LLM-as-judge) to spot a regression/gap, diagnose it, and iterate. Metrics can be numeric (e.g. coherence 5/5) and/or pass-fail with thresholds.
- **Versioning is first-class.** Every config change can be saved as a new agent **version** (v1, v2, v3…), and **Compare versions** runs two versions side-by-side on the same prompt so you can see behaviour, logs and eval scores diff in real time.
- **Don't over-spec the model.** GPT-4.1 is feature-rich but expensive — "don't get a cordon-bleu chef to make the salad." The **leaderboard** ranks 11,000+ catalog models on quality/safety/throughput/cost; the **trade-off chart** plots cost-vs-quality so you find the cheapest model that meets your bar.
- In the demo, **GPT-5.4 Nano** matched GPT-4.1's quality at far lower cost with better throughput and safety — a clear "why would I not switch?" moment. Deploying a model from compare-view drops you in the **model playground** (vs the **agent playground**).
- **Model router** is an intelligent meta-model: you point your agent at it, and it auto-selects the right backend model per prompt complexity (trivial → GPT-5 mini; complex reasoning → GPT-5). Over time it reveals which models your workload actually uses so you can pick a sensible default.
- **Grounding via file upload** is trivial: upload product manuals → portal builds a **vector index** + exposes a **file search** tool → the agent answers from *your* data (Zava catalog) and cites the source document.
- **A prompt optimizer** and detailed, structured instructions dramatically change response quality/tone (friendly greeting, emoji, concise, ends with an offer to help) — "the more detailed the recipe, the more consistent the dish."
- **Custom evaluators** come in two flavours: **prompt-based** (LLM-as-judge, ideal for subjective/intangible criteria like "friendliness/politeness") and **code-based** (deterministic functions, ideal for measurable things like conciseness/length — don't waste an LLM on it).
- **Synthetic data generation** is built in: the portal can generate test prompts (single/multi-turn, edge cases like out-of-stock/returns) so you can run a **batch evaluation** against an agent version even before real users exist; batch evals can run **continuously**.
- **Red teaming** is part of the evaluation suite: a red-team agent acts as a malicious user, applying **attack strategies** (e.g. **flip** = reversed string to slip past filters; **tense** = phrasing a harmful ask as past/hypothetical, "what would my grandma have said?") across chosen **risk categories** (violence, sensitive-data leakage, task adherence…) and reports which got through.
- **"Ask AI" / agent helper** is an in-portal expert: it inspects your project + state and explains things like "what does a coherence score of 4 mean?" with links to docs — your on-call sous-chef.
- **Observability = traces + evaluation + monitoring.** Traces show a single call's execution; evaluation assesses response quality/safety; **monitoring** surfaces operational metrics (total calls, cost, token usage, failures) per agent.
- The **operate tab** gives a fleet-level view across *all* agents in the project (e.g. the retail agent + the auto-routing agent) — cost, success/fail counts, token usage — then drill down per agent. Foundry isn't just build+deploy, it's **maintain a fleet at scale**.
- **Test kitchen → table:** when the recipe passes, click **View sample app code** to grab env vars + sample app, move to **VS Code**, and continue **pro-code** with the **Foundry SDK** (Python/JS/Java/.NET), the **Foundry toolkit** extension, **Foundry skills**, **GitHub Copilot for Azure** and the **Azure Developer CLI** — "agents helping you build agents."

## 📚 Detailed Notes

### Framing: the business scenario (Zava + Kora) and why agentic AI
Nitya opens with the standing principle that **every AI development journey starts with a business scenario**. The running example is **Zava**, a *fictitious enterprise retailer* selling home-improvement goods to DIY enthusiasts. "You" are on the AI dev team, tasked to build **Kora**, an AI shopping assistant that answers customer questions in-store or online and provides customer service. Design goals for Kora: **friendly, helpful, and cost-effective to deploy**, and — critically — able to **keep adapting** to changing conditions, systems and needs.

At the most basic level, an AI app is just **a model that takes a prompt, processes it, and generates a response**, where the response can trigger further actions that generate new prompts, and the cycle continues. That's a **monolithic** app: a single model with coordination glue around it. But **at scale** you have many models, many prompts, many concurrent conversations, plus the need to extract information from all of them to decide what to do next. A monolith can't do that agilely.

**This is where agents help.** Agentic AI brings a **microservices-based approach**: every agent is a **single unit of work that evolves independently** without rewriting the whole system. With a large application you can update/evolve **individual agents** in isolation rather than re-architecting and redeploying everything. To make that repeatable and simple you need a **"test kitchen"** — somewhere to quickly prototype these small agents before promoting them to production.

### The "test kitchen → table" analogy
The central metaphor: think of your AI solution like a **multi-course dinner menu at a popular restaurant**. You don't design recipes at the dinner table — great chefs use a **test kitchen** to rapidly experiment until a recipe passes their **taste test (evaluation)**, then move it into the **restaurant kitchen (code-first environment)** to make it better. **Microsoft Foundry portal is your test kitchen**: you go from plan → basic prototype → a recipe that works, **without writing a single line of code, all in the browser**.

### Three developer needs Foundry meets
Nitya frames Foundry around three needs:
1. **Rapidly prototype, build, and deploy** agents (microservices approach) so real customers can try them.
2. **Easy experimentation & evaluation** — because models, prompt requirements and the environment *will* change, you need to test prompts/models/datasets **without re-provisioning each time**.
3. **Trustworthy, production-ready development** — secure, scalable mechanisms, delivered as a **unified end-to-end platform**.

### What Microsoft Foundry does (Carlotta's platform overview)
Carlotta deepens the end-to-end story. Microsoft Foundry lets you:
- **Orchestrate multi-agent systems** with support for **interoperability and open frameworks**.
- Access the **best foundational and open-source models** via the **model catalog**, and find the best-fit model for a use case.
- **Connect agents to knowledge sources and tools** using built-in features to **contextualize AI responses** and let AI **take actions on behalf of the user**.
- **Continuously evaluate** across every stage of the AI lifecycle, with **content safety and security** in every layer.
- **Tune and customize** apps/agents continuously to fit business needs.
- **Deploy anywhere**, including **local and edge devices**.

She notes the session will cover *most* of this (the "green points" on her slide: **models, knowledge & tools, and observability** fully covered in the hands-on demo; **deployment** touched briefly). The portal is a **low-code solution**: experiment with models, tools and instructions for a single agent in a **browser-based playground**, with **built-in observability** (traces, evaluations, monitoring) to accelerate **inner-loop ↔ outer-loop** transitions, iterate quickly, and deploy comparable versions in real time — then move **seamlessly to code-first** environments for multi-agent solutions, more complex frameworks/workflows, and further customization. "From the test kitchen to the restaurant."

### The three-phase journey baked into the portal
The portal is structured to mimic three phases, each with the features/tools you need:
- **Design** — identify the business use case, do **model exploration**, test domain prompts across models for comparison, and **build the agent prototype** equipped with the right **tools and knowledge**. Throughout, maintain **robust tracing** to debug, inspect issues, and address them with fine-tuning/customization.
- **Optimize / Build** — once a prototype is ready, **move into code** (e.g. host in a **dev container**), **evaluate overall agent behaviour**, and **publish**. After each step (build, optimize) ask: *is this ready to move to the next phase?* — judged via traces, evaluation results and metrics you define.
- **Govern / Operate** — **safety**, **application integration**, and **shipping**; making the app production-ready with everything needed to **monitor regressions over time**.

Crucially this is **a loop, an iterative process — not linear**. You'll often move right-to-left for further model/prompt/agent customization and re-run evaluations: continuous improvement.

### Demo 1 — Creating a Foundry project & first agent (Carlotta)
Starting point: `ai.azure.com` (the Microsoft Foundry portal). The `/templates` view offers **solution templates** (AI chat app, AI agent app, multi-agent workflow, etc.) so you don't have to start from scratch — pick the one closest to your scenario. Alternatively, click **Start building** to create your **first Microsoft Foundry project** — your **workspace** where you create and manage all resources relevant to your AI app.

Flow demonstrated:
1. **Create a new project**, give it a name; under **Advanced options** configure subscription, Foundry resource name, **region**, and the **resource group** name. Click **Create** and wait a couple of minutes.
2. Switch to the **Azure portal** to watch the **resource group** appear, containing a **Foundry resource** and a **Foundry project** (created via the portal UI). The next screen exposes the **API key, project endpoints, and credentials** you'd need to connect via code.
3. Click **Create agent**. The guided flow has now created: resource group → Foundry resource → Foundry project → agent — all click-through.
4. Name the agent (`retail-based agent`, per the Zava scenario). On creation, the portal **auto-deploys GPT-4.1** (the default model engine) **and** a **text-embedding-3-large** instance (because most agents will need a **RAG** pattern and thus an embedding model).

### Demo 2 — The agent playground & default tools
The flow lands in the **agent playground**. The agent (`retail-based agent`) exposes configurable components:
- **Model** — default **GPT-4.1**.
- **Instructions** — empty by default.
- **Tools** — default **web search** (so the agent can pull fresh data from the web). You can add other **built-in tools**, e.g. **code interpreter** (executes code in a **Python sandbox**), browse **all tools**, and use tools exposed by **MCP servers**.
- **Knowledge** — add knowledge sources, connect to **Foundry IQ** (e.g. "Zava IQ" = the enterprise's knowledge).
- **Memory** — **agentic memory** so the agent retains memory across sessions for the same user.
- A **chat UI** on the right to test the agent immediately.

Under **model deployments** you can confirm the auto-provisioned **GPT-4.1** + **text-embedding-3-large**. Testing the raw agent: "what can you do?" → generic answer (nothing customized but the name). "what paint should I use for my outdoor deck?" → still generic, based on training data + web (since web search is on).

### Demo 3 — Tracing & observability (connect App Insights)
To **debug** the agent (double-check what's happening, catch errors/hallucinations), open **Traces**. But trace collection requires an **Application Insights** resource — not present by default. Click **Connect → create a new resource** to spin up **App Insights + a Log Analytics workspace** in the resource group (both then appear in the RG). Now in **Traces → Responses** you can see the conversation traces — *including traces logged before App Insights was connected* (they aren't lost).

In a trace you can inspect: **user input, user output, input/output message metadata**, and **tool call details** when a tool was invoked. You can also view **evaluation scores** per response — but first pick metrics under the **metrics drop-down** (the demo selected **task adherence, intent resolution, coherence, relevance, and attack/safety**). Then under **Logs → Evaluations** you see how the **LLM-as-judge** (AI-assisted evaluation) scored that specific response. Example: **coherence 5/5** with a **verbatim reasoning** explanation. Some metrics are **pass/fail** only; others (relevance, coherence) have **both a numeric score and a pass/fail threshold**. This enables **evaluation-driven development**: spot a gap (in logs/traces or eval results) → troubleshoot → address.

A second prompt demonstrates tool-call tracing: a **weather-forecasting** question (so a Zava customer can decide when to do an outdoor/painting DIY project). The trace's **Logs** show the **web search** tool was invoked to retrieve the weather data, plus the tool-call metadata. Takeaway: with zero extra customization — just the guided portal flow — you already have a working agent (model + pre-built web-search tool) testable in the playground, all integrated into the **quick-start experience**.

### Demo 4 — Versioning & comparing versions
Carlotta edits the **instructions** to: *"You are a friendly assistant for Zava retail. Ask the user when they are planning to do their DIY project and which city they are in, so you can check weather and advise them when to plan their project."* **Save** creates **v2**. **Compare versions** opens a side-by-side playground: same prompt against **v1** (generic response) vs **v2** (now asks the follow-up about *when* and *which city* before advising). You can inspect **logs and evaluation scores on both sides** to see if v2 improved or regressed.

### Demo 5 — Preview as a web app
To share a preview with **bug-bashers/testers**, click **Preview → Preview agent** to get a **web-app UI** of the agent. Under **Configure** you can customize it: a **display name** ("Zava retail agent"), a **description** ("this agent is the Zava retail assistant"), and **starter prompts** (e.g. "what's the weather like in Lecce today", "what paint should I use for my outdoor deck"). Saving and re-opening **Preview agent** shows the customized layout with starter prompts. Note: the **preview web app shows no developer logs/traces/evaluation results** — it's the **end-user view**, distinct from the developer playground. (Carlotta hands off to Nitya here; the prototype is built and tested.)

### Demo 6 — Improving the MODEL: leaderboard, trade-off chart, compare (Nitya)
Nitya re-configures and saves the agent as **v3** with a display name, description and **three** starter prompts — deliberately keeping the *same* prompts across iterations so each version is tested against a consistent set. The retail agent can now (roughly) answer weather, Zava products, and home-improvement questions — but it isn't perfect (not really using Zava data), and it defaults to **GPT-4.1**, a **feature-rich large model**. Analogy: *"getting a cordon-bleu chef to make the salad"* — you want a **cheaper model for the simplest task**.

How to find the best model:
- The model drop-down shows a few **popular models** (GPT-4.1, **model router**, GPT-4o, 4.1 mini, o4…), but switching to the **Discover** tab reveals the full **model catalog — 11,000+ models**.
- **Leaderboard**: a Foundry feature that runs **benchmarks** on catalog models and ranks them across **quality, safety, throughput, and benchmark cost** via pre-built charts. Scrolling shows where models sit; GPT-4.1 appears near the bottom — useful but a lot to parse.
- **Trade-off chart** (same tab): clear all models, add the default **GPT-4.1** (sits in a corner), then add candidates — **GPT-5.4**, a **nano** model, **GPT-5.4 mini**, **GPT-5.4 Nano**, **4.1 mini**, an **o3**, a **DeepSeek** model. Plotting **cost vs quality** reveals GPT-4.1 is **high-cost / low-quality**, whereas **GPT-5.4 Nano** delivers the *same quality at much lower cost*. (Nitya notes metrics are **re-evaluated daily** by the Foundry team based on current models, so your exact chart may differ — it's a *comparative* view.) You can also plot quality-vs-throughput or quality-vs-safety.
- **Compare models**: narrow to **GPT-5.4 Nano vs GPT-4.1 vs 4.1 mini** for a direct comparison. **GPT-5.4 (Nano)** earns *"all the gold stars,"* beating 4.1 on every criterion — comparable quality, lower cost, better throughput, better safety. From compare-view click **Deploy this model into my current solution**.

Deploying a model from compare-view drops you in the **model playground** (not the agent playground) — the criteria just says "you're an assistant." The new **GPT-5.4 Nano** now appears in the project's **deployed models**, so you return to the agent and switch it from GPT-4.1 to GPT-5.4 Nano and save (this is **v6**; v5/v6 differ *only* in model). Comparing **v6 (GPT-5.4 Nano)** vs **v5 (GPT-4.1)** on "what's the weather in San Francisco": GPT-4.1 used fewer tokens / slightly less time but lower quality; GPT-5.4 Nano gave full quality (cost varies per query). Another test ("what tools do I need to build a kitchen island?") confirms Nano is the **cheaper** pick. Nitya keeps Nano but flags the response is too verbose / not concise/friendly enough — next step is instructions.

### Demo 7 — Model router (intelligent auto-selection)
A short detour: **model router** is a distinct Azure Foundry "model" that looks/feels like any other model — you send a prompt and **it figures out the right backend model**. Why it matters: instead of one fixed model (great if you know your use cases), real workloads have **questions of varying complexity** — how do you pick the right model per query? Deploy model router and let it show you which models it uses.

Demo: deploy **model router** from Discover → Models → it sets up in the **model playground**. Because deploying a model in the playground lets you **save it as an agent**, Nitya creates an **"auto-routing agent."** She copies the retail agent's instructions in, saves, and fires increasingly complex prompts:
- "what is the capital of France?" → router judges it **trivial** and routes to **GPT-5 mini** (a cheap model).
- "I want to build a patio during summer for a family of five with plants that grow… draw me up a plan of action" → a **complex reasoning** task → router escalates to a **higher-performance model, GPT-5**, returning a comprehensive minute-long, token-heavy plan.
Key point: she **never changed the model/route** — model router handled it. Analogy: it's the **"kitchen organizer"** — *"this task, who in the kitchen would be good for it?"* Run it over time and you learn which models your tasks actually use, then set a sensible default.

### Demo 8 — Improving INSTRUCTIONS (+ prompt optimizer)
Back to the retail agent: the model's fine now, but responses are too long/verbose. Just as in a recipe, **detailed instructions** → consistent output — you must define *what* the agent does, *when*, and *how*. Nitya replaces the generic instructions with a **comprehensive instruction set** (and notes a built-in **prompt optimizer** is available to help write them). Saving creates **v7** (on GPT-5.4 Nano). **Comparing v7 vs v6** on "what's the weather in San Francisco": **v7 responds exactly as intended** — a **friendly greeting with an emoji**, a helpful tone, concise, and **ends with an offer to help** ("how else can I help you?"). Changing instructions improved **response format and quality** in seconds — *"the more detailed the recipe, the more consistent the dish."*

### Demo 9 — "Ask AI" / agent helper (your in-portal expert)
Nitya still sees quality/safety not fully passing (e.g. coherence **4/5** — *"why a 4 and not a 5? and what does coherence even mean?"*). Foundry's **Ask AI** (the **agent helper** button) answers in-context: ask *"what does coherence mean and what does a rating of 4 imply?"* and it **inspects your project + current state** and replies with a plain-language explanation **plus links to the docs** — the expert sous-chef you consult mid-recipe without leaving the kitchen.

### Demo 10 — Improving TOOLS & KNOWLEDGE (grounding in Zava data)
The agent still isn't using **Zava data** — "what paint should I use for my outdoor deck?" / "what tools do I need to build a kitchen island?" return generic web info, **not Zava catalog** items, because it isn't **grounded**. Under **Tools** you can **Upload files** (other options: **Foundry IQ** integration for enterprise knowledge, or **agentic memory** for short-term memory). Nitya chooses **Upload files**:
- Create a new index — **"Zava retail index."** Upload ~**10** product manuals from a local repo; the portal **indexes them into a vector store / search index** and exposes a **file search** tool to associate with the agent.
- Add more: another ~10, then the last ~5 — **~25 products** total — enough for the demo. The agent now has a **product index** to consult whenever someone asks about home-improvement items, so it always returns **Zava data**.
- Save (**v9**). Re-ask "what paint should I use for my outdoor deck?" → **Tada** — it returns the **best Zava option *with a link to the source document*** it just uploaded, and reports it used the **file search** tool (verifiable in traces). The agent now returns a **valid, correctly-formatted response anchored in your data**, and explains *how* it found the info.

### Demo 11 — The evaluator catalog (what evaluations are)
Open the **Evaluations** area: a tab for **evaluation runs** plus an **evaluator catalog**. Back to the analogy — in a test kitchen you taste dishes against a recipe's requirements, so you need a **process to taste** and a **criteria/scale** to rank against acceptance criteria. Foundry ships **many built-in evaluators** in **four categories**:
- **Quality** — coherence, fluency, response quality, formatting, etc.
- **Safety** — violence, hate, and anything that might trip safety acceptance criteria.
- **Business** — business-oriented evaluators (mentioned briefly).
- **Agentic** (the most interesting for agents) — did the agent **resolve the user's intent**, **complete** the response, **adhere** to the task, call the right tools, etc.

### Demo 12 — Custom evaluators: prompt-based vs code-based
Nitya adds a **custom evaluator** — a **friendliness** evaluator that rates friendliness against provided criteria (a *quality* dimension). Two flavours:
- **Prompt-based** = another agent acts as **judge (LLM-as-judge)**; you write a **prompt** the judge uses as grading instructions to score the first agent's responses. Best for **intangible/subjective** criteria (e.g. "politeness/friendliness" — not a discrete, measurable value).
- **Code-based** = a **function** that takes the input and returns a **deterministic** result. Best for **measurable** things, e.g. **conciseness** = *"if length > 500 and < 5,000 chars then concise, else not"* — *"I don't need to waste an LLM on that."*

Building the friendliness evaluator (prompt-based, **1–5** rating): start from the **built-in example** (coincidentally a friendliness one) and replace the prompt with rubric levels — e.g. **1 = unfriendly/hostile** (swear words/rude language); **2 = unfriendly** (does not offer help); **3 = neutral**; **4 = mostly friendly** (starts with a cheerful greeting); **5 = very friendly** (does everything asked — cheerful greeting **and** ends with an offer to help, matching the agent's instructions). Click **Create** — it takes a moment to appear in the evaluator list. Friendliness can now be used as a **custom evaluator** to check every response against the instructions.

### Demo 13 — Batch evaluation on synthetic data
Testing a single prompt isn't real coverage. **Batch evaluations** run an agent against many prompts at once and can run **manually now or continuously**. Create an evaluation and **target the agent** (any **version** — here **v7**). Because it's a brand-new agent with no real user data yet, use Foundry's **synthetic data generation**: ask the portal to **generate test prompts** (dataset "synth-gen"), choosing a model to author them and the count (Nitya keeps it small — **10 prompts** — so the run finishes quickly), and optionally **generate candidate responses** too. The generation instruction: *"generate prompts for my Zava retail agent that represent customer-support queries for a DIY retail organization selling home-improvement goods; cover single- and multi-turn conversations and edge cases like out-of-stock or returns."*

The portal **suggests evaluators**; in the interest of time Nitya keeps a handful (**tool-call accuracy, task completion, task adherence**, a couple of **quality** ones, and a couple of **safety** ones). **Batch eval → Submit** kicks off a run where the **LLM-as-judge** invokes the test prompts against the actual agent, collects responses, and **grades** them against the chosen evaluators. (She didn't include the custom friendliness evaluator this run, but you could.) Every subsequent change can re-run the evaluation, so you **watch results improve across evaluation runs over time**.

### Demo 14 — Red teaming (adversarial safety scan)
If evaluators are the *"taste test,"* **red teaming** is the *"kitchen inspector"* — it checks whether your agent is **protected from malicious users**, and it's part of the **evaluation suite**. A **red-teaming run** assesses which risks you're vulnerable to: a **red-team agent pretends to be a malicious user** and attacks your agent with prompts engineered to trigger harmful behaviour.

Configuring a scan on the retail agent: pick the **risk categories** you think you're exposed to (e.g. **violence, task-adherence**, sensitive-data leakage), and the **attack strategies** — how the red-teamer tries to slip past the guardrails (a raw harmful prompt would just hit the content-safety filters):
- **Flip** — reverse the string; flipped, it doesn't read as harmful and may pass the filters, then a smart model re-flips and executes it. (A simple/easy attack.)
- **Tense** — reframe a harmful ask as **past/hypothetical** ("this happened in the past, it's no longer an issue," or "what would my grandma have said?") to argue it's harmless. (A slightly more sophisticated attack.)
For each category the red-team agent crafts **≥3 prompts** per strategy. **Submit** the scan. At this point the agent has been fully iterated — instructions rewritten, model swapped for a cheaper one, **file search** added for grounding, **custom + batch evaluations** run, and now a **red-teaming scan** — *all in the Foundry portal, never leaving the browser or writing a line of code.*

### Demo 15 — Monitoring & the operate tab (fleet view)
**Observability = traces + evaluation + monitoring.** Traces show a single call's execution; evaluation assesses how well responses meet quality/safety criteria; **monitoring** surfaces **operational/production metrics** — total number of calls, **cost**, **token usage**, **failures**, etc., per agent. But a single agent is just one microservice; a real solution has many. The **operate tab** (alongside Discover and Build) gives the **high-level project view across all agents** (e.g. the retail agent **and** the auto-routing agent): costs, success/fail counts, token usage — with **drill-down** into each agent's details. Foundry isn't only build+deploy; it helps you **maintain your whole fleet at scale.**

### Demo 16 — Reading completed red-team & evaluation results
Because the live runs are still in progress, Nitya switches to **pre-completed** examples:
- **Completed red-teaming scan**: for each **risk category** it reports **how vulnerable** the agent is, per the chosen strategies (flip + tense). Many prompts **passed**; for **failures**, the **attack prompt itself is hidden** (so you can't reverse-engineer/refine the attack), but the **response + reasoning** are shown. Example failure reasoning: the assistant discussed *"general emotional states associated with anticipation… presented in a general context without ascribing them to a specific group; no protected class was mentioned — it's not grounded, and that's why this is a failure."* Even a **simple flip attack** elicited a response it shouldn't have given; failures spanned violence, **sensitive-data leakage**, and task adherence.
- **Completed evaluation**: a **partial** result means it finished but **some evaluations failed and some errored** — which is actually useful: you can see **which failed** (e.g. **relevance** and **groundedness**), drill in, understand the nuance, then fix the instructions/tools/grounding and iterate until they pass. (Full per-row detail may require **downloading the results**.)

### Demo 17 — Graduating to code ("test kitchen → table")
The final step (mostly pointed to, given time): when the recipe passes, **move it to the restaurant.** Click **View sample app code** to get the **environment variables + sample app code**, drop it into **Visual Studio Code**, and work the *same agent* via a **code-first** approach. In VS Code you gain extra tooling: the **Foundry toolkit** extension, **Foundry skills** with **GitHub Copilot for Azure**, and the **Azure Developer CLI** (plus other CLIs) to build more complex, multi-agent solutions — *"agents helping you build agents."* (The session's GitHub repo includes a full **step-by-step workshop** to replicate every demo.)

### Wrap-up & the big picture
Nitya recaps: **Microsoft Foundry is your end-to-end platform** for building apps and agents from initial planning all the way to production — providing **models, agents, datasets, indexes, evaluation, tracing, fine-tuning, and more**. The **Foundry portal is just one client — the low-code one** — a place to experiment until you're comfortable graduating to code. From there you can use the **Foundry SDK** (Python, JavaScript, Java, .NET) or the **VS Code Foundry toolkit + Foundry skills + GitHub Copilot for Azure**. The overarching message: **enterprise agents are microservices** that orchestrate into larger applications; you need to **evolve/adapt them rapidly**, and the **portal is the low-code path** from plan → prototype → a recipe ready for the restaurant — plus a **managed surface to build, deploy and maintain your fleet at scale.** Carlotta closes by reiterating what was covered — **discover/explore/compare models**, **build an agent with knowledge & tools**, **bake in observability & agent controls from the very start of prototyping**, and **smoothly move to code** for further customization and cloud deployment — all in a **single unified portal** (which also supports **multi-agent orchestration** and **fine-tuning/model customization** not deep-dived here).

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — end-to-end platform for building/deploying/operating AI apps & agents (models, agents, datasets, indexes, evaluation, tracing, fine-tuning, etc.).
- **Microsoft Foundry portal** (`ai.azure.com`) — the **low-code** client / "test kitchen"; browser-based agent authoring, testing, evaluation, red teaming, monitoring.
- **Foundry project** — your workspace; manages all resources for an AI app (backed by a **Foundry resource** + resource group in Azure).
- **Solution templates** (`ai.azure.com/templates`) — starter templates (AI chat app, AI agent app, multi-agent workflow, …).
- **Agent playground** — configure Model / Instructions / Tools / Knowledge / Memory and chat-test a single agent.
- **Model playground** — where you land after deploying a model directly; deployments here can be saved as agents.
- **Model catalog / Discover tab** — **11,000+** foundational + open-source models.
- **Model leaderboard** — benchmark-driven ranking on quality / safety / throughput / cost (refreshed **daily**).
- **Trade-off chart** — plots models on cost-vs-quality (also throughput, safety) to find the cheapest model meeting your bar.
- **Compare models** — side-by-side criteria comparison; deploy directly from the view.
- **Model router** — intelligent meta-model that auto-selects the backend model per prompt complexity.
- **GPT-4.1** — default model auto-deployed with a new agent (feature-rich, higher cost).
- **GPT-5.4 Nano / GPT-5.4 mini / GPT-5.4** — newer models compared; **GPT-5.4 Nano** chosen (cheaper, better quality/throughput/safety than 4.1 in the demo).
- **GPT-5 / GPT-5 mini** — backend models the router escalated to (mini for trivial, GPT-5 for complex reasoning); **GPT-4o**, **4.1 mini**, **o3/o4**, and **DeepSeek** also referenced in comparisons.
- **text-embedding-3-large** — embedding model auto-deployed for future RAG.
- **Web search tool** — default built-in tool for fresh web data.
- **Code interpreter** — built-in tool that runs code in a **Python sandbox**.
- **MCP servers / tools** — tools exposed to the agent via Model Context Protocol servers.
- **File search tool + vector index/store** — built from uploaded files to ground the agent in your data (with source citations).
- **Foundry IQ** — knowledge integration (e.g. "Zava IQ") for enterprise knowledge.
- **Agentic memory** — cross-session / short-term memory for the agent.
- **Tracing / Traces (Responses & Logs)** — inspect inputs/outputs, message metadata, tool calls, and per-response eval scores.
- **Application Insights + Log Analytics workspace** — required to collect traces/telemetry (one-click connect).
- **Evaluators / evaluator catalog** — built-in evaluators across **Quality, Safety, Business, Agentic**; numeric and/or pass-fail with thresholds.
- **Custom evaluators** — **prompt-based** (LLM-as-judge) and **code-based** (deterministic function).
- **Synthetic data generation** — portal-generated test prompts (single/multi-turn, edge cases) for evaluation.
- **Batch evaluation / continuous evaluation** — run evaluators over a dataset against an agent version.
- **Red teaming** — adversarial scanning with **attack strategies** (flip, tense) across configurable **risk categories**.
- **Ask AI / agent helper** — in-portal assistant that explains metrics/state with documentation links.
- **Monitoring + Operate tab** — operational metrics (calls, cost, tokens, failures) and a fleet-level view across all agents.
- **Versioning + Compare versions** — save agent versions; diff two side-by-side on the same prompt.
- **Prompt optimizer** — built-in helper to improve instructions.
- **Foundry SDK** — code-first integration in **Python, JavaScript, Java, .NET**.
- **VS Code Foundry toolkit extension + Foundry skills + GitHub Copilot for Azure + Azure Developer CLI (azd)** — pro-code tooling for graduating from portal to code.
- **Session GitHub repo** — deck + step-by-step instructions + a workshop version of the demos.

## 🚀 Announcements / What's New
None explicitly announced. This is an **on-demand, demo-driven tour** of existing Microsoft Foundry portal capabilities rather than a launch/keynote session — no GA/preview status changes were called out. (It does showcase newer catalog models such as **GPT-5.4 Nano** and capabilities like **model router**, **Foundry IQ**, **agentic memory**, **synthetic data generation**, **custom evaluators**, and **red teaming**, but none were framed as new releases in this talk.)

## 💡 Demos
This session is **~90% live demo** in the Foundry portal, building one agent (Zava retail assistant / "Kora") end-to-end:
1. **Create a Foundry project & first agent** — guided flow (RG → Foundry resource → project → agent); auto-deploys **GPT-4.1** + **text-embedding-3-large**. *Shows: zero-to-agent in minutes, no code.*
2. **Agent playground tour** — Model / Instructions / Tools (web search, code interpreter, MCP) / Knowledge (Foundry IQ) / Memory + chat test. *Shows: the full agent config surface in-browser.*
3. **Tracing via App Insights** — connect App Insights + Log Analytics; inspect responses, metadata, tool calls, per-response eval scores; a weather prompt reveals the **web search** tool-call in logs. *Shows: observability/debuggability from day one (and retroactive traces).*
4. **Versioning + Compare versions** — v1 vs v2 side-by-side after editing instructions. *Shows: safe, comparable iteration.*
5. **Preview as a web app** — customized display name/description/starter prompts; clean end-user view without dev logs. *Shows: easy stakeholder/bug-bash preview.*
6. **Improve the model** — leaderboard, **trade-off chart** (cost-vs-quality), **compare models**; deploy **GPT-5.4 Nano**; compare v5 vs v6. *Shows: pick the cheapest model that meets quality — "don't use a cordon-bleu chef for the salad."*
7. **Model router** — an auto-routing agent escalates trivial → GPT-5 mini, complex → GPT-5. *Shows: hands-off model selection by prompt complexity.*
8. **Improve instructions (+ prompt optimizer)** — detailed instructions → friendly, emoji, concise, offers more help; v7 vs v6. *Shows: instruction quality drives response quality/tone.*
9. **Ask AI / agent helper** — explains "coherence 4/5" with doc links. *Shows: in-context guidance while iterating.*
10. **Improve tools & knowledge (grounding)** — upload ~25 Zava manuals → vector index + **file search** tool → answers from the Zava catalog **with source citation** (v9). *Shows: grounding the agent in your data.*
11. **Evaluator catalog** — quality/safety/business/agentic built-ins. *Shows: rich evaluation criteria out of the box.*
12. **Custom evaluators** — build a **friendliness** prompt-based (LLM-as-judge) evaluator from the example rubric; contrast with code-based (e.g. conciseness). *Shows: tailor evaluation to subjective vs measurable criteria.*
13. **Batch evaluation on synthetic data** — generate 10 test prompts (edge cases: out-of-stock/returns), pick evaluators, submit a batch eval against v7. *Shows: real coverage before real users; continuous eval.*
14. **Red teaming** — configure risk categories + **flip/tense** attack strategies; submit an adversarial scan. *Shows: built-in adversarial safety testing.*
15. **Monitoring + operate tab** — per-agent operational metrics + a fleet-level view across the retail + auto-routing agents. *Shows: production observability and fleet management.*
16. **Completed results** — a pre-run red-team scan (pass/fail with hidden attack prompts + reasoning) and a partial evaluation (relevance/groundedness failures). *Shows: how to read results and iterate to green.*
17. **Graduate to code** — View sample app code → VS Code + Foundry SDK / toolkit / skills + Copilot for Azure. *Shows: seamless test-kitchen → restaurant handoff.*

## 📊 Notable Stats / Quotes
- **11,000+ models** in the Foundry model catalog (Discover tab).
- Leaderboard / trade-off metrics are **re-evaluated daily** by the Foundry team based on currently available models (your exact chart may differ — it's a *comparative* view).
- **~25 Zava product manuals** uploaded (≈10 + ≈10 + ≈5) to build the grounding vector index.
- **Versions v1 → v9** of the retail agent were iterated live during the session.
- **Model router** routed a *trivial* prompt ("capital of France?") to **GPT-5 mini** and a *complex* plan request (patio for a family of five) to **GPT-5** — same agent, never changed the model.
- In the model comparison, **GPT-5.4 Nano** earned *"all the gold stars,"* beating GPT-4.1 on quality, cost, throughput **and** safety.
- *"You don't want to get a cordon-bleu chef to make the salad."* — on not over-speccing the model for simple tasks.
- *"From the test kitchen to the table / restaurant."* — the guiding metaphor for portal (low-code prototyping) → code (production).
- *"The more detailed the recipe, the more consistent the dish."* — on the impact of detailed instructions.
- *"Agents helping you build agents."* — on the VS Code pro-code tooling (Foundry skills + Copilot for Azure).
- Conciseness, expressed as a code-based evaluator rule: *"if length > 500 and < 5,000 chars then concise, else not."*
- Model router escalated the complex patio plan to a **higher-performance model (GPT-5)** that returned a comprehensive, ~minute-long, token-heavy plan.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up a throwaway Foundry project at `ai.azure.com`, create a default agent, and **connect Application Insights** — confirm traces + per-response eval scores light up (and that pre-connection traces are retained).
  - Reproduce the **trade-off chart / compare models** flow on a real use case to find a **cheaper model** than the GPT-4.1 default (does GPT-5.4 Nano win for our workloads too?).
  - Deploy **model router**, point a test agent at it, and run mixed-complexity prompts to learn **which backend models our traffic actually uses** → pick a sensible default.
  - Upload our own docs to build a **vector index + file search** tool and verify **source-cited, grounded** answers.
  - Write one **prompt-based** custom evaluator (subjective, e.g. "brand tone") and one **code-based** evaluator (e.g. length/format) and run a **batch eval** on **synthetic data**.
  - Run a **red-teaming scan** (flip + tense strategies) against an internal agent and review failures/reasoning.
  - Click **View sample app code** and graduate one agent into **VS Code with the Foundry SDK + toolkit + Copilot for Azure**.
- [ ] Questions:
  - How do leaderboard/trade-off **benchmark costs** map to our **actual** consumption pricing for the chosen model?
  - What are the **data-residency / privacy** implications of **synthetic data generation** and **red teaming** on enterprise data?
  - How does **Foundry IQ** compare to a plain uploaded **vector index** for enterprise knowledge — when to use which?
  - What's the recommended **CI/CD** pattern to run **batch + custom evaluations** as gates once we move to the SDK?
  - How does **agentic memory** persist/scope per-user, and what are its retention/governance controls?
- [ ] Relevant to:
  - Any team prototyping **agentic AI** on Azure who wants a fast, low-code **inner loop** before committing to code.
  - **AI cost optimization** — right-sizing models via leaderboard/trade-off + model router.
  - **Responsible AI / safety** — evaluators + red teaming + monitoring baked into the dev loop.
  - **Platform/DevRel enablement** — a clean demo narrative (Zava/Kora) for teaching Foundry portal end-to-end.

## 🔗 Related
- Source list: [[2026 Build Session List]]
- Event: [[Microsoft Build 2026]]
- Platform: [[Microsoft Foundry]] · [[Microsoft Foundry portal]]
- Models & routing: [[Model router]]
- Knowledge: [[Foundry IQ]]
- Evaluation & safety: [[Foundry evaluators]] · [[AI red teaming]]
- Pro-code path: [[Foundry SDK]] · [[GitHub Copilot for Azure]]
- Related Build sessions: **BRK241** (prototype → production: build & run agents at scale) · **BRK242** (connect agents to tools/APIs/documents) · **DEM333** (Foundry + open-source frameworks) · **LAB540** ([observe, optimize & protect your hosted agents in Microsoft Foundry](https://github.com/microsoft/Build26-LAB540-observe-optimize-and-protect-your-hosted-agents-in-microsoft-foundry))
- Speakers: [Carlotta Castelluccio](https://developer.microsoft.com/en-us/advocates/carlotta-castelluccio) · Nitya Narasimhan, PhD
