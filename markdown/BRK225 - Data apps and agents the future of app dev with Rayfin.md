---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/data
  - topic/app-dev
  - topic/agents
  - topic/ai
  - topic/fabric
source: https://www.youtube.com/watch?v=ZsPq5ZVj3fE
session_code: BRK225
event: Microsoft Build 2026
speakers: Ben, Sachin, Sutapa, Carl (Replit)
duration_min: 32
aliases:
  - Data apps and agents the future of app dev with Rayfin
  - Rayfin
  - BRK225
---

# BRK225 — Data, apps, and agents: the future of app dev with Rayfin

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ben (Microsoft, app dev / Rayfin) · Sachin (Microsoft, Rayfin engineering — "under the hood") · Sutapa (Microsoft, Power BI / data-app template) · Carl (Technical Lead, Replit)  
> **Duration:** ~32 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ZsPq5ZVj3fE)

> [!note] Name note — "Rayfin"
> The auto-captions garble the product name throughout (Rayfen, Raygun, Raefin, Raizen, Raven, Waif, Raygun). The correct name is **Rayfin** — confirmed by the closing call-to-action to **`github.com/Microsoft/Rayfin`** and Microsoft's Build 2026 announcement. Rayfin (🐟) is a new **open-source SDK + CLI / Backend-as-a-Service** that lets developers *and* coding agents define a complete app backend in code and deploy it to **Microsoft Fabric**. All garbled spellings in this note have been corrected to "Rayfin".

## 🎯 TL;DR
Rayfin is Microsoft's new open-source **SDK and CLI** that gives the AI/agentic-coding era a real **enterprise backend**. Instead of "vibe-coded" apps that fall apart the moment they touch real customer data and compliance, Rayfin lets a human or a coding agent define an *entire backend in code* — database, functions, storage, APIs, and access policies — then deploy it with a single `rayfin up` command straight into **Microsoft Fabric**, where it becomes a first-class, fully-managed, governed artifact. Because apps run inside Fabric, their data lands in **OneLake** (the "OneDrive for data"), inheriting enterprise-grade security/compliance and instantly available for downstream analytics. The session demos building an operational delivery app and a Power BI–powered analytics dashboard, introduces **connectors** (to existing OneLake data), **functions**, and **templates** (incl. a Power BI **data-app template**), and announces a **Replit** partnership so non-technical users can build Rayfin apps too.

## 🔑 Key Takeaways
- **Rayfin = "the backend for the AI coding era."** Agentic coding is great at front ends; Rayfin fills the missing enterprise backend (DB, auth, services, governance).
- **Everything is defined in code** (an SDK + CLI), so both a human *and* an AI agent can understand, author, and operate it. The scaffold even includes agent instructions on how to use the Rayfin SDK/CLI.
- **One command to ship:** `rayfin create` scaffolds the project; `rayfin up` provisions and deploys all resources into Microsoft Fabric — no manual infra setup.
- **Decorator-driven data model (TypeScript):** an `@entity` decorator marks a class as a Fabric DB table; property decorators map to column types and min/max → column constraints; you can declare relationships too.
- **Security is code, not config sprawl:** a `@role` decorator + policy function expresses access rules (e.g. "only authenticated users can see their own deliveries") — row-level security defined inline.
- **Automatic schema migrations:** change/remove a column and Rayfin detects the diff and runs the migration for you — no hand-maintained migration scripts.
- **Front end and back end deploy together**, but are internally separable — you can host the front end elsewhere (e.g. Azure with custom domains), share one backend across multiple apps, and scope each app's access (App A read-only, App B read/write).
- **Connectors** let you connect to *existing* data in **OneLake** (databases, warehouses, semantic models) and selectively pull in only the tables you need as type-safe classes (e.g. just "order details" out of a 100-table semantic model).
- **Functions** run your TypeScript back-end logic in a secure Fabric sandbox (deployed via `rayfin up` as a Fabric Function) so you can safely inject credentials, fire notifications, or call external services — not in the browser.
- **Templates** standardize org apps, bundle tools (API/MCP server defs), agent instructions, sample code, and libraries (e.g. a charting lib), can be checked into a repo, and save tokens vs. re-publishing style guides.
- **Data-app template (built with the Power BI team)** unifies analytics + apps — build apps **directly on your semantic layer**, reusing your analytics investment. Three parts: **data package** (Fabric endpoint connection, query retries, caching), **visual package** (React + **Vega-Lite**, AI-first, enterprise-grade defaults), and **agent skills** (teach the agent to use the packages *with good taste*).
- **Fabric is the differentiator:** SaaS by default, governance/security inherited, one capacity meter shared across analytical + app workloads, data co-located in OneLake within one security boundary.
- **Dev locally, run in cloud:** user code (functions/web app) runs locally against remote services; underlying services run in a Fabric dev workspace or an (experimental) local Docker container; promote dev → staging → prod via Fabric workspaces.
- **Replit partnership** (announced day prior on stage with Satya) brings Rayfin app-building to non/semi-technical users in Replit's browser IDE, inheriting the same enterprise security — currently **private beta**.

## 📚 Detailed Notes

### The problem: agentic coding democratizes building, but enterprise apps need more than "good vibes"
Ben opens with a relatable framing: agentic coding is transforming app development and **democratizing who can build**. His example — coaching a U5 girls' soccer team ("the Mia Hamsters") with his friend Brent, who is *not* a software engineer. A few months ago Brent discovered agentic coding and started "spitting out applications": season-stats apps, snack schedules, practice plans. The point: agentic coding turns "the Brents of the world" into **makers**, and turns existing engineers into **super-makers**.

But the promise of "vibe coding" **falls apart** when you move from a kids' soccer app to a corporate environment with real customer data and compliance needs. In the enterprise you need:
- Databases with **real authentication**
- Configured **back-end services**
- To safely connect to **existing customer data**
- To do all of it while following the company's **compliance and governance** rules

And from the **IT admin** side it's even harder: ensuring only the right people have the right access to the right data, while maintaining the company's security and compliance posture. **That gap is why Microsoft built Rayfin.**

### What Rayfin is
Rayfin is positioned as **"the backend for this new AI coding era."** Core characteristics:
- It's an **SDK and CLI**.
- You **author the entire backend in code** — database, functions, storage, and access policies all defined in code — so both an agent and a human can understand and operate it.
- When ready, **deploy with a single CLI command** straight into **Microsoft Fabric**, where all resources are provisioned and managed for you.
- You get **enterprise-grade security and compliance right out of the gate**.

### Demo 1 — Building an operational delivery app (Ben)
Scenario: Ben works for **Zava**, a home-improvement store whose excitable CEO wants to launch a **home delivery service**. That needs a whole suite of apps (for delivery drivers, for management monitoring), all landing on Ben the engineer.

Flow shown:
1. **`rayfin create`** in VS Code with a terminal open → it asks to choose a **template**. A couple of basic starter templates exist; Ben picks the **blank app** template and names the project `delivery app`.
2. The CLI **scaffolds** the project — all files for both front end and back end, *including the agent instructions* on how to use the Rayfin SDK/CLI.
3. `cd` into the project, then **`rayfin up`** → provisions all resources in Fabric (database + app now running in Fabric). He can then run a **local dev environment pointing at those remote resources**.
4. He **prompts the agent in natural language**: build a delivery app for Zava delivery drivers — let them **log deliveries with photos and item conditions**, and let **customers confirm receipt**. ("Build demo magic" fast-forward.)
5. Result: the agent created **TypeScript files defining the tables and their properties in code**. Ben visits the app **in Fabric** — a driver can arrive at a house with a tablet and have the customer **sign off / confirm** the delivery. He confirms a delivery; the app can also open **outside the Fabric chrome** with its own URL.
6. In the **Fabric workspace** (where items/artifacts live), a new **delivery app artifact** appears alongside a **child SQL database**; drilling into that SQL DB shows the **new delivery row** landed correctly.

**Point proved:** an agent can build a complete front-end + database app and deploy it to Fabric, with data immediately queryable in the underlying SQL DB.

### Under the hood — the code model (Sachin)
Sachin walks through the generated `delivery` class:
- **`@entity` decorator** on the class → tells Rayfin this is a **database table inside Fabric**.
- **Property decorators** → hint the **column type**; **min/max** translate to **column constraints** on the database. You can also specify **relationships**.
- **Security in code:** a **`@role` decorator** + a **policy function**. In the demo it means *only authenticated users can see deliveries, and only their own* (row-level security expressed inline).
- **Automatic migrations:** if you change the data model — drop a column or restructure entirely — Rayfin **detects the change and performs the migration for you**. No hand-managed migration scripts.

**Configuration (YAML):**
- The **dialect** is **Microsoft SQL** — deploying a Rayfin app to Fabric currently spins up the **Fabric SQL server** as your database.
- **Future:** **PostgreSQL** support — your app will be able to spin up a Postgres database via *just a configuration change*. Your application code, entity declarations, and permissioning stay **exactly the same**.

**Deployment topology:**
- The app deploys **front end + back end** (both in Fabric in the demo), but **internally they're separate**. So you can host the front end elsewhere (e.g. **Azure** with **custom domains**).
- **Shared backends:** deploy a backend by itself, then build **two different apps** on top of it. Via **scopes**, App A could be **read-only** while App B can **read and write**.
- **Authentication options:** today all apps require **Fabric authentication**. Future: publish **anonymous** apps or use other providers (**Gmail/social**, etc.). Imagine an external customer signing into your app while the **data lands in your Fabric tenant**, so business users can run downstream analytics on it.

### Connectors — connecting to data you already have (Sachin)
People rarely start from an empty database; they want to connect to **existing data**, read and write it. Rayfin introduces **connectors**:
- Connect to **any data in the Fabric OneLake** — **databases, warehouses, semantic models**. Depending on the data source, you may also be able to **write back**.
- You **declare the data source in configuration**. **Agent instructions** help **pull in tables and create classes** so you get **type safety**.
- It **doesn't pull everything** — a semantic model with hundreds of tables can be narrowed to just the one you need (e.g. only **order details**), creating just that schema's types for use in the app.

### Functions — secure back-end logic (Sachin)
Sometimes you need to **execute logic**, not just move data — fire a notification, call an external service — and you **don't want that code in the browser**; you want credentials safely injected server-side. Rayfin:
- Lets you **write and define the function in TypeScript**; your app **calls it as if it were part of its own code**.
- On **`rayfin up`**, it takes that function block and **deploys it as a Fabric Function**, running in a **secure sandbox** — from there you can trigger notifications or connect to external services/data.

### Templates — standardize and share (Sachin)
Ben started from the built-in blank template; Sachin explains templates more deeply. Templates let you **avoid always starting blank** *and* **standardize apps across an organization** (e.g. a dashboard that should look/behave a certain way) **without burning tokens** on publishing style guides for the agent to read.
- Anyone in the org can use a created template; templates can be **checked into a repository** and **shared with the community**.
- A template can contain: **tools** (API definitions or **MCP servers**), **agent instructions** (how to operate those tools / generate context), **sample code** (so the agent doesn't waste time scaffolding logic), and **libraries** (e.g. a charting library for a data app).

### The data-app template — analytics + apps unified (Sutapa, Power BI)
Most enterprise apps start with **analytics**, and historically analytics and apps lived in **separate worlds** (different teams, different stacks). Rayfin's **data-app template** (built with the **Power BI team**) lets you **build applications directly on your semantic layer** — reusing all the effort already invested in your semantic model/analytics stack for your apps.

Three core components:
1. **Data package** — normalizes the **Fabric endpoint connection**, **query retries**, and **caching**: the foundational steps to connect to and query enterprise data well.
2. **Visual package** — **React + Vega-Lite** components for **AI-first, extremely flexible** visuals with **enterprise-grade defaults** (Power BI's years of data-vis experience baked in).
3. **Agent skills** — teach the coding agent how to use the packages **effectively** — building dashboards/apps with **good taste**, not just functional output ("something that's going to impress your boss").

### Demo 2 — Building an analytics app from Fabric (Sutapa)
The Zava CEO loved Ben's app and (as CEOs do) wants more: **"build me an operational dashboard so I can see if customers are actually loving this new delivery experience."**

Flow shown (starting **inside the Fabric portal**, not the CLI):
1. In a Fabric **workspace** (already full of **semantic models**), click **New item** → a new artifact type called **app**. Name it `analysis app` → **Create**.
2. Choose a template — could be **blank app**, but pick the **data app template** to auto-get scaffolding to **query the semantic model**, connect to it, and get **enterprise-grade visuals**.
3. **Copy the prompt** the template provides, switch to **VS Code**, and using **Copilot / the coding agent**, paste the prompt and hit enter → it **scaffolds the data app**.
4. Provide requirements: build an analytics app to look at **customer satisfaction**, linking the **existing semantic model**. Because it's an *app* (not just a report), make it **actionable** — add a **"flag" button to escalate issues to the product team** (which emails the product team). ("Demo magic" fast-forward; normally you iterate with the agent.)
5. Open it in Fabric → a **full-blown analytics app** from just a few prompts. Crucially she **did not** have to prompt for fine layout/formatting ("move this visual here") — the **coding agent handled formatting**, so non-design-experts get a **polished** result.

**Point proved:** you can stand up a governed analytics app on an existing semantic model in minutes, and **combine analytics with actions** — "tying the loop between how you take data and transform it into action."

### Why Fabric is so good for these apps (Sachin)
- **Enterprise-grade security & compliance are already defined on every Fabric artifact.** Since the app now lives in Fabric as Fabric artifacts, it **inherits** them.
- **All artifact data lives in OneLake** — described as the **"OneDrive for data."** So your **application's data also lands in OneLake**. A business user can then easily access it for **data science / downstream analytics**, and you can build apps that consume that data — **apps and analytical data share the same security boundary**.
- **Fabric is SaaS by default** — infrastructure is easy to provision, little to manage.
- **One capacity, one meter:** you buy **Fabric capacity** and assign compute to artifacts. The **same capacity** used for analytical workloads can now also power your **applications** (DB operations, queries) — **no multiple meters to manage**.
- **Dev locally, run in cloud:** while Fabric runs everything in the cloud, **development is local** — anything containing **user code** (functions, web app) is developed locally. For underlying services you can either spin up a **dev workspace in Fabric** or run a **local Docker container** *(currently experimental)*. **`rayfin up`** packages the whole thing for a **production workspace**, and the same workflow promotes **dev → staging → production** across Fabric workspaces.
- **Self-hosting:** they will **open-source part of the Rayfin runtime** and look to the community to help, so apps can be **self-hosted** on various infrastructure.

### Replit partnership (Carl, Replit)
Not everyone lives in an IDE or CLI. **Replit** — an **agentic, browser-based IDE** for non-technical and semi-technical users — is integrating with Rayfin + Fabric. Where Rayfin/Fabric suit the highly technical user once you're in the code, **Replit serves users who lack coding experience** but still want to build and deploy these apps, with the **same enterprise-grade privacy/security** inherited.

**Demo:** Carl spins up a dashboard "for our stand-up in an hour" — gives it the **Power BI semantic model** and lets the agent work. The agent reads the **schemas** within the semantic model and **builds the dashboard, including the DAX queries**, directly from that content, then **deploys directly into the Rayfin environment** — yielding a live app with the **same workspace and item objects** on the backend, fully manageable from Replit.
- Status: **private beta** (a couple of users).
- **Customer quote — Leatherman** (both an avid Replit *and* Fabric user): *"We appreciate how quickly we can build and iterate with Replit, but … some of our data needs to stay governed and centralized in Fabric. With Rayfin, we finally have both — fast development in the tools we prefer and the confidence that our applications run on top of our enterprise data platform. This is exactly what we've been looking for."*
- The **Replit ⨉ Microsoft partnership** was announced the **day before on stage with Satya** (Nadella).

### Wrap-up — where we are, what's shipping, where it's going (Ben)
**Now / focus:** make it easy to build **enterprise applications** — the **core building blocks**: database, enterprise auth out of the box, easy deploy to Fabric in a **managed tenant**.

**Releasing over the next couple of days / very soon:**
- **Functions** support for the backend.
- **Additional data connectors** — connect to **any data within OneLake**.
- **Blob storage** support.
- → At that point you have "the full suite" to run enterprise applications, moving beyond internal apps/data dashboards to "whatever you want to build within an enterprise tenant."

**By end of year (roadmap):**
- More **B2B and B2C** scenarios — moving **beyond Entra ("intra") auth** to **OIDC auth** and **real-time services**.
- Easier onboarding: get started **without** an Entra/company ID — use a **social login** — plus a **perpetual free tier**. (And you can use **Fabric for free** to get started today.)

**What's next for you:**
- One more **Rayfin session today at 3:00 PM** — **Chris Anderson** (their team) walking through it.
- **Go try it:** `github.com/Microsoft/Rayfin`, give feedback, build apps now.
- **Sign up for the Replit private preview.**

## 🛠️ Products / Features / Technologies Mentioned
- **Rayfin** — *(the star of the talk; captions garbled it badly)* Microsoft's new **open-source SDK + CLI / Backend-as-a-Service** that lets developers and coding agents **define a full app backend in code** (DB, functions, storage, APIs, access policies) and **deploy it to Microsoft Fabric** with one command. Repo: `github.com/Microsoft/Rayfin`.
- **`rayfin create`** — CLI command that scaffolds a new project (front end + back end + agent instructions); prompts you to pick a template.
- **`rayfin up`** — CLI command that **provisions and deploys** all resources (DB, functions, etc.) into Microsoft Fabric.
- **Rayfin SDK** — code-first definitions using **TypeScript decorators**: `@entity` (class → Fabric DB table), property decorators (column types + min/max → constraints), relationships, `@role` + policy function (row-level security).
- **Connectors** — declare a data source in config to connect to **existing OneLake data** (databases, warehouses, semantic models), pull in only needed tables as type-safe classes, and (per source) write back.
- **Functions** — TypeScript back-end logic deployed (via `rayfin up`) as a **Fabric Function** in a secure sandbox; for notifications, external service calls, and credential-safe code.
- **Templates** — reusable, shareable (repo-checked-in) scaffolds bundling tools (API/MCP defs), agent instructions, sample code, and libraries; for standardizing org apps without burning tokens.
- **Data-app template** — Rayfin template **built with the Power BI team** to build apps **on your semantic layer**; comprises a **data package**, **visual package**, and **agent skills**.
- **Microsoft Fabric** — the unified SaaS data platform Rayfin deploys to; provides governed artifacts, shared capacity, and dev/staging/prod workspaces. Apps run as **first-class Fabric artifacts**.
- **OneLake** — Fabric's unified data lake, described as the **"OneDrive for data"**; all Fabric artifact (and now app) data lands here within one security boundary.
- **Fabric SQL (Microsoft SQL)** — the database dialect/engine currently spun up for a Rayfin app on Fabric.
- **PostgreSQL** — *future* supported dialect via a config change (no app-code changes).
- **Fabric Functions** — the managed sandboxed compute Rayfin functions deploy to.
- **Fabric workspaces** — where Fabric items/artifacts live; used to organize apps + child databases and to promote dev → staging → prod.
- **Fabric capacity** — the compute you buy in Fabric; a single capacity/meter now covers both analytical workloads and Rayfin app workloads.
- **GitHub Copilot / VS Code coding agent** — the agent used to build the apps from natural-language prompts inside VS Code.
- **TypeScript** — language for entity classes, decorators, and functions across Rayfin.
- **React + Vega-Lite** — the visual package's stack for AI-first, flexible, enterprise-grade visuals in the data-app template.
- **DAX** — query language the Replit agent generated under the hood when building a dashboard from a semantic model.
- **Semantic models** — Fabric's analytics models that apps can be built directly on top of (the "semantic layer").
- **MCP servers** — can be packaged as "tools" inside a Rayfin template's tool definitions.
- **Blob storage** — *coming soon* as a Rayfin storage option.
- **Microsoft Entra ID ("intra" auth)** — the current default identity provider; today all apps require Fabric authentication.
- **OIDC auth** — *roadmap* (end of year) for B2B/B2C scenarios beyond Entra.
- **Social login (e.g. Gmail)** — *future* onboarding option to start without a company/Entra ID.
- **Replit** — partner; agentic, browser-based IDE for non/semi-technical users that deploys into the Rayfin environment with inherited Fabric governance.
- **Zava** — fictional demo company (a home-improvement store) used throughout the demos.

## 🚀 Announcements / What's New
- **Rayfin — introduced at Build 2026** as a new **open-source SDK + CLI** for code-first, agent-friendly application backends on Microsoft Fabric. **Available now** to try at `github.com/Microsoft/Rayfin`. *(Status: newly launched / early — basic starter templates; some features experimental or roadmap.)*
- **Data-app template** (built with the **Power BI team**) — build apps directly on your **semantic layer** with data/visual/agent-skills packages. *(Shown in this session.)*
- **Replit ⨉ Microsoft partnership** — announced on stage with **Satya Nadella the day before**; Rayfin integration lets non/semi-technical users build governed apps in Replit. *(Status: **private beta / private preview** — sign-up available.)*
- **Local Docker container** for running underlying services during dev — *(explicitly **experimental**).*
- **Roadmap — "next couple of days / very soon":** Rayfin **Functions**, **additional data connectors** (any OneLake data), and **Blob storage** support.
- **Roadmap — by end of year:** **OIDC auth** and **real-time services** for B2B/B2C; **social-login** onboarding (no Entra/company ID required); a **perpetual free tier**.
- **Roadmap — future:** **PostgreSQL** dialect support (config-only switch); **anonymous / alternative auth providers** for public apps; **open-sourcing part of the Rayfin runtime** for community **self-hosting**.
- **Companion session:** another Rayfin session **same day at 3:00 PM**, presented by **Chris Anderson**.
- **Free today:** you can use **Microsoft Fabric for free** to get started right now.

## 💡 Demos
- **Demo 1 — Zava delivery app (Ben):** `rayfin create` (blank template) → `rayfin up` → prompt an agent to build a driver delivery app (log deliveries w/ photos + item conditions; customer confirms receipt). Result deployed in Fabric; agent-generated TypeScript table definitions; a delivery confirmed in-app shows up as a new row in the **child Fabric SQL database** within the workspace. **Proved:** an agent can build a full front-end + DB app and deploy to Fabric, with data instantly queryable in SQL.
- **Demo 2 — Zava analytics/satisfaction app (Sutapa):** Started **inside Fabric** (New item → **app** artifact → **data app template**), copied the template's prompt into **VS Code + Copilot**, prompted for a **customer-satisfaction** analytics app on an existing **semantic model**, and added a **"flag" button** to escalate/email issues to the product team. **Proved:** a governed, polished analytics app built on a semantic model in minutes — without manual layout prompting — that also **combines analytics with actions**.
- **Demo 3 — Replit dashboard (Carl):** In Replit's browser IDE, gave the agent a **Power BI semantic model**; the agent read the schemas, **generated DAX queries**, built the dashboard, and **deployed directly into the Rayfin environment** with the same workspace/item objects on the backend. **Proved:** non/semi-technical users can build and deploy governed Rayfin/Fabric apps from Replit with inherited enterprise security.

## 📊 Notable Stats / Quotes
- **"Rayfin is the backend for this new AI coding era."** — Ben (the session's thesis).
- On democratization: agentic coding **"has the ability to turn the Brents of the world into makers … and turn existing software engineers into … super makers."** — Ben.
- On the gap: **"As a software engineer, apps in the enterprise … need more than just … good vibes."** — Ben.
- **Customer quote (Leatherman, via Carl/Replit):** *"We appreciate how quickly we can build and iterate with Replit, but … some of our data needs to stay governed and centralized in Fabric. With Rayfin, we finally have both — fast development in the tools we prefer and the confidence that our applications run on top of our enterprise data platform. This is exactly what we've been looking for."*
- On the data-app template's intent: build something **"that is going to impress your boss"** — not just a functional dashboard but apps with **"good taste."** — Sutapa.
- OneLake framing: it's the **"OneDrive for data."** — Sachin.
- *(No hard benchmark numbers or performance metrics were presented — this was a launch/architecture + demo session.)*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] `npm create @microsoft/rayfin@latest` then `npx rayfin up` against a free Fabric workspace — build a tiny app end-to-end.
  - [ ] Try the **data-app template** on an existing semantic model and see how good the auto-formatted Power BI/Vega-Lite visuals actually are.
  - [ ] Test **connectors** against existing OneLake data (warehouse/semantic model) and confirm the selective type-safe table pull-in.
  - [ ] Write a **Rayfin Function** that calls an external API and confirm credentials stay server-side in the Fabric sandbox.
  - [ ] Watch the companion **3:00 PM session (Chris Anderson)** and the related **BRK223** for the database/data-modeling deep dive.
- [ ] Questions:
  - [ ] How does Rayfin's row-level security (`@role` + policy) map onto Fabric/OneLake permissions and Entra groups at scale?
  - [ ] Capacity/cost: how do app workloads consume Fabric capacity vs. analytical workloads — any noisy-neighbor risk on a shared meter?
  - [ ] What exactly gets open-sourced for **self-hosting**, and what stays Fabric-only?
  - [ ] Migration safety: how does auto-migration handle destructive schema changes (dropped columns) on production data?
  - [ ] When does **PostgreSQL** / **HorizonDB** support land, and is the config-only dialect swap truly zero-code?
- [ ] Relevant to:
  - [ ] Azure/Fabric labs — could replace bespoke backend provisioning for demo apps.
  - [ ] Any internal data-driven app that should keep data governed in OneLake instead of a separate store.

## 🔗 Related
- [[BRK223 - From rows to reasoning]] — companion Build 2026 session on designing databases for AI apps and agents (same data/agents theme).
- Microsoft Build 2026 hero blog — *"Building agentic apps with Microsoft Fabric and Microsoft Databases"* (Arun Ulag) — context incl. **Azure HorizonDB** (PostgreSQL for AI apps, public preview).
- Rayfin GitHub repo: `github.com/Microsoft/Rayfin`.
- Microsoft Learn — *Fabric apps programming model* (decorator-driven Rayfin SDK reference).
- [[2026 Build Session List]] — source tracker for Build 2026 session notes.