---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-foundry
  - topic/agents
  - topic/twilio
  - topic/omnichannel
  - topic/voice
source: https://www.youtube.com/watch?v=JmSXpYisEVQ
session_code: DEMSP393
event: Microsoft Build 2026
speakers: Rachel (Product Manager, Twilio)
duration_min: 22
aliases:
  - Orchestrate omnichannel AI agents with Foundry and Twilio
---

# DEMSP393 — Orchestrate omnichannel AI agents with Foundry and Twilio

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Rachel — Product Manager, Twilio  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=JmSXpYisEVQ)

## 🎯 TL;DR
This Twilio partner demo shows how to build a single **omnichannel AI agent** (voice, SMS, and chat) by combining **Twilio Agent Connect (TAC)** with **Microsoft Azure AI Foundry**. The core problem it solves is customer-experience "amnesia" — agents forgetting that a customer emailed last week, called this week, or already changed something seconds ago — which produces disjointed, frustrating support experiences. The solution pairs two best-in-class, complementary platforms: Twilio owns the channels, real-time conversation management, and **persistent cross-channel memory**, while Foundry provides the models, agent framework, and **Voice Live API**. The headline architectural shift is moving deployment from Azure **Container Apps** to Microsoft's new **hosted agents** primitive (public preview), giving each conversation its own isolated, serverless, scale-to-zero sandbox with built-in observability, traces, and evals. The live demo proves the payoff: a fast voice call that changes a flight seat, then an SMS that already *knows* the seat was just changed — same agent, shared memory, minimal engineering effort.

## 🔑 Key Takeaways
- AI spend surged **44% year-over-year** (Gartner), yet value lags: **56% of leaders** say they're getting nothing from AI and only **6% of brands** improved CX scores in 2025.
- The root customer-experience failure is **memory loss / amnesia across channels** — agents don't remember prior emails, calls, or web visits, creating disjointed experiences (e.g. being asked "what do you need?" right after being texted that your flight is delayed).
- Building a real omnichannel virtual agent with memory, knowledge, and data that you can put in front of customers is genuinely **hard to deploy and scale** — very few people in the room had done it.
- Twilio + Microsoft launched a **native integration** between **Microsoft Foundry** and **Twilio Agent Connect (TAC)** specifically to reach production with **lower engineering effort**.
- The two platforms are **complementary, not overlapping**: Twilio handles every channel + region + shared customer memory; Foundry provides intelligence (Voice Live API, foundational models, Agent Framework SDK).
- **Twilio Agent Connect (TAC)** is the bridge: one **open-source SDK** with **two connectors** (one to Twilio, one to Foundry) that stitches them into a single agent across all channels.
- TAC has two main components: an **Agent Framework connector** (routes Twilio voice/messaging events into the Microsoft Agent Framework, handles Cosmos DB session persistence + contextual memory injection) and a **Voice Live connector** (direct streaming inference over WebSockets to Foundry Voice Live for low latency).
- The integration first shipped on **Azure Container Apps**, but traditional compute was built for **stateless** web services/APIs where users share instances — **agents need long-lived, stateful, per-user sessions**.
- Multi-tenant agents that write files, execute code, and access credentials create a **security/isolation problem** (customer A must never reach customer B's data), which Container Apps doesn't naturally solve.
- Microsoft built **hosted agents** as a new **compute primitive** for exactly this pattern: per-session dedicated sandbox, predictable cold starts, **scale to zero**, state persistence, unique agent identity, and out-of-the-box observability/evals/policies.
- Hosted agents recently went to **public preview** with **WebSocket support** and an **Invocations API**, which let Twilio switch its deployment to a **fully serverless** option (minimal ops burden, no idle costs).
- The new architecture is dramatically simplified: Twilio events flow over **HTTP into an API Management gateway** (validates the Twilio signature, adds auth, maps each Twilio conversation ID → a hosted-agent session ID), then routes into the hosted-agent sandbox, which calls Foundry for model inference; **voice uses native WebSocket hosting** for low latency.
- Deployment is essentially one **`azd up`** command that provisions the API Management instance and a hosted agent with TAC running inside it; the only inputs are an API key and the hosted-agents URL.
- Because it runs on hosted agents, you get **traces, monitor, evals, and a playground for free** — no extra work to build them.
- Critical deployment detail: paste the **public API Management URL** into Twilio (the hosted-agent URL is **not public**) as the webhook for both the phone number (voice) and the conversation config (SMS).
- The demo agent ran on **GPT-4.1 mini** ("chat GBT45 mini" in captions); the **voice path is Twilio Conversation Relay** under the hood, now embedded in the TAC repo, connecting to Foundry's **Voice Live API**.
- There is **no extra charge** for the integration itself — you pay only for the Twilio channels and Foundry services you use.

## 📚 Detailed Notes

### Why this session exists: the AI value gap
The talk opens by framing a paradox. Global AI spend has surged **44% year-over-year** (per Gartner), and every business is being asked how they use AI in workflows and how they build AI products for customers. Yet the returns aren't there: **56% of leaders report getting nothing out of AI**, and only **6% of brands improved their customer-experience (CX) scores in 2025**. So there's a massive jump in monetary investment without matching results — companies say they aren't finding value, and end consumers aren't enjoying the AI experiences businesses build for them. The session is positioned as Twilio's answer to *why* that gap exists and how to close it for customer-facing agents.

### The core problem: cross-channel "amnesia"
Twilio's diagnosis is that the primary challenge is **memory loss**. When a customer interacts with a business — via a virtual agent, a human agent, or a digital channel — there's amnesia: the system doesn't remember you emailed last week, called this week, or searched the website three weeks ago. Traditional CX suffers from this amnesia **across channels**, producing a disjointed end-customer experience. Rachel uses relatable failure modes everyone recognizes: getting transferred and repeating yourself over and over; calling and getting disconnected; or the airline that texts you "your flight is delayed" and then the agent answers with "what do you need help with?" The customer's frustration ("you just texted me my flight was delayed — why don't you know that?") is the emotional core of the problem.

### Second problem: building omnichannel agents is genuinely hard
Beyond memory, actually **deploying and scaling** an omnichannel AI agent is complex. Rachel polls the room — how many have built a virtual agent they've actually put in front of customers? — and almost nobody had. The point: making an agent that is omnichannel, has memory, has the right knowledge, and has the right data is *not* simple. These two challenges (amnesia + deployment complexity) are the justification for the integration.

### The solution: Foundry + Twilio Agent Connect native integration
In response, Twilio and Microsoft launched a **native integration** between **Microsoft Foundry** and **Twilio Agent Connect (TAC)**. The explicit design goal is reaching **production with lower engineering effort** and shipping a **real, production-ready agent**.

The division of labor:
- **Foundry side:** build, optimize, and govern AI agents out of the box, with a vast selection of models to choose from.
- **Twilio side:** real-time conversation management, **persistent memory**, and **multi-channel orchestration** via a new product launched "a couple weeks ago" called **Twilio Agent Connect**.

The thesis is that these are **two best-in-class, complementary (not overlapping) platforms**, and the value is combining them into **one agent**:
- **Twilio (left of the diagram):** handles every single channel, in every region, with **shared customer memory across them**.
- **Foundry:** provides the intelligence — the **Voice Live API**, the **foundational models**, and the **Agent Framework SDK**.
- **Twilio Agent Connect:** the **bridge** — **one open-source SDK with two connectors** (one to Twilio, one to Foundry) that creates **one agent across all channels**.

### Deployment v1: Azure Container Apps
The first deployment option out of the gate was **Azure Container Apps**, chosen for **full control over the agent runtime** on **production-grade Azure infrastructure**, with **session persistence** via a **Cosmos DB** connection. Architecturally (left → right): Twilio channels connect via **WebSockets** to your Container Apps; the app connects to **Azure Cosmos DB** for state management; and it calls **Foundry** for the models.

### Why Container Apps wasn't the right fit for agents
The key learning: **traditional compute wasn't built for agents.** Container Apps / traditional compute was designed for **stateless web services and APIs** where multiple users share the same instance. **Agents, by contrast, need long-lived, stateful, per-user sessions.** Rachel illustrates with customer A and customer B both calling the same agent: that agent is writing files, executing code, and accessing credentials, which creates a **security and isolation problem** — customer A must never somehow access customer B's information. Shared-instance stateless compute doesn't cleanly solve that.

### Microsoft's answer: hosted agents (new compute primitive)
To address exactly this pattern, **Microsoft invested in hosted agents** as a **new compute primitive**. The **six key benefits**:
1. **Per-session dedicated sandbox** — every session gets its own isolated sandbox (solving the A/B isolation problem).
2. **Predictable cold starts.**
3. **Scale to zero** — pay nothing while the agent isn't doing anything.
4. **State persistence.**
5. **Unique agent identity.**
6. **Out-of-the-box observability** — evaluations, policies, traces, and a playground.

The punchline Rachel repeats: it's no longer hard to *get* an agent — the hard part is making it **enterprise ready**, and hosted agents close that gap.

### Deployment v2: hosted agents (the better option)
Because Microsoft took **hosted agents into public preview with WebSocket support and the Invocations API**, Twilio was able to **switch its deployment option to hosted agents**. The Container App option still exists, but hosted agents is described as a **much better solution**: **fully serverless**, **minimal operational burden**, and you get all six hosted-agent benefits **plus native WebSocket integration**.

The new (much simpler) architecture:
- **Twilio** handles **voice, SMS, and chat**.
- Events flow over **HTTP into an API Management gateway** at the top, which:
  - **validates the Twilio signature**,
  - **adds auth**, and
  - **maps each Twilio conversation ID → a hosted-agent session ID**, giving every conversation its **own dedicated sandbox**.
- From there it **routes into the hosted-agent sandbox** where the agent logic runs, which connects to **Azure Foundry for model inference**.
- The result is **fully serverless — no compute, no scaling, no idle costs.**
- A noted nuance: the bottom of the diagram shows **HTTP for the omnichannel events** and **WebSocket hosting** for the **low-latency, native voice channel** connection.

### What TAC actually is (and why you need it in the middle)
Rachel addresses the natural question: why do you need this extra thing between Twilio channels and hosted agents? **TAC is a connector** with **two main components**:
1. **Agent Framework connector** (top right) — routes Twilio events across **voice and messaging** directly into the **Microsoft Agent Framework**; also handles **session persistence with Cosmos DB** and **contextual memory injection** (this is where the cross-channel memory lives).
2. **Voice Live connector** — provides the **direct integration with Foundry Voice Live**, doing **streaming inference over WebSockets** to make voice fast. This is why the demo voice call responds quickly.

### Live demo: the repo and the "secret sauce"
Rachel switches to a live demo, starting with the **open-source repo: "Twilio Agent Connect Microsoft"** (a QR code + link are promised at the end). The repo has READMEs and a **new "agent framework hosted agents" deploy option**. Inside the agent file is the **`TacHostedAgentsApp` class** ("TAC hosted agents app class") — the piece that **connects hosted-agent requests originating from Twilio into TAC**, installable in your own Python code via **pip**. This class is described as "the secret sauce behind all of this."

Deployment was a single **`azd up`** command (she doesn't run it live because it takes 5–10 minutes and "we'd all just sit here silently watching it"). The command **provisions the API Management instance and a hosted agent with TAC running directly inside it.**

### Live demo: what was deployed (airline use case)
Rachel shows what she'd already deployed last week — an **airline demo**, "version one." It deployed with no manual work beyond supplying her **API key** and **hosted-agents URL**. Out of the box she gets the hosted-agents goodies: **traces, monitor, evals, and a playground.**

A crucial connection detail: the deploy also stands up an **API Management service**, and its **URL is public** — so **that** is the URL pasted into Twilio, **not** the hosted-agent URL (which is **not public**).

### Live demo: wiring Twilio to the webhook (voice + SMS)
- **Voice:** In Twilio → Phone Numbers → the chosen number's **voice configuration**, the **webhook URL** is the **API Management gateway URL** — telling that phone number to point to the API Management endpoint.
- **SMS:** In Twilio → **Conversation configurations** → the airline build, the **SMS webhook endpoint** is pasted in the same way.

This is the entire "connection" — the public API Management URL bound to both the phone number (voice) and the conversation config (SMS).

### Live demo: the voice call (changing a seat)
Rachel calls the agent on speakerphone. Twilio handles speech in/out, **TAC bridges into the Foundry Agent Framework**, and **Foundry powers the reasoning**. The scenario: a customer calling to change a flight.

Transcript of the exchange:
- **Agent:** "Thanks for calling Airlines. I see you're calling from a number associated with an existing reservation. Are you calling about your flight **543 to Seattle departing tomorrow**?"
- **Caller:** "Yes, I am. I need to change my seat. I'd like a window seat."
- **Agent:** "You are currently booked in **23B**. I can easily move you to **23A**, a window seat. Would you like me to do that?"
- **Caller:** "Yes, please update the seat."
- **Agent:** "Done. I've updated your reservation for flight to seat **23A**. Have a great flight."

The point proved: the agent recognized the caller from their number (**profile resolution**), and the voice call was **fast with no real delay**.

### Live demo: the SMS that remembers (the payoff)
This is the climax — proving cross-channel memory. After the voice call, Rachel mirrors her phone and **texts** the same number (same agent): *"Hey, I forgot to add a bag to my reservation. Can I add one for my flight?"*

The agent replies that it sees she's on **flight 543, in seat 23A** — the seat she changed to **two seconds earlier on the voice call**. It has that context **immediately**, then quotes that **adding one bag will cost $45** and asks to confirm. She says yes; it responds "great, safe travels — I've added your bag."

The lesson: **same phone number, conversation moved from voice to SMS, and the agent knows who she is via profile resolution and remembers the prior conversation** — enabling a more educated, continuous conversation. Although a simple example, it generalizes to many use cases.

### Live demo: observability / traces
The traces are slow to appear (a recurring caveat — "they take a few minutes"), but eventually she shows the **input and agent response from the SMS conversation**, plus **metadata** revealing the model in use: **GPT-4.1 mini** ("chat GBT45 mini"). The emphasis: "we didn't have to do anything to build this — it's out of the box with hosted agents."

### Q&A highlights
- **Where's the business logic / can I customize?** The repo ships **generic examples** ("you're a helpful agent"), and the README documents how to **change the personality prompt, connect knowledge sources, and add tools**. You can also customize via **hosted agents inside Foundry** — change the model, add data, add evals, connect knowledge. You get **optionality**: do it in the TAC repo *or* in Foundry hosted agents.
- **"It sounds like you go directly to OpenAI / you used Conversation Relay before."** Originally, when Twilio launched **Conversation Relay**, that was the approach because the integrated deployment options didn't exist. Now that **Microsoft added WebSocket support and Twilio-signature validation**, this **direct integration** is possible. It makes **voice calls faster**, and for customers who **don't want to own the WebSocket infrastructure**, Microsoft owns it for them. You *can* still build it yourself with **Conversation Relay (C Relay)** and own your own infrastructure for full control — but many customers said they don't want to own that, or want a direct deployment option, or want **evals/observability** (which raw Conversation Relay doesn't have). Importantly: **Conversation Relay is embedded within the TAC repo** — same product, just an SDK that deploys it more easily with the direct connection. (Confirmed again later: the voice response uses **Conversation Relay connecting to the Voice Live API** in Microsoft.)
- **ISV / multi-company use case — one server per company?** With TAC *before* the Foundry integration, you'd want a **different server per company** (and probably a different subaccount). For **hosted agents**, Rachel doesn't yet know Microsoft's recommendation — whether an ISV should use **multiple projects/resources** or keep them in **one** with tenant-level separation — and offers to **follow up with Microsoft partners**.
- **On the difficult raw connection:** Twilio built products **on top of** the connection because of feedback that the **raw connection is difficult and has latency issues** — the SDK/products make it work more seamlessly. She encourages testing the repo against whatever attendees built previously.

## 🛠️ Products / Features / Technologies Mentioned
- **Twilio Agent Connect (TAC)** — newly launched (~2 weeks prior) open-source SDK that bridges Twilio and Foundry; one SDK, two connectors; handles real-time conversation management, persistent memory, and multi-channel orchestration.
- **Microsoft / Azure AI Foundry** — provides agent intelligence: model selection, build/optimize/govern agents, Agent Framework SDK, Voice Live API, model inference.
- **Hosted agents** — Microsoft's new compute primitive for agents: per-session sandbox, scale-to-zero, state persistence, unique identity, out-of-the-box observability/evals/policies; recently in public preview with WebSocket support + Invocations API.
- **Azure Container Apps** — the original deployment option; full runtime control on production-grade Azure infra; still available but superseded by hosted agents for this use case.
- **Azure Cosmos DB** — state management / session persistence store for the agent.
- **Azure API Management** — gateway that validates the Twilio signature, adds auth, maps Twilio conversation ID → hosted-agent session ID; exposes the **public** webhook URL pasted into Twilio.
- **Foundry Voice Live API** — streaming voice inference endpoint; TAC's Voice Live connector integrates with it over WebSockets for low latency.
- **Microsoft Agent Framework** — the framework into which TAC's Agent Framework connector routes Twilio voice/messaging events.
- **Twilio Conversation Relay (C Relay)** — Twilio's voice product connecting to Microsoft's Voice Live API; now embedded inside the TAC repo and used under the hood for the demo's voice path.
- **`TacHostedAgentsApp` class** — Python class (pip-installable) that connects Twilio-originated hosted-agent requests into TAC; the "secret sauce."
- **`azd up`** (Azure Developer CLI) — single command that provisions the API Management instance + a hosted agent with TAC inside; ~5–10 min to run.
- **GPT-4.1 mini** — the chat model powering the demo agent (rendered as "chat GBT45 mini" in captions).
- **WebSockets** — transport for low-latency voice (Twilio ↔ Foundry / hosted agents).
- **Twilio channels** — voice, SMS, and chat, all unified behind one agent.
- **Twilio profile resolution** — identifies the customer from their phone number to carry context across channels.
- **Hosted-agents observability suite** — traces, monitor, evals, and a playground, available out of the box.

## 🚀 Announcements / What's New
- **Twilio Agent Connect (TAC)** — newly launched product (~2 weeks before the talk) providing real-time conversation management, persistent memory, and multi-channel orchestration; open-source SDK with Twilio + Foundry connectors.
- **Native Foundry ↔ Twilio Agent Connect integration** — the headline integration enabling a single omnichannel agent with lower engineering effort; **no extra cost** beyond channels + Foundry services used.
- **New "agent framework hosted agents" deploy option in the TAC repo** — a fully serverless deployment path on Microsoft hosted agents (alongside the existing Container Apps option).
- **Microsoft hosted agents** — in **public preview**, recently gaining **WebSocket support** and an **Invocations API**, which enabled Twilio's serverless deployment. (Stated as the enabling Microsoft platform capability; preview status noted.)

## 💡 Demos
- **`azd up` deployment walkthrough (shown, not run live):** Demonstrated that one `azd up` command provisions the API Management instance + a hosted agent with TAC inside, requiring only an API key and hosted-agents URL. Proved deployment simplicity / low engineering effort.
- **Repo tour:** Showed the open-source "Twilio Agent Connect Microsoft" repo, the hosted-agents deploy option, READMEs, and the `TacHostedAgentsApp` class — proving it's installable (pip), documented, and customizable (personality prompt, knowledge sources, tools).
- **What got deployed (airline agent, version one):** Showed the already-deployed hosted agent in Foundry with its traces, monitor, evals, and playground — proving the observability suite comes free, with no manual setup beyond an API key + hosted-agents URL.
- **Twilio wiring:** Showed pasting the public API Management URL as the webhook for both the phone number's voice configuration and the conversation config's SMS endpoint — proving the entire "connection" is just one public URL bound to voice + SMS.
- **Live voice call (change a seat):** Called the agent on speakerphone; it recognized the caller by number, confirmed flight 543 to Seattle, and moved the seat from 23B to 23A — proving low-latency, accurate voice handling via TAC → Foundry Agent Framework reasoning.
- **Cross-channel memory (the payoff demo):** Texted the same number afterward to add a bag; the agent already knew it was flight 543, seat 23A (changed seconds earlier on voice) and quoted the $45 bag fee — proving persistent, shared memory across voice and SMS via profile resolution. This was the central "magic" the architecture is built to deliver.
- **Trace inspection:** Pulled up the SMS conversation's trace showing input, agent response, and metadata (model = GPT-4.1 mini) — proving end-to-end observability is available out of the box.

## 📊 Notable Stats / Quotes
- **44%** — year-over-year surge in global AI spend (per Gartner).
- **56%** — share of leaders who say they're getting **nothing** out of AI.
- **6%** — share of brands that **improved** their CX scores in 2025.
- **$45** — cost to add one bag, quoted by the agent in the SMS demo.
- **Flight 543 to Seattle, seat 23B → 23A** — the airline demo's concrete details (window seat change).
- **GPT-4.1 mini** — the model powering the demo agent.
- **~5–10 min** — time for the `azd up` deployment to complete ("we'd all just sit here silently watching it").
- > "My flight's late. You just texted me that my flight was delayed. Why don't you know that my flight's delayed?" — the relatable amnesia failure that frames the whole problem.
- > "It's really not hard now to get an agent. The hard part is actually making it enterprise ready." — the thesis for why hosted agents matter.
- > "They're not overlapping platforms. They're really complimentary." — on Twilio + Foundry working together.
- > "There's no extra money to use this integration. You're just paying for the channels and the foundry services that you're using."

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the **Twilio Agent Connect Microsoft** open-source repo and run the **`azd up`** hosted-agents deploy with a test Foundry API key.
  - Reproduce the **voice → SMS memory handoff** with the airline sample, then swap the personality prompt / connect a knowledge source per the README.
  - Compare voice latency of the **direct TAC integration** vs a hand-rolled **Conversation Relay** setup.
  - Explore the free **hosted-agents observability** (traces, monitor, evals, playground) on a deployed agent.
- [ ] Questions:
  - For an **ISV/multi-tenant** scenario, does Microsoft recommend **multiple projects/resources** per company or **one project with tenant separation** in hosted agents? (Rachel flagged this as open — follow up with MS partners.)
  - What are the **pricing details** of hosted agents at scale (scale-to-zero economics, cold-start frequency) for high-volume contact centers?
  - Where exactly does **contextual memory injection** store/scope data in Cosmos DB, and what are the retention/PII controls?
  - GA timeline for **hosted agents** (currently public preview)?
- [ ] Relevant to:
  - Building omnichannel customer-support / contact-center agents (voice + SMS + chat) with shared memory.
  - Anyone evaluating **Azure AI Foundry hosted agents** as a serverless agent runtime vs Container Apps.
  - Twilio customers modernizing from Conversation Relay to a managed, observable deployment.

## 🔗 Related
- [[Microsoft Build 2026]] — parent event for this partner demo session.
- [[Azure AI Foundry]] — the model + agent platform powering the agent's reasoning and Voice Live.
- [[Microsoft Agent Framework]] — the framework TAC routes Twilio voice/messaging events into.
- [[Hosted agents]] — Microsoft's new per-session, scale-to-zero compute primitive central to this talk.
- [[Twilio Agent Connect]] — the open-source bridging SDK (Twilio + Foundry connectors).
- [[Azure Cosmos DB]] — state/session persistence store for cross-channel memory.
- [[Azure API Management]] — the gateway that validates Twilio signatures and maps conversation → session IDs.
- Source list: [[2026 Build Session List]]
