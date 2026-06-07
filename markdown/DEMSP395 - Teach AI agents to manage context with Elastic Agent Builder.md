---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/elastic
  - topic/search
source: https://www.youtube.com/watch?v=jxKihBelsH0
session_code: DEMSP395
event: Microsoft Build 2026
speakers: Mike Richter (Microsoft), Deepthi (Elastic)
duration_min: 17
aliases:
  - Teach AI agents to manage context with Elastic Agent Builder
---

# DEMSP395 — Teach AI agents to manage context with Elastic Agent Builder

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mike Richter (Principal Partner Solution Architect, Microsoft) & Deepthi (Product Manager for Agent Builder, Elastic)  
> **Duration:** ~17 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=jxKihBelsH0)

## 🎯 TL;DR
This partner session pairs Microsoft and Elastic to show why Elastic is an enterprise-ready fit on Azure and how **Elastic Agent Builder** solves the "context gap" — the problem of business data sitting in disconnected silos that AI agents can't reach. Mike Richter covers the procurement, identity, networking, and Foundry-LLM integration story for running Elastic on Azure, while Deepthi demos a **context engine** that gathers context from inside and outside Elastic via agents, skills, connectors, plugins, and attachments. Through a banking customer-support scenario, the live demo builds and customizes an agent that queries Elastic case data, custom ESQL/index tools, and federated connectors (SharePoint, GitHub, Slack) — all in one transparent conversational flow. A key claim: by metadata-mapping fields once (e.g. recognizing personal information), Elastic reduces token usage by roughly **20–34%** while improving security and response quality.

## 🔑 Key Takeaways
- **Elastic on Azure is procurement-simple**: buy via Elastic Cloud or the Microsoft Marketplace, draw down Azure commitment (MACC) dollars, and get a single Azure bill — available in ~15 Azure regions and growing.
- **Enterprise-ready integration**: Entra ID single sign-on into the Elastic portal, **Private Link** so Elastic becomes part of your Azure VNet, no egress costs, and no added cross-region latency when co-located with your workloads.
- **Reuse Microsoft Foundry LLMs** (Anthropic, OpenAI, etc.) and your PTUs to power agents inside Elastic — no separate model stack required.
- **The core problem is the "context gap"**: data sits in siloed systems with isolated context, which breaks what AI needs to execute well; Elastic bridges this by querying data both inside AND outside Elastic.
- **Context engine** maps/aligns siloed data once and assigns the right definitions (metadata), so the system doesn't have to recompute meaning repeatedly — this is what drives the token savings.
- **Metadata understanding improves security**: once Elastic learns that first name + last name + email + phone = personal information, it recognizes those same fields in Salesforce data and the agent can decide whether to include them in a response.
- **Claimed ~20–34% reduction in token usage** from this curated, pre-mapped context approach.
- **Building blocks**: Agents + Skills (built on your data), Connectors (fetch external context), Plugins (domain-specific skills/connectors), and Attachments (dashboards, file uploads) — all unified by the context engine.
- **Transparency by design**: Agent Builder shows which tools/skills/plugins were called for each response, removing the "black box" feel and giving developers traceable reasoning.
- **Customization is first-class**: custom instructions, custom **skills** (swim lanes with set instructions/format + associated tools), and custom **tools** built via ESQL query language, an index, workflows, or MCP.
- **Federated connectors** (SharePoint / SharePoint Server, Slack, GitHub) extend agents beyond Elastic for true cross-system retrieval.
- **Write actions require human approval**: sending a summary to Slack (Teams already in preview) prompts for explicit approval because write operations can be complex/risky.

## 📚 Detailed Notes

### Speakers & Framing
- **Mike Richter** — Principal Partner Solution Architect at Microsoft. His mission is helping partners build and sell solutions on Azure; he frames Elastic as an ideal partner and notes he personally built demo applications on Elastic Agent Builder.
- **Deepthi** — Product Manager at Elastic, primarily focused on **Agent Builder**. She owns the product walkthrough and live demo.
- Mike mentioned he'd be staffing the **"apps and agents" yellow booths** right after the session for follow-up conversations and to show what he built.

### Part 1 — Elastic on Azure: The Partnership Story (Mike)
The first segment is the business/platform case for running Elastic on Azure:

- **Easy to buy**: Elastic is available in ~15 Azure regions today, with more being added. Microsoft customers with Azure commitment dollars (a MACC agreement — which most large companies have, often without realizing it) can spend those committed dollars on Elastic.
- **Single Azure bill**: Purchase through Elastic's cloud offering or the Microsoft Marketplace, and it consolidates into one Azure bill — simplifying procurement for enterprise customers.
- **Deployment options**: Both Elastic's **hosted** offering and its **serverless** offering are now available on Azure.
- **Co-location benefits**: If your Azure workloads run in a supported region (e.g. East US), you can talk to Elastic with **no egress costs** and **no additional latency** — avoiding cross-region hops.
- **Identity / Entra ID**: Sign into the Microsoft portal with Entra ID and use that same identity to sign into the Elastic portal — to create indexes, create agents, and do everything inside Elastic.
- **Private networking**: You can talk to Elastic's managed service over **Private Link**, so Elastic is effectively part of your Azure VNet. This satisfies compliance requirements where data sources must be reached privately — and it works whether running via Elastic Cloud or the Marketplace.
- **Vector / RAG ready**: Elastic has first-class **vector support**; the solution is built for RAG and agentic applications on Azure.
- **Foundry LLM reuse**: Customers with a MACC agreement and PTUs can reuse Microsoft Foundry LLMs (Anthropic, OpenAI, etc.) to power their Elastic agents.
- **Agent Builder on Azure**: Elastic Agent Builder runs in Azure — which is the bridge to Deepthi's segment.
- **Free credits offer**: Deepthi added that attendees could get up to **$1,000 in Elastic credits** by visiting the Elastic booth.

### Part 2 — The Context Gap Problem (Deepthi)
Deepthi reframes from "Elastic is on Microsoft" to "what does Elastic actually do in the world of AI?":

- **The problem**: Disparate systems hold data, and that data/state sits in **siloed context**. When you try to leverage AI — or run your own business with AI — this siloed context "breaks the whole theme" of what needs to be executed from an AI perspective.
- **Elastic's answer**: Bridge the context gap not just by **bringing data into Elastic**, but also by **querying data that sits outside Elastic** in different systems — then wrapping it in good context retrieval to return a response that is both **high quality** AND **token optimized**.

### Part 3 — The Architecture / Context Engine
Deepthi walks through a layered architecture for solving the context gap:

- **Lowest tier — gather context**: Collect information/context from different sources, whether the data is in Elastic or outside Elastic in the broader Microsoft ecosystem.
- **Build your own**: Create your own agents and capabilities around **skills** and **connectors** — these pull in context sitting across systems.
- **Dispatch to endpoints**: Send results to entry points / endpoints such as an agent in **Microsoft Foundry**, an agent on **MCP / Copilot Studio**, or any other endpoint even outside the Microsoft ecosystem.

**The building blocks of the context engine:**
- **Agents & Skills** — build on top of your data.
- **Connectors** — fetch context from different external systems.
- **Plugins** — domain-specific skills and connectors that add deeper domain-level knowledge.
- **Attachments** — dashboard attachments or file uploads that add context to your agent.

**What the context engine does (the differentiator):**
- It **maps / aligns** each piece of siloed data and sets up the **right definitions** so the system doesn't have to churn and recompute what the data means again and again.
- **Worked example**: Phone number, email, first name, and last name together constitute **personal information**. Elastic "metasizes" (assigns metadata to) these as personal-information metadata. Later, when retrieving Salesforce customer data with those same fields, it recognizes that it is handling personal information.
- **Downstream effect**: The agent then understands "this is personal information — should I really dispatch it as part of the response?" → improving security, while the compute/understanding of the data is **quickened**.
- **Result**: Token usage is reduced by roughly **20–34%** (stated as "almost 20 27 to 34%" in the captions — interpreted as the ~20–34% range; the "27" appears to be a caption artifact).

### Part 4 — Live Demo: Banking Customer Support Scenario
**Setup**: You're a bank customer-support team. Case data currently lives in Elastic, while related data — policy documents, engineering issues — sits in other systems like **GitHub**. These systems don't communicate with each other. The demo shows Agent Builder bridging them in a super-easy conversational manner.

**Step 1 — Simple query & transparency**
- Prompt: *"How many interactions happen by channel — phone, email, or chat?"*
- Agent Builder computes the response behind the scenes and is **transparent about what it's computing** — it shows which tools (and, in future, which skills/plugins) were called.
- This removes the **black-box tendency** of some agents and gives transparent reasoning throughout the session.

**Step 2 — Rich output, not just text**
- The response isn't limited to an AI-generated summary — it can also **generate a dashboard you can save**. This is the agent "in a nutshell" / bare-minimum capability.

**Step 3 — Customize the agent with a custom Skill**
- Beyond custom instructions, you can add **skills**. Skills are building blocks that keep an agent in a **"swim lane"** — a specific set of instructions, a format to follow, and associated tools.
- Elastic ships a comprehensive set of ready-to-use skills, but you can also create your own for domain/industry-specific needs.
- **Demo skill created**: a **"financial exposure report" skill** that generates a financial summary on demand, with holistic instructions plus added tools.

**Step 4 — Customize with custom Tools**
- Tools are described colorfully as "elves on the shelves" / "the actual soldiers on the ground" — the things that actually execute.
- Elastic provides a comprehensive set of built-in tools, but you can create your own multiple ways:
  - **ESQL** (Elastic's query language) — build a tool using the query language.
  - **Index** — build a tool from your indexed data.
  - **Workflows**
  - **MCP**
- **Demo tool**: a tool created from **indexed data** — data already in Elastic — to look up a **financial policy** simply by indexing it.

**Step 5 — Break the silo with Connectors (federated search)**
- Up to this point everything was within Elastic. Connectors extend reach to external systems: **SharePoint / SharePoint Server, Slack**, etc.
- Connectors primarily perform **federated search** across these systems to retrieve the most relevant data.

**Step 6 — Complex query combining skill + custom data**
- Prompt: create a **"dispute book"** for all dispute-related customer issues raised in the past, based on the user's data.
- The agent calls the **custom skill just created** and returns a comprehensive, reusable response.

**Step 7 — Pull a specific policy from SharePoint**
- Follow-up: retrieve a specific policy located in a **SharePoint document/folder** and associate it with a specific **case ID**.
- The agent surfaces the relevant policy tied to that case — all in the same conversation, without leaving the flow.

**Step 8 — Check engineering dependencies via GitHub connector**
- Follow-up: *"Can you check if there are any GitHub dependencies or open engineering issues that impact the case resolution?"*
- Using the designed skill and tools, the agent returns a **ranked** list of issues directly impacting the case.

**Step 9 — Send summary to Slack with approval gate**
- The user likes the summary and wants to share it to stakeholders over a **Slack channel** (Deepthi notes **Teams is already in preview** for this too).
- A **workflow** was created to send the summary to a specific Slack channel.
- Crucially, the agent **requests approval** before executing — because write operations are complex and potentially risky, Agent Builder gates such write actions behind explicit user approval.
- **Result**: A comprehensive summary of that same conversation thread is posted to the Slack channel and shared with the team.

### Closing
Deepthi frames the demo as one simplistic example of how Agent Builder **minimizes the context gap** and delivers the value of data sitting in silos — bringing it together into comprehensive responses that enable quick business decisions.

## 🛠️ Products / Features / Technologies Mentioned
- **Elastic Agent Builder** — Elastic's product for building, customizing, and running AI agents over your data (in and outside Elastic); the focus of the session.
- **Elastic Context Engine** — maps/aligns siloed data and assigns metadata definitions so meaning isn't recomputed; drives token optimization and security decisions.
- **Elastic Cloud (Hosted & Serverless)** — Elastic's managed deployment offerings, both available on Azure.
- **Skills (Elastic)** — building blocks that keep an agent in a "swim lane" with set instructions, format, and associated tools; built-in or custom.
- **Tools (Elastic)** — executable units; built-in or custom-built via ESQL, index, workflows, or MCP.
- **Plugins (Elastic)** — domain-specific skills and connectors adding deeper domain knowledge.
- **Attachments (Elastic)** — dashboards or file uploads that add context to an agent.
- **Connectors (Elastic)** — federated-search integrations to external systems (SharePoint, SharePoint Server, Slack, GitHub).
- **ESQL** — Elastic's query language, usable to define custom tools.
- **MCP (Model Context Protocol)** — one method to create custom tools / dispatch to endpoints (e.g. MCP on Copilot Studio).
- **Workflows (Elastic)** — used to create custom tools and to define actions like sending a Slack message.
- **Elastic vector support** — first-class vector capability for RAG/agentic apps.
- **Microsoft Azure** — cloud platform Elastic runs on (~15 regions).
- **Azure Commitment / MACC dollars** — committed Azure spend usable to purchase Elastic.
- **Microsoft Marketplace** — alternate purchase path producing a single Azure bill.
- **Microsoft Entra ID** — single identity for Microsoft and Elastic portals (SSO).
- **Azure Private Link** — private connectivity making Elastic part of your VNet.
- **Microsoft Foundry** — source of LLMs (Anthropic, OpenAI, etc.) reusable to power Elastic agents; also a dispatch endpoint.
- **PTUs (Provisioned Throughput Units)** — reserved model capacity reusable with Elastic agents via Foundry.
- **Microsoft Copilot Studio** — named as an MCP/agent endpoint.
- **GitHub** — external system; source of policy/engineering data via the GitHub connector.
- **SharePoint / SharePoint Server** — external content systems reachable via connectors.
- **Slack** — destination for sending summaries (via workflow, with approval).
- **Microsoft Teams** — Slack-equivalent destination, noted as already in preview.
- **Salesforce** — example external CRM whose customer data is recognized as personal information via metadata.

## 🚀 Announcements / What's New
- **Elastic Cloud serverless on Azure** — highlighted as now available alongside the hosted offering.
- **Teams write/send action** — noted as **already in preview** (Slack shown live in the demo).
- **Elastic credits offer** — up to **$1,000 in Elastic credits** available to attendees via the Elastic booth (event-specific promotion).
- No formal GA/preview dates were given for Agent Builder itself in this session; the talk is primarily a capability + partnership demo rather than a launch keynote.

## 💡 Demos
- **Banking customer-support agent (end-to-end, single conversation):**
  - **Interaction-count query** → proved transparent, traceable reasoning (shows which tools were called) and rich output (can generate a saveable dashboard, not just text).
  - **Custom "financial exposure report" skill** → proved agents can be constrained to a domain swim lane with custom instructions, format, and tools.
  - **Custom index-based tool for financial policy lookup** → proved tools can be built from indexed Elastic data (alongside ESQL/workflow/MCP options).
  - **"Dispute book" complex query** → proved the agent correctly invokes the user's custom skill to assemble a comprehensive, reusable result.
  - **SharePoint policy retrieval tied to a case ID** → proved federated connectors bring external documents into the same conversation and bind them to specific records.
  - **GitHub dependency/issue check** → proved cross-system retrieval can rank external engineering issues by impact on case resolution.
  - **Slack summary send with approval prompt** → proved write actions are gated behind explicit human approval before execution, then deliver the thread summary to a channel.

## 📊 Notable Stats / Quotes
- **~20–34% reduction in token usage** from the context engine's pre-mapped metadata approach (stated as "almost 20 27 to 34%").
- **~15 Azure regions** where Elastic is available today, with more being added.
- **Up to $1,000** in Elastic credits offered at the booth.
- **Personal-information example**: first name + last name + email + phone number → recognized once as PII metadata, then auto-recognized in Salesforce data.
- "Tools are nothing but **elves on the shelves**… the actual **soldiers on the ground**." — Deepthi, describing tools.
- Transparency removes the **"black box tendency"** some agents have, giving "transparent reasoning throughout the sessions."

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up Elastic Cloud (serverless) on Azure in `australiaeast` and test Private Link into a VNet.
  - Wire an Elastic agent to a Foundry-hosted model (reuse PTUs) and compare token usage with/without the context engine to sanity-check the 20–34% claim.
  - Build a custom tool three ways (ESQL, index, MCP) and a custom skill (swim lane) to feel the customization workflow.
  - Test the SharePoint + GitHub + Slack connectors end-to-end and confirm the write-approval gate.
- [ ] Questions:
  - Is the 20–34% token saving measured against a baseline RAG pipeline, and under what query mix?
  - How does the context engine's metadata/PII classification get configured or audited (and can it be governed centrally)?
  - What's the current GA/preview status of Agent Builder, the connectors, and the Teams write action?
  - Does Entra ID SSO + Private Link cover serverless as fully as hosted?
- [ ] Relevant to:
  - Enterprise agentic-search / RAG architectures on Azure where data is siloed across SharePoint, GitHub, CRM, and chat.
  - Procurement/MACC-driven buying decisions where a single Azure bill matters.
  - Governance scenarios needing PII-aware agent responses and human-in-the-loop approval for write actions.

## 🔗 Related
- [[BRK240 - Build context-aware agents]] — Microsoft's own take on context-aware agents; compare context-engineering approaches.
- [[DEM331 - Turn APIs tools and data into real agent velocity]] — tools/data-to-agent theme overlap.
- 
