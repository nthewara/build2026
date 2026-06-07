---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/multimodal
  - topic/memory
  - topic/azure
  - topic/mcp
source: https://www.youtube.com/watch?v=o_rcIQUU-k4
session_code: DEMSP390
event: Microsoft Build 2026
speakers: Ido (Napster), Microsoft Azure partner team, Marius (PM), Igor (Lead Engineer)
duration_min: 20
aliases:
  - Create multimodal AI agents with persistent memory
---

# DEMSP390 — Create multimodal AI agents with persistent memory

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** **Ido** (Napster — founder/presenter, author), a **Microsoft Azure partner-team colleague** (announces the Azure native integration), **Marius** (Product Manager) and **Igor** (Lead Engineer) — Napster engineers who run the live demos  
> **Duration:** ~20 min (partner/ISV demo session)  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=o_rcIQUU-k4)

## 🎯 TL;DR
A partner demo by **Napster** showing their **Omni Agent API** — a single API that turns any web app into a **multimodal AI agent** (video, audio, text, WhatsApp, phone) with a **video avatar** and **persistent memory**, so users interact with an agent "like a person" rather than a chatbot. The big reveal: Napster is now available as an **Azure-native offering in public preview**, with unified marketplace billing and SSO from the Azure portal into Napster, sitting as an *experience layer* on top of an **Azure AI Foundry** agent (the *intelligence layer*). The technical core is an **"edge MCP" server compiled into the website's own JavaScript at author time**, giving the agent local "hands" (capabilities) and "eyes" (state providers) via the DOM — no slow/expensive VLM screen-scraping. Pitch: a single developer can wire all this up from their existing Git repo with **one prompt + an API key in a day**, and video avatars now cost **1¢/min vs ~20¢/min (a 20× reduction)**, making production rollout viable.

## 🔑 Key Takeaways
- **Napster Omni Agent API** = one API to make an agent "omni" / **multimodal**: video, audio, text, WhatsApp, or phone call — the *same* agent reachable across a call center, kiosk, or website.
- **Persistent memory is the headline feature** — agents "remember you just like a person you have a relationship with." Ido frames *relationship* as the next interface surface (analogy: multi-touch was to the iPhone what relationship is to agents).
- **Azure-native public preview announced:** Napster on Azure via Azure native integrations → **unified billing through the Azure Marketplace**, provisioned as an Azure resource using the Azure portal/native tooling.
- **Layered architecture:** **Napster (experience/face/avatar layer)** sits on top of an **Azure AI Foundry agent (intelligence/brain layer)** — Foundry holds the memory, knowledge, and tools; Napster adds presence (see/hear/talk).
- **"Edge MCP" breakthrough:** an MCP server is generated **into the site's JavaScript at the source level / compile time**, so the agent calls tools **locally through the DOM** instead of hitting remote endpoints — described as lightning-fast vs VLM-based browser agents.
- **Two skills do the wiring:** an **"identify" skill** parses the web app's source code to build the edge-MCP controller; an **"agent" skill** creates/maintains the agent in Foundry.
- **One-developer, one-day, one-prompt** workflow via "vibe coding" — point it at the Git repo on your laptop, supply the prompt + API key; it studies the codebase and augments the app with the agent. No big cross-org team, no separate knowledge base to maintain.
- **Cost breakthrough for video avatars: ~1¢/min vs ~20¢/min (≈20× cheaper)** — the difference between "demo-only" and "ship it on your live site/app."
- **Auto-generated persona:** the omni agent infers and creates a fitting avatar/persona from the site's domain (e.g. an electronics site gets a matching persona) from a "latent space of an endless universe of agents."
- **Minimal Azure permissions:** the Foundry-based flow needs only **two Entra ID roles — Cognitive Services User and Azure AI Foundry/Developer User** — and exposes none of your other services.
- **Requires frontier models:** the team says this was impossible 3 months earlier — only achievable with current frontier models (references the new OpenAI model and **Opus 4.8**) able to read an entire codebase and predict user intent to wire up the MCP interface.
- **Vision:** the web is built for humans, so the human interface (a person you talk to) becomes the universal app interface — agents that *use* the apps you build, on the user's behalf.

## 📚 Detailed Notes

### Framing — "a time machine to Build 2027"
Ido opens with a deliberately theatrical bit: "welcome to Build 2027… we're going to use a little time machine." The rhetorical point is that **next year's agents won't be chatbots — they'll be "like people, exactly like people."** He shows a video of a "crew of agents" (all AI-generated; "these people don't exist") branded as Napster, claiming you can go from setting up an agent to bringing it to life as a **multimodal agent in a few clicks** using **Foundry**.

### Napster's stack and form factors
Napster positions itself as a **complete stack including hardware**:
- **"The View"** — a holographic display that sits on top of your screen, giving an end user a crew of agent "crew members" available at all times.
- **A full kiosk** — can be deployed in a store, designed to survive a very noisy environment (e.g. ordering at a fast-food joint). Both are shown at their Build booth "down the hall."

### The "vibe coding" pitch
Ido leans into the current developer moment — jokes about "losing a few hours to Claude code" and "walking around with a laptop open while the agent is doing stuff." He wrote a **book** (scan a QR code) about this moment of "us vs AI," the idea that we're all building **"human emulators"** — AI that can do everything we do — and what that means for our kids, companies, and how we "ascend" / do more.

**Getting started is reduced to three things:** a **vibe-coding harness**, an **API key** (scan a QR for a free token offer), and **a prompt**. That's all that's needed to reproduce what's demoed. The repeated theme: work that used to take **"months or years with a big company rolling out an agent" now happens in one day, by one developer, with no team.**

### The Omni Agent API — what "omni" means
The **Omni Agent API** is a single API that makes an agent **multimodal ("omni")** across:
- **Modalities:** video, audio, text.
- **Channels:** WhatsApp, phone call (like a call center), or in-person at a kiosk.

Crucially, it's the **same agent** across all surfaces, and it has **persistent memory** — "they remember you just like a person you have a relationship with." Ido argues the **next surface of innovation is *relationship***: just as the iPhone added multi-touch, agents add relationship — building an "emulator layer" so users have ongoing relationships with agents.

### Azure-native integration (the announcement)
A **Microsoft colleague** joins to announce the **public preview of Napster on Azure, powered through Azure native integrations.** What it means for developers:
- **Unified billing through the Azure Marketplace** + value-added benefits.
- You **provision Napster as an Azure resource** using the **Azure portal** and native Azure tooling.
- **Flow:** developer → Azure portal → provision Azure resource → click the **single sign-on link** → land in the **Napster portal** → use the **Omni Agent** → which talks to your **Foundry agent** (the underlying intelligence layer).
- **Mental model:** **Napster = experience layer on top; Foundry = intelligence layer below; all natively integrated within Azure.**

Ido adds the enterprise angle: because it's in the **marketplace**, **procurement is already solved** — minimal friction to adopt.

### Building an Omni Agent — the developer workflow (time-lapse demo)
Ido plays a time-lapse of building an omni agent for an e-commerce site ("Watson," the site for the provider):
1. As a developer, go into your environment.
2. Drop in **the prompt + your API key**.
3. Come back after a few minutes → an agent exists that **knows the site's content because it lives in the Git on your laptop and studies your website's code**, producing an agent that can *use* your website.

**Contrast with traditional agent setup:** normally you stand up an agent, then separately wire up knowledge, tool-calling, and MCPs — which "suddenly involves a lot of people in your org," and when the knowledge changes you have "two parallel universes in your codebase." Napster collapses this: the **individual developer who controls the front-end business logic** runs one prompt against their Git repo and it's auto-augmented with an omni agent — **"one omni universe"** instead of two.

The agent can then **talk to the user and control the website the same way a vision model would have** — but without the VLM.

### The technical breakthrough — Edge MCP (MCP in the JavaScript)
The core innovation: an **MCP server built into the JavaScript of the site at the source level.**
- Part of the prompt **analyzes your website/code and creates a "virtual instance" of what they call an *edge MCP* that lives in the JavaScript.**
- When the agent is on the page and you ask a question, instead of calling tools from a remote endpoint, **everything happens locally through the DOM by connecting to that MCP locally.**
- That MCP is a **harness to your website**: it does **pre-processing at compile time** and "knows everything about your website" — the user's intent, the steps they need to take, etc.

**The two skills (architecture diagram):**
- **Identify skill** — takes the source code of your web app and **creates the MCP server that controls it** ("wiring up everything on your website").
- **Agent skill** — **creates the agent in Foundry** so you can continue to maintain it.

All of this happens in your code environment (any code harness — **Visual Studio / VS Code**) and, **soon, on the Foundry playground.**

### Why this is only possible now
Igor (the engineer demoing) stresses: **"We could not have done this three months ago."** It depends on current **frontier models** — he cites the **new OpenAI model** and **Opus 4.8** — because the ability to **read an entire codebase and predict what a user might do, then wire it up as an MCP interface,** wasn't feasible before. He calls it a paradigm shift in how we "identify"/build experiences.

### Skills + Copilot one-liner deployment
A new **skill** lets you deploy by simply prompting Copilot — e.g. *"create for me an Azure AI [agent]"* — and it will:
1. **Deploy an agent to Azure AI Foundry.**
2. **Create the visual layer inside the Napster platform.**
3. Give you a **URL**; you provide the **Microsoft Foundry key** and with **one click** you can talk to your agent.

**Everything is controlled inside Azure AI Foundry** — you can use all the built-in Foundry tools and **don't need to expose access to any of your services.** The only Entra ID permissions required: **Cognitive Services User** and **Azure AI Foundry/Developer User** — "nothing else."

### The cost story — making video avatars shippable
Ido addresses the elephant in the room with video agents (referencing companies like **HeyGen** and **Synthesia**): the avatars are amazing but **cost is prohibitive** — fine for a demo, not for rollout. Napster's engineering team spent years optimizing this to offer it at **~1¢/min vs ~20¢/min — a 20× pricing improvement.** Practical impact: you can put **fully-fledged talking video avatars** on your website/app, solving users' problems, with **one day of development** — not "wasting time building a prototype."

He also notes the omni agent **auto-creates the persona** (what the person looks like) to match the site's domain — e.g. an electronics site gets a fitting persona — drawn from a **"latent space of an endless universe of agents."**

### The three-layer model (Marius)
Marius reframes the architecture as **three layers**:
1. **Bottom — your app:** the single source of truth.
2. **Top — the agent.**
3. **Middle — the "agent bridge" / edge MCP server living in the browser**, which lets the agent communicate with the app.

The edge MCP exposes two things:
- **Capabilities = the "hands"** — what the agent can *do* inside your app.
- **State providers = the "eyes"** — what the agent can *see* on the screen.

This makes the agent behave **"exactly like a human, without a VLM."** Typical agentic browser examples work through a **VLM that takes a screenshot, uploads it, and analyzes it — slow and costly.** Napster is **"lightning fast"** because the **cognitive load of teaching the agent how to use the site is paid once at authoring time, on the developer's laptop.**

### Brain + Face composition (Marius)
If you **already have an agent in Foundry**, that's great — it already has the **memory, knowledge, and tools configured; you don't have to change anything. That's the "brain."** On top, you add the **Napster Omni Agent API = the "face"/avatar**, which provides **presence** (people can hear it, see it, talk with it). The result is a **co-worker that gets real work done** *inside your own application*, using the edge-MCP principle.

### The real-world analogy and the use cases
Ido's grounding example: you walk into a **Best Buy** and ask an associate "I'm looking for a GPU with 32 GB of VRAM" — what do they do? They walk to a monitor and **use the Best Buy website to filter and find the product.** That's literally what an omni agent does: a person-like agent that **uses the systems you build, on the user's behalf.** Other examples: **booking a seat on a flight at the airport**, or **triage with a nurse at a counter.** All of these — people using systems — can now be done by an omni agent, and **implementing it takes one day, not months.**

### Final live demo (real implementation)
The team shows the **real implementation** (the earlier one was a time-lapse). The user asks the agent: **"Show me OLED TVs under $2,000."** On a **left-hand debug panel**, you can see:
- The **capabilities from the edge MCP server being called in real time.**
- **State updates being sent from the web page to the agent.**

This proves the agent, via the in-browser edge MCP, **controls the website AND sees what the user is doing — full context all the time.** Note: in this case the "add to cart" action is **reversible**. Ido adds you can ask it to **"compare this screen to this screen"** and it produces the comparison — doing things "you didn't even plan for," because it has strong intelligence baked in at author time. Compared to similar demos from **OpenAI and Google**, those require building a whole new system; **this happens with one prompt.**

### Close
Ido jokes the talk was scheduled for 25 minutes and he was "done 10 minutes ago." Wrap-up CTAs:
- **Scan the QR codes** for tokens + the prompt.
- Visit the **booth down the hall** ("fancy toys" — the View hardware, the kiosk).
- A **hackathon with over $2,000 in prizes** is open now (run by Tanal/Tanya).
- The QR gives you **the View hardware device, the book (physical copy), and a lot of tokens.**
- Thanks to **Marius (Product Manager)**, **Igor (Lead Engineer)**, and Microsoft for support.

## 🛠️ Products / Features / Technologies Mentioned
- **Napster** — partner/ISV building a complete multimodal-agent stack (software + hardware); the experience/presence layer on top of Foundry.
- **Omni Agent API** — single API that makes an agent multimodal (video/audio/text/WhatsApp/phone) with persistent memory; the core product.
- **Edge MCP (a.k.a. "agent bridge")** — an MCP server generated into the site's JavaScript at compile/author time, running locally in the browser via the DOM; exposes capabilities ("hands") + state providers ("eyes").
- **Identify skill** — analyzes web-app source code and builds the edge-MCP server that controls the site.
- **Agent skill** — creates and maintains the agent in Azure AI Foundry.
- **Azure AI Foundry** — Microsoft's agent platform; the "intelligence layer"/"brain" holding memory, knowledge, and tools; provides built-in tooling and the agent playground.
- **Azure native integrations / Azure Marketplace** — delivery mechanism for Napster on Azure: provision as an Azure resource, unified billing, SSO into Napster.
- **Azure portal** — where developers provision the Napster resource and click the SSO link.
- **Microsoft Entra ID** — identity; only **Cognitive Services User** + **Azure AI Foundry/Developer User** roles needed.
- **"The View"** — Napster hardware: a holographic display that sits on top of your screen showing the agent crew.
- **Napster kiosk** — in-store hardware unit built to work in noisy environments (e.g. fast-food ordering).
- **Video avatars** — talking, fully-rendered persona avatars driven by the agent; auto-generated to match the site's domain.
- **Visual Studio / VS Code** — supported code harnesses for the dev workflow.
- **Foundry playground** — where the wiring workflow will soon be available (roadmap).
- **GitHub Copilot** (implied "Copilot") — prompt-driven deployment entry point.
- **Frontier models — new OpenAI model + Opus 4.8** — the foundation models that make whole-codebase intent prediction possible.
- **HeyGen, Synthesia** — named as existing video-agent vendors (cost-comparison context).

## 🚀 Announcements / What's New
- **Public preview: Napster on Azure via Azure native integrations** — unified billing through the Azure Marketplace, provisioned as an Azure resource with SSO from the Azure portal into the Napster portal. *(Status: public preview, stated explicitly.)*
- **New skills for one-prompt deployment** — `identify` (build edge MCP from source) and `agent` (create/maintain Foundry agent); plus a Copilot-prompt flow that deploys an agent to Azure AI Foundry and spins up the Napster visual layer with a one-click "talk to your agent" URL. *(Status: shown/available in the demo workflow.)*
- **Edge-MCP capability** — MCP server compiled into site JavaScript for local, DOM-based tool calling (no VLM). *(Presented as a new breakthrough; "could not have done this three months ago.")*
- **~1¢/min video-avatar pricing** — ~20× cheaper than the ~20¢/min status quo. *(Pricing claim made on stage.)*
- **Roadmap:** the wiring workflow coming to the **Foundry playground**; minimal-permission Foundry-controlled deployment.
- **Hackathon** — open now with **$2,000+ in prizes** (run on-site by Tanal/Tanya).

## 💡 Demos
- **Time-lapse build of an omni agent ("Watson" e-commerce site):** drop a prompt + API key into your dev environment → after a few minutes an agent exists that knows the site (from the Git repo) and can control the website by talking. **Proves:** one developer can augment an existing web app with a multimodal agent from their codebase, no separate knowledge base/tool wiring.
- **Live "OLED TVs under $2,000" e-commerce demo:** user asks the in-browser agent to show OLED TVs under $2,000; a left-side debug panel streams **edge-MCP capability calls** and **state updates** from the page to the agent in real time; add-to-cart is reversible. **Proves:** the edge MCP gives the agent both control ("hands") and live awareness ("eyes") of the page locally — fast, no VLM — and it can even do unplanned tasks like "compare this screen to that screen."
- **Opening "crew of agents" video:** AI-generated multimodal agent personas ("these people don't exist"). **Proves:** the multimodal/persona vision and that personas can be conjured to fit a use case.

## 📊 Notable Stats / Quotes
- **~1¢/min vs ~20¢/min for video avatars → "a 20× factor of pricing."**
- **"$2,000+ in prizes"** in the open hackathon.
- **"We could not have done this three months ago"** — only possible with current frontier models (new OpenAI model + **Opus 4.8**).
- **"They remember you just like a person that you have a relationship with."** — on persistent memory.
- **"The next surface is relationship"** — analogy: multi-touch was to the iPhone what relationship is to agents.
- **"Now it's just one omni universe"** — vs the "two parallel universes" of a separate agent knowledge base + codebase.
- **Best Buy GPU analogy:** "I'm looking for a GPU that has 32 gig of VRAM" → the associate uses the website to filter; the omni agent does exactly that, on the user's behalf.
- **"Implementing that takes one day. It doesn't take months."**
- Required Entra roles: **only Cognitive Services User + Azure AI Foundry/Developer User.**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Scan the Napster QR offer for free tokens + the prompt; try the one-prompt flow against a small e-commerce repo in VS Code and inspect the generated **edge MCP** in the site's JS. Stand up a minimal **Azure AI Foundry** agent and connect the Napster "face" via the Azure Marketplace preview.
- [ ] Questions: Is the "edge MCP in JavaScript" a true MCP-spec server or an MCP-shaped local shim? How does it handle SPA/dynamic DOM and auth-gated state? Where does **persistent memory** actually live — Foundry (brain) or Napster — and what's the data-residency/privacy story? How does the 1¢/min figure scale at concurrency? How is "Napster" (the agent ISV) related to / distinct from the music brand?
- [ ] Relevant to: any web app / e-commerce / kiosk / call-center scenario where a multimodal, memory-equipped agent should *use the UI* on the user's behalf; Azure AI Foundry agent projects; MCP tooling strategy; "agent as the new interface" experiments.

## 🔗 Related
- [[Azure AI Foundry]] — the intelligence/brain layer this stack builds on
- [[Model Context Protocol (MCP)]] — the edge-MCP concept extends MCP into the browser/DOM
- [[Microsoft Build 2026]] — event index
- Other Build 2026 multimodal / agent sessions in this folder