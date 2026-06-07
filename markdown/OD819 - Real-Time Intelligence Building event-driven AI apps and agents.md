---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/fabric
  - topic/real-time-intelligence
  - topic/event-driven
  - topic/ai
  - topic/agents
source: https://www.youtube.com/watch?v=ywmZvOPekU4
session_code: OD819
event: Microsoft Build 2026
speakers: Tessa Cluster, Arindam Chatterji, Anul Sharma
duration_min: 46
aliases:
  - "Real-Time Intelligence: Building event-driven AI apps and agents"
---

# OD819 — Real-Time Intelligence: Building event-driven AI apps and agents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Tessa Cluster (Partner Director of Product Management, Real-Time Intelligence & IQ) · Arindam Chatterji (Principal Product Manager, Fabric Real-Time Intelligence — ingestion/processing) · Anul Sharma (Principal Product Manager, Real-Time Intelligence — analytics/action)  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ywmZvOPekU4)

## 🎯 TL;DR
Microsoft Fabric **Real-Time Intelligence (RTI)** is the event-driven backbone of the unified intelligence platform — "there is no AI without RTI." This session walks the full end-to-end loop: **ingest → process/route → analyze → act**, framed around a real-world stadium game-day operations scenario (hundreds of data points, thousands of events per second). Eventstream brings ~40 managed connectors (Kafka/AMQP endpoints, SQL or no-code processing, schema registry, the new **Deltaflow** for CDC). **Eventhouse** is a purpose-built petabyte-scale time-series/event store (demoed at **378 trillion records**, ingesting **13.5–14 billion records/minute**) queryable with KQL or SQL, feeding real-time dashboards and Power BI. An intelligence layer adds anomaly detection, ontology-based business context, Activator rules/alerts, **Eventhouse MCP + Fabric skills** for agent-first analytics, and the headline announcement: the **Operations Agent is now Generally Available**, running 24×7 in Teams to observe, reason, recommend, and act autonomously.

## 🔑 Key Takeaways
- **"There is no AI without RTI"** — high-volume, high-granularity, fresh, time-sensitive data is the prerequisite for accurate, useful AI; RTI provides that operational foundation.
- RTI is the marriage of **enterprise real-time platforms** (Azure Event Hubs, Event Grid, Stream Analytics, Data Explorer, Azure Maps) with **self-service Fabric experiences** — a fully integrated native SaaS, democratizing previously highly technical systems to users of all skill levels.
- The RTI loop has four stages — **ingest → process/route → analyze/model/visualize → act** — all built on **OneLake** with shared governance and Copilot integrated throughout.
- **Eventstream** offers **~40 managed connectors** (and growing), exposing both **Kafka and AMQP** endpoints; data can be processed in-motion via **SQL** (joins, window functions) or a **no-code drag-and-drop** operator, with a **schema registry** for governance.
- Processed events can fan out to **multiple destinations from a single SQL operator** — Eventhouse, another Kafka endpoint, or directly to **Activator**.
- **Deltaflow** (public preview) makes CDC dramatically easier — transforms Debezium events, auto-manages schema drift and hundreds/thousands of source tables into analytics-ready form, so you build the app instead of plumbing.
- **Fabric Spark + notebooks** can read directly from Eventstream (auto-generated boilerplate), apply AI/LLM function calls in Python, and publish **Fabric business events** back into the system.
- **Eventhouse** is a purpose-built, multimodal store for event/log/time-series analytics at **petabyte scale with sub-second query performance**; schemaless ingestion of text, JSON, metrics, and time series with no need to pre-model.
- Eventhouse uses a **medallion architecture** — raw **bronze** → **update policies** (lightweight transforms) → **silver** → **materialized views** (dedupe/aggregate) for reporting.
- One engine spans diverse analytics: **time-series** (decomposition, prediction, anomaly detection), text/JSON search, relational queries, **sequence analysis**, **geospatial**, **vector similarity** (for RAG), and inline **Python** — all without moving data.
- Live-demo scale was staggering: a single table held **~378 trillion records**, with **~13.5–14 billion new records added per minute**; a separate live GitHub-events table held **~3.6 billion rows**.
- **Copilot** turns natural-language questions into KQL (also a great way to learn KQL); the same analytics foundation is shared by both humans and agents.
- **Agent-first analytics:** **Eventhouse MCP** lets agents query live data; **Activator MCP** lets agents define rules/alerts in natural language; **Fabric skills** give agents reusable RTI capabilities and domain knowledge, wired into tools like **GitHub CLI / GitHub Copilot CLI** and "cloud code."
- **Anomaly Detector** (public preview) auto-selects the best out-of-box model based on seasonality/pattern — no data scientist required — and emits anomaly events others can subscribe to.
- **Ontology item** maps business context (entities + actions) onto raw data, giving agents real understanding rather than just raw rows (see the Fabric IQ session).
- 🚀 **Operations Agent is GA** — a virtual operations team member that runs 24×7 in Teams, closing the observe→analyze→decide→act loop autonomously, with playbooks, root-cause analysis, parameter confirmation, and full activity monitoring.
- Other shipped/updated bits called out: **MQTT connector** (new version), **Oracle DB CDC** connector, **Mirror DB change feed** connector, **custom stream connector** (private preview), **Delta change feed** connector (public preview), **Fabric business events**, **Eventstream observability** via workspace monitoring, and new **Activator actions**.
- Fabric ships **every single week** — keep an eye on the release planner/notes; free hands-on **workshops/labs** are available in many countries via the session's QR codes/links.

## 📚 Detailed Notes

### Why AI matters — and what gets in the way
Tessa opens by reframing the AI conversation around real value. AI excels at finding the signals that matter across the noise, distilling them, and helping make good decisions **in time**. But a lot gets in the way today: data volumes are too large, there are far too many instances for an individual human to comprehend, and even when humans can distill and understand the data, they often can't **act in time** to drive a positive outcome. That gap is exactly where a system can help — but in the AI era it needs more **structure and layers** to provide an operational foundation for the modern enterprise.

### The layered platform: unified data + unified intelligence
Thinking of signals coming in and actions feeding back, the enterprise needs distinct layers: a **unified data estate**, a **unified data platform** to make sense of it, and a **unified intelligence platform** on top — so the entire team (humans *and* agents) gets the most out of the system and can act at the right time. **Microsoft Fabric** is positioned as that unified data platform for the AI transformation.

### Where RTI sits in Fabric
Fabric spans a wide range of capabilities: data integration, big-data analytics, out-of-box databases, **Real-Time Intelligence** (today's topic), the **IQ capabilities** (announced at Ignite), and Power BI — all built on the unified Fabric platform with **OneLake**, shared governance, and **Copilot integrated throughout**. RTI specifically takes Microsoft's enterprise real-time data platforms — **Azure Event Hubs, Event Grid, Stream Analytics, Data Explorer, Azure Maps** — and marries them with self-service experiences tailored to business users, **democratizing** previously highly technical, high-end systems and delivering a fully integrated **SaaS** experience natively in Fabric.

### What "Real-Time Intelligence" actually is
RTI is a collection of capabilities that always starts with the **data**. On the input side there's a wide range of out-of-box connectors for Microsoft sources and cross-cloud, making it easy to land streaming/event data wherever it originates. As data flows in, RTI provides "different tools in the toolbox": **stream processing/transform/route** in real time, rich **analytics curated for time-series**, **modeling** (geospatial, and graph for relationship/causal modeling), truly real-time **operational visualization**, and — most importantly — the ability to **act** on it and change the surrounding business and systems so the business keeps up at the **speed of data**. Customers across healthcare, sports, manufacturing, financial, and retail use RTI today to mitigate risk and improve efficiency.

### The stadium scenario (the running example)
Arindam grounds the whole session in a stadium/game-day operations story (with a nod to a continent-wide wave of soccer games next month). Fans pass through turnstiles, buy concessions, and enjoy the game — generating data at **hundreds of points** and **thousands of events every single second**. Game-day operations teams must **collect** all of it, **make sense** of it, and **act within minutes — sometimes seconds**. The demos show how RTI + Eventstream accomplish exactly that.

### Ingestion: connectors and Eventstream basics
Arindam (Principal PM on Fabric RTI) covers ingest/process/route. Much of an organization's data starts **outside** Fabric and is real-time in nature. Rather than writing lots of code, RTI provides a **managed experience** via **close to 40 connectors**, started with simple click + drag-and-drop. From those sources, messages get routed to an **Eventstream**, which exposes both a **Kafka** and an **AMQP** endpoint — giving flexibility for open-source clients or AMQP-based apps.

### Processing events in motion: SQL or no-code
Once ingested, there are two ways to process events while they're in motion: a **SQL** way (familiar SQL for querying, transforming, processing) or a **no-code** experience (drag-and-drop operators onto a surface). As events flow, their shape changes; those evolving structures can be registered into a **schema registry** and managed there, giving governance as data moves through the system.

### Destinations and downstream integration
After processing/transforming, events can go to several destinations. The flagship is **Eventhouse** (high-performance, low-latency, high-volume time-series database — covered later by Anul). Eventstream can also **integrate output with other systems** — e.g., send to another **Kafka endpoint** if the application needs it. You can also **act** on the data via **Activator** rules and integrate with other systems. Finally, **Spark** is a first-class option: with stream-processing code in **Python**, you can use **Fabric Spark + Fabric notebooks** to pull data from Eventstream, process it, and send it to further downstream endpoints Spark can reach.

### Demo 1a — Turnstiles via MQTT (the developer journey)
Arindam starts in the **Real-Time Hub** (shows all streaming assets), goes to **Add data**, and from the dozens of connectors picks the **MQTT** connector for the turnstiles (MQTT is a great protocol for turnstile events). He sets up a secure connection to the MQTT **broker**, configures the **topic name**, chooses **MQTT v3** (widely used in IoT), reviews connection details — and in a few clicks has an Eventstream ingesting data from all turnstiles. He then enters **edit mode**, launches the **SQL code operator**, and edits the starter `SELECT *` query (pasting in code he'd pre-written, "maybe with some agents"), doing simple filtering and routing to different destinations. A standout productivity feature: he can **test the query directly from the editor** without moving to production. He saves and **publishes** the Eventstream — now live, processing, and delivering turnstile passage events into the Eventhouse destination, which he verifies by opening the Eventhouse.

### Demo 1b — Late/out-of-order events + fraud detection
In real game-day operations, events arrive **late** and **out of order**. Eventstream handles this with a few simple **policies** that guide how late/out-of-order events are treated. Arindam then builds something more interesting: detecting **duplicate tickets** (fraud) using simple **window aggregations** — specifically a **hopping window** that flags when the **same ticket is used within 120 seconds** at different gates (or even the same gate). With a second SQL code operator set up, he wires it to the **Activator UI** so that each time a duplicate/fraud event occurs, a **custom action** fires — alerting operations staff to act quickly. Powerful insights from turnstile events in just a few clicks.

### Eventstream recap + connector announcements
Arindam recaps that MQTT is just one of dozens of ever-growing connectors and calls out specifics: the **new MQTT connector version**, the **Oracle DB change-data (CDC) connector** (now available), an **HTTP connector** (pull from REST endpoints automatically — very popular), and a **Mirror DB change feed connector** (for change feeds from databases/delta tables/mirror databases). More connectors are "on deck" and coming soon. For developers who don't want to wait on first-party connectors, he announces a **custom stream connector** (**private preview**): create your own connector, upload the package, and Fabric **hosts it for you** to pull from your own sources into an Eventstream. He reiterates Eventstream's powerful **SQL semantics** (joins, window functions), the ability for a single SQL operator to **write to multiple destinations** (Eventhouse or directly Activator), **complex event-time handling policies** for production, and developer-productivity features around **interactive preview, testing, and debugging** — with much more coming.

### Demo 2a — Concessions via SQL CDC + Deltaflow
Now the fans hit the **concession stands**, so inventory must always be tracked. Arindam creates a **second Eventstream**, this time choosing **SQL CDC** as the source because concession transactions and inventory levels live in **Azure SQL** (no app changes needed). He grabs **CDC events** from all the tables, then makes an important choice: enabling **Deltaflow** (**public preview**) to quickly convert CDC into an **analytics-ready** form bound for Eventhouse. He names the **schema registry** (where schemas + source tables are stored), connects, and — in a few simple steps — simple CDC events flow into the Eventstream and on to Eventhouse. He configures it to use each **source table's schema to create matching tables** in Eventhouse, keeps **separate tables per schema**, and elects to land **just the payload, not metadata**. On publish, within seconds Eventhouse shows **~6–7 tables** created, the **initial snapshot replication** begins, and the SQL data (and its changes) is now available in Eventhouse for downstream applications.

### Demo 2b — Spark notebook + a sprinkle of AI → Fabric business events
To react quickly when a concession stand needs **replenishment**, Arindam opens a **notebook**, connects it to the concession Eventstream, and chooses **read with Spark**. The system **auto-generates all the boilerplate** connection/reading code (initially outputting to console). He then writes logic — much of it **AI-generated** — building a **prompt based on the inventory-level data** and calling **generate response** to get the AI's output. He then publishes a new **Fabric business event**, so the Spark job is now emitting **business events** into Fabric. Back in the **Real-Time Hub**, the business event appears; opening it shows trends, but he wants to **act**. Each time a **"replenish concession"** event fires, he gets an event — and the sample AI output says, e.g., *"queue up 200 units of hot dogs"* from one place in the stadium to another. To stay on top of things on game day, he also enables **monitoring for Eventstream**: with a few clicks, detailed telemetry/logs about Eventstreams flow into the **workspace monitoring** databases, from which simple operational **dashboards** can be built.

### Eventstream/CDC recap + more announcements
Arindam recaps the second demo's new pieces. **Deltaflow** builds on existing CDC connectors to make processing **Debezium** events even easier — quickly transforming them, gracefully handling **schema changes on the source side**, and managing hundreds (sometimes thousands) of source tables into the destination, so teams build apps instead of plumbing. Because much data now lives in **delta tables** in Fabric (via **mirror database**), he announces the **public preview** of a **Delta change feed connector** that works great with **mirror databases** — and **very soon** with general **lakehouse delta tables**. **Spark structured streaming** brings Spark's huge ecosystem closer to Eventstreams — AI function calls, Python code, and open-source libraries now in your hands. **Fabric business events** shift the focus from merely processing/creating more data to **identifying business events** that can be published and acted on. And tying it together for game day, **Eventstream observability as part of workspace monitoring** gives the capabilities to constantly monitor the running system.

### Analyze + act at scale: enter Eventhouse
Anul Sharma (Principal PM, RTI) takes over for analyze/act. Once data streams in at **high velocity and high granularity**, the next challenge is **ingest → analyze → act** — which is where **Eventhouse** comes in: a **purpose-built store for event/log and time-series analytics**, designed for **petabyte scale with sub-second query performance**.

### The end-to-end real-time analytics flow (medallion in Eventhouse)
A typical flow: connectors on the left bring data in; it's modeled in a **medallion architecture** with multi-tier staging. Data first lands in the **bronze** (raw ingestion) layer. **Update policies** — lightweight transformation functions — automatically transform/enrich data as it arrives and move it into **silver**. You can then optimize further with **materialized views** (deduplicating, creating aggregations) so reports run efficiently on top. For querying, use **KQL** for deep analytics or **SQL** for familiarity. On the output side, this data powers **real-time dashboards** and **Power BI** reports. Critically, everything lives in **OneLake** — not siloed, fully integrated across the broader data estate.

### The intelligence layer on top
Where it gets powerful is adding an **intelligence layer**: define **rules**, create **alerts** with **Activator**, run **anomaly detection**, and build an **ontology** that maps business context onto the data. Ultimately, **agents** — operation agents and **data agents** in Fabric — act on your behalf, enabling AI-driven automation and **real-time decisioning** directly on streaming data.

### Eventhouse as a multimodal analytics platform
Eventhouse is a true **multimodal** analytics platform designed for **diverse, schemaless** data — ingest **text, JSON, metrics, time series** without pre-modeling or forcing data into rigid structures before getting value. This is critical for **high-granularity data across time and space** (logs, telemetry, user actions, IoT signals) where the data's shape constantly evolves. Once in, you can seamlessly move across: **time-series analysis** (decomposition, prediction, anomaly detection), **text and JSON search**, **relational queries**, **sequence analysis**, **geospatial** insights, and even **vector similarity search** for **AI-driven RAG** scenarios. For deeper analytics, run **Python code inline** without moving data out. The key idea: **one engine** handling **diverse data and diverse analytics patterns at scale and in real time**.

### Demo 3a — Eventhouse at staggering scale (KQL & SQL)
Anul opens a **KQL query set** attached to one of his Eventhouses. Counting rows on a table returns **~378 trillion records** — huge. Looking at the last hour shows roughly **13.5–14 billion new records added every minute** — immense real-time processing. He shows the same insight is reachable via **SQL** as well as KQL.

### Demo 3b — Live GitHub events analysis
Switching scenarios to a hypothetical **GitHub team** responsible for user scenarios, usage, and platform health: live **GitHub events** (developer actions like pull/push requests) flow through an **Eventstream** into an **Eventhouse**. A count shows **~3.6 billion rows**. Inspecting event types reveals push/create events etc. The data is a **mix of structured and semi-structured** — some fields hold **JSON key-value pairs**, which KQL can **expand and project** into fixed columns (e.g., a user's display name) to analyze a specific user's activity. For **capacity forecasting**, an inbuilt **forecasting function** projects future patterns from existing data. Conditional queries can power **alerts via Activator** (Teams messages, custom workflows, invoking notebooks). And for those who'd rather not write queries, **Copilot** turns **natural-language** questions into **KQL** — a great way to both get insights and **learn KQL**.

### Agent-first analytics: MCP + Fabric skills
Anul anticipates the 2026 mindset: *"my agents are doing most of the job for me — what do you have for them?"* The question shifts from *how do I analyze* to *how do I empower the agent*. The answer: **Eventhouse MCP** (agents ask questions directly over live data for instant insights), **MCP-enabled items like Activator** (define rules/alerts in natural language), and **Fabric skills** — reusable capabilities + domain knowledge teaching agents how to interact with RTI items, wired into tools like **GitHub CLI** and **"cloud code."** So agents can **reason, act, and detect** in real time, not just query.

### Demo 4 — End-to-end agentic flow via GitHub Copilot CLI
Anul builds an end-to-end real-time analytics flow entirely from **GitHub Copilot CLI** with **Fabric skills** installed. Listing skills shows **Eventhouse**, **Eventstream authoring**, and **consumption** skills. He prompts: *create a new Eventhouse, build a medallion architecture with everything we just learned, and surface interesting insights.* Granting permissions, the agent leverages an **authoring skill**, logs in with his credentials, **creates the Eventhouse**, finds the **KQL DB URI**, and executes the **medallion schema** (all three layers, **update policies**, **materialized views**) by generating KQL ("hopefully the LLM gods are with us"). It then **ingests data** and **verifies** — because the skill instructs it to validate after creating anything — and returns a tidy summary of what was built (three layers, transformation function views, etc.). Rather than trust the agent blindly, Anul verifies in the **Eventhouse UX**: the **entity diagram view** visually confirms the three layers; the **ingestion view** and **data preview** confirm data is flowing correctly.

### Demo 4 (cont.) — Wiring up Eventhouse MCP
For agent-first analytics, every **Eventhouse endpoint comes with a remote MCP URL**. Anul copies it back into the GitHub CLI, adds it as an **HTTP/remote MCP**, authenticates, and inspects the tools it exposes — **execute query**, **get schema**, and more — that let the agent interact with Eventhouse. A loose prompt (*"share some interesting insights from the data I just created, using the configured MCP"*) has the agent quickly run **five–six queries**, read the data, describe its shape, and even **suggest follow-ups** (e.g., advanced anomaly-detection functions). Recap: using **MCP + RTI skills**, an entire flow — item creation, data ingestion, and analysis — was built **agentically via CLI**. The same MCP-powered analysis is also available in **Copilot experiences** (insights and visualizations generated directly), ideal for **business users** preferring a **low-friction web interface**. Whether building automated agent workflows or interactively exploring via Copilot, both operate on a **shared foundation** — the same tools and capabilities for **agents and humans** alike.

### Closing the loop on AI: "no AI without RTI"
Tessa returns to take the AI thread further. Multiple customers echo that **"there is no AI without RTI"** — fresh, time-sensitive, high-volume, high-granularity data is **necessary** to power accurate, useful AI solutions. Being Build (developer-focused), the earlier demos leaned technical, but the final demos deliberately go **more UI-focused** to show the same deep technical power is **accessible to users of all skill levels**.

### Demo 5a — Anomaly Detector (no data scientist required)
The **Anomaly Detector** is a **public preview** capability that easily leverages streaming data landed in Eventhouse. With a couple of clicks you configure the right anomaly model for your data — **no data scientist needed**. In the demo, Tessa just picks a **table and field** to monitor; by connecting the data, the system analyzes it and **recommends the best-suited out-of-box model** based on **seasonality and pattern**. It explains models in **user-friendly terms**, shows the data and detected anomalies **side-by-side** (building confidence), tells you **where the anomalies are**, and lets you **publish** it into the organization. Once running, new data → new anomalies, and from the **Real-Time Hub** you can **subscribe and create a rule** directly on the emitted anomaly events (choosing/filtering fields) — yielding a new alert listening for anomalies to share across the org.

### Demo 5b — Operations Agent (Generally Available)
The headline: the **Operations Agent** is now being released **more broadly / GA**. It's like a **new virtual team member** in your operations team that runs the **observe → analyze → decide → act** loop autonomously. In Fabric you **create a new Operations Agent**; it loads configuration in a user-friendly UI. On the left you provide **natural language** to onboard it like a new hire — **business goals** and **specific instructions** — and connect it back to data. Crucially, you connect it not to raw data but to the new **semantics via the ontology item** (see the **Fabric IQ** session), so it understands **business context, entities, and even actions** out of the box. After configuring, you **save and generate the playbook** — the agent's understanding of the data, its objectives, and the actions it can take. The generated playbook reports back the **terms/entities it understands**, the **rules** it watches, and **what it'll do**. You then **publish the agent into Microsoft Teams**, where it runs **24×7**. When it detects a matching condition, it **alerts the team**, presents the **data**, **recommends an action**, and offers to **investigate further (root-cause analysis)**. Choosing root-cause yields deeper insight and more confidence; then, from the same experience, you **confirm the action and parameters** and the agent **updates the system**. Rich **monitoring** shows what's running/pending and lets you drill into any activity — the **rule** it watched, the **query** it executed, and the **decision** it made — for high confidence in the running system.

### Wrap-up: one platform, many scenarios
Tessa closes by tying the **stadium operations** theme back to the full RTI picture — streaming, analysis, modeling, visualizations, and acting all working together to build an entire solution. Beyond stadiums, RTI unlocks operational reporting, connected assets, and a "command center" for the business. On the **unified intelligence platform for AI**, these layers stack to provide a full system for **human teams and agent teams** to improve the business **in time**. Fabric ships **every single week** — watch the **release planner/notes**. Free **hands-on workshops/labs** are available in many countries (via QR codes/links), with docs, forums, communities, and LinkedIn updates for going deeper.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Fabric** — unified data platform for the AI transformation (OneLake, shared governance, Copilot throughout).
- **Real-Time Intelligence (RTI)** — Fabric's native SaaS for event/streaming data; ingest → process → analyze → act.
- **Eventstream** — ingestion/processing/routing; ~40 connectors; **Kafka + AMQP** endpoints; SQL + no-code operators; schema registry; multi-destination output; event-time policies; interactive preview/test/debug.
- **Eventhouse** — purpose-built, multimodal, petabyte-scale time-series/event store; sub-second query; medallion (bronze/silver) with update policies + materialized views; schemaless (text/JSON/metrics/time series).
- **KQL** — deep analytics query language over Eventhouse (JSON expansion, forecasting, anomaly detection, time-series, geospatial, vector similarity).
- **SQL on Eventhouse** — familiar SQL alternative to KQL for similar insights.
- **Activator** — rules/alerts and custom actions (Teams messages, custom workflows, invoke notebooks); MCP-enabled for natural-language rules.
- **Real-Time Dashboards** & **Power BI** — monitoring/reporting on streaming data.
- **Real-Time Hub** — central catalog of all streaming/event assets; add data, subscribe, create rules.
- **Deltaflow** — *public preview*; analytics-ready CDC transform (Debezium), schema-drift handling, hundreds/thousands of tables.
- **Fabric Spark + Notebooks** — Spark structured streaming from Eventstream; Python; AI/LLM function calls; auto-generated boilerplate.
- **Fabric business events** — publish/identify/act on business-level events (vs. raw data).
- **Workspace monitoring / Eventstream observability** — telemetry + logs in monitoring DBs; build operational dashboards.
- **Anomaly Detector** — *public preview*; auto-selects model by seasonality/pattern; emits anomaly events; no data scientist required.
- **Ontology item** — maps business context (entities + actions) onto data; powers agents (tie-in to Fabric IQ).
- **Operations Agent** — *GA*; autonomous observe→analyze→decide→act loop; playbooks; root-cause analysis; runs 24×7 in Teams.
- **Data agents** in Fabric — act on streaming data for AI-driven automation/decisioning.
- **Eventhouse MCP** — remote MCP URL per endpoint; tools like execute query / get schema for agent access.
- **Fabric skills** — reusable agent capabilities + RTI domain knowledge (Eventhouse, Eventstream authoring, consumption skills).
- **Copilot** — natural language → KQL; generated insights/visualizations for low-friction web use.
- **Connectors called out** — **MQTT** (new version), **Oracle DB CDC**, **HTTP/REST**, **Mirror DB change feed**, **SQL CDC**, **Delta change feed** (*public preview*), **custom stream connector** (*private preview*).
- **GitHub Copilot CLI / GitHub CLI** & **"cloud code"** — agentic clients used to drive Fabric skills + MCP.
- **Underlying Azure platforms** — Azure Event Hubs, Event Grid, Stream Analytics, Data Explorer, Azure Maps.

## 🚀 Announcements / What's New
- 🟢 **Operations Agent — Generally Available (GA).** Autonomous virtual operations team member running 24×7 in Teams (observe/analyze/decide/act, playbooks, root-cause analysis). *(Headline announcement.)*
- 🟡 **Deltaflow — public preview.** Analytics-ready CDC transform for Debezium events with automatic schema-drift and large-scale table management.
- 🟡 **Anomaly Detector — public preview.** Auto-selects best out-of-box model by seasonality/pattern; emits subscribable anomaly events.
- 🟡 **Delta change feed connector — public preview.** Works with **mirror databases** now; general **lakehouse delta tables** "very soon."
- 🟠 **Custom stream connector — private preview.** Build/upload your own connector package; Fabric hosts it to pull from your sources.
- ✅ **MQTT connector — new version** launched.
- ✅ **Oracle DB change-data (CDC) connector** — now available.
- ✅ **Mirror DB change feed connector** — launching to get change feeds from databases/delta/mirror DBs.
- ✅ **Fabric business events** — publish/act on identified business events.
- ✅ **Eventstream observability** as part of **workspace monitoring**.
- ✅ **Eventhouse MCP** (remote MCP URL per endpoint) + **Fabric skills** for agent-first analytics; **Activator** MCP for natural-language rules.
- ✅ **New Activator actions** and broader connector set across Eventstream (more "on deck," coming soon).
> Note: GA vs preview status above reflects what was stated in-session; several items (MCP, skills, business events, new connectors) were demoed/announced without an explicit GA/preview label and are marked ✅ as "shown/available."

## 💡 Demos
- **Demo 1 — Stadium turnstiles (MQTT).** Real-Time Hub → Add data → MQTT connector (secure broker, topic, MQTT v3) → SQL code operator (filter + route, in-editor test) → publish → verify passage events in Eventhouse. Then late/out-of-order policies + **fraud detection** via a **120-second hopping window** on duplicate tickets, wired to **Activator** for staff alerts.
- **Demo 2 — Concessions (SQL CDC + Deltaflow + Spark/AI).** Second Eventstream from **Azure SQL CDC** → **Deltaflow** → Eventhouse (~6–7 tables auto-created, initial snapshot replication). Then a **Spark notebook** (auto-generated boilerplate) + **AI-generated prompt** on inventory → publishes **Fabric business events** (e.g., *"queue 200 units of hot dogs"*) → act via Real-Time Hub rule; enable Eventstream monitoring.
- **Demo 3 — Eventhouse scale + GitHub events.** KQL/SQL over a **~378T-record** table (**~13.5–14B records/min** ingest); live **GitHub events** table **~3.6B rows**; JSON expansion, forecasting function, Activator alerts, Copilot NL→KQL.
- **Demo 4 — Agentic end-to-end via GitHub Copilot CLI.** Fabric skills create an Eventhouse + medallion schema (bronze/silver/gold, update policies, materialized views), ingest + self-verify; then wire **Eventhouse MCP** (execute query/get schema) and have the agent run 5–6 queries + suggest follow-ups. Verified in Eventhouse UX (entity diagram, ingestion view, data preview).
- **Demo 5 — Anomaly Detector + Operations Agent.** Anomaly Detector picks the best model from a chosen table/field, shows anomalies side-by-side, publishes events + Real-Time Hub rule. Operations Agent onboarded via NL (goals/instructions) + **ontology item**, generates a **playbook**, publishes to **Teams** (24×7), alerts with data + recommended action + **root-cause analysis**, then confirms parameters and updates the system; rich activity monitoring.

## 📊 Notable Stats / Quotes
- **"There is no AI without RTI."** — recurring theme from multiple customers.
- **~40** managed Eventstream connectors ("close to 40," and growing).
- **~378 trillion** records in a single demo Eventhouse table.
- **~13.5–14 billion** new records added **per minute** (last-hour view).
- **~3.6 billion** rows in the live GitHub-events table.
- **120-second hopping window** used to detect duplicate-ticket fraud.
- **~6–7 tables** auto-created in Eventhouse from SQL CDC via Deltaflow.
- Agent ran **5–6 queries** autonomously over Eventhouse MCP to surface insights.
- Operations Agent runs **24×7** in Microsoft Teams.
- Eventhouse: **petabyte scale** with **sub-second** query performance.
- Fabric releases **every single week**.
- *"Hopefully the LLM gods are with us"* — Anul, during the agentic schema-deploy demo.
- Sample AI business-event output: *"queue up 200 units of hot dogs"* from one stadium location to another.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up an **Eventstream** with the **MQTT** or **HTTP/REST** connector and test a SQL operator in-editor before publishing.
  - Try **Deltaflow** (public preview) on an **Azure SQL CDC** source → Eventhouse and watch schema-drift handling.
  - Build a tiny **medallion** Eventhouse (bronze → update policy → silver → materialized view) and query with both **KQL** and **SQL**.
  - Wire **Eventhouse MCP** into **GitHub Copilot CLI** with **Fabric skills** and reproduce the agentic create→ingest→analyze flow.
  - Configure the **Anomaly Detector** (public preview) on a real metric and emit events to a **Real-Time Hub** rule.
  - Spin up an **Operations Agent** (GA) connected to an **ontology item**; review its generated **playbook** before publishing to Teams.
  - Try **Copilot NL→KQL** as a way to learn KQL faster.
- [ ] Questions:
  - What are the exact **licensing/capacity (CU)** implications of Eventhouse at very high ingest rates, and of running Operations Agents 24×7?
  - How does **Deltaflow** handle breaking schema changes / column drops vs. additive changes?
  - What guardrails/permissions scope an **Operations Agent's** ability to *act* on systems (action approvals, RBAC, audit)?
  - Which **anomaly models** ship out-of-box, and can custom models be plugged in?
  - **Eventhouse MCP**: auth model, rate limits, and which tools beyond execute query / get schema exist?
  - GA/region availability + roadmap dates for **Delta change feed** (lakehouse delta tables) and the **custom stream connector**.
- [ ] Relevant to:
  - Event-driven / IoT and operational-monitoring architectures (stadiums, manufacturing, connected assets, command centers).
  - Agentic data platforms — MCP + skills patterns for letting agents build and query data estates.
  - Anyone evaluating Fabric RTI vs. ADX/Stream Analytics/Event Hubs for real-time analytics + action.
  - Fabric IQ / ontology work (semantics for agents).

## 🔗 Related
- [[OD811 - Powering the next AI frontier with a unified data platform]] — sibling Fabric platform keynote/session (unified data platform context).
- [[OD812 - Fabric IQ Bringing enterprise intelligence into the developer workflow]] — sibling Fabric session; **ontology item** + Fabric IQ referenced directly here.
- [[Microsoft Fabric]] — the unified data + intelligence platform RTI is part of.
- [[Real-Time Intelligence]] — the RTI capability set (Eventstream, Eventhouse, Activator, dashboards).
- [[Eventhouse]] — petabyte-scale time-series/event store featured in the demos.
- [[KQL]] — query language for deep analytics over Eventhouse.
- [[Model Context Protocol (MCP)]] — Eventhouse/Activator MCP enabling agent-first analytics.
- [[Operations Agent]] — the GA autonomous operations agent (observe→analyze→decide→act).
- Source list: [[2026 Build Session List]]
