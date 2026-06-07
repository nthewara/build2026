---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/devops
  - topic/github
  - topic/azure-devops
  - topic/ai
source: https://www.youtube.com/watch?v=flf2nfwDcJE
session_code: BRK202
event: Microsoft Build 2026
speakers: Dave Burnison (GitHub), Dan Helm (Azure DevOps)
duration_min: 44
aliases:
  - Azure DevOps meets GitHub AI powered SDLC
---

# BRK202 — Azure DevOps meets GitHub, the path to AI powered SDLC

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Dave Burnison — Senior DevOps Advocate, GitHub (former Azure DevOps advocate at Microsoft); Dan Helm — Program/Project Manager, Azure DevOps (Repos, Boards, Wiki, AI)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=flf2nfwDcJE)

## 🎯 TL;DR
Azure DevOps and GitHub have long been treated as separate platforms, but Microsoft is positioning their integration as the on-ramp to an agentic, AI-powered SDLC. The core message: let teams pick the best tool chain for their workflow — small green-field teams may live entirely in GitHub, while enterprises with heavily customised Azure Boards, Pipelines, and Test Plans can keep those investments while moving code to GitHub to unlock GitHub Copilot Cloud Agent. Dave demos driving Azure DevOps from the GitHub Copilot app/CLI via the Azure DevOps MCP server (querying work items, refining backlogs, linking GitHub security alerts to Azure Boards). Dan announces a wave of new capabilities for teams that *stay* in Azure DevOps: an **Enterprise Live Migrator** (low-downtime repo migration to GitHub), **Copilot code reviews for Azure Repos**, **Copilot Autofix for GitHub Advanced Security (GHAzDO)** — all billed to your Azure subscription, no GitHub account/Copilot licence required — plus model selection for the Copilot agent and pay-as-you-go Microsoft-hosted agents.

## 🔑 Key Takeaways
- **Positioning:** Integrating Azure DevOps with GitHub is "your path to Agentic AI" — keep Boards/Pipelines/Test Plans investments while harnessing GitHub Copilot Cloud Agent.
- **Tool-chain choice is the message:** small startup/green-field teams can use GitHub Issues + Projects for everything; enterprises with customised Boards/Pipelines should integrate rather than fully migrate.
- **Two Azure DevOps MCP servers exist** — **local** (best/"platinum" from VS Code + GitHub Copilot) and **remote** (built on Entra). Both expose the same tools: work items, repos, wiki, test plans, pipelines.
- **Why two MCP servers:** the remote server runs on Entra, which restricts non-Microsoft clients — Claude, Cursor, Codex currently won't work against the remote server, so the local server stays until Entra restrictions are resolved.
- **GitHub Copilot app + CLI** can drive Azure DevOps via the ADO remote MCP server — a low-barrier entry point for non-technical PMs who live in Azure Boards, not VS Code. The same local config is also valid for the Copilot CLI.
- **Wiki → agents/instructions:** Copilot can read Azure DevOps wiki pages (e.g. "what makes a good epic/feature/user story") and convert them into a custom **backlog manager agent** and **work-item quality custom instructions** (markdown files).
- **Security campaigns ↔ Azure Boards:** GitHub Advanced Security campaigns can be linked into Azure Boards — Copilot can auto-create a feature + a user story per alert, with assignee parity, so security work is tracked alongside everything else.
- **Enterprise Live Migrator (public preview):** full-fidelity, low-downtime (~20–30 min cut-over) migration of Azure Repos → GitHub, bringing all commits, PRs, branches and full history, and auto-reconnecting Pipelines and Boards.
- **Copilot code reviews for Azure Repos (announced, preview):** brings GitHub Copilot PR code review to Azure Git Repos with **no Copilot licence and no GitHub account required**; spins up a dynamic background pipeline, shallow-clones, sends diffs to Copilot, appends suggestions to the PR. **TFVC not supported** (no plans).
- **Copilot Autofix for GHAzDO (announced, preview):** auto-generates fixes for CodeQL alerts (creates a PR); starting with CodeQL, expanding to all scanning alerts incl. third-party tools, and to security campaigns.
- **Billing model for the new Azure-Repos AI features:** consumption-based, **billed to your Azure subscription** as an "AI credit for ADO" meter — visible in Cost Management; runs can be a few cents each. Advice: start slow with a few repos.
- **Scale work:** repos-per-project-connection limit raised from **500 → 2,000**; real customer asks of **30,000** and **80,000** repos per project show this is an ongoing challenge. ~**2.8 million** repos are active in Azure DevOps today.
- **Copilot Cloud Agent improvements:** you can now **pick the model** the agent uses (rolling out during the session), and the choice is "sticky" per selection.
- **Licensing friction reduced:** buying a **GitHub Enterprise** licence now includes a **Basic** Azure DevOps licence; integration + scale improvements are included with **GitHub Enterprise Cloud with data residency**.
- **Dogfooding:** Microsoft (specifically the Copilot agents & platform org) is actively migrating internal repos to GitHub and working there — AI is a "forcing function"; some repos move, some stay in Azure Repos.
- **Bonus capability:** Copilot can edit project *metadata* — e.g. it generated **56 sprints** (sprint schedule for two fiscal years) from a single user-story prompt instead of manual point-and-click.
- **Pay-as-you-go Microsoft-hosted agents** (incl. Apple/Mac for pay-per-minute billing) in Azure Pipelines are now available for sign-up.

## 📚 Detailed Notes

### Framing & Strategy — "Choose your tool chain"
Azure DevOps and GitHub were historically seen as separate platforms. Over the last few years Dan's team has built deeper, better integrations, and the session reframes that integration as the on-ramp to agentic AI. The guiding principle: whether you're a small startup or an enterprise with thousands of developers, Microsoft wants you to choose the best tool chain for your team's workflow and project requirements.

- **Small / green-field team:** GitHub alone may have everything you need — Issues and Projects for planning/tracking, plus repos.
- **Enterprise with heavy ADO customisation:** if you have heavily customised Azure Boards, lots of Azure Pipelines templates, portfolio roll-ups across team projects, etc., integrate Azure DevOps with GitHub. This "supercharges" teams with AI — you fully harness GitHub Copilot's agent power while continuing to leverage Azure Boards, Azure Pipelines, Test Plans, and more.
- **Teams that should stay in Azure DevOps for now:** e.g. sustaining-engineering projects in Azure Repos needing stability/continuity. Microsoft is continuing to invest in Boards, Repos, Pipelines, and Test Plans for these teams (this is the bulk of Dan's segment).

### Driving Azure DevOps from the GitHub Copilot app (Dave's demos)
Dave used a series of pre-recorded videos (to avoid waiting on Copilot live). Starting point: a normal Azure DevOps environment using Boards, with a work-item hierarchy/backlog shown on the dashboard.

**Setup — MCP configuration.** In the GitHub Copilot app **Settings → MCP servers**, the **Azure DevOps remote MCP server** is configured by:
1. Plugging in the server name.
2. Plugging in the URL to your organisation.
3. Specifying which tools to enable — e.g. work items, Azure Pipelines, Test Plans, Wiki. (Dave deliberately *didn't* enable repo tools because his repos are in GitHub.)

He then connected the app to his GitHub repo and asked which Azure DevOps projects he could access — Copilot reached out via the **ADO remote MCP server** and listed team projects.

**Querying work items.** Prompt: *"Are there any user stories or bugs recently assigned to me where state = New or Active in the Tailspin Shelter project? If so, show details."* It returned the user stories, and because of the configured instructions, included a link straight to each user story so he could open it.

**Querying pipelines & repo status.** He asked for pipeline run status and saw multiple pipelines — PR checks plus a build-and-deploy pipeline — all currently succeeding. He could also see the connected Tailspin Shelter repo, the last commit, jump into the latest PR, and view unit-test results — all from inside the Copilot app via the MCP server.

### Wiki pages → Copilot agents & custom instructions
A recurring theme: turn existing Azure DevOps **wiki** content into reusable AI assets. At Ignite the previous fall, Dan had built a wiki defining what makes a good **epic / feature / user story**, including sample markdown.

- Prompt: *"Do we have any information in Azure DevOps that would make for a good Copilot custom agent or skill?"* Copilot identified the wiki pages.
- Dave had it **create a user story** ("Convert wiki contents into Copilot agents") and **a pull request** for it. The agent generated:
  - a **backlog manager custom agent**, and
  - a set of **work-item quality custom instructions**.
- Both are just **markdown files** — the agent pulled the wiki content and produced the agent + instructions automatically.

### Refining a backlog item with the custom agent
Scenario: a dog-adoption website with a basic user story (you can pick dogs; goal is to filter by breed).
- Dave asked for user stories assigned to him → found **user story 42**.
- Asked *"Does this user story follow our standards?"* → Copilot said no (weak acceptance criteria, etc.).
- Prompt: *"Use that backlog manager agent to help me refine this work item."* → it applied significant refinements.
- Opening the work item's **history** showed every change the agent made — a clear audit trail of the refinement.

### Assigning work to the Copilot Cloud Agent + security gates
He then assigned the refined user story to **Copilot** to do the work. When selecting the agent, alongside the backlog agent he also had agents for **Bicep**, **Azure Pipelines**, and others.

Key benefit highlighted of having code in GitHub: the agent's changes are automatically checked with **Copilot code review** and **CodeQL** security scanning:
- Based on code-review comments, the agent made a couple of follow-up updates.
- Evidence of the security scans was visible in the session (no findings this time).
- Important point: *"You don't have to have licenses for code… to run code on the code that the agents are generating"* — i.e. the goal is to keep agent-written code as secure as possible by default.

He then opened the result in a **Codespace**, ran it locally, and verified the **breed filter** worked (e.g. selecting "American Staffordshire Terrier") — "a good start," more refinements to come.

### Connecting GitHub Advanced Security campaigns to Azure Boards
Presented as a "really cool" way to tie GitHub and Azure DevOps together.
- In **GitHub Advanced Security**, at the org level he had multiple **campaigns**, including one for Tailspin Shelter scoped to *all critical and high alerts* with a deadline of **Monday, June 15th**. Both alerts could be fixed by **Copilot Autofix**.
- Back in the Copilot app: *"Are there security campaigns that include this repo?"* → it listed campaigns and highlighted the repo-specific one.
- Prompt (for security campaign 14): *"Create an Azure Boards feature, create a user story for each of those alerts, and link the campaigns/alerts into the work items so I can track them where I track all my other project work,"* plus *"assign the work items the same way the alerts are assigned in the campaign."*
- Result: a new **feature** + **two user stories**, with **links back to the security campaign**, assignee parity, and the items appearing in the Azure Boards backlog.
- One alert's autofix wasn't a one-line change — it touched several lines — demonstrating the agent can handle more sophisticated fixes.

### Copilot CLI parity
When you configure the GitHub Copilot app locally, that configuration is **also valid for the Copilot CLI**. From the CLI Dave could see the same **ADO remote MCP** configuration and query both Azure DevOps and GitHub:
- *"What does the code in this repo do? What's the tech stack?"* → a summary that also noted **Azure Pipelines for CI/CD** and **Azure Boards for project management**.
- *"Show me active or resolved user stories assigned to me"* → found the "filter pet listings by breed (multi-select dropdown)" story.
- *"What's the status of the filter-by-breed user story in the related code?"* — notably he **didn't have to specify the ID (AB42)**; it resolved by description and showed the PR waiting to be merged/deployed. Conclusion: even from the command line you can bring Azure DevOps and GitHub together.

### MCP servers — deeper detail (Dan)
Azure DevOps now has **two MCP servers**: **local** and **remote**, both with essentially the same tools (work items, repos, wiki, test plans, etc.).
- **Local** = the "platinum experience," especially when driven from **VS Code + GitHub Copilot**.
- **Remote** = consolidated a bunch of tools; now supports **service principals** and **managed identities**; you can create an agent in **Azure AI Foundry** (ADO is part of that catalog).
- **In progress:** integration with **Copilot Studio** — worked on for several months, hoped to ship in the "next few weeks."
- **Why two servers:** the remote server is built on **Entra**, which imposes restrictions on which other clients can use it. Right now **Claude, Cursor, and Codex won't work** against the remote MCP server. Microsoft is working with the Entra team to remove these limits; until then the **local server stays** so non-Microsoft clients have a path.

### Integration maturity, traceability & scale (Dan)
For teams that move repos to GitHub but keep Boards/Pipelines/Test Plans, Microsoft has invested heavily over the last couple of years — much of it not new, but solidified:
- **Full traceability** between work items and GitHub commits, pull requests, and branches.
- **Scale improvements:** repos-per-project-per-connection raised from **500 → 2,000**, driven by larger orgs moving repos to GitHub.
- **Ongoing scale challenge:** a customer "today" wanted to connect **30,000** repos to a single project; one "last week" wanted **80,000** (≈ 1.5 repos per person in the company). This is something the team expects to keep working on "forever."
- **Pipelines:** with the integration you can open a pipeline and connect it to the moved repo — no need to rework pipelines.
- **Licensing friction reduced:** buying a **GitHub Enterprise** licence gets you a **Basic** ADO licence as part of that purchase. **GitHub Enterprise Cloud with data residency** (released by GitHub ~1.5–2 years ago) includes the integration and scale improvements discussed.

### Copilot Cloud Agent — model selection (Dan)
Improvement to the work-item ↔ Copilot Cloud Agent integration Dave showed:
- You can create and pick your own agent (as demoed), and **now also pick the model** the agent uses.
- Rationale: certain models work better in certain repos depending on the agent, instructions, and how much you want to pay.
- Feature was **rolling out "as we speak"**, and the selection is **sticky** — once chosen it persists for subsequent runs.

### Enterprise Live Migrator — Azure Repos → GitHub (Dan)
For teams with hundreds/thousands of repos in Azure Repos, the next big challenge after deciding to move is the migration itself. Microsoft's answer is a tool in **public preview** called the **Enterprise Live Migrator (ELM)**.
- **Full fidelity:** moves the whole repo — all pull requests, all commits, the **entire history**.
- **Seamless, low-downtime cut-over:** ~**30 minutes** of downtime. Contrast with the existing **GitHub Enterprise Importer**, where some very large repos saw **4–5 days** of downtime — unacceptable for most customers.
- **Auto-reconnects** Pipelines and Boards when the repo moves, so those aren't extra manual steps.

**CLI workflow shown** (UX is coming in the preview; commands are also exposed via the MCP server so an agent can assist):
1. **Create the migration** — supply org, repository, target destination (e.g. GitHub Enterprise Cloud with data residency), user ID, agent pool, etc. This **queues** the migration.
2. **Check status** repeatedly. First step is **validation** — checks file sizes, push packs, legitimacy; reports problems if any. Usually quick.
3. **Synchronisation** — copies all files, the whole repo, the entire history. Can take **hours or days**, but you can **keep working on the repo in Azure DevOps during sync**. Sync continues on a recurring basis (every few hours) to stay up to date.
4. **Cut-over** — once synced and caught up, schedule a cut-over date. At cut-over the repo becomes **read-only** in Azure DevOps (you can no longer work on it there); cut-over itself is ~**20–30 minutes**, then it's marked **migrated**.
5. Verify in GitHub — repo, all PRs, all branches, full history are present.

**UX preview:** a dedicated "migrating to GitHub" page (left nav) shows per-repo status — migrated, in synchronisation, in cut-over, plus any errors — and lets you queue repos and start migrations, mirroring the CLI.

### Keeping Azure-Repos-only teams happy (Dan)
There are ~**2.8 million** active repos in Azure DevOps; many can't move short-term (compliance, tooling, etc.). Microsoft's stated goal: bring Copilot/AI features **into Azure DevOps** so those teams stay productive and don't leave the Microsoft/GitHub ecosystem for other tools.

### Copilot code reviews for Azure Repos (Dan — announced)
Announced on the blog "yesterday." Brings GitHub Copilot **PR code review** to **Azure Git Repos**:
- **No Copilot licence and no GitHub account required** — "it just magically works on the back end."
- Code must be in **Azure Repos**; **billed to your Azure subscription**.
- **Two control levels** (a third is likely coming): enable at the **organisation** level, then flip on per **repo** — deliberately gated so big orgs don't enable it everywhere and get a "monster bill," especially during preview.

**How it works:** request a review on a PR → it **spins up a dynamic pipeline in the background** → does a **shallow clone** → collects **diffs** → sends a package to **Copilot** → Copilot reviews and **appends suggestions** to the PR. The interface lets you view critical bugs/suggestions, **apply changes**, commit, and **re-request** in a loop.

**Known gaps before GA:**
- **Doesn't yet honour Copilot instructions** in your repo (it's a "generic" reviewer for now) — this *will change* before GA.
- **Doesn't handle previous suggestions well** — Dan hit loops where fixing one suggestion produced a different suggestion on the same line. Adding prior-run context is planned to improve decisions.
- **Scope:** Azure **Git** Repos only — **TFVC is not supported, with no plans** to support it.

**Tracking/observability:** runs are tracked under **Agent Pools** in Azure Pipelines — you can find code-review runs there (currently raw JSON; the interface is planned to improve).

### Billing for the new Azure-Repos AI features (Dan)
- Consumption is **billed to your Azure subscription**. In **Cost Management → Cost Analysis** you can see daily cost per run; runs can be **a couple of cents** each (e.g. a busy day on the 14th), scaling with PR complexity/size and reasoning required.
- Under **Resources** you can break cost down per organisation; the meter is the **"AI credit for ADO."** Example shown: ~**0.5 cents** for the month.
- **Guidance:** billing is part of the preview (not free). Start slow — a few repos — to understand value and pricing limits before scaling.

### Copilot Autofix for GitHub Advanced Security (GHAzDO) (Dan — announced)
Brings GitHub Copilot **Autofix** to **GHAzDO** customers:
- Demo: a repo with **CodeQL** scans already finding issues (e.g. **SQL injection**) showing severity, description, and recommendation. Previously you'd open VS Code, fix manually, raise a PR.
- Enable via **Manage repositories → Code security plan → Autofix**. Then a **"Generate fix"** button appears (top-right). Like Copilot code reviews, it **spins up a background dynamic pipeline**, applies the changes, and **creates a PR**. These fixes take longer — roughly **3–5 minutes**.
- **Roadmap:** starting with **CodeQL alerts**; plan to expand to **all scanning alerts**, including **bring-your-own third-party tools**; and to add **autofix to security campaigns** (campaigns were a GHAzDO feature released "a couple of sprints ago").

### Technical previews & sign-up (Dan)
There are **three technical previews** (ELM, Copilot code reviews for Azure Repos, GHAzDO Autofix). A blog post went out "yesterday," with more per-feature posts to follow.
- Sign up via the link on the slide — they collect your **organisation name** and a bit of your **email**.
- Rollout is **wave-based**: enable a wave, observe, add the next wave. You'll get an **email from the product team** when your access is ready.

### Microsoft dogfooding (Dan + Dave)
Microsoft is "practicing what we preach": internal teams are actively **migrating repos to GitHub** and working there. The migration need was a big driver for building ELM. AI is a "forcing function" internally just as it is for customers — pushing teams to adopt more AI and do more. As with everyone else, some Microsoft repos move easily and some don't, so some teams migrate while others stay in Azure Repos. Dave clarified this is **not all of Microsoft** — it's one slice: the **Copilot agents & platform** org — and it's "just getting started." The point: Microsoft is adding tools to make migration easier for itself *and* for external customers.

### Bonus — Copilot editing project metadata (Dave)
A capability Dave fit in at the end: using Copilot/AI to manage **team-project metadata**, not just code/work items. He wrote a user story containing all the prompt detail, then told the Copilot app: *"Go do the work for user story number three"* ("Create sprint schedule"). The agent generated **56 sprints** — a sprint schedule for the next **two fiscal years** — which then appeared in Azure DevOps **project configuration**. Done in a few minutes instead of repetitive point-and-click (or hand-rolling the APIs).

### Bonus — pay-as-you-go Microsoft-hosted agents (Dan)
One more new release noted from the blog post: the ability to do **Apple/Mac pay-per-minute (pay-as-you-go) billing** is included for sign-up. This gives customers the long-requested capability for **Microsoft-hosted agents in Azure Pipelines** on pay-per-minute billing.

### Resources & wrap-up
- The team created a **repo of resources** for the session: link to the blog post with key info, plus a **release containing all of Dave's demo videos** (including a couple not shown live).
- References the big **GitHub blog post** ("yesterday") covering the Copilot app, sandboxes, and more; a **direct link to Enterprise Live Migrations**; and links to docs for the new features.
- **Slides will be made available** after the session (they contain URLs to dive deeper).
- The speakers also offered to demo adding the **MCP server to Azure AI Foundry**.
- Follow-up: they'd be at **Ship & Tell** in the other pavilion ~**3:00 pm** for questions.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure DevOps** — Microsoft's ALM suite (Boards, Repos, Pipelines, Test Plans, Wiki).
- **GitHub** — code hosting + the agentic AI layer (Copilot) this session integrates with ADO.
- **Azure Boards** — work tracking (epics/features/user stories/bugs, backlogs, portfolio roll-ups).
- **Azure Repos** — Git (and legacy TFVC) repositories in Azure DevOps.
- **Azure Pipelines** — CI/CD; also hosts the dynamic background pipelines for code reviews/autofix and pay-as-you-go hosted agents.
- **Azure Test Plans** — manual/automated test management in ADO.
- **Azure DevOps Wiki** — markdown docs; here used as a source to generate Copilot agents/instructions.
- **GitHub Copilot** — the AI assistant powering reviews, autofix, and the cloud agent.
- **GitHub Copilot Cloud Agent** — autonomous agent that does work items end-to-end (code, PRs).
- **GitHub Copilot app** — client where you configure MCP servers and chat to drive ADO/GitHub; low barrier for PMs.
- **GitHub Copilot CLI** — command-line Copilot; reuses the local Copilot app's MCP config.
- **Copilot custom agents** — user-defined agents (e.g. backlog manager, Bicep, Azure Pipelines) selectable for work.
- **Copilot custom instructions** — markdown instruction files (e.g. work-item quality standards).
- **Copilot code review** — AI PR review producing inline suggestions; now coming to Azure Repos.
- **Copilot Autofix** — AI-generated fixes (as PRs) for security alerts.
- **Azure DevOps MCP server (local)** — best from VS Code + Copilot; works with non-Microsoft clients.
- **Azure DevOps MCP server (remote)** — Entra-based; supports service principals/managed identities; in Foundry catalog; Entra restricts other clients.
- **Model Context Protocol (MCP)** — protocol exposing ADO tools (work items, repos, wiki, test plans, pipelines) to AI clients.
- **GitHub Advanced Security (GHAS / GHAzDO)** — security scanning; "GHAzDO" = GHAS for Azure DevOps.
- **CodeQL** — static analysis / code-scanning engine surfacing alerts (e.g. SQL injection).
- **Security campaigns** — GHAS feature grouping alerts with deadlines; linkable to Azure Boards.
- **Enterprise Live Migrator (ELM)** — public-preview tool for low-downtime, full-fidelity Azure Repos → GitHub migration.
- **GitHub Enterprise Importer** — existing migration tool (the slower, higher-downtime contrast to ELM).
- **GitHub Enterprise Cloud with data residency** — GHEC variant; includes the ADO integration + scale improvements.
- **Azure AI Foundry** — agent platform/catalog where the ADO remote MCP can be added.
- **Copilot Studio** — agent-building platform; ADO MCP integration in progress.
- **GitHub Codespaces** — cloud dev environments; used to run/test the breed-filter feature.
- **Entra (Microsoft Entra ID)** — identity platform underpinning the remote MCP server (and its client restrictions).
- **Azure Cost Management** — where consumption-based AI billing ("AI credit for ADO" meter) is viewed.
- **Agent Pools** — where code-review/autofix runs are tracked in Azure Pipelines.
- **Claude / Cursor / Codex** — third-party AI clients that currently can't use the *remote* ADO MCP server.
- **Bicep** — Azure IaC language; a Copilot agent for it was shown in the agent picker.
- **TypeScript** — language of the sample PR used in the Azure Repos code-review demo.
- **Tailspin Shelter / Tailspin Toys** — sample projects/repo used throughout the demos.

## 🚀 Announcements / What's New
- **Enterprise Live Migrator (ELM)** — *Public preview (sign-up).* Full-fidelity, low-downtime (~20–30 min cut-over) Azure Repos → GitHub migration; brings all PRs/commits/branches/history; auto-connects Pipelines and Boards; CLI today (UX in preview), commands also in the MCP server.
- **Copilot code reviews for Azure Repos** — *Announced (blog) + technical preview (sign-up).* GitHub Copilot PR review for Azure Git Repos with no Copilot licence / no GitHub account; billed to Azure subscription; org + repo level enablement (third control likely). Gaps before GA: doesn't yet honour Copilot instructions; weak handling of prior suggestions. TFVC unsupported.
- **Copilot Autofix for GHAzDO** — *Announced + technical preview (sign-up).* Autofix for CodeQL alerts (generates a PR); roadmap: all scanning alerts incl. third-party tools, and autofix for security campaigns.
- **Copilot Cloud Agent model selection** — *Rolling out during the session.* Pick the model the agent uses (per-repo/per-agent/cost trade-offs); choice is sticky.
- **Repos-per-project-connection scale** — *Increased 500 → 2,000.*
- **MCP remote server enhancements** — service principals, managed identities, Foundry catalog presence; **Copilot Studio** integration *in progress* ("next few weeks").
- **Licensing** — GitHub Enterprise purchase now includes a **Basic** ADO licence.
- **Pay-as-you-go Microsoft-hosted agents (incl. Apple/Mac pay-per-minute)** in Azure Pipelines — *available for sign-up.*
- **Security campaigns ↔ Azure Boards linking** + Copilot auto-creating linked work items — shown as a working integration.

## 💡 Demos
- **Configure ADO remote MCP in the Copilot app** — proved a PM can connect to ADO and list team projects without VS Code.
- **Query work items / pipelines / repo from the Copilot app** — showed conversational access to user stories, succeeding pipeline runs, last commit/PR, and unit-test results via MCP.
- **Wiki → backlog manager agent + work-item quality instructions** — proved existing ADO wiki standards can be auto-converted into reusable Copilot agents/instructions (markdown), via an auto-created user story + PR.
- **Refine user story 42 with the backlog manager agent** — proved AI can enforce backlog quality standards, with full change history/audit trail in the work item.
- **Assign work to Copilot Cloud Agent with security gates** — proved agent-written code is auto-checked by Copilot code review + CodeQL; sophisticated multi-line autofix; result validated by running the breed filter in a Codespace.
- **Security campaign 14 → Azure Boards** — proved Copilot can create a feature + a user story per alert, link them to the campaign, and mirror assignees, unifying security tracking in Boards.
- **Copilot CLI driving ADO + GitHub** — proved CLI reuses the app's MCP config and can resolve a work item by description (no ID), surfacing the PR awaiting merge/deploy.
- **Copilot code reviews for Azure Repos** — proved enabling the feature (org + repo) lets you request a review on a PR; background dynamic pipeline shallow-clones, sends diffs, and appends critical-bug suggestions you can apply/commit/re-request.
- **Azure Cost Management view** — proved per-day/per-run consumption visibility (cents per run; ~0.5¢/month example) under the "AI credit for ADO" meter.
- **Copilot Autofix for GHAzDO (CodeQL)** — proved enabling Autofix adds a "Generate fix" button that creates a fix PR for a CodeQL alert (e.g. SQL injection) in ~3–5 min.
- **Enterprise Live Migrator (CLI + UX)** — proved the create→validate→synchronise→cut-over flow with continued work during sync, read-only at cut-over, and full repo/PR/branch/history arriving in GitHub.
- **Sprint schedule generation** — proved Copilot can edit project metadata, generating 56 sprints (two fiscal years) from one user-story prompt.

## 📊 Notable Stats / Quotes
- **~2.8 million** active repos in Azure DevOps today.
- Repos-per-project-connection limit: **500 → 2,000**.
- Real customer asks: **30,000** repos to one project (today) and **80,000** (last week, ≈ 1.5 repos/person).
- **56 sprints** generated (two fiscal years) from a single prompt.
- ELM cut-over downtime: **~20–30 minutes** vs **4–5 days** seen with the GitHub Enterprise Importer for very large repos.
- Autofix duration: **~3–5 minutes** per fix; code-review runs: **cents per run** (e.g. ~0.5¢ for a month in the demo).
- Session length: only **~45 minutes** for a lot of material ("I covered a lot of information in a short time").
- *"Integrating GitHub with Azure DevOps is your path to Agentic AI."* — Dave Burnison.
- Copilot code reviews for Azure Repos need **no Copilot licence and no GitHub account** — *"it just magically kind of works on the back end."*
- On dogfooding: *"AI is a forcing function for us internally just like it is probably for all of you."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Configure the **Azure DevOps remote MCP server** in the GitHub Copilot app (and confirm it carries to the Copilot CLI) against a test ADO org.
  - Convert an existing ADO **wiki** standards page into a **backlog manager agent** + **work-item quality instructions**.
  - Sign up for the three previews: **ELM**, **Copilot code reviews for Azure Repos**, **GHAzDO Autofix** (via the blog post links).
  - Pilot **Copilot code reviews for Azure Repos** on 1–2 repos and watch the **Azure Cost Management** "AI credit for ADO" meter to gauge cost.
  - Try linking a **GHAS security campaign** to **Azure Boards** and have Copilot create linked work items per alert.
- [ ] Questions:
  - Timeline for the remote MCP server to support **Claude/Cursor/Codex** (Entra restrictions) — and for **Copilot Studio** GA?
  - When do **Copilot instructions** start being honoured by Azure Repos code review (the named pre-GA item)?
  - Pricing detail/limits for the "AI credit for ADO" meter beyond "start slow"?
  - Does ELM support **TFVC → GitHub** or Git only? (Code review explicitly excludes TFVC.)
  - What's the practical ceiling for repos-per-project today vs the 30k/80k asks?
- [ ] Relevant to:
  - Enterprise teams on Azure Boards/Pipelines/Test Plans evaluating a move to GitHub for Copilot agents.
  - Platform/DevEx teams planning large-scale **Azure Repos → GitHub** migrations (ELM).
  - Security teams wanting **Autofix** + campaign-to-Boards traceability without per-dev GitHub licences.

## 🔗 Related
- [[Build2026]]
- 