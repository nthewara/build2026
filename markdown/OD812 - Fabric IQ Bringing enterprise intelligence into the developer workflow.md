---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/fabric
  - topic/fabric-iq
  - topic/ontology
  - topic/real-time-intelligence
  - topic/ai
  - topic/agents
source: https://www.youtube.com/watch?v=ZUbLJDM82EQ
session_code: OD812
event: Microsoft Build 2026
speakers: Yitzhak Kesselman, Tessa Kloster
duration_min: 52
aliases:
  - Fabric IQ Bringing enterprise intelligence into the developer workflow
---

# OD812 — Fabric IQ: Bringing enterprise intelligence into the developer workflow

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Yitzhak Kesselman (Microsoft Fabric — data/IQ leadership) & Tessa Kloster (Microsoft Fabric — Real-Time Intelligence / product). Guest: Dr. Werner, Siemens Healthineers (caption-uncertain surname).  
> **Duration:** ~52 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ZUbLJDM82EQ)

## 🎯 TL;DR
This session lays out Microsoft Fabric's vision for moving organizations from **reactive, dashboard-driven** operations to **proactive, autonomous** operations where humans and AI agents work as one team. It frames Fabric as a three-layer "operational foundation": **OneLake** (unified data estate across cloud/on-prem, batch/streaming), **Real-Time Intelligence (RTI)** (reason about and act on streaming/event data at planet scale), and **Fabric IQ** (a semantic layer of ontologies — the "virtual brain of the business" — built over analytical, operational, geospatial, and real-time data). The core argument is that AI agents are only as good as the **context** they're grounded in, so Fabric IQ gives agents the same business meaning, relationships, rules, and actions that a trusted human employee has. Big announcements: **Fabric IQ graph is now GA**, **operations agents are GA**, **data agent is GA**, **anomaly detector is in public preview**, plus a strategic **NVIDIA partnership** bringing physical AI / digital twins (Omniverse) into Fabric (in preview). Demos run a single end-to-end **stadium operations** scenario, with customer proof from **Siemens Healthineers** (real-time medical-device service) and **Vanderlande** (airport digital twins).

## 🔑 Key Takeaways
- **The shift is reactive → proactive/autonomous.** Customers want to stop reading stale hour/day-old reports and instead have software + agents that proactively and autonomously find the signals that matter and act on them, across thousands of interconnected business signals.
- **Operational foundation = 3 architectural layers:** (1) a **unified data estate** (all data, cloud + on-prem, batch + streaming, in one place), (2) **engines that reason** over that data, and (3) an **intelligence layer** that extracts meaning to power both human and agent decisions.
- **"Chief Information Officer, not Chief Integration Officer."** Fabric's reason for being is to unify the data platform so CIOs stop spending their time integrating systems; data lands in OneLake and many engines (Data Factory, analytics, Power BI, RTI) work seamlessly on top.
- **Fabric's three layers for builders:** Unified Data (OneLake) → Business Intelligence (semantic models) → Operational Intelligence (RTI + ontologies/IQ).
- **Agents need the same context as your best employees.** To act, reason, and decide like a trusted employee, an agent needs the same access and understanding (Outlook/Teams/docs *and* operational systems/customer production data). The **Microsoft IQ layer** unifies enterprise data + knowledge + business state: **Work IQ** (how employees work), **Foundry IQ** (institutional knowledge — documents/procedures), **Fabric IQ** (state of the business + ability to operate it).
- **OneLake** brings data in via physical copy **or virtual shortcut**, stores in **open formats (Delta/Parquet)**, gives **one layer of governance and security**, and exposes data to Microsoft *and* non-Microsoft/SaaS ecosystems. **170+ connectors.**
- **BI scale today:** **20M+ semantic models** and **35M+ monthly active users** across the ecosystem — a curated repository of analytical business understanding.
- **"No AI without RTI."** Agentic solutions need the highest-volume, highest-granularity, freshest, most accurate data — exactly what Real-Time Intelligence provides; it's not limited to *time* but also *where* it happened and *what's related/impacted*.
- **RTI runs at planet scale:** **600T+ messages/month**, **14.3 exabytes** of events+logs/month, **7.8B real-time queries/day**, **five-nines (99.999%) messaging reliability** — and is cost-competitive (public benchmark vs Confluent + Snowflake: **12× faster, 37% more cost-effective**).
- **Ontology = the "virtual brain of the business."** It models the business by **entities** (rich: properties, measures, geospatial, time-series, actions), **business-meaning relationships** (not just data keys), **rules/policies**, and **objectives** (e.g. satisfaction, profitability) — so people and agents reason in the *language of the business*, not tables and schemas.
- **The problem Fabric IQ solves:** today analytical and operational systems are separate, actions aren't immediately reflected back, teams run fragmented data estates, and even "what is an active gate?" gets different (locally correct) answers — producing reactive, slow organizations.
- **Build ontologies fast with Copilot + no-code visual tools.** Copilot suggests entity types, properties, data bindings, and relationships from your existing **semantic models** and **Event House** data, can pull in **industry standards**, and you approve suggestions into a live ontology — not a one-time effort.
- **Fabric IQ graph is GA:** native graph over OneLake data (no extra ETL), with a **visual no-code GQL query builder** for multi-hop relationship/causal analysis (entrance → seating section → concession → warehouse).
- **Operations agents (GA) are onboarded like a team member:** you give goals + instructions, connect the **ontology** (entities/relationships/actions auto-available), add custom actions, and it **generates a playbook**, then monitors, does root-cause investigation, recommends/takes actions (e.g. reorder low concession stock) directly in a Teams channel, with an **activity log** for trust/refinement.
- **Anomaly detection without data science.** A no-code **anomaly detector** (public preview) analyzes Event House data, recommends the best model, and emits anomaly events as new data streams in — feeding alerts and operations agents.
- **Agent grounding spectrum (no-code → pro-code):** Foundry, Copilot Studio, and out-of-the-box Fabric agents are all grounded/integrated on Fabric IQ ontologies and powered by RTI; **Fabric IQ APIs + MCP + skills** let developers build and consume ontologies programmatically.
- **Physical AI via NVIDIA partnership (preview):** combine RTI (live signals) + Fabric IQ (ontology brain) + **NVIDIA Omniverse** (physically-accurate 3D / **OpenUSD** scenes + simulation) for **digital twins** with **bidirectional cross-highlight**, embedded in real-time dashboards — extending operations from the digital world into the physical world.
- **Connect Fabric IQ ↔ Foundry IQ** to unite live business context with document/communication knowledge, giving Foundry-built agents trusted decision context and continuous operations optimization.

## 📚 Detailed Notes

### The opening narrative — from fragmented data to a unified living system
Yitzhak Kesselman opens (caption renders his name as "Sakasaman"/"Yetac"/"Ysack") by framing the talk around bringing **the data, the semantics, and the ontology behind the data** to power applications in the age of AI. An intro video sets the theme: today's world moves faster than most organizations can react; problems and opportunities appear in real time and signals pour in from every direction, changing second by second until the volume becomes overwhelming. To stay ahead, a business must see itself **not as fragmented data but as a unified living system** — one system that shows what's connected, what's changing, and what every action will affect, letting teams and AI **think in the language of the business** from the smallest detail to the big picture, instantly and intuitively. People and AI agents operate as **one team**, not only spotting issues/opportunities but understanding full context and what to do; agents continuously monitor and act when it makes sense, recommend options, and coordinate in real time with their human teammates. **Decisions become actions, and actions ripple across the organization, changing outcomes in the moment.** This is positioned as the present reality and as **Microsoft Fabric**.

### The core shift: reactive/manual → proactive/autonomous
Across the board, customers want to move away from **reactive, manual** work — looking at reports/dashboards that are stale by hours or days — toward **proactive and autonomous** software and agents that find insights behind the data and help operate the business. Returning to the recurring **stadium operations** scenario, the goal is to collect all the signals across different entities, pair them with **actions** and the **sense/meaning** behind them. Running business operations means connecting **thousands of signals** across the business, understanding what they mean as a whole, and finding the signals that **really matter** to drive a change in business outcome — with humans and agents working together.

### The operational foundation: three architectural layers
From an architectural perspective, the operational foundation is **three layers**:
1. **Unified data estate** — bring all data together across cloud and on-prem, batch and streaming, into one place, so you can reason about how the business operates across its whole majority.
2. **Engines that reason** — engines that can reason over and understand all this data together.
3. **Intelligence layer** — find the reasoning and meaning behind the data to power both human and agent decisions.

The aim is to connect all data — streaming, batch, structured, semi-structured, unstructured — into one unified place. **That is where Fabric came into place.** CIOs say "I want to be the *Chief Information* Officer, not the *Chief Integration* Officer," and Fabric is the unified data platform answer: bring all data in, reflect it in **OneLake**, and let different engines (Data Factory, analytics, Power BI, Real-Time Intelligence) work seamlessly on top.

Mapped onto the operational story, the three layers become: **OneLake** (represents all the data across the organization), **Real-Time Intelligence** (reason about the data, take actions, understand it), and **Fabric IQ** (create the semantic understanding behind analytical data, plus ontologies to drive business operations). These are the critical components that let humans and agents work together.

### Agents as trusted, productive employees — and the Microsoft IQ layer
The stated goal for building agents: make them **as trusted and as productive as your best employees**. For that, agents need the **same context and understanding** a person has. A human employee has access to Outlook, Teams, and company documents, **but also** operational systems — customer production environments and systems. Agents need that same context to act, reason, and decide the same way a person can. That is the role of the **intelligence layer** — powering both humans and agents to understand all organizational data together with created knowledge and the **state of the business** (and what actions can be taken).

This is **Microsoft IQ**, which unifies all enterprise data and understanding into one layer, composed of:
- **Work IQ** — understands how your employees work.
- **Foundry IQ** — understands institutional knowledge: all the documents, procedures, communications.
- **Fabric IQ** — understands the **state of the business** and helps you **operate** it.

For the stadium scenario, that means collecting and understanding all the data across the business; the session then dives deep into **Fabric IQ** specifically.

### Fabric's three layers for software builders
For anyone building software on Fabric, it consists of three layers:
1. **Unified data** — connect all structured, semi-structured, and unstructured data into one place.
2. **Business intelligence** — use **semantic models** that represent the analytical understanding of the business.
3. **Operational intelligence** — take all the data + analytical understanding and power it with **reasoning, streams of data, and events** that happen in the business, plus the ability to **act** on that data. The capstone is **ontologies in IQ**, which create the **virtual brain** of business operations and let people and agents work together to operate the business.

### Layer 1 — OneLake (the unified data estate)
OneLake is a critical part of Microsoft Fabric. It brings data in across sources — on-prem and cloud, Microsoft and non-Microsoft — either as a **physical copy** or **virtually as a shortcut** (just point to the data). Once data is in OneLake:
- It's accessible across Microsoft systems and via **Excel** or other sources.
- It's accessible through **other SaaS providers** that can read OneLake.
- It uses **open-format sources** — **Delta/Parquet** — and Fabric's engines are optimized to work seamlessly and performantly on top of it.

A key emphasis is **governance and security**: OneLake provides **one security layer across all data sources**. Once you mirror or shortcut data into OneLake (across on-prem, cloud, or other data platforms), all of it is secured and governed in one layer — essential for working with data + AI responsibly. Fabric ships **170+ connectors** to bring data in across sources, enabling a **full unified view** of business data.

### Layer 2 — BI and semantic models (the analytical brain)
There are **20M+ semantic models** in organizations today, representing the analytical understanding of businesses. They run day-to-day analytical understanding and provide a **curated repository** for business understanding and analytical decisions. **35M+ users** use these semantic models regularly (monthly) across the ecosystem. These become a primary source Copilot draws on later when generating ontologies.

### Layer 3 — Operational intelligence (RTI + ontologies/IQ)
The third layer splits into two aspects: **Real-Time Intelligence** and **ontologies/IQ**. Yitzhak hands over to **Tessa Kloster** for RTI.

### Real-Time Intelligence (RTI) — overview
RTI gives access to all **streaming and event data**. It starts from a **wide range of connectors** (Microsoft and cross-cloud, with more added every week). The full capability set is a "toolbox" spanning the end-to-end solution:
- **Connectors + data ingest** — easy access to streaming/event data.
- **Streaming** capabilities directly in the streaming area.
- A **curated engine for analysis** — query **petabytes** of data in **seconds**.
- **Model & contextualize** the data to understand it.
- **Visualize** it in a truly **operational format** so you see data as it arrives.
- **Act on / understand** the data within the rest of the system.

Crucially, RTI **isn't limited to time**. The temporal aspect matters (sequence of events, how things change over time), but you also need **where** it happened (geospatial) and **what is related / could be impacted** — for a holistic understanding of operations.

### Demo 1 — RTI end-to-end (stadium operations)
Tessa walks the **Real-Time Hub** (the central location for all streaming/event data):
- **Ingest via MQTT:** uses the **new MQTT connector** to bring in **turnstile events**; very easy to connect and land data directly into the system.
- **Event stream:** sees the MQTT source in the event stream, can mix in custom events or other streaming sources into the same stream, and load to destinations (**Event House**, notebooks).
- **Notebook processing:** opens a notebook to do additional processing — e.g. detecting increased volume coming into the stadium worth monitoring/acting on.
- **Business events (new capability):** from the notebook, **emits a business event** when congestion is detected. Back in the Real-Time Hub, the new **business events** capability shows a **"turnstile congested"** event; from that view she **sets an alert** so the team is notified when the condition occurs. Business events are curated events that can flow to the rest of the system.
- **Task flow → Event House → dashboards:** data lands in Event House and flows all the way to **real-time dashboards**, where the team monitors stadium operations live.
- **Real-time dashboard + Copilot:** on the dashboard she sees streaming data from a wide range of sources, including **security health**. Drilling into **duplicate ticket scans**, she uses **Copilot** to break down duplicate ticket scans by **ticket type per entrance** — revealing the **VIP entrance** (premium + VIP) has the highest duplicate scans (concerning). She refines the chart colorings so anyone viewing gets the info.
- **Geospatial:** integrates **rich geospatial** capabilities with the real-time operational data — sees stadium traffic/people flow, **hotspots**, which entry points have congestion, and what concessions/areas will be impacted.
- **Alert → action:** from the operational dashboard she sets an alert on **rising average wait time**, but goes beyond notification to **take an action** — running a **notebook for load balancing** across areas, passing **specific parameters** from the query as it runs/detects. (This is the **manual** path; the **autonomous** path comes later with operations agents.)

The demo shows the full **event condition → action** loop. Although focused on stadiums, RTI customers span **sports, energy, airports, airlines, manufacturing, retail** and more.

### "No AI without RTI" — and planet-scale infrastructure
Customers say there's **no AI without RTI**: any AI solution — especially an **agentic** one — needs the **highest-volume, highest-granularity** data, and it must be **fresh** and **accurate**. The user-friendly experiences shown are built on **planet-scale infrastructure for real-time data**:
- **600 trillion+ messages per month**
- **14.3 exabytes** of events and logs per month
- **7.8 billion real-time queries per day**
- **five-nines (99.999%) reliability** across messaging

On **cost**, RTI is competitive on scale + performance + cost (you don't give any up). A **public benchmark vs Confluent and Snowflake** showed RTI was **12× faster and 37% more cost-effective** across the scenarios.

### RTI updates shipped leading up to Build
Tessa runs through recent RTI updates:
- **GA: SQL operator in Eventstream** — express custom business logic using **SQL**.
- **Spark Structured Streaming with Eventstream** — stream-process using **Python**, with a rich connection between Eventstream and Spark notebooks.
- **Delta flow** for event-driven apps — easily transform **Debezium feeds** directly into analytics-ready events without customizing inside the event stream.
- **Business events in the Real-Time Hub** — publish business events for anyone in Fabric to subscribe to (analytics or action).
- **Copilot in RTI** — not just visualize, but understand and explore data in context.
- **MCP + skills for RTI** — bring real-time data directly to your agents.
- **GA: geospatial visualization (map item)** — generally available for all geospatial needs, real-time and alongside the rest of Fabric.

Tessa hands back to Yitzhak for Fabric IQ.

### Fabric IQ — modeling the business, not the tables
Yitzhak reframes: Fabric unifies **data**; the next level is unifying **business operations**. Looking closely at the stadium scenario, the goal is to understand the **entities** involved: the **stadium, gates, food stands, attendees**. These are **rich entities** — they have properties and measures, but also:
- **Geospatial** info (e.g. the location of a gate).
- **Time-series** data (e.g. how many people pass through a gate).
- **Actions** you can apply (e.g. assign crew, schedule a repair).

Critically, these entities are interconnected by **business meaning** — **not just a data-key relationship**, but a relationship that means something to the business. That lets you apply **rules and policies** (e.g. crowd management, food safety) and ultimately drive the **objective** of the business (e.g. satisfaction, profitability). **That is how the business actually thinks about operations** — in entities, properties, goals, and actions.

### Why today's reality falls short
In reality, teams work with **tables and schemas**. Questions spawn **analytical reports**; more questions spawn more reports. Those analytical systems are **separate from operational systems**, so an action taken on the operational side **isn't immediately reflected** on the analytical side — they don't work in tandem. Wanting to understand something, act, and see feedback becomes slow and disconnected. Zooming out, an organization has **multiple teams** on **multiple data estates** running **different operational systems**, creating a **complex, fragmented** scenario. The classic example: ask **"what does an *active gate* mean?"** and different teams give **different answers** — each correct in its own context, but **confusing for the broader organization**. The net effect: companies trying to run their business across all their data end up **fragmented, reactive, and slow to act**.

### The fix — connect data to meaning, then act
The goal is to **connect the data to the meaning and drive actions** on top of it: collect data from applications, IoT devices, telemetry, user behavior, etc., and empower business operations where humans and agents work in tandem. The familiar developer cycle — **collect → observe → analyze → decide → act** — needs the **semantic understanding** of what all those signals and actions mean. That semantic understanding becomes an **ontology** that represents the **virtual brain of the business**: all entities, how they interconnect, the policies, the rules, and the actions you can apply — used to power the business for both humans and agents, across all operational systems.

### Fabric IQ intro video — the semantic foundation
The Fabric IQ video reinforces: **data is the fuel that powers AI, but data alone is not enough** — AI needs an understanding of **what the data means, how things relate, and which actions turn insight into impact**. **Microsoft Fabric IQ** is the **semantic foundation** that unites **data, business meaning, and action** into a single unified view of the organization. You **model your business with visual no-code tools** so the people who know the company can adapt it as fast as it evolves; create **entities over all your OneLake data** — not only analytical data and Power BI semantic models, but also **operational, geospatial, and real-time** data. You **navigate the business the way it actually runs** — by organizational concepts, not tables/schemas — and elevate teams + AI to **ask, reason, and act in the language of the business** over a **live unified view**. You **trigger actions in real time using rules** and empower **AI operations agents** to run the business because they understand its **live context**. Finally, **connect Fabric IQ with Foundry IQ** to unite live business context with knowledge captured in documents/communications — giving developer-built Foundry agents **unmatched context** for trusted decisions and continuous operations optimization. **"From unified data to unified intelligence — this is IQ in Microsoft."**

### Demo 2 — Building & using an ontology (Copilot + no-code)
Tessa returns to show the product. Fabric IQ has three things to highlight: the **ontology** (the brain), **actions & rules** in the ontology item, and **graph analytics**.

**Creating the ontology:**
- Start as with anything in Fabric by **creating an item** — a new **ontology item** — and choosing which **workspace** it lives in (helps with permissions/control).
- You can **import** or start directly with **Copilot**. Using Copilot, she types in **natural language** to start creating the ontology; it suggests **leveraging existing semantic models**, and she selects a couple that hold the right entities/relationships for **stadium and security** data.
- She gives more intent in natural language: **"create a game-day stadium operations ontology,"** specifying concepts to model. She can even specify **industry standards** or other org/web sources for Copilot to pull in.
- Copilot reasons and produces **entity types, properties, data bindings, and relationships**, assembling them in the ontology. She **approves them all** into the actual ontology.
- From there it's easy to keep building: **add entity types and relationships**; open an entity type (e.g. **Event** / **Entrance**), see how it relates to others, and **add more data** — e.g. selecting **Event House** data to bring in real-time/streaming data, **binding the precise timestamp** to time-series properties. Copilot **suggests properties** to bring in, and she can add explicit ones — landing that data alongside the existing semantic-model data in a few clicks.
- She can also add **rules and actions** directly from the entity type (powerful because it's about **everything that makes up the entity**, not a single data source), and even connect **reports** — producing a **unified view** of all components of each business entity.

**Using the ontology:**
- Back in the **ontology view**, she opens the **entity-type overview** for the **Entrance** entity to see what's happening **right now**: streaming data like **queue length / wait time in minutes**, the **relationship graph**, and the data context.
- The overview shows **eight instances** of entrances and how data is distributed across them. Selecting a specific instance (the **North entrance**) drills into that instance — properties like **where it is**, plus data views narrowed to that item.

### Demo 3 — Graph analytics in Fabric IQ (GA)
Tessa announces **graph is generally available** — **native graph** that takes OneLake data + the ontology and helps you understand all the information together (**no extra ETL** for relationship analysis and more):
- Continuing from the North-gate entrance that needed more investigation, she goes into the **graph item** and uses the **visual no-code query builder** to build a rich **GQL** query **without writing code**.
- She picks **Entrance**, and the builder helps add related nodes (**course/concourse segment, seating section**), filters down, and returns **fast graph results** — seeing entrances and the areas they relate to.
- Using **seating section 204** as an example, she explores the implications of something happening at an entrance on section 204, specifying a GQL query for related areas + nearby entrances, switching to a **list view** for clarity.
- A richer query goes from **area → related gates → which concession stands are involved**, so that during a **surge** you know which concessions need to be on standby with enough **staff and supplies**. One more **hop** goes all the way to the **warehouse** — understanding which warehouses power which concession stands near which entrances. This **multi-hop analysis** across the entire system is presented as the key power of graph built directly into the ontology.

### Planning in Fabric IQ
Tessa notes **planning in Fabric IQ** (announced at **FabCon**): over the same trusted data you can **plan and run what-if scenarios**, powerful for **business and finance teams**.

### Customer story — Siemens Healthineers (Dr. Werner)
Yitzhak welcomes **Dr. Werner** (surname caption-uncertain; rendered "Worer"/"Verer"/"M") from **Siemens Healthineers** ("Simmons Health"/"Seammeners"). Siemens Healthineers sells **medical products** — **CTs, MRIs, angiography systems, ultrasound systems** — to customers and receives data back; Dr. Werner's job is to **analyze the data and develop cloud solutions** for good customer-service outcomes.

- **Evolution:** from **plain old batch file processing** toward **proactive service** and **real-time streaming**. For 20–25 years they transferred **log files** from systems for customer service / data analysis.
- **Three main service use cases:**
  1. **Predictive service** — forecast an upcoming failure (hard if you only get a file once per day).
  2. **Proactive service** — something already happened on the system that's not good; Siemens knows before the customer realizes, so they're prepared if the customer calls.
  3. **Reactive service** — mission-critical, especially in **angiography**: a **patient is on the table** mid-treatment and the doctor says the system isn't working — *should I relocate the patient?* You need the data **immediately**, analyzed **immediately**; technology must enable that.
- **Before → now:** previously used **other products/databases** where data scientists were **stuck building intermediate tables**. Moving to Microsoft's native stack — **Event Grid, Event Hub, Azure Data Explorer** — changed things dramatically; data scientists now have time to find the **patterns** that reveal what's actually wrong, helping customers and patients.
- **Onto Fabric RTI:** Fabric is a **natural successor** to that prior stack, with impact on two aspects: (1) **Development speed increases** — the nitty-gritty details are automated; (2) **Operations** — no time spent operating VMs, clusters, servers; it's automated, **decreasing operational costs**.
- **Business/customer impact:** **streaming is now a commodity** — systems must stream in real time. Fabric helps **reactive service hit the exact point** of a problem, **order spare parts** if required, and **prevent downtime** for customers — a net benefit on the customer side.

Yitzhak's takeaway: exactly the goal — developers focus on their **specific IP/knowledge**, not the **plumbing** or system maintenance.

### Applying AI: ML + LLMs, grounded on the ontology
Everyone talks about AI, but the question is generating **real value**. Two aspects: **machine learning** and **LLMs (large language models)**. AI excels at **finding the needle in the haystack** and reasoning about it — using those signals to drive operations. Fabric IQ's difference: instead of working on **tables and schemas / raw data without business context**, it **grounds agents on the real business context** — what the business represents, all the actions, rules, and policies (the virtual brain).

Across the **agent spectrum** (no-code → pro-code custom agents), you want agents **grounded on the ontology + Fabric IQ and powered by RTI**. Microsoft's integrations — **Microsoft Foundry, Microsoft Copilot Studio, and out-of-the-box agents from Fabric** — are all **grounded and integrated on Fabric IQ ontologies**.

### Demo 4 — Anomaly detector + Operations agent (GA)
Tessa demos **operations agent** capabilities (**generally available**), starting with an **anomaly detector**:

**Anomaly detector (public preview):**
- Leverages the **same Event House data**, brings the **power of data science**, analyzes the data and its patterns, and **recommends the best model** to detect anomalies.
- For non-data-scientists, it uses **user-friendly terminology** (e.g. **"fast outlier scanner," "core pattern finder"**) shown alongside the data so you understand what the model will do and whether it matches the anomalies you know in your business.
- In a few clicks she **creates and publishes** the anomaly detector; as new data streams in it runs the analysis and **emits an anomaly-detector event** when conditions are met — fully automating what she earlier did manually. Subscribing, she can **filter to specific values**, and the alert can run alongside the team and notify them.

**Operations agent (GA):**
- Monitors and understands all the data — **anomaly-detector events, Event House data, the ontology** — in **real time**, and most importantly **acts** alongside the business.
- **Onboarded like a team member:** she gives it **goals** (e.g. ensure **stock levels for concession stands** are adequate) and detailed **instructions**, then connects it **directly to the ontology** so all **entities, relationships, and actions** are **automatically available**. She can also add **custom actions**.
- **Generate the playbook:** the agent reports back what it understood — the relevant **entities** for the goals, the interesting **properties**, and the **rules** it will monitor *and act on* when conditions are met.
- **Running alongside the team in Teams:** the agent appears in the **Teams channel** and has already found a condition — a specific **concession has low stock** — and **recommends an action to reorder**. She can also choose **investigate further**, prompting the agent to do **root-cause analysis** to ensure the suggested action is best (still **reorder**), then asks her to **confirm parameters** — going from **identify → understand → act/resolve** automatically.
- **Activity log (out-of-box):** shows not just what happened but **what was run/executed** and the **alert/action taken**, building **confidence** and enabling **refinement** so the agent works best alongside the business.

**Other AI capabilities across the system:** build a **RAG** solution directly with **Event House**; the **anomaly detector** (public preview) connects easily to existing Event House data; **data agent is GA** in Fabric IQ for **natural-language questions**; and **operations agent is GA** in Fabric IQ. You can also use **Foundry** to connect to the **same ontology** across the Fabric data estate to build **custom agents**.

### Physical AI — NVIDIA partnership & digital twins (preview)
Yitzhak takes it further: use real-world signals + the ontology brain to move into the **physical world** — **physical AI**, via a **strategic partnership with NVIDIA**. In an **airport operations** scenario with many entities (**robotic arms, conveyor belts, baggage, cameras**), the question is how to collect, analyze, understand, and act on signals — with humans and agents **and** in the physical world:
- **Fabric Real-Time Intelligence** collects all the real-time signals.
- **Fabric IQ** (ontologies) contextualizes them into the **virtual brain** of operations.
- **NVIDIA Omniverse** creates **3D visualization** of the real world plus **simulations** to mimic the physical world.

Together this is a **unified spatial context**: bring all data into one place and drive operations in **both the digital and physical world**. The solution is **in preview** — connect the streams, embed them in the **real-time dashboard** using **OpenUSD scenes** integrated with **NVIDIA Omniverse libraries**, producing a **3D visualization** that shows in real time how systems operate, with **bidirectional cross-highlight**, all powered by a **unified operations picture**.

### Demo 5 — Vanderlande airport digital twin (video)
The Vanderlande ("Vanderland") video shows the future: airports manage **thousands of moving assets** in real time, but operations are spread across fragmented systems, making it hard to see what's happening now or what risks are coming next. With **Vanderlande's Open Air platform**, live operational data flows into **Microsoft Fabric Real-Time Intelligence**, creating **digital twins built over an ontology** connecting **flights, gates, passengers, bags, and equipment**. **Physically-accurate 3D visualizations on NVIDIA Omniverse libraries** add spatial context, while the **operations agent in Fabric** monitors, surfaces risks, and recommends actions — humans and AI working side by side:
- The agent alerts that a **delayed inbound flight** was **reassigned to a new parking position** with a **tight connection window**; passengers must clear security fast. It recommends to **prep the position immediately**; using the **3D view**, the operator finds **suitable nearby vehicles** and with **one click** approves work orders and dispatches ground teams.
- A **failing conveyor motor** slows baggage throughput; the agent **flags the risk and highlights the conveyor in 3D**. After verifying, the operator approves a **reroute** and a **maintenance work order**, keeping transfer bags/connections on schedule.
- Inside the terminal, the 3D view shows a **heat map** of congestion at **security checkpoint A**; the agent recommends **opening lanes and rerouting passengers**. The operator **verifies, then approves**, dispatching staff to escort tight-connection passengers via a faster route to their gates.

Result: an **integrated real-time view with spatial context and AI-driven operations** — detect risks earlier, act proactively, reduce disruptions, improve passenger experience. The operator **stays in control** throughout (verify → approve).

### Roadmap & getting started
Yitzhak closes: this is the **future of data and AI** — developers using signals to create a representation of the **physical world**. New capabilities were **announced today at Build** (highlighting **GA of operations agents** and more), with features shipping **every week/month** — feedback requested. **Fabric IQ** was **announced as preview at Ignite**, with more capabilities and a **new code** coming; all the demoed capabilities can be used via **APIs and MCP (with skills)** to create ontologies.

Getting started resources:
- **Real-Time Intelligence in a Day** workshop.
- **Skills** to use and learn.
- **Ontology Playground** — create ontologies within Fabric today.
- Hands-on **documentation, skills, and learning** materials (scan the QR codes).
- **Featured partners** to help accelerate onboarding.
- Recommended related Build sessions: a **unified Fabric overview** ("Nets"), and a **deep-dive on Real-Time Intelligence** from Tessa.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Fabric** — the unified data + analytics + operational-intelligence platform underpinning the whole talk.
- **OneLake** — Fabric's unified data lake; brings data in via physical copy or **virtual shortcut**, stores in **open formats (Delta/Parquet)**, one governance/security layer, 170+ connectors.
- **Microsoft IQ** — the umbrella intelligence layer unifying enterprise data + knowledge + business state.
- **Work IQ** — understands how employees work.
- **Foundry IQ** — understands institutional knowledge (documents, procedures, communications); connectable to Fabric IQ.
- **Fabric IQ** — the semantic foundation: ontologies, entities, relationships, rules, actions = the "virtual brain of the business."
- **Real-Time Intelligence (RTI)** — access/reason/act on streaming + event data at planet scale.
- **Real-Time Hub** — central location for all streaming/event data.
- **Eventstream** — stream ingest/processing; supports SQL operator (GA), Spark Structured Streaming, Delta flow.
- **Event House** — curated analytics store for real-time/streaming data; also supports RAG solutions.
- **MQTT connector** — new connector used to ingest turnstile events.
- **Business events** — curated events emitted (e.g. from a notebook) and published in the Real-Time Hub for others to subscribe to.
- **Activator** — the alerting/action engine (referenced for the "wide range of actions, more added every week").
- **Real-time dashboards** — operational visualization of streaming data as it arrives.
- **Copilot (in RTI / in ontology creation)** — explore/understand data, and generate ontology entities/properties/bindings/relationships from natural language.
- **Geospatial map item** — GA geospatial visualization integrated with real-time/operational data.
- **Semantic models** — Power BI analytical models (20M+ exist; 35M+ MAU); a primary source for ontology generation.
- **Ontology item** — the Fabric item where you model entities, relationships, rules, actions; created in a workspace.
- **Graph (Fabric IQ)** — native graph over OneLake data; **visual no-code GQL query builder**; multi-hop relationship/causal analysis. **GA.**
- **GQL** — graph query language used by the graph builder/queries.
- **Planning (Fabric IQ)** — what-if scenarios over trusted data for business/finance (announced at FabCon).
- **Anomaly detector** — no-code data-science anomaly detection over Event House data; recommends best model; emits anomaly events. **Public preview.**
- **Operations agent** — agent onboarded with goals/instructions + ontology; generates a playbook; monitors, investigates (root-cause), recommends/takes actions in Teams; activity log. **GA.**
- **Data agent** — natural-language Q&A over Fabric IQ data. **GA.**
- **Microsoft Foundry** — build custom (pro-code) agents grounded on the same Fabric IQ ontology.
- **Microsoft Copilot Studio** — build agents grounded/integrated on Fabric IQ ontologies.
- **Fabric IQ APIs / MCP / skills** — programmatic creation and consumption of ontologies; bring real-time data + ontologies to agents.
- **NVIDIA Omniverse (libraries)** — physically-accurate 3D visualization + simulation for digital twins.
- **OpenUSD** — open scene format used to embed 3D scenes in real-time dashboards.
- **Azure Data Explorer, Event Grid, Event Hub** — prior-generation Microsoft streaming stack used by Siemens Healthineers before Fabric RTI.
- **Data Factory / analytics / Power BI** — engines that work seamlessly over OneLake data.
- **Spark notebooks / Python** — stream processing via Spark Structured Streaming with Eventstream; notebook-based processing + load balancing actions.
- **Debezium feeds** — CDC feeds transformed into analytics-ready events via Delta flow.
- **Vanderlande Open Air platform** — customer airport-operations platform feeding live data into Fabric RTI for digital twins.

## 🚀 Announcements / What's New
- **Fabric IQ graph — Generally Available (GA).** Native graph over OneLake + ontology, no extra ETL, with visual no-code GQL query builder.
- **Operations agent — Generally Available (GA)** in Fabric IQ.
- **Data agent — Generally Available (GA)** in Fabric IQ (natural-language questions).
- **Anomaly detector — Public Preview.** No-code, data-science-backed, over Event House data.
- **Fabric IQ — announced as Preview at Ignite**; more capabilities + a "new code" coming. (Note: the source brief also referenced Fabric IQ GA framing; the transcript itself explicitly states Fabric IQ was *announced as preview at Ignite* and is adding capabilities — recorded as stated.)
- **NVIDIA partnership / physical AI / digital twins — Preview.** Fabric RTI + Fabric IQ + NVIDIA Omniverse + OpenUSD scenes embedded in real-time dashboards, bidirectional cross-highlight.
- **SQL operator in Eventstream — GA.** Custom business logic via SQL.
- **Geospatial visualization (map item) — GA.**
- **Spark Structured Streaming with Eventstream** — stream processing in Python (shipped leading up to Build).
- **Delta flow** for event-driven apps — transform Debezium feeds into analytics-ready events without custom event-stream code.
- **Business events in the Real-Time Hub** — publish/subscribe business events across Fabric.
- **Copilot in Real-Time Intelligence** — understand/explore data in context (beyond visualization).
- **MCP + skills for Real-Time Intelligence** — bring real-time data directly to agents.
- **Fabric IQ APIs + MCP + skills** — create/consume ontologies programmatically.
- **Planning in Fabric IQ** — what-if scenarios (previously announced at FabCon; referenced here).
- A general roadmap of new capabilities was **announced today at Build**, with features shipping every week/month.

## 💡 Demos
1. **RTI end-to-end (stadium operations)** — Real-Time Hub → MQTT connector ingest of turnstile events → Eventstream → notebook processing → **emit a "turnstile congested" business event** → set alert → land in Event House → real-time dashboard. Then **Copilot** breaks down **duplicate ticket scans by ticket type per entrance** (VIP entrance highest), **geospatial** hotspots, and an **alert → action** running a **load-balancing notebook** with query parameters. *Point proved:* full event-condition-to-action loop on live streaming data, manual path.
2. **Build & use an ontology (Copilot + no-code)** — create an ontology item in a workspace, use **Copilot + existing semantic models** to generate entity types/properties/bindings/relationships for a "game-day stadium operations ontology," approve them, add **Event House** time-series data (bind precise timestamp), add **rules/actions/reports**, then view the **Entrance** entity overview (queue length/wait time, 8 instances, drill into North entrance). *Point proved:* fast, no-code modeling of the business brain over analytical + real-time data.
3. **Graph analytics (GA)** — **visual no-code GQL** query builder: Entrance → concourse segment → seating section (e.g. 204), then **multi-hop** area → gates → concession stands → **warehouse**. *Point proved:* causal/relationship analysis across the whole system, no extra ETL, built into the ontology.
4. **Anomaly detector + Operations agent (GA)** — create/publish a **no-code anomaly detector** over Event House (recommended model, friendly terms) that emits anomaly events; then onboard an **operations agent** with goals (keep concession stock adequate) + the **ontology**, **generate a playbook**, and watch it detect **low stock** in a **Teams channel**, **investigate (root cause)**, recommend/confirm a **reorder**, with an **activity log**. *Point proved:* autonomous, ontology-grounded operations with human-in-the-loop confirmation.
5. **Vanderlande airport digital twin (video)** — Open Air platform → Fabric RTI → **digital twin over an ontology** (flights/gates/passengers/bags/equipment) visualized in **NVIDIA Omniverse 3D**, with the **operations agent** handling a reassigned delayed flight, a failing conveyor motor, and security-checkpoint congestion (heat map) — operator verifies then one-click approves. *Point proved:* physical-AI operations bridging digital + physical worlds.

## 📊 Notable Stats / Quotes
- **20M+** semantic models in organizations today; **35M+** monthly active users of them.
- **170+** connectors into OneLake.
- RTI planet scale: **600 trillion+ messages/month**, **14.3 exabytes** of events+logs/month, **7.8 billion real-time queries/day**, **five-nines (99.999%)** messaging reliability.
- Public benchmark vs **Confluent + Snowflake**: RTI was **12× faster** and **37% more cost-effective**.
- Query **petabytes** of data in **seconds** (curated analysis engine).
- Siemens Healthineers transferred system **log files** for **20–25 years** before moving to streaming/Fabric.
- **8** entrance instances shown in the ontology Entrance entity overview.
- *"I want to be the **Chief Information Officer**, not the **Chief Integration Officer**."* — the CIO pain Fabric is built to solve.
- *"There really is **no AI without RTI**."* — agentic AI needs the highest-volume, freshest, most accurate data.
- *"Build agents that are as **trusted and as productive as your best employees**"* — they need the **same context** a human has.
- *"From unified **data** to unified **intelligence** — this is IQ in Microsoft."*
- Ontology described as the **"virtual brain of the business."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: spin up the **Ontology Playground** in Fabric and build a small ontology from an existing semantic model via **Copilot**; wire an **anomaly detector** over an Event House and connect an **operations agent** to the ontology to see the playbook generation + Teams loop end-to-end.
- [ ] Things to try: test the **Fabric IQ MCP + skills** and **APIs** to create/query an ontology programmatically; try the **visual no-code GQL** graph builder for a multi-hop query; run the **"Real-Time Intelligence in a Day"** workshop.
- [ ] Questions: What's the exact GA vs preview status of **Fabric IQ** itself right now (transcript says "announced as preview at Ignite, new code coming" — confirm the Build-timeframe status)? What does the **operations agent** pricing/consumption model look like at scale? How does **Foundry IQ ↔ Fabric IQ** wiring work in practice for a pro-code agent? Which **graph** limits apply (node/edge counts, query latency) on large estates?
- [ ] Questions: How does **OpenUSD + Omniverse** licensing/integration work for the **physical-AI preview**, and what hardware/runtime does the 3D digital twin need? How is **ontology** change/versioning governed across multiple teams to avoid the "active gate means different things" problem?
- [ ] Relevant to: any **operations-heavy** domain with real-time signals — stadiums/venues, **airports/airlines**, **manufacturing**, **energy**, **retail**, logistics; teams building **agentic** solutions that need grounded **business context**; **Azure/Fabric** data platform modernization away from bespoke streaming stacks (cf. Siemens Healthineers' Event Grid/Event Hub/ADX → Fabric RTI path).

## 🔗 Related
- [[2026 Build Session List]]
- Related Build sessions mentioned: unified **Fabric overview** session ("Nets"); **Real-Time Intelligence deep-dive** (Tessa Kloster).
- Concepts: **OneLake**, **Real-Time Intelligence**, **Fabric IQ / ontologies**, **operations agents**, **MCP**, **Foundry IQ**, **NVIDIA Omniverse / OpenUSD**, **digital twins / physical AI**.
- Customers: **Siemens Healthineers** (real-time medical-device service), **Vanderlande** (airport digital twins).
