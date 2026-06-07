---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/livekit
  - topic/realtime
  - topic/multimodal
  - topic/agents
  - topic/voice
  - topic/azure
  - topic/webrtc
source: https://www.youtube.com/watch?v=_K7gAvZgHw0
session_code: ODSP937
event: Microsoft Build 2026
speakers: LiveKit presenter (partner/On-Demand session; speaker not named in captions)
duration_min: 10
aliases:
  - Build realtime multimodal agents with LiveKit and Azure
---

# ODSP937 — Build realtime multimodal agents with LiveKit and Azure

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** LiveKit presenter (LiveKit partner / On-Demand session — the individual speaker is not named in the auto-captions)  
> **Duration:** ~10 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_K7gAvZgHw0)

## 🎯 TL;DR
This LiveKit partner session makes the case that **real-time multimodal agents (voice/video/data) are "built different"** from text agents: latency is unforgiving, and the hard problems live in the **real-time media infrastructure**, not the models. LiveKit is pitched as the **open-source real-time media layer** (built on WebRTC) plus an **Agents SDK** (Python or TypeScript) that together get users to your agent and your custom logic back to users reliably, across any device — phones, laptops, telephony/SIP, cars, wearables, robotics. The talk walks through the **cascaded voice pipeline** (VAD → STT → LLM → TTS), shows how **Azure plugs into all three model slots** (Azure STT, Azure OpenAI LLM, Azure TTS), and stresses using the **LiveKit MCP docs server / skill** so coding agents build against up-to-date APIs. It closes with a live demo building a working Azure-powered voice agent from `lk app create` templates in a single `agent.py` file.

## 🔑 Key Takeaways
- **Real-time is "built different."** Text agents tolerate latency (a spinner/dimmer is fine); real-time voice agents need a full mic→model→speaker round trip in **a few hundred milliseconds** over networks you don't control.
- **Models are now the easy part — everything around them is hard.** Network conditions, echo/noise cancellation, turn detection, and graceful interruption are the real engineering challenges, and they belong to the **media infrastructure**, not the model.
- **Interruption must be smart.** Users should be able to interrupt the agent, but a cough, sneeze, or back-channel ("mhm", "oh yeah") should *not* trigger an interruption.
- **WebRTC is the right substrate, but raw WebRTC is non-trivial.** It's exactly what real-time media needs, yet building production infrastructure around it is hard — which is the gap LiveKit fills.
- **LiveKit = open-source real-time media layer on WebRTC**, carrying not just voice but also **video and data**, that your agent and orchestration run on.
- **Two parts:** the **transport layer** (LiveKit server: transport, jitter buffering, codecs, SIP, fanout — self-hosted or LiveKit Cloud) and the **application/orchestration layer** (the **Agents SDK**, Python or TypeScript, where your code, models, tools, MCP servers and business logic live).
- **Same agent, any device.** One agent runs across phones, laptops, SIP/telephony, embedded devices, cars, wearables, robotics, and more.
- **The cascaded (voice) pipeline:** user speech → **VAD** (don't process/pay for silence) → **STT** → **LLM** → **TTS** → audio back to the user.
- **LiveKit is model-agnostic.** It ships no models; you pick STT/LLM/TTS, mix and match, and **swap any model with one line of code**.
- **Azure fits all three model slots:** **Azure STT**, **Azure OpenAI** for the LLM, and **Azure TTS**.
- **Use the LiveKit MCP docs server / skill** when coding — LiveKit ships features almost weekly, and your coding agent needs the most complete, up-to-date context to build accurately (presenter's "most important slide").
- **Credibility signal:** LiveKit is the **transport layer ChatGPT chose for its voice mode**.
- **Getting started is genuinely simple:** scaffold with `lk app create` (Python agent + React front-end templates), edit a **single `agent.py`**, set a handful of env vars, and run — LiveKit Cloud gives **three free env vars** on signup.

## 📚 Detailed Notes

### Why real-time agents are a different problem
Most agents being built today are **single-modal text agents**, and for text, **latency is forgiving** — users accept a spinner or a dimmed text field as a signal that "something's happening." **Real-time agents flip that:** latency becomes the defining constraint. The session's framing line is that **"real-time is built different."**

The concrete real-time loop for voice: take the user's voice from **their microphone, wherever they are in the world**, ship it to the models, generate a reply, and return it to **the user's speakers** — and to *count* as real-time, the whole round trip must land within **a few hundred milliseconds**, all **over networks you don't control**.

### The hard part isn't the model — it's everything around it
A central thesis: **"models are the easy part now; everything around it is the hard part."** Building an excellent real-time voice experience means handling a stack of media problems that the model is not responsible for:
- **Network conditions** (variable, lossy, out of your control).
- **Echo and noise cancellation.**
- **Turn detection** — knowing when the user has actually *finished* talking.
- **Interruption handling** — letting the user barge in, but **not** treating a **cough, sneeze, or back-channel** ("mhm", "oh yeah") as a real interruption.

On top of correctness, there's **scale**: a successful app must serve not one user but **tens or hundreds of thousands of concurrent users**. All of this is the responsibility of the **real-time media infrastructure** — something many teams "aren't even thinking about." This is precisely what **WebRTC** was designed for, but **building infrastructure around WebRTC is not trivial**, which is the opening for LiveKit.

### What LiveKit is
**LiveKit is an open-source real-time media layer** that your **agent and orchestration run on**. It carries **voice, video, and data**, and it's **built on WebRTC**. Alongside the media layer is the **Agents SDK**, available in **Python and TypeScript**.

Together these let you **bring the same agent to any device**: phones, laptops, **SIP and telephony**, embedded devices, **cars, wearables, robotics**, and more. A strong external proof point: **LiveKit is the transport layer ChatGPT chose for their voice mode.**

### The voice pipeline (a.k.a. the cascaded pipeline)
The "very basic voice pipeline," also called the **cascaded pipeline**, flows as:

1. **User speech** — the starting point.
2. **VAD (Voice Activity Detection)** — detect when the user *starts* speaking. Critical because you **don't want to process silence**, which would "cost a lot of money."
3. **STT (Speech-to-Text)** — transcribe the detected speech into text.
4. **LLM** — take that text and **generate a reply, in text**.
5. **TTS (Text-to-Speech)** — turn the reply text into voice.
6. **Audio back to the user.**

It's "cascaded" because each stage feeds the next (speech → text → text → speech).

### The zoomed-out architecture: transport layer vs application layer
A wider system view stacks two layers:

**Transport layer — the LiveKit server.**
- The user, on **any device, anywhere**, connects via **WebRTC** — "every modern device already speaks it," and it's an **open browser standard.**
- The **LiveKit server** handles **transport, jitter buffering, codecs, SIP, and fanout.**
- It's **open source**, so you can **self-host** it, or use **LiveKit Cloud** and have LiveKit host it for you.

**Application / orchestration layer — the Agents SDK.**
- This is **where your code lives** and where you **connect media to the model.**
- The **voice pipeline lives here**, and this is where you **pick which models to use** and where your **tools, MCP servers, custom functions, and custom business logic** sit.
- The "box below the Agents SDK" in the slide is a zoom-in of what's *inside* the Agents SDK (i.e. the pipeline + your logic).

**The key architectural takeaway:** **WebRTC gets users to your agent reliably, and the Agents SDK gets your custom business logic to your users reliably.** That split — reliable transport on one side, reliable orchestration/logic on the other — is the whole mental model.

### Model-agnostic by design (and where Azure fits)
**LiveKit ships no models of its own — it is model-agnostic.** You choose **which STT, which LLM, and which TTS** you want, **mix and match freely**, and swapping a model is **a single line of code**. The slide shows a non-exhaustive list of popular models usable through LiveKit.

**Azure plugs into all three slots:**
- **Azure STT** for speech-to-text,
- **Azure OpenAI** (OpenAI through Azure) for the LLM,
- **Azure TTS** for text-to-speech.

So an entire real-time agent can be built end-to-end on Azure models, orchestrated by LiveKit.

### The "most important slide": use the LiveKit MCP docs server / skill
The presenter explicitly calls this out as, in their opinion, **the most important slide**: when building with LiveKit, **use the LiveKit MCP docs server (or the LiveKit skill)** so your coding agent has the **most up-to-date context.**

The reasoning: **LiveKit ships new features almost every week** and their **docs are always up to date — but your agent doesn't know that.** A coding agent needs the **most complete, current context** to build **accurately** against LiveKit's rapidly-changing API. The presenter's stated preference is the **MCP server** ("it's amazing").

### Building the agent (demo walkthrough)
The build is scaffolded entirely from templates and one Python file.

**Scaffold with the LiveKit CLI:**
- In a terminal, run **`lk app create`** and choose the **agent starter Python template** for the agent.
- Run it again to install the **React starter template** for the **front end**.

**Inside `agent.py` (the single file holding all agent logic):**
- **Imports** from **LiveKit Agents** and **LiveKit plugins**, notably the **Azure plugin for LiveKit.**
- **The assistant/agent definition** — nameable to anything. It sets up the **LLM first**, here using the **Azure LLM** wired to **environment variables from the presenter's Azure deployment** (an OpenAI model served from Azure).
- **Instructions** — e.g. *"you're a friendly and reliable voice assistant demoing at Microsoft Build,"* plus some Microsoft Build info baked in (collapsible).
- **`on_enter`** — when the agent enters the session, it should **greet the user**, so it's instructed to *"greet the user and warmly welcome them to Microsoft Build,"* etc.
- **Server** defined as the **agent server**, with **Silero VAD** set up here (caption rendered it "Solero"; this is the **Silero** voice-activity-detection model).
- **Session** — given a **name/identifier** ("my agent") so the **front end knows which agent to connect to**; the front end must use that **same identifier.**
- **Agent session config** — this is where **STT and TTS** (and other variables) are defined, using **Azure STT** and **Azure TTS**, with the **voice specified here.**
- **Start + await connection**, then **run the file.** The takeaway: it's "very, very simple" to get the agent running.

**Environment variables:**
- **Three env vars from LiveKit Cloud** (free on signup).
- **Azure env vars** for the **STT and TTS** models.
- An **OpenAI API key** (also from Azure).

**Run sequence:**
- `cd` into **agent**, then **`uv sync`**, then **`uv run agent.py download-files`** — this downloads the **small Silero VAD** voice-activity-detection model.
- `cd` into the **front end**, **`pnpm install`**.
- **`uv run` the agent in dev mode**, and **`pnpm dev`** for the front end.
- The presenter customized the front end with a **Microsoft Build theme**, then started talking to it live.

### What the live conversation showed
The running agent held a natural, low-latency voice conversation (transcript excerpt):
- **Agent (greeting):** "Hi there. Welcome to Microsoft Build. I can help with questions about Microsoft technologies like Azure, Windows, Microsoft 365, GitHub, or the latest AI work Microsoft is sharing here. What would you like to explore?"
- **User:** asks for the **dates of Microsoft Build.**
- **Agent:** "Microsoft Build 2026 takes place on **June 2nd and June 3rd**. It is a **two-day event in San Francisco at Fort Mason**, with an online experience as well. Are you planning to attend in person or join online?"
- **User:** notes that's *today* and he's already there.

The closing line: *"That's it. Quick and easy. Integrate Azure. Give it a try today and let us know what you think."*

## 🛠️ Products / Features / Technologies Mentioned
- **LiveKit** — open-source real-time media layer (voice, video, data) built on WebRTC; the transport + media foundation your agent and orchestration run on.
- **LiveKit Agents SDK** — application/orchestration layer where your code, models, tools, MCP servers and business logic live; available in **Python** and **TypeScript**.
- **LiveKit server** — the transport layer handling transport, jitter buffering, codecs, SIP, and fanout; self-hostable.
- **LiveKit Cloud** — hosted LiveKit option; provides three free environment variables on signup.
- **LiveKit plugins (Azure plugin)** — integration package that wires Azure STT/LLM/TTS into the Agents SDK.
- **LiveKit MCP docs server / LiveKit skill** — keeps a coding agent supplied with the latest LiveKit docs/context (presenter's preferred = the MCP server).
- **`lk` CLI (`lk app create`)** — scaffolds projects from templates (agent starter Python template, React starter front-end template).
- **WebRTC** — open browser standard for real-time media; the substrate LiveKit is built on; spoken by every modern device.
- **Azure Speech-to-Text (Azure STT)** — STT model slot in the pipeline.
- **Azure OpenAI (OpenAI via Azure)** — the LLM slot in the pipeline.
- **Azure Text-to-Speech (Azure TTS)** — TTS model slot in the pipeline; voice selectable in config.
- **Silero VAD** — small downloadable voice-activity-detection model used to detect speech start (captioned as "Solero").
- **VAD / STT / LLM / TTS** — the four model stages of the cascaded voice pipeline.
- **SIP / telephony** — supported transport target, so agents can run over phone systems.
- **uv** — Python package/runner used (`uv sync`, `uv run`).
- **pnpm** — Node package manager used for the front end (`pnpm install`, `pnpm dev`).
- **React** — front-end framework (starter template).
- **ChatGPT voice mode** — cited as a production user of LiveKit's transport layer.

## 🚀 Announcements / What's New
None explicitly announced. This is a technical/partner explainer and demo, not a release announcement. The presenter notes that **LiveKit ships new features "almost every week"** (hence the push to use the MCP docs server for current context) but does **not** call out any specific new release, preview, or GA in this session.

## 💡 Demos
- **End-to-end Azure-powered voice agent built live.** Scaffolded with `lk app create` (Python agent template + React front-end template), all agent logic in a single `agent.py`, using the **LiveKit Azure plugin** with **Azure STT**, **Azure OpenAI LLM**, and **Azure TTS**, plus **Silero VAD**.
  - **What it proved:** A production-style, low-latency real-time voice agent on Azure models can be stood up with minimal code (one file), a few env vars, and a handful of `uv`/`pnpm` commands — reinforcing the "models are easy, infra is hard, and LiveKit handles the infra" thesis.
- **Live spoken conversation with the agent.** The Build-themed front end greeted the user, then correctly answered a question about Build 2026 dates (June 2–3, San Francisco, Fort Mason) and asked a natural follow-up.
  - **What it proved:** The cascaded pipeline (VAD→STT→LLM→TTS) delivers a fluid, conversational, real-time experience in practice — including a sensible greeting on session enter and contextual follow-up questions.

## 📊 Notable Stats / Quotes
- **"A few hundred milliseconds"** — the latency budget for the full mic→model→speaker round trip to qualify as real-time.
- **Scale target: "tens or hundreds of thousands of users concurrently."**
- **"Models, they are the easy part now. Everything around it is the hard part."**
- **"Real-time, it is built different."**
- **"WebRTC gets users to your agent reliably and the Agents SDK gets your custom business logic to your users reliably."** — the core architectural takeaway.
- **"It's just one line of code to change out a model."** — on LiveKit's model-agnostic swapability.
- **"LiveKit is the transport layer ChatGPT chose for their voice mode."**
- On the MCP slide: **"this is actually, I think, in my opinion, the most important slide here."**
- **Three free environment variables** from LiveKit Cloud on signup.
- Agent's spoken fact: **Build 2026 = June 2–3, San Francisco, Fort Mason** (two-day event + online).

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Run `lk app create` with the Python agent starter + React front-end templates and stand up an Azure-only voice agent (Azure STT + Azure OpenAI + Azure TTS) end-to-end with `uv sync` / `uv run agent.py download-files` / `pnpm install` / `pnpm dev`.
- [ ] Things to try: Wire up the **LiveKit MCP docs server** in my coding-agent setup so it builds against current LiveKit APIs; compare vs the LiveKit skill.
- [ ] Things to try: Swap models with the "one line of code" claim — e.g. switch TTS/STT providers and measure latency/quality differences in the cascaded pipeline.
- [ ] Things to try: Experiment with turn detection + interruption tuning so coughs/back-channels ("mhm") don't falsely interrupt.
- [ ] Questions: What's the real-world latency floor on the Azure STT→Azure OpenAI→Azure TTS path, and where's the biggest contributor (network vs STT vs LLM vs TTS)?
- [ ] Questions: Self-hosted LiveKit server vs LiveKit Cloud — what are the cost/ops/scale tradeoffs at the "hundreds of thousands of concurrent users" tier?
- [ ] Questions: Does LiveKit support a **speech-to-speech / realtime (non-cascaded)** model path, or is the cascaded pipeline the recommended pattern? (Session only covered cascaded.)
- [ ] Questions: How does SIP/telephony bridging work in practice for taking the same agent to phone systems?
- [ ] Relevant to: Any voice-assistant / real-time multimodal agent build on Azure; telephony/IVR modernization; embedded/automotive/wearable voice UX; demos needing a fast "wow" voice agent.

## 🔗 Related
- 
