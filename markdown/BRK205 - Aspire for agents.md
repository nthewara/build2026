---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet-aspire
  - topic/agents
  - topic/distributed-apps
  - topic/ai
  - topic/azure
  - topic/dotnet
source: https://www.youtube.com/watch?v=ge5PM7pX49k
session_code: BRK205
event: Microsoft Build 2026
speakers: Mattie Monola (PM, .NET Aspire); David Fowler (Distinguished Engineer / "Fowler")
duration_min: 46
aliases:
  - Aspire for agents
---

# BRK205 — Aspire for agents: Transform how you build and deploy distributed apps

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mattie Monola (PM on the .NET Aspire team) & David Fowler ("Fowler", Distinguished Engineer / Aspire architect). Beth and Glenn supported from the Aspire booth.  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ge5PM7pX49k)

## 🎯 TL;DR
Aspire is positioned as an **"agent-ready, code-first tool to compose, debug, and deploy any distributed app."** The session reframes Aspire away from a .NET-only orchestrator: in 2026 you can author the **app host in TypeScript, C#, Python, Java** (Go/Rust coming), and it orchestrates any-language apps. The core idea is that one file — the **app host** — becomes the single source of truth for both local dev and deployment, eliminating config drift. The talk is mostly live demo: a mini "book a meeting + agent goes off and reasons" app spanning a Vite front end, an API, a background worker, a Postgres container, Microsoft Foundry, and a sandboxed agent container. Heavy emphasis on the new **agent story**: everything visible in the Aspire dashboard is now exposed via API/CLI so coding agents (Copilot, Claude, etc.) get the *same* observability humans do — traces, logs, browser F12 console output — letting them close the loop (profile → analyze → edit → re-run). Aspire also manages ports across git work trees, provisions per-developer Azure sandboxes with role-based security, and deploys to Azure Container Apps + Foundry hosted agents via `aspire deploy`, generating Bicep you can fully customize.

## 🔑 Key Takeaways
- **Aspire one-liner:** "an agent-ready, code-first tool to compose, debug, and deploy any distributed app." If you have a website + a database, you already have a distributed app.
- **Big 2026 change:** the **app host can now be authored in C# *or* TypeScript** (and Python/Java; Go coming soon), even though the orchestrated apps can be any language. This is the headline shift from Aspire's .NET roots.
- **One file = single source of truth** for dev *and* deploy. The same app host generates deployment manifests/assets, so there is **no config drift** between local and cloud.
- **Aspire is not a runtime** — "it's literally a process starter and stopper" (plus dependency restore, container pulls, health checks, config wiring). No magic; it just puts the right environment variables in the right place.
- **New `aspire start` (non-blocking) vs `aspire run` (blocking):** `start` launches the app host in the background and returns, because coding agents choke on long-running/blocking terminal commands. `aspire ps` / stop manage running instances.
- **Everything in the dashboard is now exposed to agents** (big change landed in build 13.0; matured by 13.4). The dashboard is "just UI over an API," and that API is available to both the CLI and the dashboard — so agents can do anything a human can: pull traces, search logs, analyze, edit code, re-run.
- **Integrations encapsulate the "right way" to run/debug/deploy a thing** (Vite, Node, Python, Redis, Postgres, etc.) — including injecting dev certs for HTTPS, OpenTelemetry config, and language-specific env vars. ~100+ hosting integrations; all built on the **same public primitives** you can use yourself.
- **Port management across work trees:** Aspire randomizes/overrides ports (e.g. overriding Vite's port) so multiple agents/sessions in parallel git work trees don't collide on 3000/8080.
- **Reference-based wiring, no hardcoded ports/URLs:** you pass endpoint *references* (e.g. backend URL into the front end) and Aspire resolves the real value per environment — solving the "works locally, breaks on deploy" HTTPS/port problem.
- **Per-developer Azure sandboxes:** if you're authenticated (Azure CLI / VS Code / azd), the dashboard prompts to provision real Azure resources for you — each dev gets their own subscription/sandbox, including the **resource group, Foundry project, deployed model, and RBAC roles** so only the right app component can reach the resource.
- **Secrets/parameters are stored in your user profile, not the repo** — unique per work tree, and impossible to accidentally commit (a real pain point with AI coding agents pushing tokens).
- **Browser logs integration (new):** `WithBrowserLogs` (`Aspire.Hosting.Browser`) launches a tracked/debuggable browser so F12 **console + network logs flow back into the dashboard and to the agent** — no more screenshotting DevTools.
- **Agent "skills" instead of (or alongside) MCP:** `aspire agent init` installs Aspire skills (monitor the app, use custom commands/resources, "wait for healthy/successful"). A Postgres MCP can also be auto-wired (`WithMcp`/MCP server) from the app host.
- **Dashboard as a Trojan horse:** can run standalone as an OpenTelemetry viewer — even to watch what your Copilot is doing (tokens, tool calls, turns). Recommended onboarding path for teams.
- **Deployment is multi-target & not vendor-locked:** integrations exist for Azure Container Apps, vanilla Kubernetes, vanilla Docker Compose, and AWS. `aspire deploy` generates the right asset (Bicep/YAML/Helm) and **exposes the full Bicep object model in your language** for customization — with escape hatches (`aspire publish`) for advanced DevOps teams.
- **Cadence:** Aspire ships roughly **every ~4 weeks** with big changes; docs auto-update via PRs on every change. Current build at talk time was **13.4** (with 13.42 patches already out). Get it at **aspire.dev**.

## 📚 Detailed Notes

### What Aspire is (and isn't)
Aspire is pitched as the answer to distributed-app complexity. The moment your dev loop grows from a single `npm run` to `npm run` + `docker compose up` + `dotnet run` — getting ports right, keeping processes from tripping over each other — apps get complicated, and **what works in the dev loop doesn't translate cleanly to deployment**. Something that runs fine in isolation on your box often behaves differently in a containerized environment, App Service, or a vanilla Kubernetes cluster.

Aspire's original premise was twofold:
1. **Turn on things you should turn on** in an app (this matters less now because Copilot/your agent does it for you).
2. **"Glue-stick" the individual pieces of your stack together** so running locally feels as close to real life as possible, and you can compose and debug the whole thing meaningfully instead of piece-by-piece in isolation.

The canonical one-liner (delivered as a deliberate, grammatically-correct, Oxford-comma'd run-on): **"Aspire is an agent-ready, code-first tool to compose, debug, and deploy any distributed app."** The speakers describe it informally as "kind of like a bootstrapper… kind of like a Docker Compose replacement with better types," but stress you have to use it to *get* it.

**Crucial framing — Aspire is not a runtime.** "It is literally a process starter and stopper." It does not host your threads. Everything ultimately runs on a thread somewhere (in Docker or not); Aspire starts/stops those processes and wires them together.

### The pieces of Aspire (each usable on its own)
Aspire is several composable parts, and **every piece can be wielded independently**:
- **The CLI** — the thing that actually runs everything and ties the other pieces together. Install from **aspire.dev**.
- **The app host file** — where you build out a custom developer experience for your app (the app *model*). This is where most of the session's time is spent.
- **Integrations** — Aspire's packaged *opinions* on the right way to turn on, run, and connect to resources locally and in the cloud. ~100+ hosting integrations; fully overridable.
- **The dashboard** — runs completely standalone (you don't need a fully "Aspirified" app). Can be used purely as an **OpenTelemetry viewer** — e.g. there's a VS Code YouTube demo using it to watch a Copilot's emitted telemetry (tokens, tool calls, turns). The recommended team-onboarding move: use the dashboard as a viewer first — the **"Trojan horse"** for adopting more of Aspire.

**Same primitives everywhere:** all integrations are built on the *same primitives* exposed to users. The opinionated experiences for Redis, Azure Container Apps, ElastiCache, etc. use the exact building blocks you can use yourself. An app host can be as trivial as "run `ls`, run `gp`" — it's all just code (you can comment lines out, wrap them in `if` statements, use launch profiles). Anecdote: on an "Aspire Fridays" stream, the Codespaces team turned a random repo script into an app host and it became "super nice and organized."

**Aspire vs Pulumi / cloud IaC:** Aspire is about the **developer experience first**, then translating that DX into something ops-appropriate. It was never meant to replace deployment manifests — but the app host has matured enough that the same file can generate manifests/assets for whatever runtime you target. (Fowler runs apps hit by a couple hundred people/month where "my CI is `aspire deploy`.")

### OpenTelemetry ("hotel") as a foundation
"Hotel" = OpenTelemetry (OTel), referred to that way throughout. It's the eminent standard for **tracing, logs, and metrics**, and works across container resources, backends, and front ends. The dashboard surfaces all of this. If you ask your coding agent to add Aspire to your app, "it will do it in one shot" today.

### The agent story (why Aspire is "agent-ready")
Over the last ~7–9 months the team built features specifically to optimize coding-agent interaction:
- **Deterministic harness:** Aspire gives the agent a deterministic description of how the app runs and how parts connect. On a new session the agent doesn't have to grep files, parse a (possibly stale) README, and fall over itself starting things — there's a **single source of truth** it can inspect with one CLI command.
- **Port management:** Aspire manages ports so multiple agents across multiple work trees don't all conflict on 3000/8080.
- **Getting info back to the agent:** integrations pull more information back out to the agent — e.g. browser F12 developer logs into the coding agent **without screenshot-and-paste**.
- **Philosophy:** Aspire is **dev-first / human-first** (a person typing or prompting), and then brings that *same* experience to coding agents and to new teammates onboarding.

A landmark change in **build 13.0**: "everything in the dashboard must be visible to agents." Because the dashboard is just UI over an API, and that API is exposed to both the CLI and the dashboard, by **13.4 and beyond the agent can do the same things humans can.** Tell Copilot/Claude "tell me when the app is slow" and it will run `aspire <hotel/logs/traces>`, export traces, analyze, edit code, re-run, and loop to optimize. Fowler's real story: to find why `aspire start` was slow for non-app cases, he instrumented the CLI, dashboard, orchestrator, and RPC, added a command that booted the dashboard and collected traces, and the agent "read it in a loop and optimized four parts of it." They call this **"giving the agent eyes / senses."**

### The demo app — "book a meeting, agent reasons about it"
The scenario: you book an appointment in your calendar, and a background **agent** goes off and does smart things — tells you whether to wear long or short pants that day, flags scheduling conflicts, suggests where to prep earlier in the day, and (if there's an agenda) what to prep. Think a mini version of what Google/Office might do.

Building this is "never one thing": a **web front end**, a **back end (API)**, an **agent that runs in the background**, which must be **secure** and run in a **sandbox/container**. The mental model the speakers use: **Lego bricks**, and Aspire is the **Lego base plate** that lets you snap front end + back end + agent together. The whole app host was "slopped together perfectly" in ~3 days (48 hours).

The visible demo: drag to book a meeting → hit **Book** → the agent runs a background process and returns prep time (e.g. "book your prep 10:30–10:45"), a weather note ("it's wet in Seattle, wear a rain coat"), travel time, and a build checklist. Simple UX, but a lot has to happen behind the scenes end-to-end.

### Running it: `aspire start` vs `aspire run`
- Install the CLI from **aspire.dev** (the download button on the site — "no one can figure out what it means," per the running joke about Glenn). As of the day before the talk it's in **WinGet** (`winget install aspire...`); **Homebrew** and **npm** distribution coming "pretty soon."
- `aspire --help` lists all commands ("so many commands, Maddie").
- **`aspire start`** runs the app host **in the background** and dumps info, then returns — this is **new** and exists *because coding agents hate blocking processes* in the terminal (they watch for the command to end to know it's done; many can't background reliably).
- **`aspire run`** is the **blocking** version (the team even made "aspire run" shirts before realizing they'd want `start` too — both exist).
- **`aspire ps`** lists running Aspire instances on the machine; you can control them, stop them, and see versions.

The app host shown is an **`.mts` (TypeScript)** file — underscoring that you can now author the app host in C# *or* TypeScript in 2026 (apps themselves can be any language).

### What `aspire start` actually did
Reading the app host, on start Aspire:
1. Ran a couple of **`npm install`s** — it found `package.json`s, saw dependencies, and restored them.
2. Ran **`npm run dev` with a custom port** for the web front end (its port-management mechanism so work trees don't conflict).
3. **Pulled and started the container image** (Postgres). If the Postgres container weren't present it would go to **Docker / Podman / Rancher**, pull the image, open it, and ensure connection values/strings are correct. (They pre-pulled to avoid making the audience watch a Docker pull.)
4. **Health-checked** everything — each resource signals health differently, or Aspire takes its "educated guess" — then reports healthy.

### Custom commands & resources in the dashboard
A recurring real-world need: admin/utility actions that aren't really part of the app (e.g. "clear the calendar to start over," seed random data). Normally you'd build an auth-gated admin UI, or hit raw endpoints via Swagger/Scalar. Instead, the **Aspire dashboard lets you author commands** that appear on individual resources (each row — container, process, etc., is a resource). In the demo they added two commands: **"make a random calendar"** and **"clear the calendar"** (with a confirmation prompt). Clicking clears all events in the app; another generates a calendar from build data or randomly — essentially **database seeding** driven from the app host.

The point: **express behavior for individual apps/projects in the app host** so it's always working — instead of the classic stale `run-this-giant-bash-file` script that breaks for every new dev because the README is out of date. This UI is **driven entirely by code in the app host**.

### The dashboard as a command center
The Aspire dashboard is "a really good command center for your app," all driven from the one app host file:
- **Resource detail:** click a resource row to see the thread it runs on, where it runs from, and which process it is.
- **Config / environment variables:** scroll and you can see and manage **all the config injected** to a resource — mostly via environment variables. Example: a front end's #1 need is its **backend URL**; instead of hardcoding "backend runs on :8080," Aspire overrides common config with env vars so work trees don't break. "It's really not magic… we just have really smart people who know which environment variables need to be set and when."
- **HTTPS / dev certs:** the demo runs on HTTPS using **dev certs** (`dotnet dev-certs`-style). Injecting certificates differs per language (Node vs C# etc.); each integration encapsulates build/debug/dev/deploy behaviors for its thing (Next, "unicorn"/uvicorn-style Python servers, etc.). So a single `AddNodeJsApp` line has to inject the OTel config, dev certs, and `NODE_ENV` for *that* language — Aspire understands each language/integration and translates Aspire's behaviors into it.
- **Traces tab:** the app is instrumented with OpenTelemetry and polls roughly every second (you can hit **pause** to stop collecting traces). Clicking a trace gives a **full end-to-end trace** — e.g. a click → DB pull → "did the agent see any changes?" The example trace shows a **204 from the worker (where the agent runs) into the API, which then hits the Postgres database.** Useful both to debug flows *and* to **profile performance** ("why is this call slow? oh, it's calling the database 17 times").
- **Console log viewer:** consolidates all console logs that would otherwise be scattered across 7 terminals or 7 agent background tasks. Filter by resource; **download/export** logs (and traces/metrics) to hand the whole stream to your team.
- **Resource graph:** a draggable visual graph of the app showing connections between front end, client app, browser, back end, and database — making complex apps much easier to debug. (If your app is a single static file + an on-disk DB, you may not need Aspire; the value kicks in the moment you add a database, cache, or front-end/back-end split.)

### Browser logs integration (new)
A new integration — **`Aspire.Hosting.Browser`**, used via a **`WithBrowserLogs`** method on a web front-end resource — opens a **tracked browser with a debug port** and scrapes the console + network requests. You launch this "tracked browser" (it looks normal), open a log panel, and see **network traffic and console debug logs** (e.g. Vite output + all client requests) right in the dashboard. The killer property: **the agent has the same information** — `aspire logs` dumps the same data, and the agent can `aspire logs search <...>` to search logs, traces, and all info. This debugs the *entire* stack — client → backend → database — and solves CORS-debugging-in-a-cramped-F12-pane pain.

### Microsoft Foundry integration & per-dev Azure provisioning
Setting an env var in the dashboard (e.g. enabling inference with the Copilot SDK) turned on a **new resource: Microsoft Foundry** — Microsoft's **agent platform**. Aspire reads strongly-typed/"strongly-resourced" env vars (built-in **Aspire parameters**) you define in the app host, and you can set/unset/change them from the dashboard or CLI at will.

**Provisioning flow:** at dev time, if you're authenticated anywhere on your machine with Azure (**Azure CLI, VS Code, or azd**), the **Foundry integration** has the dashboard pop a dialog: "We see you have an Azure account — would you like us to provision a resource for you to develop against?" (This dialog/UI capability isn't in Aspire core — it's in the **Azure base libraries**; it queries the Azure CLI on your machine, finds your application, and prompts an Azure login. The same pattern works for **any Azure resource**, not just Foundry, and you can build it for anything.)

This replaces the painful manual ritual (out-of-date README → find the dev sub → copy/paste subscription ID → tenant ID → decide on a resource group → maybe use the az CLI by hand — "terrifying"). The demo picked **Sweden Central** because the model is likely to deploy/run there ("the Swedes are asleep," so capacity is free). What provisioning does:
- **Each dev gets their own subscription/sandbox** — no sharing resources, no conflicts on the same Azure object. (You could imagine sharing a subscription with different resource names, but the common pain is teams colliding on the same Azure thing, so per-dev play spaces win.)
- Provisions the **resource group, the Foundry project, and deploys a model** — and crucially provisions **RBAC roles** so only the correct components inside the app host can talk to the resource (e.g. the front end is what "knows about" Foundry, so that role is assigned to that resource). This is real security expressed from the app host — "I can't have some random person hit this from the internet." (Funny story: it was so locked down the presenter couldn't reach his own agent — only the app could.)

**Secrets/parameters:** Aspire does **not** save parameters in your environment or a file — it puts them in your **user profile**, so they're **unique per work tree** (test against different subs in different trees) and **can't be accidentally committed** to source. This directly addresses AI agents pushing tokens to repos (it's improved, "but they still do"). The agent can also set parameters/secrets itself.

Net: with Aspire you can **clone and run an app with provisioned resources** (Azure or external endpoints) with **no portals and no click-ops** beyond clicking in the dashboard (or letting the agent do it).

Aspire deliberately worked with the Azure teams on its integrations, and it's **not vendor-locked to Azure** — there's an **AWS** integration, **vanilla Kubernetes**, and **vanilla Docker Compose**.

### Agent skills, work trees & the GitHub app
- **`aspire agent init`** (for existing Aspire users) adds/updates Aspire **skills** — and you "don't even need an MCP." (There is an MCP, but the CLI + skills suffice.) There's a whole repo of skills, including: the right way for the agent to **monitor the app**, how to **wield custom commands/resources** (e.g. the agent discovers available custom commands and uses them to inspect the database), and a **"wait for X to be healthy/successful"** skill so the agent doesn't blindly `sleep 120`.
- In the demo the agent was told to check logs; it found the "monitor the app" skill and started running `aspire logs` and related commands to diagnose. The agent can even launch a browser from the terminal to "see" the browser.
- **GitHub app** (brand new — released ~the week before, became available the day of the talk): a left-hand **sessions** panel where each session is a unique **git work tree**. You can configure a **run script** so that **on workspace start it runs the app host isolated** (`aspire start --isolated`-style): take all the app's ports and **randomize them** to avoid conflicts, and make a **unique copy of any dev secrets per work tree**. On stop it deletes the work tree and tears down the app host. This lets you **preview multiple app hosts in parallel** while working in the same source tree.

### Deployment: from app host to the cloud
Deployment reuses the **same building blocks** as dev. The demo app was deployed to an **Azure Container Apps environment** by pulling in `AddAzureContainerAppEnvironment` (an integration — same primitive, but deployment-specific). The flow:
- **Each resource knows how to generate its own deployable asset** (a Dockerfile or whatever makes sense for it).
- The **Azure Container Apps environment integration** knows how to take those resources and translate them into **Bicep** (or YAML, Helm charts — "name your integration here"), and how to override properties — so you **never hand-edit Bicep**.
- **`aspire deploy`** generates the assets, uses the correct mechanism for the runtime (per integration), deploys to the cloud (e.g. a Container Apps environment), connects things together, and seeds everything correctly. **`aspire publish`** is an **escape hatch** — it generates the assets without deploying, for teams that need to inspect/own what happens.

**Why escape hatches matter:** it depends on the app. A green-field app or a small team can do the entire end-to-end with `aspire deploy`. But an advanced DevOps team does **not** want a black-box single `aspire deploy` with no visibility — especially in production. For **ephemeral dev environments** it's great to spin up and see the whole thing working; when you **promote** you want more lockdown, more rules. Aspire serves both stages.

**Customizing the generated infra:** Aspire **exposes the full Bicep object model in your language** (C# / TypeScript). This object model is built by the **Azure SDK team** (not the Aspire team). Aspire gives sensible defaults, then your job is to mutate any property you want — nothing is locked down. Example shown: setting the **capacity SKU** for a Foundry resource — adding a Foundry project/deployment adds a **GPT-5 mini** chat model, and on deploy the **capacity is set to 10** ("~10× something"). You can literally `await chat.<...>` and scroll through every property available on your Container App / App Service / Helm resource, then produce the correct Bicep for your use case.

### Multi-platform topology (the deployed app)
The deployed version spans **multiple compute environments**:
- **Azure Container Apps** hosts the **front-end website** and the **back-end worker process**.
- **Foundry hosted agents** host the **agent container sandbox** (two agents were visible "hanging out").

Doing this by hand is non-trivial — you'd have to span ACA *and* the Foundry hosted-agent service. Aspire makes it declarative: you say *which* compute environment each resource targets via `WithComputeEnvironment`. "Take my API resource, the worker, and the front end → put them in **ACA**. But put the **sandboxes** in the **hosted agent service** because it's secure — I can spin one up on the fly and have it go away." That isolation lets a coding agent "crap on disk" in a throwaway sandbox without touching other customers' data. So you design the topology in Aspire and it becomes "pretty trivial."

### Closing & community
- **aspire.dev** is the home for everything (CLI download, docs). Docs auto-update via PRs on every Aspire change (AI-drafted, human-reviewed) so they stay current with the product — a big improvement over early days.
- **Cadence:** ships every ~4 weeks with substantial changes; check aspire.dev / "what's new" to keep up. At talk time: **13.4** shipped Monday ~3pm, with **13.42** patches already out.
- Join the **Discord**; the team **live-streams to YouTube most Fridays** ("Aspire Fridays"). Fill out the session evaluation. **Sample code for the demo app** to be uploaded that night.
- **Adoption anecdote:** Chris Reington, who set up the machines for the dev-tools-and-frameworks area, first used Aspire only ~2 weeks before the event (forced to install it on everything) and "since then he has not been able to create a project without it." The team's thesis: "once you use it, you're never going to be able to go back" — so they're arming fans and contributors with tools to explain and demo it, since the hardest part is explaining what Aspire *is* without showing it.

## 🛠️ Products / Features / Technologies Mentioned
- **.NET Aspire** — agent-ready, code-first tool to compose, debug, and deploy any distributed app (a process orchestrator + integrations + dashboard + CLI, not a runtime).
- **Aspire CLI** — runs everything; `aspire start` (background, non-blocking), `aspire run` (blocking), `aspire ps` (list/manage running instances), `aspire deploy`, `aspire publish`, `aspire logs` (+ `search`), `aspire hotel` (telemetry), `aspire agent init` (install skills). Install via aspire.dev / WinGet (Homebrew & npm coming).
- **Aspire app host** — the single-file app model; authorable in **C#, TypeScript** (`.mts`), **Python, Java** (Go/Rust coming); orchestrates apps in any language.
- **Aspire dashboard** — command center: resource detail, env/config management, traces, console logs, resource graph, custom commands. Runs **standalone** as an OpenTelemetry viewer.
- **Aspire integrations** (~100+ hosting) — opinionated packaging of run/debug/deploy for a tech; all built on the same public primitives. Named: `AddPostgres`, `AddNodeJsApp`, `AddViteApp` (a Vite/"VIT" front end), `AddAzureContainerAppEnvironment`, `Aspire.Hosting.Browser` (`WithBrowserLogs`), `WithComputeEnvironment`, plus Redis support.
- **Aspire parameters** — strongly-typed/"strongly-resourced" env vars/secrets defined in the app host; stored in the **user profile** (per work tree; not committed).
- **Aspire skills** (`aspire agent init`) — agent skills repo: monitor the app, wield custom commands/resources, "wait for healthy/successful." Reduce need for an MCP.
- **Aspire MCP** — exists but optional given skills.
- **OpenTelemetry (OTel / "hotel")** — tracing, metrics, structured logs standard underpinning the dashboard.
- **Microsoft Foundry** — Microsoft's agent platform; Aspire integration provisions a Foundry project, deploys a model, assigns RBAC roles, and hosts agent sandboxes ("Foundry hosted agents").
- **GPT-5 mini** — chat model deployed by the Foundry integration in the demo (capacity set to 10 on deploy).
- **Copilot SDK** — referenced for enabling inference in the app ("enable inference with the Copilot SDK").
- **Azure Container Apps (ACA)** — deployment target for front end + back-end worker.
- **Azure SDK / base libraries** — provide the Azure auth/provisioning dialogs and the **Bicep object model** exposed in C#/TypeScript.
- **Bicep** — generated IaC for Azure deploys; fully customizable via the object model.
- **Container engines:** Docker, Podman, Rancher — used to pull/run container images (e.g. Postgres).
- **PostgreSQL** — database container; optional add-ons: **PgWeb** (web viewer) and **Postgres MCP** (auto-wired MCP server).
- **dev-certs** — dev HTTPS certificate injection per language.
- **Vite** — front-end build tool/dev server (port overridden by Aspire).
- **npm / pnpm** — package managers (pnpm switchable; "yes it works").
- **GitHub app** (new) — sessions UI mapping to git work trees; configurable run scripts to start the app host isolated with randomized ports + per-tree secrets, torn down on stop.
- **Cross-cloud/runtime integrations:** **AWS**, **vanilla Kubernetes**, **vanilla Docker Compose** (Helm/YAML deploy targets).
- **azd (Azure Developer CLI), Azure CLI, VS Code** — auth sources Aspire detects to offer provisioning.
- **Coding agents:** Copilot, Claude ("cla") — consume Aspire's CLI/skills/telemetry to close the dev loop.
- **Observability tools (interop):** Grafana, Prometheus, Honeycomb — Aspire can export OTel to these alongside its own dashboard.
- **aspire.dev**, **Aspire Discord**, **Aspire Fridays** YouTube live streams — community/resources.

## 🚀 Announcements / What's New
- **App host authoring in TypeScript (and Python/Java) alongside C#** — the major 2026 shift; app host shown as an `.mts` file. **Go coming soon** (Rust floated jokingly).
- **`aspire start`** — new **non-blocking** background run command (complements blocking `aspire run`), built for coding agents that hate blocking terminal processes.
- **Full agent visibility (build 13.0 → matured 13.4+):** "everything in the dashboard must be visible to agents" — dashboard is UI over an API exposed to both CLI and dashboard, so agents get the same traces/logs/observability and can close the loop. Current build **13.4** (with **13.42** patches) shipped during Build week.
- **`Aspire.Hosting.Browser` / `WithBrowserLogs`** — new integration that opens a tracked, debuggable browser and pipes F12 console + network logs into the dashboard and to the agent.
- **Aspire skills + `aspire agent init`** — installable agent skills (monitor, custom commands, wait-for-healthy) reducing reliance on MCP.
- **Postgres MCP auto-wiring** (`WithMcp` / MCP server) and **PgWeb** add-ons defined directly in the app host.
- **Per-developer Azure provisioning** via the Foundry/Azure integration — dashboard-driven provisioning of resource group, Foundry project, deployed model, and RBAC roles per dev sandbox; secrets stored in user profile (per work tree, non-committable).
- **WinGet distribution** of the CLI — available as of the day before the talk (`winget install aspire...`); **Homebrew and npm coming soon**.
- **GitHub app** — brand new (released ~a week prior, available the day of the talk): work-tree sessions with configurable isolated app-host runs (randomized ports, per-tree secrets, auto teardown), enabling parallel app-host previews.
- **Auto-generated docs** — every Aspire change opens a PR to the docs repo (AI-drafted, human-reviewed), keeping docs in sync.
- **Multi-compute deployment topology** via `WithComputeEnvironment` — mix ACA (front end/worker) and Foundry hosted agents (sandboxes) from one app host.
- **Roughly 4-week release cadence** with large changes each release.

## 💡 Demos
- **"Book a meeting" agentic app (main demo):** Drag-and-book a calendar meeting → background agent returns prep time, weather/clothing advice, travel time, and a build checklist. Proves Aspire composing a real multi-component agentic app (Vite front end + API + background worker + Postgres + Foundry agent sandbox) from one app host.
- **`aspire start` + `aspire ps`:** Launching the app host in the background and inspecting running instances — proving the non-blocking, agent-friendly run model and what Aspire restores/pulls/health-checks on start.
- **Custom dashboard commands:** "Clear the calendar" (with confirmation) and "make a random/build-based calendar" appearing on a resource — proving app-host-authored commands replace stale seed scripts/admin UIs.
- **Dashboard tour:** Resource config/env-var management, an end-to-end **trace** (204 worker → API → Postgres), console log consolidation/export, and the draggable resource graph — proving the dashboard as a single command center over one file.
- **Live env-var toggle → Foundry resource:** Setting an Aspire parameter in the dashboard turned on the Microsoft Foundry resource and kicked off Azure provisioning (resource group + Foundry project + model + roles), in Sweden Central — proving dashboard/CLI-driven, no-portal, secure per-dev provisioning. (Took ~5–7 min over conference Wi-Fi; pre-deployed for the agent demo.)
- **Browser logs integration:** Launching the tracked browser and viewing Vite console + network logs in the dashboard, then `aspire logs (search)` giving the agent the same data — proving full-stack client→DB debugging shared between humans and agents.
- **Agent + skills + work trees:** Telling a coding agent to check logs; it found the "monitor the app" skill and ran `aspire logs`/commands to diagnose; GitHub app showed multiple work-tree sessions with isolated app hosts — proving parallel agent sessions without port/secret conflicts.
- **Deployment:** Pre-deployed app on **Azure Container Apps** (front end + worker) and **Foundry hosted agents** (two agent sandboxes), shown alongside `aspire deploy`/`publish` and the Bicep object model (GPT-5 mini capacity = 10) — proving multi-platform deploy from the same model with full IaC customization. (Live `aspire deploy` hit flakiness mid-demo — a candid "it should be fine… no, it failed before" moment.)

## 📊 Notable Stats / Quotes
- **"Aspire is an agent-ready, code-first tool to compose, debug, and deploy any distributed app."** — the canonical one-liner.
- **"Aspire is not a runtime… It is literally a process starter and stopper."**
- **"We're not [using a magic runtime]. We're just sticking environment variables in the right place. We just have really smart people who know which environment variables need to be set and when."**
- **"Everything in the dashboard must be visible to agents"** — the principle behind the 13.0 change; dashboard = "just UI over an API."
- **"Giving the agent eyes / senses"** — how they describe feeding agents Aspire's observability so they can close the loop.
- **~100+ hosting integrations**, all on the same public primitives.
- **Ships every ~4 weeks**; at talk time **13.4** (with **13.42** patches) shipped during Build week.
- **Capacity 10** for the deployed **GPT-5 mini** Foundry model; provisioning region **Sweden Central** (chosen for likely model availability).
- Demo app built in **~3 days (48 hours)**; Foundry provisioning **~5–7 minutes** over conference Wi-Fi.
- **Chris Reington** went from first use **~2 weeks ago** to **unable to create a project without Aspire**: "since then he has not been able to create a project without it… once you use it, you're never going to be able to go back."
- If you ask your coding agent to add Aspire to your app, **"it will do it in one shot."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up the **standalone Aspire dashboard as an OTel viewer** to watch a Copilot session's tokens/tool calls/turns (the VS Code YouTube demo).
  - Spin up a TypeScript (`.mts`) app host for a Node/Vite + API + Postgres app and use **reference-based wiring** (no hardcoded ports) end to end.
  - Run **`aspire agent init`** on an existing project and have Copilot/Claude use the monitor/wait/custom-command skills to profile a slow endpoint.
  - Add **`WithBrowserLogs`** to a front end and confirm F12 console/network logs flow into both the dashboard and `aspire logs search`.
  - Try **per-dev Foundry provisioning** + RBAC and a multi-compute deploy (`WithComputeEnvironment`: ACA for web/worker, Foundry hosted agents for the sandbox).
  - Test the **GitHub app** work-tree isolation (randomized ports + per-tree secrets) to run multiple app-host previews in parallel.
- [ ] Questions:
  - When do **Homebrew / npm** CLI distribution and **Go** app-host authoring actually land?
  - For enterprises: recommended split between `aspire deploy` (ephemeral/dev) and `aspire publish` + owned pipelines (prod) — governance pattern?
  - How does per-dev subscription provisioning scale cost-wise across a large team, and can it be pointed at a shared sub with unique resource names instead?
  - Maturity/coverage of the **AWS** and **vanilla Kubernetes/Helm** deploy integrations vs Azure?
- [ ] Relevant to:
  - Building agentic/distributed apps (front end + API + worker + DB + agent sandbox) with one source of truth for dev *and* deploy.
  - Improving coding-agent workflows (giving agents real observability + skills to close the loop).
  - Azure-first teams using Foundry, ACA, Bicep — and anyone wanting no-click-ops per-dev sandboxes.

## 🔗 Related
- [[2026 Build Session List]]
- Topic: .NET Aspire · distributed apps · agentic apps · OpenTelemetry · Microsoft Foundry · Azure Container Apps
- aspire.dev · Aspire Discord · "Aspire Fridays" (YouTube)
