---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/business-apps
  - topic/ai
  - topic/agents
  - topic/blazor
  - topic/devexpress
source: https://www.youtube.com/watch?v=_dTUUKlvKx8
session_code: ODSP911
event: Microsoft Build 2026
speakers: Paul Usher (DevExpress)
duration_min: 14
aliases:
  - Build AI-first business apps that turn dashboards into actions
---

# ODSP911 — Build AI-first business apps that turn dashboards into actions

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Paul Usher — DevExpress  
> **Duration:** ~14 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_dTUUKlvKx8)

## 🎯 TL;DR
A DevExpress-led walkthrough of how to embed AI into a modern **Blazor** line-of-business app *without* just bolting a chatbot next to it. By wiring **Azure OpenAI** (via `IChatClient`) to DevExpress controls using **tool calling**, the demo turns passive dashboards into an actionable "application assistant": users express **intent** in natural language ("group by profit", "export", "highlight payment risk", "translate this report", "review this contract"), and the AI invokes a curated, app-registered toolbox that drives the real control APIs. The recurring principle: **AI handles the intent, DevExpress handles the interaction** — Azure OpenAI provides the intelligence, the controls give that intelligence *shape* and somewhere structured to act.

## 🔑 Key Takeaways
- The goal is **not** code generation and **not** a chatbot dropped beside an app — it's connecting AI to the **controls, data, and workflows** users already rely on.
- Stack: **Visual Studio + .NET + DevExpress Blazor controls + DevExpress Reporting + Azure OpenAI** accessed through **`IChatClient`**.
- **Tool calling** is the core mechanism: the AI is given a *toolbox* of approved, screen-scoped methods (filter, group, export, summarize, etc.) — it never gets the whole application.
- "**AI handles the intent, DevExpress handles the interaction**" — the assistant *triggers* actions through controlled DevExpress APIs rather than telling the user how to do them.
- The grid demo's **main loop**: user prompt → Azure OpenAI → DevExpress tool → public control API → real UI action.
- Tools are just **normal static C# methods with metadata**; the `[AIIntegrationTool]`-style description tells the model *when* to use a function and what its parameters mean — these descriptions drive tool selection.
- DevExpress **injects the live control instance** (e.g. the DX Grid) from the tools context at runtime — the model never supplies the grid; the method body calls the same API you'd call from a button click.
- Registration happens in **`Program.cs`** via a **keyed chat client** (`DXTools`) using `UseDXTools` (adds DevExpress tool definitions) + `UseFunctionInvocation` (executes calls, feeds results back to the model).
- Three integration **patterns** are shown: (1) AI **drives a control** via tool calling, (2) AI is **built into the control** (Report Viewer translation), (3) AI is part of a **custom workflow** whose output a report visualizes.
- The **Report Viewer owns the AI experience** for translation — no custom chat panel needed; enabled in `Program.cs` with `AddBlazorReportingAIIntegration` + `AddTranslation`.
- The **contract review** pattern decouples AI from rendering: the report knows *only* whether each clause `IsRisky` (true/false) and applies conditional formatting — "**AI creates the state, DevExpress presents the state**."
- Architecturally, the **AI layer doesn't swallow the app**: pages keep using DevExpress controls for UX, services still own business data, AI tools expose only *selected* capabilities.
- Custom-thought-out buttons only cover scenarios you anticipated; natural-language + tools let users work in ways you *didn't* pre-build — and when a request can't be honored, the user gets an **explanation, not a flat "no."**

## 📚 Detailed Notes

### Thesis: connect AI to controls, not chatbots beside apps
The session opens by ruling out two anti-patterns: this is **not about generating code**, and **not about dropping a chatbot beside an existing app and calling it done**. The real objective is to connect AI to the **controls**, the **data**, and the **workflows** users already use. The demo app is built in **Visual Studio** with **.NET**, **DevExpress Blazor controls**, **DevExpress Reporting**, and **Azure OpenAI through `IChatClient`**. Three worked examples follow, each illustrating a different integration pattern.

### Example 1 — AI drives a DevExpress Grid via tool calling
**The command center.** The home page is a "command center" with KPI cards, a **DX Chart** control, a **DX Grid**, and a **DX AI Chat** on the right. Sales data comes from a **CSV** loaded through a **data service**: `GetOrders()` feeds the grid (~**10,000 rows** of USA sales data), `GetSummary()` feeds the KPI cards, and `GetRegionMetrics()` feeds the chart. The presenter uses pre-baked recorded prompts.

**Traditional interaction still matters.** Users conventionally filter, sort, group, page, and export — and the DX Grid is very good at all of it (demoed: filter to **Texas**, group by **region**, expand, sort by **customer name**). You *could* build buttons for these, but buttons only cover the scenarios you thought of ahead of time. The framing question: **can we give the user a more natural way to work with this data?**

**Natural language → control actions.** Via the DX AI Chat the user asks in plain language:
- *"How did we perform this week?"* → handled by the **sales analysis tool**, which can call methods like `SummarizePerformance` (built-in executive-summary method) producing a concise business summary. (Analysis-only; no UI change.)
- *"Group the orders by customer."* → the grid responds and **groups by customer**.
- *"Group by profit"* → the code-behind has been deliberately scoped, so instead of silently failing or refusing, the user is **given an explanation** of what's going on.
- *"Highlight the payment risk accounts."* → grid updates; behind the scenes it calls a `FilterRiskAccounts` method.
- *"Export."* → an **XLSX** download is created via the export API.

**The key distinction.** This is the difference between a **chat answer** and an **application assistant**: the AI is *not telling the user how* to export — it **triggers the export through a controlled DevExpress API**. Mantra: **AI handles the intent, DevExpress handles the interaction.**

### Code deep-dive (Example 1)

**`Home.razor` — the chat control.** The page hosts the **DX AI Chat** control. The crucial setting is `ChatClientServiceKey = "DXTools"`, which points the chat control at the **tool-enabled AI client** registered in `Program.cs`. `IncludeFunctionCallInfo` is set to **true** for the demo so it can show which calls the tools make; in production you'd typically set this to **false**.

**Registering the toolbox (`OnAfterRender`).** A new **AI Tools Context Builder** is created. It registers two **live targets** — the actual **DX Grid instance** and the **sales data service** — then registers the methods the AI is *allowed* to call: `FilterByRegion`, `FilterByState`, `FilterRiskAccounts`, `GroupBy`, `ClearView`, `Export`, `Summarize`, and `ListTopCustomers`. This is the **toolbox for the current screen** — the AI does **not** get the whole application, only the approved capabilities registered here. At the end of the method the context is added to the **AI tools container**, making it available to the **DevExpress tool-calling pipeline**.

**A single tool (`SalesGridAITools` → `FilterByRegion`).** Each tool is a **normal static C# method with metadata**:
- An AI-integration-tool attribute gives the model the **function name**.
- A **description** tells the model *when* to use the function and what the parameters mean — *these descriptions matter because they guide tool selection.*
- The **DevExpress-specific part**: the model does **not** provide the grid; **DevExpress injects the live DX Grid instance** from the tools context at runtime.
- The method body then calls the **normal DevExpress Grid API** — the same code you'd write from a button click.
- All other tools follow the same pattern; **not every tool changes the UI** (some only return analysis).

**`Program.cs` — wiring the chat client.** Configuration is read from **.NET user secrets**: the **Azure OpenAI endpoint**, **key**, and **deployment name**. A **keyed chat client** named **`DXTools`** is created, and:
- `UseDXTools()` adds the **DevExpress tool definitions**.
- `UseFunctionInvocation()` **executes the tool calls and feeds the results back to the model**.

This is exactly what the DX AI Chat on the home page consumes. **The main loop** is stated as a key takeaway: **user prompt → Azure OpenAI → DevExpress tool → public control API → real UI action.**

### Example 2 — AI built into the DevExpress Report Viewer (translation)
The second pattern moves into the **Report Viewer**, showing a generated **quarterly memo report** built with DevExpress Reporting — but written in **French**. Using the **built-in AI tooling**, the user selects to translate the **entire document back to English** and presses **Translate**. Notably there is **no custom chat panel** on this page: **the DevExpress Report Viewer owns the AI experience**.

**Under the hood.** The report is a standard `XtraReport` that sets up a French memo section and a simple **report header / detail band / footer / page footer**. In `Program.cs`, AI behavior is enabled via **`AddBlazorReportingAIIntegration`** and **`AddTranslation`**. Configured languages include **English, French, Spanish, German, and Japanese**. `EnableTranslation` adds translation, and `EnableInlineTranslation` lets the translated content appear **inside the rendered report**. Pattern summary: **the control owns the AI experience.**

### Example 3 — AI as a custom workflow; report visualizes the result (contract review)
The third pattern composes a **custom workflow**. A **Master Service Agreement** is rendered in the DevExpress Report Viewer. The goal is **not** a text summary — the team wants **Azure OpenAI to identify risky clauses** *and* the **document itself to show them**. A button asks the chat control to **"review for issues."** The AI reviews the contract, identifies **risky / one-sided clauses**, and the report re-renders with **visual warnings**: a **side-panel findings** list, **highlighted clauses**, a **warning tag**, and a **red left border**. The answers appear on the right, but the **experience lives inside the document**.

**Code deep-dive — `ReviewAsync`.** Here there is **no DX AI Chat control**; the page **injects the AI chat client directly**:
- A **system prompt** instructs the model to act as a **commercial contract attorney**.
- The **user prompt** sends the **full contract text** via `ContractReport.GetFullText()`.
- `ChatClient.GetResponseAsync(...)` sends the request to the configured AI client; the response is stored for the findings panel.
- `ParseRiskyClauseNumbers` extracts references like **"clause 4"** or **"clause 9"**.
- The page constructs a **new `ContractReport`**, passing in the **risky clause numbers**.
- `RenderFindings` formats the AI response for the side panel, **preserving line breaks and bold headings**.

**Decoupling AI from rendering.** `ContractReport` holds the **12 contract clauses** and a clause source. `GetFullText` joins clauses into plain text for the model. The constructor receives the **risky clause numbers** and projects each clause into the report data source with **`IsRisky` = true/false**. Crucially, **the report doesn't know anything about AI** — it only knows whether each clause is risky; if risky, it **changes the band color and adds the warning tag**. Principle: **AI creates the state, DevExpress presents the state.**

### Architecture: the AI layer doesn't swallow the app
A quick look at the **project structure** — component pages, an **AI** folder, **reports**, **services**, and **data** — illustrates the design value: the **AI layer doesn't swallow the application**.
- **Pages** still use DevExpress controls for the user experience.
- **Services** still own the business data.
- **AI tools** expose only **selected capabilities**.
- **Reports** render through the **DevExpress Reporting APIs**.

The DevExpress controls make the AI *useful* by giving it **somewhere structured to act**: a grid can filter/group/sort, a report viewer can translate and render document content, and a report can **visualize AI-derived state through conditional formatting**. **The AI is powerful, but the control gives it shape.**

### Closing: intent → action, three ways
Across three pages the session shows practical ways to bring AI into a DevExpress app: (1) AI **drives the grid** via tool calling; (2) AI is **built directly into the control** (Report Viewer); (3) AI becomes part of a **custom workflow** that DevExpress reports **visualize**. The point is **not** to add a chatbot beside every app — it's to **let users express intent and use controls to turn that intent into action**. The closing line: **Azure OpenAI provides the intelligence, DevExpress provides the application service, and Visual Studio brings it all together.**

## 🛠️ Products / Features / Technologies Mentioned
- **DevExpress Blazor Controls** — DX Grid, DX Chart, KPI cards, **DX AI Chat** control.
- **DevExpress Reporting** — `XtraReport`, **Report Viewer**, conditional formatting (band color, warning tags), report header/detail band/footer.
- **DevExpress AI integration** — tool-calling pipeline, AI Tools Context Builder, `UseDXTools`, AI-integration-tool attributes/metadata, `AddBlazorReportingAIIntegration`, `AddTranslation`, `EnableTranslation`, `EnableInlineTranslation`.
- **Azure OpenAI** — accessed via **`IChatClient`** (Microsoft.Extensions.AI); `UseFunctionInvocation` for tool execution; `GetResponseAsync`.
- **.NET / Blazor** — `Program.cs` service registration, **keyed chat client** (`DXTools`), **.NET user secrets** for endpoint/key/deployment.
- **Visual Studio** — the IDE tying the solution together.
- **Data layer** — CSV-backed data service (`GetOrders`, `GetSummary`, `GetRegionMetrics`), ~10,000 rows USA sales data.

## 🚀 Announcements / What's New
None explicitly announced. This is a practitioner/partner demo session (DevExpress) showing patterns and existing capabilities for integrating Azure OpenAI tool calling with DevExpress Blazor controls and Reporting — no new product launches or release dates were called out.

## 💡 Demos
1. **AI-driven grid (command center).** Natural-language prompts ("how did we perform this week?", "group by customer", "group by profit", "highlight payment risk accounts", "export") drive a 10k-row DX Grid via tool calling, producing real grouping, filtering, an executive summary, and an XLSX export — with a graceful explanation when a request is out of scope.
2. **In-control report translation.** A French quarterly-memo report is translated **back to English** entirely through the DevExpress Report Viewer's built-in AI tooling (no custom chat panel), with inline translation appearing inside the rendered report.
3. **Contract review workflow.** A Master Service Agreement (12 clauses) is sent to Azure OpenAI with a "commercial contract attorney" system prompt; risky clauses (e.g. clause 4, clause 9) are parsed and re-projected into the report, which renders highlighted clauses, warning tags, red left borders, and a side-panel findings list.

## 📊 Notable Stats / Quotes
- **~10,000 rows** of USA sales data bound to the DX Grid.
- **12 contract clauses** in the contract-review report; risky ones flagged with `IsRisky = true`.
- Supported translation languages: **English, French, Spanish, German, Japanese**.
- *"This is the difference between a chat answer and an application assistant."*
- *"AI handles the intent, DevExpress handles the interaction."*
- *"The AI does not get the whole application, simply the approved capabilities that we register here."*
- *"AI creates the state. DevExpress presents the state."*
- *"The AI is powerful, but the control gives it shape."*
- *"Azure OpenAI provides the intelligence, DevExpress provides the application service, and Visual Studio brings it all together."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Build a minimal Blazor sample wiring a **keyed `IChatClient`** + `UseDXTools` + `UseFunctionInvocation` to drive a DX Grid by tool calling.
  - Experiment with **tool description wording** to see how much it affects model tool-selection accuracy.
  - Reproduce the **`IsRisky` conditional-formatting** pattern to visualize AI-derived state in a report independent of the AI call.
  - Try the **Report Viewer inline translation** with `AddTranslation` across the five supported languages.
- [ ] Questions:
  - How are tool-call failures / refusals surfaced to users beyond the "explanation, not no" example — is there a standard guardrail pattern?
  - What's the latency/cost profile of `UseFunctionInvocation` round-trips for multi-step grid operations on 10k rows?
  - Which DevExpress + Microsoft.Extensions.AI versions are required, and does this work with non-Azure `IChatClient` providers?
  - How is sensitive data (full contract text, sales data) handled re: Azure OpenAI data-handling / content filtering?
- [ ] Relevant to:
  - Internal Blazor LOB apps that want **agentic, intent-driven** UX over dashboards.
  - Teams evaluating **`IChatClient` / Microsoft.Extensions.AI** tool-calling patterns.
  - Reporting/document-heavy workflows (translation, contract/risk review) needing **AI-derived visual state**.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[Azure OpenAI]]
- [[Blazor]]
- [[IChatClient]]
- [[DevExpress]]
- [[AI Tool Calling]]
- Source list: [[2026 Build Session List]]
