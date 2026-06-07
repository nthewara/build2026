---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/oracle
  - topic/mcp
  - topic/microsoft-iq
  - topic/data
  - topic/ai
source: https://www.youtube.com/watch?v=F2dmwt8fPfM
session_code: ODSP919
event: Microsoft Build 2026
speakers: Jeff Smith (Oracle), Ram Kakani (Oracle Database@Azure, Microsoft)
duration_min: 20
aliases:
  - Move from data to intelligence with Oracle MCP and Microsoft IQ
  - Oracle MCP + Microsoft IQ
---

# ODSP919 — Move from data to intelligence with Oracle MCP and Microsoft IQ

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jeff Smith (Product Manager, Oracle — covers MCP servers for the Oracle Database) and Ram Kakani (Product Manager, Oracle Database@Azure team within Microsoft)  
> **Duration:** ~20 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=F2dmwt8fPfM)

## 🎯 TL;DR
This Oracle + Microsoft partner session shows how to turn enterprise data sitting in Oracle databases into intelligence that AI agents can reason over — without ETL or migrating the data out of Oracle. The pattern connects an **Oracle-hosted, managed MCP server** (Model Context Protocol) to Microsoft's **IQ intelligence layer** (Foundry IQ for reasoning/grounding, Fabric IQ for historical analytics, Work IQ for Outlook/Teams/Excel context) so a single agent — built in Azure AI Foundry, Copilot Studio, or GitHub Copilot — can query live Oracle data securely. Identity flows end-to-end via Microsoft Entra ID (OAuth 2 / OBO tokens) so the database sees the *actual* user and Oracle's native security rules still apply, all governed by Entra Agent ID and Agent 365. The live demo builds an "Accounts Payable analyst" agent for a fictitious company (Zava) that finds unpaid invoices, reasons over vendor contracts/compliance policies to spot PO mismatches and duplicates, recommends which to release, and then drafts a reply email in Outlook — all from natural language, with a human approving each query.

## 🔑 Key Takeaways
- **Data stays in Oracle; intelligence comes from Microsoft.** The whole architecture lets Oracle data remain safe in Oracle while Microsoft's AI/IQ stack reasons over it — "Oracle data stays safe in Oracle. That's enterprise ready."
- **MCP is the bridge.** Oracle offers **managed, hosted MCP servers** native to both Oracle Cloud Infrastructure (OCI) and **Oracle Database@Azure**. The MCP server itself is **no additional cost** — you only pay for the database and the AI tooling you use.
- **Four-layer mental model:** (1) **AI / dev surface** (Azure AI Foundry, Copilot Studio, GitHub Copilot — pro-code or low-code, same runtime); (2) **Intelligence layer** = Microsoft IQ (Foundry IQ, Fabric IQ, Work IQ); (3) **Oracle data tier** via two patterns — Oracle MCP server for live reads, Fabric mirroring for historical/cross-source analytics; (4) **Governance plane** (Entra Agent ID + Agent 365).
- **"Same agent code, both ways."** Whether reading live via the Oracle MCP server or analyzing historical/cross-source data via Fabric mirroring, the agent code is the same.
- **Two access patterns for Oracle data:** **Oracle MCP server = live reads** straight from the database; **Fabric mirroring = historical or cross-source analytics** when you have more than one data source.
- **Identity propagates all the way into the database.** Using Microsoft Entra ID + OAuth 2 + an OBO (on-behalf-of) token, the Oracle database sees the real user (e.g. "Ram") — not a shared service account — so Oracle's fine-grained, fancy security rules (row/table visibility via proxy users tied to the identity domain) still apply.
- **Governance is not bolted on.** Entra Agent ID gives every agent a first-class identity with least-privilege scoping; Agent 365 provides tenant-wide agent inventory and governance.
- **Natural language → SQL** is the headline MCP tool pattern: the LLM translates a question ("how many widgets did we sell last week?") into a SQL query the database runs through an MCP tool.
- **Zero ETL.** The demo solves a real AP problem ("invoice volume up 30% on flat headcount, cycle times past 45 days") with the *same* agent and *same* Oracle data and **zero ETL** — built in weeks, not quarters.
- **Human-in-the-loop is mandatory.** Every query must be approved by a human validating it's hitting the right tables, returning the right data, and has the right authZ/authN. Memorable framing: **"You're the actual pilot, not the co-pilot."**
- **Only ~4 pieces of dev stack** are needed: Foundry Agent Service (hosts agents + native MCP client), the MCP server endpoint, the dev surface (GitHub Copilot / Copilot Studio), all governed by Entra Agent ID + Agent 365.
- **Setup is config-driven, self-serve.** You define the MCP server characteristics (which tools, how auth works), point it at the identity domain, add users to an MCP server group, register the agent as an MCP client (enabling the OAuth 2 flow), and you're done — Oracle runs it for you.
- **Work IQ closes the loop into productivity apps** — after the data reasoning, the agent drafts an Outlook email on the same thread, handling "the human stuff."

## 📚 Detailed Notes

### Framing: from data to intelligence
Jeff Smith (Oracle PM) opens the partner session by setting the thesis: data stored in **Oracle databases** pairs very well with **Microsoft's AI platform**, and the goal is to make Oracle data "useful in serving your business." Ram Kakani (Oracle PM on the Oracle Database@Azure team *inside* Microsoft) co-presents; he specifically covers **MCP servers for the Oracle database**. The session is squarely about making enterprise Oracle data **AI-ready** so you can build "business-aware enterprise agents."

### The architecture: four stacked planes
Ram walks through how it "all comes together" as four layers (he calls them "plates"):

1. **AI / Dev surface (top).** Azure AI Foundry, Copilot Studio, GitHub Copilot. Pro-code **or** low-code — **same runtime** underneath. This is where developers build and host agents.
2. **Intelligence layer (Microsoft IQ).** Turn on what your scenario needs:
   - **Foundry IQ** — reasoning and grounding.
   - **Fabric IQ** — historical analytics.
   - **Work IQ** — delivers results into **Outlook, Teams, Excel** and brings your **work context** into the agent.
3. **Oracle data tier ("Oracle Atlas").** Two patterns to reach Oracle data, with the **same agent code** for either:
   - **Oracle MCP server → live reads** directly against the database.
   - **Fabric mirroring → historical or cross-source analytics**, used when you have more than one source of data.
4. **Governance plane (bottom).** Explicitly **"not bolted on."**
   - **Entra Agent ID** ("on-try agent ID" in the captions — i.e. Microsoft **Entra** Agent ID) gives every agent a **first-class identity with least-privilege scoping**.
   - **Agent 365** provides **tenant-wide inventory and governance** of agents.
   - Net effect: **Oracle data stays safe in Oracle → "enterprise ready."**

### The dev stack — only four cross pieces
Ram stresses how little code this takes — "four pieces of dev stack, if you will":
- **Foundry Agent Service** — hosts the agents *and* provides the **native MCP client**, which can point to **any MCP server** (here, the Oracle MCP server).
- **MCP client → Oracle MCP server** connection (native MCP support).
- **GitHub Copilot or Copilot Studio** — your choice of **pro-code vs low-code** dev surface.
- All of it **governed by Microsoft Entra Agent ID + Agent 365**.

"Just a few pieces of code that'll take your life with an agent" — i.e. a small amount of wiring gets you a working agent over Oracle data.

### What MCP is, and Oracle's managed MCP servers
Jeff takes over for the MCP deep-dive:
- **MCP = Model Context Protocol**, which "came onto the scene in late 2024 and caught on like wildfire all throughout 2025."
- Oracle has shipped **MCP servers for Oracle AI Database since July** (2025), and now offers them **for the cloud** — both in **Oracle Cloud Infrastructure (OCI)** and for **Oracle databases running at Azure** (Oracle Database@Azure).
- These are **managed, hosted MCP servers, native into Oracle's cloud environments**. As a customer/partner you simply **define the characteristics** of the MCP server: **which tools** to expose and **how authentication works** — and Oracle **runs it for you at no additional cost**.
- **Cost model:** the **MCP server itself is no cost**; you only pay for **using your database** and **using the AI tooling**.

### Step-by-step: wiring Oracle data to the Azure IQ pieces
Jeff describes the setup flow to connect the Azure/IQ side to the actual data in the database:

1. **Database connection first.** As with any database, you supply a **set of credentials**, and *those credentials shape the view of the data the AI will see.* You can use a **proxy user tied to your identity domain** to determine what data is visible — down to **which tables you can see, or whether the tables are visible at all.**
2. **Create the MCP server** and point it at the **identity domain**, where your **Azure Entra ID users** are defined.
3. **Grant users access** by adding them to an **MCP server group** (e.g. "add Ram to the group"), which gives them privileges to connect to and talk to the MCP server **using their existing Entra ID login**.
4. **Define the MCP tools.** Tools are "sort of the APIs" that let MCP clients/agents request things on their behalf. The **best-known pattern is natural language → SQL**: a user asks "show me how many widgets we sold last week," the **LLM translates that to a SQL query** the database understands, and it's **submitted to run through the MCP tool**.
5. **Register the agent as an MCP client**, which enables the **OAuth 2 workflow**. The **first time only**, the user logs in, Entra ID credentials are verified, and the user is asked for **permission to grant the agent to act on their behalf** — producing an **OBO (on-behalf-of) token**. The agent then grabs an **access token via OAuth 2** and "you never see the login stuff ever again."

### Why end-to-end identity matters (security)
A core selling point: **the user's identity is propagated all the way into the database.** When Ram uses an agent that talks to Oracle via AI, **the Oracle database sees Ram as Ram** — his actual **Azure Entra ID user**, not a generic service account. Because of that, Oracle can enforce **all of its very fancy native security rules** (table/row visibility, etc.) per real user. As long as the user's identity has the **required group membership** to interact with the Oracle MCP server and database, they're good to ask questions. This is the crux of "Oracle data stays safe in Oracle."

### The demo problem statement (the "why")
Ram frames a concrete business pain to justify the whole pattern:
- An **Apex/AP team** asks a developer for help.
- **Invoice volume is up 30% on flat headcount.**
- **Cycle times have crept past 45 days.**
- Data sits in an **Oracle database**, and **dashboards only tell them *what* happened** — they don't *act*.
- They need **an agent that moves the work**, and the **budget is weeks, not quarters.**
- Solution promise: **same agent, same Oracle data, zero ETL** — built in **Foundry**, wired with **Foundry IQ + Work IQ**, talking to the Oracle database through the **Oracle MCP server**.

### Demo walkthrough — building & running the AP agent
Ram drives the live build:

**1. Oracle Database@Azure in the Azure portal.** He shows the **native Oracle database services** offered through the Azure portal: **Autonomous AI Database, Exadata Database (incl. Exadata Database on Exadata scale infrastructure), Base Database Service, and GoldenGate.** For the demo, the **supply-chain data is hosted in an Exadata database** in a **VM cluster in UK South**, provisioned in the customer's **VNet and subnet**.

**2. Foundry portal → build an agent.** You can create an agent from scratch (name it, continue self-serve), but for time he opens a pre-built **"Accounts Payable analyst" agent** responsible for AP insights. Its **remote MCP server is already pre-provisioned and connected into the tools.**

**3. How tools get connected.** Go to **create tools → connect a tool → catalog → Oracle → Oracle's remote MCP server → create.** You provide:
- the **remote MCP server endpoint**,
- **parameters for region and offset**,
- **authentication** — which (as Jeff said) can be **key-based or OAuth-based**,
- then hit **Connect**.
The shown MCP server connection is provisioned in **UK South**, has a **connection ID**, and is **currently used in two agents**.

**4. Add the IQ tools.** Same connect-a-tool flow for **Work IQ** (he uses the **Work IQ email MCP server**) and **Fabric IQ** (for historical trends).

**5. The fully-wired agent (fictitious company "Zava").** It is connected to:
- the **remote MCP server** for the Oracle database,
- **Work IQ email** (configured),
- **Fabric IQ** for historical trends,
- a **knowledge base** ("Zava knowledge IQ") built from two sources: **compliance reports stored in Microsoft OneLake** and **vendor policies / contractual documents stored in Azure Blob Storage** — these power the knowledge base and thus the agent's reasoning.

**6. Prompt 1 — find the invoices (live read via MCP).** "Show the last 90 days of invoices that are unpaid and over $50,000, including the reasons and age." The user gives **consent / authenticates**, the agent **connects to the MCP server** and **executes pre-populated queries** to fetch the data. Jeff's punchline: as a developer he "used to write 50 lines of boilerplate code in the OCI SDK" just to set up connections — "but look at this, the magic of MCP." Result: a few suppliers have unpaid invoices over $50K — **Acme Car Parts** and others have one each, **Winner X has three.**

**7. Prompt 2 — reason over policies (Foundry IQ + knowledge base).** "Look at how these unpaid invoices are — do they have PO mismatches or duplicates, and which can be released vs held?" This is **Foundry IQ in action**: the agent looks at **vendor agreements and compliance policies** to analyze the delays and duplicates. Ram stresses **human-in-the-loop**: you approve each query, validating it's hitting the right tables, getting the right data, and has the right authZ/authN. Result: the agent **reasons over all invoices against the supplied knowledge-base documents** and recommends — the **best candidate likely safe to release is Acme Group, but only after resolving a duplicate.** The user can then **cancel the duplicate payment** and let the AP head release the order/invoice for Acme.

**8. Prompt 3 — put Work IQ to work (draft the email).** "Look at all my ongoing discussions and emails about Acme Group for these specific invoices. Summarize what was agreed, then draft a reply to **James Chen** with the latest on the same thread about the cancellation." The agent **searches** (user approves the search parameters/filters to find the right conversation), **retrieves the message**, and **creates a draft reply** — noting Acme Group ordered the subject in error, to cancel the duplicate and release it. This **generates a draft in Outlook** (connected via Work IQ) that the user can **review and hit send** after validating. Jeff: "That's the real magic — it wrote the email for us and dealt with the human stuff I'm not good at."

### Recurring theme — accountability over autonomy
Throughout the demo both speakers hammer the **human-in-the-loop** discipline because the agent touches **mission-critical enterprise data in Oracle**. Jeff's quotable line: **"Just because this stuff is fast and looks good doesn't mean you can take your eyes off or your hands off. You're the actual pilot, not the co-pilot."** Ram reinforces: be conscious of **what the agent is accessing, why, and the outcome.**

### Close & call to action
Jeff notes this was his first time speaking at Build. They leave resources: a **LinkedIn community** for "Oracle Database@Azure" practitioners, links for **pricing/technical details**, and **QR codes**. They invite viewers to **set up a call** where Oracle engineers will show how to get **traditional on-premises Oracle databases running as Oracle Database@Azure** and help **set up the MCP servers** so agents work as demonstrated.

## 🛠️ Products / Features / Technologies Mentioned
- **Model Context Protocol (MCP)** — open protocol (emerged late 2024) that lets agents/LLM clients call tools; the bridge between agents and Oracle data here.
- **Oracle MCP Server (managed/hosted)** — Oracle-run MCP servers, native to OCI and Oracle Database@Azure; expose tools (e.g. NL→SQL) over the database; no additional cost. Available for Oracle AI Database since July (2025).
- **Oracle Database@Azure** — Oracle database services offered natively through the Azure portal, in the customer's VNet/subnet.
- **Oracle Autonomous AI Database** — one of the Oracle DB services available via Azure portal.
- **Oracle Exadata Database Service** (incl. on Exadata scale infrastructure) — hosts the demo's supply-chain data (VM cluster, UK South).
- **Oracle Base Database Service** — another Oracle DB service listed in the portal.
- **Oracle GoldenGate** — data replication service listed among the Oracle@Azure services.
- **OCI (Oracle Cloud Infrastructure)** — Oracle's cloud; also hosts MCP servers; the OCI SDK is the "50 lines of boilerplate" MCP replaces.
- **Azure AI Foundry / Foundry portal** — the dev surface used to build and host the agent.
- **Foundry Agent Service** — hosts agents and provides the native MCP client that points to any MCP server.
- **Foundry IQ** — Microsoft IQ component for reasoning and grounding (used to reason over vendor agreements/compliance policies).
- **Fabric IQ** — Microsoft IQ component for historical analytics / trends.
- **Work IQ** — Microsoft IQ component delivering into Outlook/Teams/Excel and bringing work context; exposes a Work IQ **email MCP server** used to draft the Outlook reply.
- **Microsoft Fabric mirroring** — pattern for historical/cross-source analytics over Oracle data (alternative to live MCP reads).
- **Microsoft OneLake** — stores the compliance reports used as a knowledge source.
- **Azure Blob Storage** — stores vendor policies / contractual documents used as a knowledge source.
- **Copilot Studio** — low-code dev surface option for building the agent.
- **GitHub Copilot** — pro-code dev surface option.
- **Microsoft Entra ID (Entra Intra ID in captions)** — identity provider; users/groups defined in the identity domain; powers OAuth 2 / OBO sign-in.
- **Microsoft Entra Agent ID** — gives every agent a first-class identity with least-privilege scoping (governance plane).
- **Agent 365** — tenant-wide agent inventory and governance.
- **OAuth 2 / OBO (on-behalf-of) token** — auth flow that lets the agent act as the user; identity propagates into the Oracle database.
- **Natural language → SQL** — the flagship MCP tool pattern (LLM translates questions into SQL run via an MCP tool).
- **Proxy user (Oracle, tied to identity domain)** — credential mechanism shaping which tables/rows the AI can see.

## 🚀 Announcements / What's New
- **Managed, hosted Oracle MCP servers for Oracle Database@Azure and OCI** are available **at no additional cost** (you pay only for database + AI tooling usage). MCP servers for **Oracle AI Database have existed since July** (2025) and are **now offered for the cloud** in both OCI and Oracle@Azure environments. (No explicit GA/preview label was stated for the Azure-hosted variant in the talk.)
- The session showcases **end-to-end integration of Oracle MCP with Microsoft's IQ stack** (Foundry IQ, Fabric IQ, Work IQ) and **Entra-based governance (Agent ID, Agent 365)** as the recommended architecture — presented as available/working today via the live demo, though specific preview/GA status of individual IQ components was not called out.

## 💡 Demos
- **Accounts Payable analyst agent ("Zava" company), built in Azure AI Foundry**, demonstrating the full "data → intelligence" loop with zero ETL:
  - **Prompt 1 (live read via Oracle MCP server):** Surface last-90-day unpaid invoices over $50K with reasons + age → proved the agent connects to the Oracle Exadata DB through the MCP server and runs queries (replacing ~50 lines of OCI SDK boilerplate). Output flagged Acme Car Parts, Winner X (3 invoices), etc.
  - **Prompt 2 (reasoning via Foundry IQ + knowledge base):** Detect PO mismatches/duplicates and recommend release vs hold by reasoning over vendor agreements + compliance policies (sourced from OneLake + Azure Blob) → recommended Acme Group as safe to release *after* resolving a duplicate; proved grounded, policy-aware reasoning with human approval per query.
  - **Prompt 3 (action via Work IQ email):** Summarize prior email discussion with Acme and draft a reply to James Chen on the same thread about the cancellation → created an Outlook draft ready to review/send; proved the agent can act in productivity apps, closing the loop from insight to action.
- **Azure portal tour:** showed the native Oracle Database@Azure services and the Exadata VM cluster (UK South) hosting the supply-chain data.
- **Tool-connection walkthrough:** connecting Oracle's remote MCP server (endpoint + region/offset params + key/OAuth auth) from the Foundry tool catalog, plus connecting the Work IQ email and Fabric IQ tools — proving how few clicks it takes to wire data + intelligence + productivity into one agent.

## 📊 Notable Stats / Quotes
- **"You're the actual pilot, not the co-pilot."** — Jeff Smith, on keeping a human accountable even when the agent is fast and impressive (Ram: "Good one, I like that").
- **"Just because this stuff is fast and it looks good doesn't mean you can take your eyes off or your hands off."** — Jeff Smith on human-in-the-loop discipline.
- **"The magic of MCP"** replaces **~50 lines of OCI SDK boilerplate code** that a developer used to write just to set up connections and fetch the data.
- **Invoice volume up 30%** on **flat headcount**; **cycle times past 45 days** — the business pain motivating the AP agent.
- Budget framing: **"weeks, not quarters"** to deliver the agent.
- **Zero ETL** — "same agent, same Oracle data, zero ETL."
- Demo query scope: **unpaid invoices, last 90 days, over $50,000**, with reasons + age.
- **MCP server is no cost** — you pay only for the database and the AI tooling.
- MCP **"came onto the scene in late 2024 and caught on like wildfire all throughout 2025."**
- Oracle has had **MCP servers for Oracle AI Database since July** (2025).
- **"Oracle data stays safe in Oracle. That's enterprise ready."**
- Demo MCP server connection was **provisioned in UK South** and **used by two agents**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up an **Oracle MCP server on Oracle Database@Azure** (Exadata or Autonomous AI DB) and connect it as a tool in **Azure AI Foundry**; confirm the "no additional cost" claim against actual billing.
  - Verify the **NL→SQL** tool quality and how queries are "pre-populated" / approved (human-in-the-loop UX).
  - Test **end-to-end Entra identity propagation** into the Oracle DB (does the DB really see the Entra user via OBO?) and pair it with Oracle row/table security via a proxy user.
  - Compare the **live-read (Oracle MCP)** path vs **Fabric mirroring** path for analytics, using the *same* agent code.
  - Wire **Work IQ email** + **Foundry IQ knowledge base** (OneLake + Azure Blob sources) and reproduce the AP "find → reason → draft email" loop.
- [ ] Questions:
  - What is the **GA vs preview status** of the Azure-hosted Oracle MCP server and of Foundry IQ / Fabric IQ / Work IQ as used here?
  - Beyond **NL→SQL**, what other **MCP tools** does Oracle expose (writes? procedures? vector search on Oracle AI DB)?
  - How does **Agent 365** governance surface these Oracle-backed agents, and what least-privilege scoping does **Entra Agent ID** apply?
  - Auth options: when to choose **key-based vs OAuth/OBO** for the MCP connection?
  - What regions beyond **UK South** support Oracle Database@Azure + managed MCP servers (e.g. australiaeast)?
- [ ] Relevant to:
  - Any enterprise with **mission-critical data locked in Oracle** wanting agentic AI without migrating/ETL-ing data out.
  - Accounts Payable / finance-ops automation, vendor-contract compliance reasoning.
  - Azure AI Foundry agent builders needing **secure, identity-aware** access to external databases via MCP.

## 🔗 Related
- [[BRK223 - From rows to reasoning]] — designing databases so AI/agents can reason over enterprise data (the relational-data-to-intelligence counterpart).
- [[OD820 - Designing Reliable Multi-Agent Apps with Azure Cosmos DB]] — agent memory + reliable data access patterns that complement Oracle-backed agent workflows.
- [[OD811 - Powering the next AI frontier with a unified data platform]] — the Microsoft IQ / Fabric IQ intelligence layer this Oracle MCP integration plugs into.
- [[DEM333 - How Foundry integrates with open-source frameworks and tools]] — MCP/A2A open-standard plumbing for connecting tools and data into Foundry agents.
- [[OD832 - From workflows to agentic automation with Azure Logic Apps]] — Knowledge-as-a-Service / managed RAG over enterprise data, an adjacent zero-ETL pattern.
- [[ODSP909 - Take AI agents from prototype to production with OpenTelemetry]] — observing/governing the agents that consume these MCP data tools in production.
- Source list: [[2026 Build Session List]]
