---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/elastic
  - topic/github-copilot
  - topic/agents
  - topic/ai
  - topic/rag
  - topic/observability
source: https://www.youtube.com/watch?v=tg2zMWEM3a0
session_code: DEMSP385
event: Microsoft Build 2026
speakers: Elastic Developer Advocate (partner demo, name not stated in captions)
duration_min: 18
aliases:
  - Build context-aware agents using GitHub Copilot, Elastic, and Azure AI
---

# DEMSP385 — Build context-aware agents using GitHub Copilot, Elastic, and Azure AI

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Elastic Developer Advocate (partner demo session; speaker name not stated in the captions — Elastic × Microsoft)  
> **Duration:** ~18 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=tg2zMWEM3a0)

## 🎯 TL;DR
This is a hands-on partner demo showing how to make code review **context-aware** by wiring Elasticsearch into the GitHub pull-request flow. Instead of a PR review only answering "does the code compile / is it syntactically correct?", the demo adds a second, far more valuable question: **"will this change re-trigger an incident we already had in production?"** The trick is to feed past postmortems, RCAs, and OpenTelemetry traces (all stored in Elasticsearch) into an agent built with **Elastic Agent Builder**, invoked automatically from a **GitHub Action** on every PR. When a code diff semantically matches a prior production failure, the agent posts a PR comment with the specific incident date, root cause, the offending traces, and a suggested fix. The developer can then drop into **VS Code + GitHub Copilot** — which talks to the same Elastic data via an **MCP server** — to investigate and auto-apply the fix without ever leaving the editor. The core thesis: *move PR review from "looks syntactically fine" to "this exact change broke production on April 7th — maybe don't."*

## 🔑 Key Takeaways
- Traditional CI checks validate **correctness** (does it build, is it syntactically valid); this approach adds **operational memory** (did this pattern cause a real incident before).
- The architecture is a closed loop: **PR pushed → GitHub Actions fire → call an Elastic workflow → which calls Elastic Agent Builder → semantic match against incidents/traces → comment pushed back to the PR.**
- **Elastic Agent Builder** is Elastic's agent platform (run inside **Kibana**) for building and running custom agents over your Elastic data — agents have **skills**, **tools**, and **custom instructions**.
- Matching is **semantic / vector search, not keyword matching** — the agent looks for *patterns* (e.g. "concurrency / race condition") rather than literal string matches in the diff.
- Embeddings are generated **in-cluster using Jina AI embeddings** ("Gina AI" in the captions) across all postmortems, comments, and incident data, so a code change can be matched semantically to prior failures.
- The same underlying Elastic data and tools are exposed three ways: (1) automatically via the **GitHub Action**, (2) interactively by **chatting with the agent in Kibana**, and (3) inside **VS Code via an MCP server + GitHub Copilot** — pick whichever fits the developer's workflow.
- A **GitHub Action workflow** just gathers PR context (diff, title, repo, PR number) as environment variables, calls the Elastic workflow URL, and parses any returned match into a PR comment. End-to-end run takes **~1 minute** depending on data volume.
- The agent's tools are concrete Elastic queries: **search incidents** (semantic), **find similar traces** by HTTP route, and **find latency spikes** on those routes — backed by OpenTelemetry data in Elasticsearch.
- Elastic's tool queries use **ES|QL** (a newer SQL-like query language for Elastic) and a **`match` query function** that is deceptively powerful — it performs semantic/vector search rather than literal keyword matching.
- **Skills** can encode recurring failure knowledge: e.g. after a recurring race-condition incident, you add a skill that tells the agent specifically to watch for race conditions, making the LLM's generic awareness sharply targeted to *your* known problems.
- The agent doesn't just say "this looks risky" — it must **cite evidence**: the incident date, the root cause, sample traces, and concrete production impact, so the recommendation is defensible.
- **GitHub Copilot + MCP** lets a developer investigate and **auto-apply the suggested fix** in VS Code (Copilot rewrites the code, removes the unsafe change, makes the DB statement thread/checkout-safe, even adds an extra safety check).
- This guards against the modern failure mode where a **coding agent** (not a human) confidently introduces a change that already broke production — the incident memory catches it regardless of who/what wrote the code.
- You don't need the full stack to get value: **even just loading OpenTelemetry latency data** lets you catch spikes; postmortems and RCAs add richer matching on top.
- The pattern works in **dev too** — run postmortems in dev, store those lessons in Elastic, and match against them to get ahead of issues before they reach production.

## 📚 Detailed Notes

### The problem: PR review only checks correctness, not operational history
Today, when you push a PR, automated review tells you whether the code *works* — is it syntactically correct, does it pass the checks you've configured. If it fails, it's blocked; otherwise you merge. What that review **doesn't** tell you is whether the change will reproduce a failure you've already lived through. The speaker's framing: shift from *"now it looks good"* to *"it might be syntactically correct, but it hits the same production issue that happened last month."* The raw materials to answer that — **postmortem incidents, RCAs, and OpenTelemetry traces** — already exist in Elasticsearch; the demo ties them into the review.

### High-level architecture
The end-to-end flow:
1. You push a **PR** in GitHub.
2. **GitHub Actions** fire — running whatever checks you already have.
3. An added step calls an **Elastic workflow**, which in turn calls **Elastic Agent Builder** (Elastic's agent platform).
4. Using **semantic search** over OpenTelemetry similarities and incident postmortems, the agent decides whether this change matches a known prior failure.
5. If it matches, it **pushes a comment back into the PR**, and you decide what to do.
6. Optionally, you **drop into VS Code and use GitHub Copilot + the MCP servers** (wired back to Elasticsearch) to investigate and fix.

The whole point is to move review from "this looks fine" to "this is syntactically valid but it caused a production incident last month."

### The demo app: Wayfinder (e-commerce inventory)
The example application is **Wayfinder**, a fictional outdoor/adventure e-commerce store. The speaker's running gag: they're from Chicago, dream of climbing California's mountains, so they buy all the adventure gear and never use it. The **critical correctness property** is inventory accuracy under concurrency: if there's *one pair of boots left* and *three people try to buy it*, only **one** buyer must actually win the sale. This is the classic high-throughput **race condition** setup that the rest of the demo revolves around.

### Step 1 — The risky refactor (the PR)
The speaker opens a PR with a small, innocuous-looking refactor intended to improve behaviour **under high throughput**. The substantive change: instead of doing an **atomic checkout** inline, the new code **sets the quantity once and reuses a pre-computed value** in a couple of places. It's a minor, *valid* change — it passes all normal checks because there's nothing syntactically wrong with it. (The speaker had several practice PRs queued up because it's a big event.) This is exactly the kind of change a human — or a coding agent — might happily approve.

### Step 2 — The Elastic PR agent comment
On the PR's conversation tab, alongside the usual checks, there's an **Elastic PR agent** check — the heart of the demo. Elastic Agent Builder runs through the diff and posts a comment along the lines of:

> "The PR introduces a critical **race condition** that previously caused a production incident."

Crucially, the recommendation is **not** based purely on the LLM's training about code/reviews. It's grounded in *your actual data*:
- It cites a specific incident: **April 7th**, which caused **504 Gateway Timeouts**.
- It pulls **OpenTelemetry (OTel) traces** with specific trace examples.
- It explains the **root cause** of the earlier incident and why this change is a bad idea.
- It even includes a **suggested fix** to make the change without breaking production.

The narrative: "you (or a coding agent) made this change before, and we broke production at least once — maybe don't do it again."

### The GitHub side — how the Action is wired
The setup is deliberately simple. The GitHub Action calls **one workflow URL**. In real time it takes about **a minute** to run, depending on how much production data, how many incidents/RCAs, etc. The workflow file:
- Calls **Elastic Agent Builder**, optionally posting a comment if it matches a prior failure.
- Passes the needed **environment variables**: PR number, title, repo — whatever the Elastic-side agents need.
- The bulk of it is just **gathering PR data to send to the agent**: getting the diff, collecting context, instructing the agent to use its tools (e.g. searching OTel traces).
- At the bottom, logic to **parse the agent's response** and, if something came back, generate the PR comment.

So the GitHub responsibility is narrow: **gather PR info + diff → send to Elastic → parse the result → comment.**

### The Elastic side — Kibana, Agent Builder, and the agent's configuration
Hopping into **Kibana** (Elastic's UI on top of Elasticsearch), the speaker opens the **Agent Builder / Agent UI** (described as fairly new — Elastic, "like everyone else here at Build", is embedding agents as much as possible). Key elements:

- **Conversation history** — every run is stored, *including the automated GitHub-triggered ones*, so you can go back and see what each PR review did.
- **Skills vs Tools** (an important distinction):
  - **Skills** provide *information/guidance* — how something should be done, info about a system, or a set of actions/procedures.
  - **Tools** provide *functions* — actual capabilities like querying Elasticsearch, doing semantic/vector search, reaching out to **MCP servers**, or running **workflows**.
- **Custom instructions** — because it's a custom agent, you brief it: *"You are an AI pull-request reviewer. Wayfinder is the store. You have access to OpenTelemetry data, historical incidents, postmortems…"* The instructions walk the agent through the steps: **fetch the PR diffs → identify the routes being used → look for patterns (not keywords) → use the tools.** Tools don't have to be hardcoded into the instructions — they're injected automatically.
- The agent is explicitly told to **look for patterns, not keywords** — semantic lookup, not string matching — and, when it finds a match, to **explain what the match is, how it was found, and give specific examples**, so the verdict is "production actually broke" rather than a vague "seems like a bad idea."

### Skills as institutionalised RCA knowledge
A powerful idea: when you have a **recurring incident**, part of your postmortem/RCA can be **creating a skill** that teaches the agent to watch for that specific failure class — e.g. a skill that looks for **race conditions**. The LLM already "knows" what a race condition is, but a skill lets you be *very specific* about the failure modes that have actually bitten *your* system, so the agent's attention is focused where your real risk lives.

### Tools in detail — ES|QL and the semantic `match` function
The agent has several Elastic tools:
- **Find similar traces** based on HTTP routes.
- **Find latency spikes** on those routes.
- **Search incidents** — matching against previous incidents.

The speaker polls the room on **ES|QL** (Elastic's newer **SQL-like query language**) — few hands up, since it's newish. The incident-search tool is described as a "dead simple ES query," but the key subtlety is the **`match` query function**: it looks like a keyword match but is actually doing **semantic / vector search**. This works because **embeddings are generated in-cluster using Jina AI embeddings** (captioned "Gina AI") across all postmortem incidents, comments, and data — so a full-text query can match **semantically** on what was going on, not just on literal terms. Tool descriptions are kept short in the demo but can be more verbose in a real production environment.

### Workflows — the other half of the GitHub bridge
Earlier, the GitHub-side workflow gathered env vars and called an Elastic workflow. In Kibana, the speaker shows the **Elastic-side workflow** that receives it. Reviewing a run from the prior week's setup: it's straightforward — it collects the env vars / PR info and then **calls the agent in Elasticsearch**. The **input** is a body containing e.g. **PR 37** plus the passed context; the **output** (because it's a demo, it found a match) reported that it ran for PR 37, the **agent responded 200**, and the comment got sent back via the **GitHub MCP tool**. (The comment isn't stored in the workflow run itself — it's posted into GitHub.)

### Talking to the agent directly (interactive mode in Kibana)
Beyond the automated path, because all the data is in Elastic and it's an agent, a developer can **chat with the agent directly** — even *before* submitting a PR. Example question: *"I'm looking at a PR that removes the atomic quantity check — are there any known patterns this matches?"* The agent then:
- Calls its **search-incident tool** — looking for **concurrency patterns**, and actually invokes it **three times** with different phrasings/terminology to cover what you might be describing.
- Returns **five results** per call (different results), then calls **find similar traces** for the endpoint to check for real events and **latency spikes**.
- Produces a **human-friendly answer** grounded in evidence: it references the **April 7th** incident, a fix that was applied, and concrete impact — e.g. **847 lock-contention events** caused the production **success rate (ability to actually sell items) to drop from 99.7% to 76%.** It surfaces the **postmortem**, sample traces, and a **recommendation**.

You can also ask about a **specific endpoint** ("I'm going to work on this endpoint — anything in past postmortems for it?") and the agent finds recent telemetry showing it broke. The throughline: every answer is grounded in **real incidents, OTel traces, and postmortems**, getting you ahead of breakage.

### VS Code + GitHub Copilot + MCP (the developer-native path)
Many developers would rather **never leave VS Code** — and that's fully supported. In VS Code with **GitHub Copilot**, the speaker has the **Elastic MCP server** hooked up, so all the Elastic data and **all the tools the agent has** are exposed over the **MCP protocol**: find similar traces, search incidents, OpenTelemetry incident analysis, etc. The developer asks Copilot, in plain language: *"I got this PR comment for the inventory reserve — can you tell me what was happening and what went on?"* The same flow happens, **without leaving the editor**:
- Copilot calls the same **MCP tools** (find similar traces, find latency spikes), analyses the data, and assembles a response: it was in a **prepared statement**, hit the cache rate, and **matches exactly the pattern from April 7th**.
- The conclusion is the same: someone (or a coding agent) made this change before and it already broke; here's how to fix it.

### Auto-applying the fix with Copilot
Rather than editing by hand, the developer just says **"yes"** and lets **Copilot make the change**. Copilot:
- Removes the early **hard-coding of the new quantity** and deletes the **misleading comment**.
- Changes the **DB statement (line 46)** to be **thread-safe / checkout-safe**.
- **Adds a second check**, noting that this still isn't *truly* transactional — it's doing its best to manage concurrency; if you wanted full guarantees you could make it an **actual SQL transaction**, but the code does what it can.

Copilot then **reports back** on exactly what it changed, and the developer can **commit and push**.

### Validating the fix — the test harness
Finally, a quick terminal demo: a **test harness fires 20 concurrent requests** — the "one pair of boots, 20 eager buyers" scenario — to confirm only **one** buyer gets assigned the item. After the fix, the test passes: *"we wanted one, we got one."* Simple, but it closes the loop from "agent flagged the risk" to "fix applied" to "concurrency verified."

### Closing thesis
You don't have to adopt everything at once. Even just loading **OpenTelemetry data** lets you watch for **latency-spike changes**. Layer in **postmortems and RCAs** for richer matching. By calling **Elasticsearch automatically as part of a GitHub Action**, you get ahead of **recurring production issues**. And the same approach works in **dev**: run postmortems in dev, store those lessons in Elastic, and match against them so dev learnings prevent future breakage. (Sign-off: Elastic is in the other building with build-it-yourself Lego/clicky fidget things — thanks for hanging out.)

## 🛠️ Products / Features / Technologies Mentioned
- **Elasticsearch** — the search/data store holding postmortems, RCAs, incident records, comments, and OpenTelemetry traces; queried semantically to match code changes to past failures.
- **Elastic Agent Builder** — Elastic's agent platform (run within Kibana) for building/running custom agents over Elastic data, with skills, tools, custom instructions, and conversation history.
- **Kibana** — Elastic's UI layered on Elasticsearch; hosts the Agent Builder / Agent UI used in the demo.
- **ES|QL** — Elastic's newer SQL-like query language used to write the agent's tools (e.g. the incident-search query).
- **`match` query function (semantic)** — an Elastic query function that looks like keyword matching but performs semantic/vector search against in-cluster embeddings.
- **Jina AI embeddings** (captioned "Gina AI") — the embedding model used **in-cluster** to vectorise postmortems, comments, and incident data for semantic matching.
- **OpenTelemetry (OTel) traces** — the telemetry data (HTTP routes, latency, error traces) used to evidence incidents and detect latency spikes.
- **GitHub** / **GitHub Actions** — the PR platform and CI; an Action gathers PR context and calls the Elastic workflow, then posts the agent's comment back to the PR.
- **GitHub MCP tool / GitHub MCP server** — used by the Elastic workflow to post comments back into GitHub.
- **GitHub Copilot** (in VS Code) — the in-editor AI that calls Elastic tools via MCP, explains incidents, and auto-applies the suggested fix.
- **MCP (Model Context Protocol) server (Elastic)** — exposes all the agent's Elastic data and tools (find similar traces, search incidents, OTel incident analysis) to clients like Copilot/VS Code.
- **VS Code** — the developer-native environment where the whole investigate-and-fix flow can happen without touching Kibana.
- **Wayfinder** — the fictional adventure/outdoor e-commerce demo app whose inventory race condition drives the scenario.
- **Skills (Elastic agent)** — encode procedural/system knowledge (e.g. "watch for race conditions") derived from recurring RCAs.
- **Tools (Elastic agent)** — concrete functions: query Elasticsearch, semantic/vector search, find similar traces, find latency spikes, search incidents, call MCP servers, run workflows.
- **Workflows (Elastic)** — orchestration that receives PR context, calls the agent in Elasticsearch, and returns results to GitHub.

## 🚀 Announcements / What's New
None explicitly announced. This is a demo of an integration pattern rather than a product-launch session. The speaker notes that the **Elastic Agent Builder / Agent UI is "fairly new"** and that Elastic has been increasingly **embedding agents** into its products, and that **ES|QL** is "newish" — but no specific preview/GA dates, version numbers, or new releases were announced in the captions.

## 💡 Demos
- **End-to-end PR review on a risky refactor:** Pushed a PR to Wayfinder that replaced an atomic inventory checkout with a pre-computed/reused quantity. It passed all normal checks, but the **Elastic PR agent** commented that it reintroduces a **race condition** tied to the **April 7th** incident (504 timeouts), citing OTel traces, root cause, and a suggested fix. *Proved: review can be grounded in real operational history, not just code correctness.*
- **Walkthrough of the GitHub Action workflow:** Showed the (single-URL) workflow that gathers PR env vars/diff, calls Elastic (~1 min runtime), and parses the response into a PR comment. *Proved: the GitHub-side setup is minimal — just gather + call + parse.*
- **Kibana Agent Builder configuration:** Showed conversation history (including automated runs), the **skills vs tools** distinction, the agent's **custom instructions** ("AI PR reviewer… fetch diffs, identify routes, match patterns not keywords"), and the race-condition **skill**. *Proved: how the agent is briefed and how RCA knowledge is institutionalised.*
- **Tool internals (ES|QL + semantic match):** Showed the incident-search tool as a "dead simple ES query" whose `match` function actually does **vector/semantic search** via in-cluster Jina embeddings, plus find-similar-traces and find-latency-spikes tools. *Proved: matching is semantic, not keyword-based.*
- **Elastic-side workflow run (PR 37):** Showed the workflow that receives PR context and calls the agent; the run found a real incident match, returned **agent response 200**, and posted the comment via the GitHub MCP tool. *Proved: the GitHub↔Elastic round trip.*
- **Interactive agent chat in Kibana:** Asked the agent about removing the atomic quantity check; it called search-incident **3×** with varied phrasing (5 results each), found similar traces/latency spikes, and gave a grounded answer citing April 7th, **847 lock-contention events**, and a **99.7% → 76%** success-rate drop. *Proved: developers can query the same memory ad hoc, even pre-PR.*
- **VS Code + Copilot + MCP investigation and auto-fix:** Asked Copilot about the PR comment; it used Elastic MCP tools to confirm the April 7th pattern, then auto-applied the fix (removed unsafe hard-coding + misleading comment, made the DB statement thread/checkout-safe on line 46, added a second safety check) and reported back. *Proved: the developer can investigate and remediate without leaving the editor.*
- **Concurrency test harness (20 requests):** Fired 20 concurrent buy requests at the single-stock item; after the fix, exactly one buyer was assigned ("we wanted one, we got one"). *Proved: the applied fix actually holds under concurrent load.*

## 📊 Notable Stats / Quotes
- **99.7% → 76%** — the production success rate (ability to actually sell items) dropped this far during the original April 7th incident.
- **847 lock-contention events** — the volume of contention events tied to that incident.
- **504 Gateway Timeouts** — the user-facing symptom of the April 7th production incident.
- **April 7th** — the date of the prior incident the agent repeatedly cites as evidence.
- **~1 minute** — typical end-to-end runtime for the PR review (varies with data volume / number of incidents/RCAs).
- **PR 37** — the example PR used in the Elastic-side workflow run (agent responded **200**).
- **3 calls / 5 results each** — the agent invoked the search-incident tool three times with varied phrasing, returning five results per call.
- **20 requests** — the concurrency test harness load against the single-stock item.
- **"Move from *now it looks good* to *it might be syntactically correct, but it hits a production issue that happened last month*."** — the session's core thesis.
- **"We're looking for patterns, so not keywords… we're doing semantic look-up."** — on how matching actually works.
- **"Production broke, probably don't — maybe don't do that."** — the tone of an evidence-grounded agent recommendation.
- **"Maybe the coding agent decided this was a good idea, but we broke production at least once before — maybe you don't want to do it."** — on catching risky changes regardless of whether a human or an agent wrote them.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up an **Elastic Agent Builder** agent over a sample dataset of postmortems + OTel traces and wire it to a **GitHub Action** on a test repo to reproduce the PR-comment flow.
  - Experiment with the **`match` query function + in-cluster Jina AI embeddings** to confirm semantic (not keyword) matching of code diffs to incident text.
  - Hook the **Elastic MCP server** into VS Code + GitHub Copilot and try the "explain + auto-fix" loop end-to-end.
  - Build an Elastic **skill** that encodes a specific recurring failure class (e.g. race condition) and measure whether it sharpens the agent's recommendations.
  - Write the same concurrency **test harness** (N parallel buy requests on a single-stock item) as a guardrail to validate fixes.
- [ ] Questions:
  - How does the agent reliably extract "routes being used" from an arbitrary PR diff across different languages/frameworks?
  - What governs match precision/recall — embedding model choice, how postmortems are written, ES|QL tuning? How do you avoid false-positive PR comments that annoy developers?
  - Where does **Azure AI** fit (it's in the title but not detailed in the captions) — is it the model backing Copilot/Agent Builder, or an Azure-hosted embedding/LLM endpoint?
  - What's the cost/latency profile at real production scale (many incidents/RCAs), given the demo quotes ~1 min?
  - How are skills/instructions versioned and governed so the reviewer agent stays trustworthy over time?
- [ ] Relevant to:
  - Any team running **CI/CD on GitHub** that already has **observability (OpenTelemetry)** and **postmortem/RCA** practice — this turns that history into an active PR guardrail.
  - Platform/SRE teams wanting to **prevent recurring incidents** rather than just detect them post-deploy.
  - Teams adopting **AI coding agents** who need a safety net against confident-but-regressive changes.
  - Anyone evaluating **Elasticsearch as a RAG/agent substrate** with semantic search over operational data.

## 🔗 Related
- [[GitHub Copilot]] — The in-editor AI used here with the Elastic MCP server to investigate incidents and auto-apply fixes.
- [[Model Context Protocol (MCP)]] — The protocol exposing Elastic's tools/data to Copilot and other clients.
- [[Elasticsearch]] — The vector/semantic search store underpinning the context-aware agent.
- [[OpenTelemetry]] — The trace/telemetry data used as evidence for incidents and latency spikes.
- [[RAG - Retrieval Augmented Generation]] — The broader pattern of grounding agent answers in retrieved (here, semantically matched) operational data.
- [[Race conditions and concurrency]] — The specific failure class the demo guards against (inventory checkout under load).
- Source list: [[2026 Build Session List]]