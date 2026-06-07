---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/foundry
  - topic/agent-365
  - topic/governance
source: https://www.youtube.com/watch?v=uQEvIZKUyCc
session_code: DEM340
event: Microsoft Build 2026
speakers: Shri (Group Product Manager, Agent 365)
duration_min: 26
aliases:
  - Build work-ready agents with Foundry and Work IQ
  - DEM340
---

# DEM340 — Build work-ready agents with Foundry + Work IQ, govern with Agent 365

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Shri — Group Product Manager, Agent 365 (builds agents + enables IT admins to govern them)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=uQEvIZKUyCc)

## 🎯 TL;DR
This demo-heavy session walks the full lifecycle of building an enterprise-ready agent in **Microsoft Foundry** and governing it with **Agent 365**. The core thesis: *context is king*, and an agent is only as good as the data, context, and tools it's given. **Work IQ** delivers that enterprise context (email, Teams, SharePoint) in a single click via an MCP tool, while **Foundry IQ** provides reusable, vector-indexed knowledge bases (RFPs, pricing guides, invoices) backed by Azure AI Search with agentic RAG. The speaker then builds "Agent 007," adds both IQ sources, runs evals (groundedness, task completion, etc.), publishes to the company store, and switches to the IT-admin hat to show how Agent 365 observes, governs, and secures every agent in the tenant — including local agents like GitHub Copilot CLI, OpenClaw, and Claude Code, which can be sandboxed in Intune-powered Microsoft Execution Containers (MXC).

## 🔑 Key Takeaways
- **Context is the king** — agents only succeed when given the right instructions, the right tools, and (most critically) the right context, which lives locked up in SQL/SAP databases, emails, Teams chats, and SharePoint.
- **Work IQ** unifies email + Teams chat + SharePoint documents into a single context layer fed to the agent, reducing token-heavy back-and-forth prompting.
- Work IQ is **generally available mid-June 2026** (~2 weeks from the session).
- Adding Work IQ to a Foundry agent is a **one-click** catalog action — the endpoint, connection credentials, and Entra ID are all wired up automatically.
- Work IQ exposes **MCP, A2A, and REST** protocols, plus a **secure ephemeral workspace** (scratchpad) that clears when the agent runtime finishes so data isn't stored forever.
- Access is **permission-trimmed and identity-aware** — agents (via agent identity) only see the SharePoint docs and emails they're authorized to see.
- **Foundry IQ** = reusable knowledge databases from your existing blob containers (RFPs, sales orders, invoices); Azure AI Search auto-converts blobs into vector indexes with **agentic RAG enabled automatically** and enterprise-grade permission honoring.
- **Evals are built into Foundry** — single-turn or multi-turn, using simulated data or existing human conversations; evaluators include **task completion, task adherence, customer satisfaction, groundedness, and coherence**.
- **Groundedness matters most** because models are biased toward always answering (from abundant internet knowledge) even when they lack the right answer — you must verify responses are grounded in your IQ sources and not hallucinating.
- Publishing to the **company store** auto-creates the Azure Bot Service, assigns an **Agent ID**, and pushes the agent to Teams + M365 Copilot channels *and* the Agent 365 registry — full build-to-publish in ~10–15 minutes.
- There's a **52-point governance gap** between how many agents run in production vs. how many are mature enough to deserve running in the enterprise — the problem Agent 365 solves.
- **Agent ID** has two critical components: a **unique principal** identifying the agent regardless of where it's deployed/running, and **identity permissions just like a human user** so you can scope its access.
- **Agent 365** brings four pillars under the hood: **Intune** (MXC sandbox), **Purview** (sensitivity labels), **Defender** (prompt-injection / exfiltration protection), and the agent registry/observability.
- The **Agent 365 SDK** lets you instrument agents built on **LangChain, AWS Bedrock, etc.** to get the same observability/security/governance — Microsoft is not forcing you onto its stack.
- Agent 365 detects **local/shadow agents** (GitHub Copilot, OpenClaw, Claude Code) across devices and can push an Intune policy to **isolate them in an MXC container** with folder-path access controls.
- **Tool governance** lets IT admins control MCPs/plugins/connectors centrally — e.g., block Work IQ MCP so no agent in the company can ever be built with it (extreme-governance example).

## 📚 Detailed Notes

### Framing: Context is King
The session opens by reinforcing a theme heard repeatedly across Build: **context is the key to an effective agent**. Every agent needs context — a shopper agent needs to find products, an interior-design agent needs design images, an inventory agent needs to know stock levels and supplies. The problem is that **all this context lives locked up inside the work organization**: SQL databases, SAP systems, emails, meeting chats, and documents.

Agents do well only when given three things: the **right instructions**, the **right tools**, and most importantly the **context** (delivered in the form of "IQ"). The speaker frames the common pain point: building an agent where context was missing, then spending so much effort teaching it that doing the task manually would have been faster. That gap is what Work IQ closes — bringing email, Teams chat, and SharePoint documents together to feed the agent enough knowledge so you don't burn tokens repeatedly re-prompting it.

**Context consists of three things:** data, context, and skills/tools. Today's focus is the **Work IQ MCP**, but behind the Work IQ API sits a broader set of capabilities.

### Work IQ — Crash Course
- **What it is:** A unified context layer that brings your email, Teams chats, and SharePoint documents together to feed agents enterprise knowledge.
- **Availability:** Generally available **mid-June 2026** — playable within ~2 weeks of the session.
- **Properties:** Agents become *optimized for use*, *secure*, and *comprehensive*. "Secure/comprehensive" means access is **permission-scoped**: you only get the SharePoint docs and emails you're supposed to see — and this holds true for agents using the **agent identity** too.
- **Protocols exposed:** Although the demo focuses on the Work IQ **MCP**, Work IQ also exposes **A2A** and **REST APIs**. This lets an agent chat, get context, and invoke tools.
- **Secure workspace:** Work IQ provides a secure workspace where the agent can store its "homework" — a **scratchpad** for safely keeping in-progress work without exposing it. As soon as the agent runtime finishes, the **workspace clears up** so none of the data is stored forever.
- **Where you can build with it:** Copilot Studio (declarative agents), and Foundry agents. This session demos the **Foundry** path.

### Demo 1 — Building "Agent 007" with Work IQ in Foundry
The speaker switches to the Foundry UI (familiar to most attendees who'd built Foundry agents). Steps shown:
1. **Start building an agent** — quick and simple. Names it the "super agent" / **Agent 007**.
2. **Give instructions** — for the demo, just "you know it all because you're 007." Unwanted tools are removed.
3. **Add Work IQ from the catalog** — Work IQ "lights up" in the tool catalog; you simply type/select "Work IQ" and **add it in one click**. The **Work IQ endpoint** is exposed and **all connection credentials + Entra ID are configured automatically**. With that single click the agent now has the context of emails, SharePoint, and Teams.
4. **Save and test** — the speaker asks: *"What was the last email from David?"* The **Work IQ MCP tool is invoked**, and a **human-in-the-loop prompt** asks whether to approve the tool call. The speaker approves all tools (for demo flow so it doesn't keep popping up).

This is the core "wow": one click to wire enterprise context into an agent.

### Foundry IQ — Crash Course
- **What it is:** **Reusable knowledge databases** you've already created — think **blob containers containing blobs**: RFPs, RFQs, sales orders, invoices, anything moved to blob storage becomes a Foundry IQ knowledge source.
- **How it works:** **Azure AI Search automatically converts those blobs into vector indexes**, which are then available to the agent for rich **semantic** retrieval. Indexing is done *for you* by Foundry — **agentic RAG is enabled automatically** thanks to Azure AI Search under the hood.
- **Enterprise-grade security:** It **honors all the permissions** you set on the storage containers when they were built.

### Demo 2 — Adding Foundry IQ to the Agent
1. **Add Foundry IQ** — when creating it, you set up a **connection to your Azure AI Search index**. The speaker has pre-created some knowledge bases.
2. **Behind the scenes:** In the storage account, the speaker created a **container** (via "Add Container") and dumped files into it — **pricing guide, battle cards, product specifications**. Azure AI Search **automatically created the index** over that container.
3. **Connect the knowledge source** — back in Foundry, connect to the index; the knowledge source attaches. The agent is now enriched with **both Work IQ and the Foundry IQ knowledge base files**.
4. **Test queries:**
   - Work IQ query (e.g., the email lookup) — picks up Work IQ tools, invokes the needed tool in "ask mode," returns the answer.
   - Foundry IQ query — *"What is the guidance on the discount for these products?"* — pulls from the storage container (pricing specs). Because the live run was slow, the speaker shows a **pre-run agent (timestamp 06:03)** where the same question returns an answer **with a citation** sourced from **"answer synthesis" (i.e., Foundry IQ)**.
   - Combined action — the speaker uses the **Work IQ tool to reply back to David** about the order he was asking about.

> The takeaway: it's "as simple as bringing all the enterprise knowledge to your agent."

### Evals in Foundry
After building, the agent isn't ready to publish — **it must be tested**. Foundry lets you **create and run evals in place**:
1. **Pick the agent** to evaluate (Agent 007).
2. **Choose turn type:** **single-turn** or **multi-turn** (complex, human-like simulated interaction).
3. **Choose eval data source:**
   - **Simulate data** (generate new),
   - Use **existing conversations** (if the agent has been tested with humans), or
   - **Upload a dataset** — there's a downloadable **sample** structure. The speaker uploads pre-made **"007 data."**
4. **Dataset structure (human-writable):** prompts, test-case description, expected output, and desired number of turns. Not a fancy JSON/CSV — **a human can handwrite it** and upload.
5. **Confirm agent config** (already set) and move on.
6. **Evaluators run:** **task completion, task adherence, customer satisfaction, groundedness, and coherence.**
   - **Groundedness** is emphasized: with Work IQ + Foundry IQ feeding the agent, you must ensure responses are **grounded in the knowledge and not hallucinating**. Models have a **bias toward always answering** (internet knowledge is abundant) whether or not they actually found the right answer — so groundedness testing is essential.
7. **Run + results:** The eval runs all prompt combinations (takes time). Pre-completed results are shown as **scores out of 100** — e.g., **88%, 94%** — across evaluators including **tool selection** (was the right tool chosen?), **tool output utilization** (was output optimal?), accuracy/success evaluators, etc. The agent scores well → **100% ready to publish**.

### Publishing to the Company Store
- **Target:** the **company store** — a central repository where all organization employees can start using the agent.
- **Automatic plumbing:** Publishing **auto-creates the Bot Service** — no manually going to Azure Bot Service, creating a bot, and assigning permissions. Foundry makes build → publish achievable in **~10–15 minutes**.
- **Distribution:** Publishing pushes the agent to **Teams and M365 Copilot channels**, and **also registers it in the Agent 365 registry**.
- **Approval gate:** After publishing, the system says to **go back to the admin center to approve it** — handing off to the IT-admin governance flow.

### Switching Hats — The Agent 365 (Admin) View
The speaker role-switches from "Shri the dev" to **"Shri the IT admin."** The **Agent 365 view** shows **all AI artifacts deployed in the tenant**:
- A **scorecard**, **agents at risk**, **active users**, and rich telemetry.
- The newly published agent appears in the registry. As IT admin, you can see **what it is, who published it, when it was published**, and its **security permissions**.
- The agent has an automatically created **bot service** and an assigned **Agent ID**.

### Agent ID — Why It Matters
**Agent ID** has two most-important components:
1. A **unique principal** that identifies the agent **regardless of where it is deployed or running** in the tenant.
2. **Identity and permissions just like a human user** — so you can **control the scope** and grant permissions exactly as you would to a human user.

### Why Agent 365 — The Governance Gap
- **The problem:** a **52-point governance gap** between how many agents are running in production vs. how many are **mature/capable/deserving** of running in the enterprise. Agents are doing things they shouldn't, and IT admins don't know.
- **The promise of Agent 365:** **observe → govern → secure** these agents.

### The Most Important Slide — What You Get with Agent 365
- **Agent identity** (Agent ID, scoped permissions).
- **Agent observability.**
- **Agent interoperability** — e.g., Work IQ enabling agents to interact with SharePoint, Teams, etc.
- **Agent 365 SDK** — instrument agents built on **LangChain, AWS Bedrock**, etc., to get the **same observability, security, and governance**. *Microsoft is not forcing you onto its stack* — just use the SDK to instrument your existing agent.

### The Four Products Under the Hood
Agent 365 brings the power of four products together:
1. **Intune → the sandbox (MXC).** The **Microsoft Execution Container (MXC)** from Satya's keynote is delivered via Intune through a **policy pushed out** to make all devices sandbox-enabled. This lets **GitHub Copilot CLI, Claude Code, OpenClaw** run in a **sandboxed environment**.
2. **Purview → sensitivity labels.** Data tagged highly sensitive is honored by agents — they respect the labels you've assigned.
3. **Defender → exfiltration + prompt-injection protection.** Agents can be manipulated "like a teenager or even a small kid" to do things they shouldn't. With the Agent 365 SDK, traffic passes through a **tooling gateway with deep Defender integration**, providing:
   - Protection from **data exfiltration** (e.g., DNS smuggling) and **real-time prompt-injection** protection.
   - Blocking agents from **visiting harmful sites**.
   - Blocking agents from **sending/replying to suspicious emails** (phishing attacks, etc.).
4. **(Registry/observability)** rounding out the governance story.

> **Key principle:** *The agent (and the model) doesn't decide what agents do when running an enterprise — your enterprise policies define how the agent behaves.* That's the big differentiator.

### Demo 3 — Agent 365 Capabilities Deep-Dive
- **Agent registry (map view):** A rich view of **all agents across all platforms** — Copilot, Foundry, and more. Supports **external agents** brought in from **Amazon, Google, Databricks, Agentforce** — you can **sync them into your registry**. A **map view** shows how different platforms interact.
- **Requests:** Every time a new agent is published, **admins approve it** here (the earlier publish flow lands here).
- **Local agent detection (the "coolest" demo):** Tied to Satya's keynote — **GitHub Copilot and other local agents** are detected as part of the registry. Agent 365 shows the **devices where GitHub Copilot is running**.
  - You can **deploy a policy to isolate the agent** — forcing it to run in the **MXC container** — and set **deeper controls over which folder paths are accessible** to it.
- **Shadow-agent / security detection:** Agent 365 helps **detect other agents (shadow agents)** running, using **Intune + GSA (Global Secure Access)** technology to detect the traffic, with **Microsoft Defender** detecting endpoints running local agents.
- **Tool governance:** Beyond controlling agents, you can govern the **MCPs, plugins, and connectors** exposing data through API connections. Lock these down and you worry less about the agent side. Example: the **Work IQ MCP** shows up in tool governance — as IT admin you can see **any agent ever built in the company using Work IQ**, know what tools they'll use, set **RBAC-style policies**, or **block it entirely** so **no agent can ever be built using Work IQ** (an extreme-governance example to illustrate the option).
- **Bring Your Own MCP server:** Using the SDK you can **publish your own MCP servers**; they appear in the admin view where **IT admin can approve or reject** them.

### Closing
**Build your agents with Foundry, govern them with Agent 365.** Final key takeaway: start building with **Microsoft Foundry**, then govern with **Agent 365**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — platform for building, evaluating, and publishing enterprise agents (demo home base).
- **Work IQ** — unified enterprise context layer (email + Teams + SharePoint) delivered to agents; exposed via MCP, A2A, and REST.
- **Work IQ MCP** — the MCP tool/endpoint added to agents in one click; appears in tool governance for admins.
- **Foundry IQ** — reusable, vector-indexed knowledge bases built from blob storage (RFPs, invoices, pricing guides), with agentic RAG.
- **Agent 365** — the governance/observability/security suite for all agents in a tenant (observe → govern → secure).
- **Agent 365 SDK** — instruments third-party agents (LangChain, AWS Bedrock, etc.) for unified observability/security/governance; also used to publish custom MCP servers.
- **Agent ID** — unique agent principal + human-like identity/permissions, portable across deployments.
- **Agent 365 registry** — central inventory/map of all agents across platforms (Copilot, Foundry, Amazon, Google, Databricks, Agentforce).
- **Azure AI Search** — auto-converts blobs to vector indexes; powers Foundry IQ's agentic RAG.
- **Azure Blob Storage / Storage Containers** — source for Foundry IQ knowledge (files dumped into a container).
- **Azure Bot Service** — auto-created on publish (no manual bot setup needed).
- **Microsoft Intune** — pushes sandbox policy enabling the MXC; isolates local agents.
- **Microsoft Execution Container (MXC)** — Intune-powered sandbox for running local agents (GitHub Copilot CLI, Claude Code, OpenClaw).
- **Microsoft Purview** — sensitivity labels honored by agents.
- **Microsoft Defender** — prompt-injection, exfiltration, harmful-site, and phishing protection via a tooling gateway.
- **Global Secure Access (GSA)** — traffic detection used (with Intune/Defender) to surface shadow agents.
- **Copilot Studio** — alternative build surface for (declarative) agents using Work IQ.
- **Microsoft 365 Copilot & Teams channels** — publish targets for the agent.
- **Company store** — central org repository where published agents become available to employees.
- **Human-in-the-loop tool approval** — Foundry prompt to approve/deny tool invocations.
- **Foundry Evals** — single/multi-turn evaluation with task completion, task adherence, customer satisfaction, groundedness, coherence, tool selection, and tool-output-utilization scoring.
- **GitHub Copilot CLI / Claude Code / OpenClaw** — examples of local agents detected and sandboxable via Agent 365.
- **External agent platforms** — Amazon, Google, Databricks, Agentforce (syncable into the registry).

## 🚀 Announcements / What's New
- **Work IQ → Generally Available mid-June 2026** (~2 weeks after the session). *(Explicit timeline given.)*
- **Foundry IQ** — reusable knowledge bases with automatic agentic RAG via Azure AI Search, presented as available/demoed.
- **Agent 365** — observability/governance/security platform demoed with: registry + map view, agent requests/approvals, **local-agent (GitHub Copilot/OpenClaw/Claude Code) detection**, **MXC sandbox isolation policies**, **tool governance** (MCP/plugin/connector control), shadow-agent detection (Intune + GSA + Defender), and **bring-your-own-MCP-server** publishing.
- **Microsoft Execution Container (MXC)** — referenced from Satya's keynote; delivered via Intune policy.
> Note: Most items are demoed capabilities; the only explicit dated GA in this talk is **Work IQ (mid-June 2026)**.

## 💡 Demos
1. **Build Agent 007 + add Work IQ (one click):** Showed creating a Foundry agent, adding Work IQ from the catalog with auto-configured endpoint/credentials/Entra ID, and querying *"What was the last email from David?"* with a human-in-the-loop tool-approval prompt. **Proved:** enterprise context (email/Teams/SharePoint) can be wired into an agent in a single click.
2. **Add Foundry IQ knowledge base:** Connected an Azure AI Search index over a storage container holding pricing guide, battle cards, and product specs; queried *"guidance on the discount for these products"* and showed a **cited answer** from "answer synthesis" (Foundry IQ) in a pre-run agent (06:03). **Proved:** reusable blob-based knowledge becomes grounded, citable agent context via auto-indexing/agentic RAG.
3. **Run Foundry Evals:** Configured an eval on Agent 007 (single/multi-turn), uploaded handwritten **"007 data"** (prompts, descriptions, expected outputs, turn counts), selected evaluators (task completion, task adherence, customer satisfaction, groundedness, coherence), and showed pre-completed **scores out of 100 (e.g., 88%, 94%)** including tool selection and tool-output utilization. **Proved:** agents can be quantitatively validated for groundedness/quality inside Foundry before shipping.
4. **Publish to company store:** Published the agent — auto-creating the Bot Service and Agent ID, pushing to Teams + M365 Copilot, and registering in Agent 365 — then routed to admin-center approval. **Proved:** full build-to-publish in ~10–15 min with no manual Azure Bot Service plumbing.
5. **Agent 365 admin governance:** Showed the scorecard/agents-at-risk view, the published agent's details + permissions + Agent ID, the cross-platform registry **map view** (incl. Google/Amazon/Databricks/Agentforce), **GitHub Copilot/local-agent device detection**, **MXC sandbox isolation + folder-path controls**, shadow-agent detection, **tool governance** (Work IQ MCP block example), and **bring-your-own-MCP-server** approval. **Proved:** IT admins can observe, govern, sandbox, and secure every agent (cloud *and* local) in the tenant from one pane.

## 📊 Notable Stats / Quotes
- **52-point governance gap** — the gap between how many agents run in production vs. how many are mature/capable/deserving enough to run in the enterprise. *(The central justification for Agent 365.)*
- **Eval scores out of 100** — example results of **88%** and **94%** across evaluators.
- **~10–15 minutes** — time to build and publish an agent in Foundry.
- **Work IQ GA: mid-June 2026** (~2 weeks out).
- *"Context is the key to an effective agent."* / *"Context is the king."*
- *"The biggest problem for adoption of AI is: I don't know what AI is doing in my system. I'd rather know it, govern it, and then shut it down if I don't like it."* — the IT-admin mindset.
- *"The agent doesn't decide, your model doesn't decide what agents do when you're running an enterprise — your enterprise policies define how the agent behaves."*
- On agent manipulation: agents can be influenced *"very much like a teenager or even a small kid to do things it's not supposed to do."*
- *"Build your agents with Foundry, and govern with Agent 365."* — the closing one-liner.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] Spin up a Foundry agent and add **Work IQ** in one click once it hits GA (mid-June 2026); test permission-trimming with a low-privilege test user.
  - [ ] Build a **Foundry IQ** knowledge base from a blob container of sample docs and verify auto-indexing + citations ("answer synthesis").
  - [ ] Run a **Foundry eval** with a small handwritten dataset; inspect groundedness + tool-selection scores.
  - [ ] In **Agent 365**, check whether our local agents (GitHub Copilot CLI, Claude Code, **OpenClaw**) get detected, and test the **MXC** isolation policy + folder-path controls.
  - [ ] Try **tool governance** on the Work IQ MCP and the **bring-your-own-MCP-server** publish/approve flow.
- [ ] Questions:
  - [ ] What exactly distinguishes **Work IQ** vs **Foundry IQ** vs **Foundry knowledge sources** — is Work IQ a managed-graph layer over M365 and Foundry IQ purely your-own-blob RAG?
  - [ ] How is **Agent ID** issued/managed — is it an Entra workload identity / service principal variant? Licensing?
  - [ ] What's the **Agent 365** licensing/SKU story, and which pieces require Intune/Purview/Defender/GSA entitlements?
  - [ ] How deep is **A2A/REST** parity vs the **MCP** surface for Work IQ?
  - [ ] How does the **secure ephemeral workspace** (scratchpad) handle multi-turn/long-running agents — true per-run teardown?
  - [ ] Is the **MXC** the same container surfaced for Copilot CLI elsewhere, and what's the host OS coverage (Windows/macOS/Linux)?
- [ ] Relevant to:
  - [ ] Enterprise agent platform/governance strategy; anyone shipping Foundry/Copilot Studio agents into Teams/M365.
  - [ ] IT admin / security teams evaluating shadow-AI detection and local-agent sandboxing.
  - [ ] Our own OpenClaw setup (local-agent detection + MXC sandbox implications).

## 🔗 Related
- [[Build2026]] — Microsoft Build 2026 session index
- Other Build 2026 notes on **Foundry**, **Agent 365**, **Work IQ / Foundry IQ**, and **Copilot Studio**
- Satya keynote references: **MXC (Microsoft Execution Container)**, local-agent registry/detection
- Topics: [[Azure AI Search]], [[Microsoft Intune]], [[Microsoft Purview]], [[Microsoft Defender]], [[Model Context Protocol]]
