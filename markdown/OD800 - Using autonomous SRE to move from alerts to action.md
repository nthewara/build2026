---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/sre
  - topic/observability
  - topic/agents
  - topic/devops
  - topic/azure
  - topic/incident-management
source: https://www.youtube.com/watch?v=sf3y8TRcBDI
session_code: OD800
event: Microsoft Build 2026
speakers: Vom Nagrani, Deepti Jalupati
duration_min: 44
aliases:
  - Using autonomous SRE to move from alerts to action
---

# OD800 — Using autonomous SRE to move from alerts to action

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Vom Nagrani (Product Manager, Azure SRE Agent team) & Deepti Jalupati (Product Manager, Azure SRE Agent team)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=sf3y8TRcBDI)

## 🎯 TL;DR
This session explores what happens when AI agents don't just *observe* incidents but actually *act* on them, using **Azure SRE Agent** — an AI-powered agent for incident management and resource optimization in production environments. The presenters frame the AI-agent era as a shift not in *what* developers are responsible for, but in the **scale, speed, and how much of that responsibility can now be offloaded, orchestrated, and automated**. Through two live demos they show the agent (1) preventing bad code from reaching production by automatically canary-testing pull requests, and (2) autonomously diagnosing, root-causing, and remediating a production incident end-to-end in minutes. The agent is fully customizable (your runbooks, connectors, skills, sub-agents), secretless by design (managed identity + on-behalf-of elevation), and governed with human-in-the-loop review or fully autonomous run modes. The closing pitch: it's an always-on SRE teammate that never sleeps, built natively on Azure, extensible to your environment, and integrated with the DevOps/observability tools you already use.

## 🔑 Key Takeaways
- **Azure SRE Agent** is an AI-powered agent for **incident management and resource optimization** in production, positioned as an "always-on SRE teammate" that learns your environment and acts the way you configure it.
- Three core value props: **(1)** automates operational tasks to keep apps running and protect revenue, **(2)** accelerates root-cause analysis (RCA) to improve reliability/availability, **(3)** is **fully customizable** to your operational standards.
- The agent attacks two big problem spaces: **preventing issues / reducing operational toil at scale** (fewer incidents, less repetitive work) and **reducing downtime / speeding recovery** (faster resolution, fewer handoffs and context switches).
- **You don't need the Azure portal** — the entire lifecycle (create, configure, manage, interact with the agent) can be driven from developer tools like the **terminal and GitHub Copilot CLI**, because the SRE Agent endpoint is exposed as an **MCP server**.
- Agents are created from **recipes** hosted in Microsoft's SRE Agent repo — pre-packaged bundles of connectors, tools, and skills so you don't configure from scratch. Config lives in a folder of simple **YAML + markdown** files (connectors, skills, custom agents, knowledge, invocation triggers).
- The agent can be invoked three ways at config time: an **HTTP trigger** (e.g. wired to a GitHub Actions workflow on each PR), an **incident platform** (ServiceNow / PagerDuty / Azure Monitor alerts), or a **scheduled task** (cron).
- **Demo 1 (outer-loop / PR gating):** on each new PR a GitHub Action fires the agent via HTTP trigger; the agent deploys the change to staging, runs a **5-minute synthetic/canary test**, detects that staging mock responses differ from production behavior, flags the PR **high-risk**, and comments on it automatically.
- **Demo 2 (reactive incident response):** a ServiceNow incident (simulated by rotating a backend DB password without updating the app) triggers the agent, which consults its **knowledge base + memory of past incidents**, correlates logs and Azure activity logs, identifies a **"credential desync" recurring pattern**, confirms root cause, opens a GitHub issue, and **autonomously remediates** then verifies the new revision is healthy.
- Three reliability pillars: **multi-path transparent RCA** (evaluates multiple hypotheses against telemetry), **automated mitigation** (safe, reversible actions like restarts/scale/rollback with guardrails + human-in-the-loop), and **enhanced incident response** (head start for on-call with synthesized cause + next steps).
- **Extensibility is the headline differentiator:** the agent adapts to *your* org — custom logic, your data sources, proprietary troubleshooting steps, domain checks, and remediation workflows — and deeply integrates with **GitHub Copilot**, logging actions as GitHub issues for traceability and a detect→diagnose→fix→improve feedback loop.
- **Trust & control are built into every layer:** three RBAC roles (reader / standard user / administrator), per-agent **user-assigned managed identity** (no secrets/API keys), **on-behalf-of (OBO)** flow for temporary elevation, **review vs autonomous** run modes, command-validation hooks, and a **full KQL-queryable audit trail** in Application Insights.
- **Secretless, sandboxed architecture:** credentials never enter the reasoning context; an isolated **identity sidecar** issues short-lived per-call tokens; each agent run gets its own **microVM sandbox** (Azure dedicated compute) so no cross-agent data leaks; all egress goes through a validating proxy (BYO VNet supported).
- Three usage modes across the operational lifecycle: **interactive** (chat/co-pilot in the portal), **reactive** (alert-driven — the primary way most customers use it), and **proactive** (scheduled autonomous health/compliance/security/optimization scans).
- Built-in observability of the agent itself: **session insights**, an **incident metrics dashboard** (mitigation rates, hours saved), **agent consumption** (Azure AI units/day), and inbuilt **evals** (e.g. an "intent met" quality score on a 1–5 scale, auto-calculated per completed thread).
- **Customer proof points:** AstraZeneca +40% developer velocity (GitHub Copilot), Ford up to +70% modernization efficiency (GitHub Copilot app modernization), and a lab/customer cut SRE daily alerts from **30–40/day down to under 10/day** using Azure SRE Agent. Gartner: **90% of enterprise software engineers** will use some form of AI coding/ops assistance by **2028**.
- **Get started in 3 steps** — *teach it* (upload runbooks/docs, connect repos, share team knowledge), *connect it* (Azure Monitor, App Insights, PagerDuty, ServiceNow, Datadog, anything via MCP), and *let it work* (round-the-clock investigation, scheduled compliance scans, auto-filed issues, proposed fixes) at **sre.azure.com**.

## 📚 Detailed Notes

### Framing: from observing incidents to acting on them
The session opens with a provocative question: *what happens when AI agents don't just observe incidents but actually act on them?* The thesis is **autonomous SRE** — moving teams from **noisy alerts to automated, intelligent action**. The presenters (Vom Nagrani and Deepti Jalupati, both PMs on the Azure SRE Agent team) set the macro context: generative AI is transforming how we work, and AI agents are a major driver of adoption — especially in software development, where **Gartner estimates 90% of enterprise software engineers will use some form of AI coding or ops assistance by 2028**.

The key insight on the developer role: the fundamentals haven't changed (writing code, fixing bugs, designing features, moving the product forward), but the ground *is* shifting. Developers now:
- Don't just build apps — they **migrate and modernize entire systems**, increasingly *with agents* doing part of the work.
- Own far more of the lifecycle — **incidents, security, releases, documentation** — often running continuously, with agents working alongside them and sometimes ahead of them.

So the real change in the AI-agent era **isn't what you're responsible for — it's the scale, the speed, and how much of that responsibility you can now offload, orchestrate, and automate** with agents.

### What is Azure SRE Agent?
**Azure SRE Agent is an AI-powered agent for incident management and resource optimization in production environments.** Three core value propositions:
1. **Automates operational tasks** to keep applications running and protect revenue.
2. **Accelerates root-cause analysis** to improve reliability and availability.
3. **Fully customizable** — you manage and configure the agent to meet your unique operational needs and the standards your enterprise/company follows.

Mental model: **an always-on SRE teammate that learns how your environment works and acts according to how you want it to.**

### The problem it solves
Developers and SRE teams are buried in **repetitive operational toil** across both the **inner loop and outer loop** of software development. They spend time:
- Detecting issues *before* they roll out to production.
- Verifying that Azure best practices are followed.
- Doing this across **hundreds or thousands of resources** spanning multiple stacks.

This work is **repetitive, well-defined, error-prone, and slow when done manually** — exactly the profile that suits automation. Azure SRE Agent is designed to take this burden off teams so they can **focus on building, not firefighting**.

### Two scenarios covered
1. **Preventing issues & reducing operational toil at scale** — the agent automates and customizes workflows → outcome: fewer incidents, less repetitive work.
2. **Reducing downtime & speeding up recovery** — the agent accelerates RCA and triggers mitigation → outcome: faster resolution with fewer handoffs between teams and less churn across windows/tools.

Each scenario is presented as capabilities + a live demo.

### Scenario 1 — Preventing production regressions (the "outer loop")
**The developer pain (Deepti):** Shipping many deployments week over week, you want to ensure nothing breaks in production, but today it's manual — get other developers to review the code, test in staging to check for regressions, and rely on however much test coverage you happen to have. Things slip through to production. The goal is that **nothing slips into production**.

**How the agent helps:**
- Connect the agent to **code repositories** (GitHub or Azure DevOps).
- Set it up with an **event/webhook trigger** so it can run **asynchronously** — developers push PRs, and the agent acts on them to verify the code is good.
- In the demo, the agent is connected to all telemetry data sources: **Dynatrace, Log Analytics workspace**, and **Azure activity logs**, and scoped to the **resource groups** to monitor (the team has a **production** RG and a **staging** RG).
- The developer **never leaves the CLI/IDE** — the whole workflow runs without opening the Azure portal.

### Demo 1 walkthrough — PR canary gating from the CLI
**Creating the agent from a recipe:**
- Instead of the portal, the agent is created/configured/operated entirely from **developer tools** — the **terminal** and **GitHub Copilot CLI**.
- Use a **recipe** from Microsoft's SRE Agent repo: a recipe ships a ready-made set of **connectors, tools, and skills** out of the box, so you don't build from scratch.
- A **script** first generates the agent **configuration**, then you **deploy** it. The chosen recipe connects to **GitHub + Dynatrace** and is customized to understand the app architecture (e.g. **App Service + PostgreSQL**). The presenter supplies just the few connector-specific values; the rest comes from the recipe. This produces a `contoso-demo-5` folder containing the entire agent configuration.

**Anatomy of the agent configuration folder (shown in VS Code while deployment runs):**
- **Hosting:** when you create an SRE Agent in an Azure subscription you give it a **resource group** to host the agent; you can change name / RG / subscription / **region** (three regions supported at the time).
- **Target scope:** optionally set **target resource groups/subscriptions** to monitor (here: production + staging).
- **Connectors:** recipe ships **Dynatrace + Log Analytics workspace**; you can add your own connectors and their config details.
- **Skills & custom agents:** configure the agent with **skills or custom agents**; you can bring skills authored in other tools because the format is a **markdown file for instructions** plus a **simple YAML file** for the prompt/spec.
- **Invocation:** choose how to invoke — **HTTP trigger**, an **incident platform**, or a **scheduled task**. Here an **HTTP trigger** is wired to a **GitHub Actions workflow**, so the SRE Agent is invoked on every new PR to run **canary testing** and judge whether the change is safe for production.
- **Knowledge:** teach the agent about your environment/systems (a knowledge folder); anything that should go into the agent's **core memory** (extracted from an existing agent or seeded) goes under **system-synthesized knowledge** — all simple **markdown files**.

**Post-deploy:**
- Deployment succeeds, then runs a **post-hook configuration** (notably to connect GitHub), returning an **OAuth URL** the user visits to authorize.
- To keep one consistent interface, the presenter uses **Copilot CLI** to connect to and manage the agent: the **SRE Agent endpoint is accessed as an MCP server** (available for a while now). They edit the local MCP JSON config to point at the **new agent's URL** from the deployment, confirm it's connected, and then interact via Copilot CLI.

**Verifying & teaching the agent via Copilot CLI:**
- Ask the agent what it's connected to → it returns the **production + staging resource groups** and connected **Log Analytics workspaces**.
- Confirm **GitHub** is connected and which repo.
- Define the desired behavior: on a new PR, take the change, **deploy it to staging, run synthetic traffic, and determine whether the change risks production** so risky changes get prevented/reviewed carefully.
- Use Copilot CLI to **create a skill** (it uses the SRE MCP server to do so), then create a **sub-agent** connected to that skill. Now there's a **skill + custom agent + GitHub Actions workflow wired to the HTTP trigger** — all set up.

**Triggering it with a real code change:**
- Switch to the coding workspace, change a **URL**, create a **new branch**, and open a **new PR**.
- The PR creation fires the GitHub Action → invokes the agent via the **HTTP trigger** → the agent fetches PR details, deploys the image to **staging**, and sends traffic to judge whether it's a good deployment.
- While the fresh run proceeds, an **earlier run from that morning** is shown: a similar case where the **database URL was switched**. The agent deployed to staging, identified exactly which files changed, ran a **5-minute synthetic/canary test**, and found that **staging mock responses differed from production** (the backend database would return different results). It correctly judged this **should not go to production**, **flagged it high-risk**, and **added a comment on the PR**.
- Payoff: a fast-moving team gets automatic low-risk/high-risk verdicts on PRs, keeping production safe — the agent watches PRs at the velocity teams ship today.

### Reliability & performance — the three pillars (Vom)
1. **Root-cause analysis (RCA):** instead of engineers manually correlating logs/metrics/alerts across multiple dashboards, the agent performs a **multi-path, transparent RCA automatically** — it **evaluates multiple hypotheses, tests them against telemetry**, and produces a **clear, explainable result + diagnostic summary**. This cuts time-to-insight **from hours to minutes**.
2. **Automated mitigation:** resolves common issues proactively using **your guardrails and human-in-the-loop workflows**, executing **safe, reversible actions** (restarts, scale adjustments, rollbacks) to eliminate repetitive toil while **keeping humans in control**.
3. **Enhanced incident response:** the moment an alert fires the agent activates — **ingests signals from Azure Monitor or third-party tools**, performs initial analysis, and gives the on-call engineer a **head start**: a synthesized explanation, a **probable cause**, and **actionable next steps**. Net effect: drastically reduced downtime and improved operational consistency.

### Extensibility — the key differentiator
Every org has unique standards, processes, and compliance requirements, and **Azure SRE Agent adapts to yours, not the other way around**:
- Integrate **custom logic, your own data sources, your own custom knowledge** into the agent's reasoning.
- Encode **proprietary troubleshooting steps, domain-specific checks, and specific remediation workflows** so the agent behaves consistently with internal standards.
- **Intelligent multi-source insights:** correlates across **logs, metrics, configurations, and historical patterns** to detect anomalies hard to spot manually.
- **Deep GitHub Copilot integration:** any action the agent performs (diagnosing, mitigating, recommending) can be **logged automatically as GitHub issues** for traceability and follow-up, creating a continuous **detect → diagnose → fix → improve** feedback loop.
- Bottom line: extensibility makes the agent your **operational expert, shaped by your environment and aligned to how your teams already work**.

### Scenario 2 — Autonomous incident response (the "inner loop" / production reality)
Even with PR gating, **issues still happen in production**, and IT operations need a **very small mean-time-to-resolution (MTTR)** to keep apps healthy and quickly available. Today's workflow is painful: jump between tools (e.g. Dynatrace), check Azure, look across multiple log sources (especially with a multi-source Azure telemetry strategy), piece it all together, find where things went wrong, then mitigate.

The same agent that developers use for the outer loop can be reused by **DevOps / IT operations**, hooked up to **ServiceNow, PagerDuty, or Azure Monitor alerts** (whatever incident platform you use). You define a **response plan** for which incident types the agent should handle and feed it **knowledge sources / runbooks** for contextual understanding. When an incident pops up, **the agent starts handling it right away with no human intervention** and — depending on configuration — performs diagnosis + RCA, then either **creates a dev ticket** or goes further to **fix the code and open a PR**.

### Demo 2 walkthrough — ServiceNow incident → diagnosis → autonomous remediation
**Setup:** A second recipe is deployed that connects to **ServiceNow** (could equally be PagerDuty/Azure Monitor). It ships the **skills** to handle app-related-error incidents plus a **custom agent** that performs the investigation. Workflow: ServiceNow incident → custom agent → connected tools + skills.

**Simulating the failure:** The presenter mimics a real-world case — an **IT person/team rotates a backend database password** (because it expired) but the **applications aren't updated** with the new credentials, breaking the app. A **ServiceNow incident is sent** to simulate it.

**The agent's autonomous investigation:**
- **Incident #3** appears; the agent **picks it up immediately** and starts investigating. Because the password was rotated, the **order service** is failing with errors.
- **Starts with the knowledge base:** since app-architecture knowledge was uploaded, the agent first reads the knowledge base — *like a team member who builds context before jumping into investigation*.
- **Uses memory of past incidents:** it recalls prior investigations to spot patterns — noticing that **someone has been rotating passwords frequently**.
- **Correlates telemetry sequentially** (via Dynatrace + Azure tools): first checks **logs** to identify which **app and revision** is failing, then examines **activity logs** and finds that **~3 minutes ago the password was rotated** (true). It matches this against the symptoms the user is experiencing.
- **Root cause confirmed:** *"the database password is rotated, but the container app hasn't been updated"* — that's the cause of the failure. It cross-references **past issues** and recognizes this as a **recurring "credential desync" pattern**.
- **Tracking:** creates a **new GitHub issue** to track the incident and the remediation.
- The narrator emphasizes the agent behaves like an **expert engineer**: tapping past knowledge/incidents to find patterns and **using data to validate/support its hypotheses** throughout — all **within minutes** vs. the **multiple hours and tool/context-switching** this would normally take. You don't have to watch it finish; the incident is picked up automatically and results can be routed to **GitHub issues, Outlook, or Teams**.

**Autonomous remediation:**
- The agent was **configured to perform actions/mitigations autonomously**, so — recognizing the recurring pattern — it **proceeds with remediation**: update the credentials and ensure they **flow down to the apps**.
- It then **verifies the new revision is healthy** and creates the **GitHub issue** with the full analysis.
- Important caveat: *in theory you can configure the agent to only provide analysis and take **no automated actions** on your behalf* — autonomy is opt-in.
- **Final summary:** the agent reconstructs the **sequence of events** leading to the password change as root cause, applies the fix, confirms health, and leaves a **trackable GitHub issue** with the full incident summary — turning manual incident handling into automated diagnosis + mitigation + documentation.

### Trust & control — built into every layer
**Permissions / RBAC:**
- Three built-in roles — **reader, standard user, administrator** — each scoped to what that persona needs.
- At creation you choose **reader vs. privileged** permission level for the agent's **managed identity**.
- **Every agent gets its own user-assigned managed identity** → **no secrets or API keys to manage**.
- When the agent needs to act beyond its standing permission, it uses the **on-behalf-of (OBO) flow** to **temporarily elevate using your credentials** — **no standing write access required**.

**Governance / run modes:**
- **Review mode:** the agent **proposes** an action and **waits for an administrator to approve**.
- **Autonomous mode:** the agent **executes directly** — ideal for non-production or trusted recurring tasks.
- **Command-validation hooks** inspect and validate **every command before execution** (and every tool call before it's returned).
- **Every single action** (tool calls, model invocations, approval decisions) is **logged to Application Insights as a full audit trail** queryable with **KQL**.

**Security (secretless by design):**
- **Credentials never enter the reasoning context.**
- An **isolated identity sidecar** issues **short-lived, per-call tokens** — that's where the permissions live.
- **Each agent run gets its own dedicated sandbox** powered by **microVM** (an Azure dedicated compute environment), as do your **Python tools** → **no cross-agent data is leaked**.
- Connectors to external systems (**GitHub, Datadog, ServiceNow**) all use **OAuth-based authentication flows**.
- **All outbound network access goes through an egress proxy** that validates requests and controls what each agent can reach — or you can **bring your own VNet**.

**Monitoring / observability of the agent itself:**
- **Session insights:** a structured summary of any conversation — what was found, what was recommended, etc.
- **Incident metrics dashboard:** shows **mitigation rates, hours saved**, and per-response-plan plus summary-level views.
- **Agent consumption:** tracks how many **Azure AI units** the agent used on a day-to-day basis.
- **Inbuilt evals:** e.g. an **"intent met" quality score**, automatically calculated on **every completed thread** and **rated on a 1–5 scale**, so you can measure effectiveness over time.
- **Bottom line:** you get the **full autonomous power** of Azure SRE Agent **with full enterprise controls**.

### Three ways to use the agent (across the operational lifecycle)
1. **Interactive mode (co-pilot):** chat directly with the agent **in the Azure portal** — ask questions, run diagnostics, perform natural-language operations, even **upload task files / HAR files** for traces or analysis. Assumes a **human is driving** the flow. Caveat: *if this is the only way you use the agent, you're probably missing ~90% of the value* an agent can unlock beyond a co-pilot.
2. **Reactive mode (alert-driven) — the primary way most customers use it:** the agent responds **automatically to Azure Monitor alerts** and integrates with **PagerDuty and ServiceNow**. It performs **automated triage, initial RCA**, and can **trigger mitigation with your approval**, tracking incident metrics/insights over time (as shown in Demo 2).
3. **Proactive mode (scheduled / autonomous):** the agent operates autonomously on a schedule via **cron expressions** — running **continuous health and compliance checks**, **detecting anomalies** across resources, **assessing security posture**, and providing **resource-optimization recommendations**.

Together these three modes give **full coverage from ad-hoc troubleshooting to always-on autonomous operation** running in the background.

### Why choose Azure SRE Agent
- **Built natively on Azure** → understands your infrastructure deeply: your **resource graph, Monitor signals, and entity model**.
- **Extensible** → adapts to your environment instead of forcing you into a rigid workflow.
- **Secure by design** → managed identity, **RBAC**, full audit trails.
- **Integrates with the tools you already use** → **GitHub, PagerDuty, ServiceNow, Datadog, Dynatrace**, and more.
- **Scales to any team size** → from a single SRE, to a team of five ops managers, to an org supporting **thousands of services** — it meets you where you are.

### Getting started — a simple three-step process
1. **Teach it:** upload your **runbooks and documentation**, connect your **code repositories**, and share **team knowledge** — the agent learns from every session, just like a human SRE would.
2. **It connects:** the agent integrates with **Azure Monitor, Application Insights, PagerDuty, ServiceNow, Datadog** — basically anything connectable via **MCP**.
3. **It works for you:** investigates incidents **around the clock**, runs **scheduled compliance scans**, **triggers issues automatically**, and **proposes fixes**. You give it context; it connects to your tools and starts working — *a teammate that never sleeps*.

Get started at **sre.azure.com** — the Azure SRE Agent portal, with documentation, blog posts, walkthroughs, **DIY hands-on labs**, and links to support / file feedback.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure SRE Agent** — the AI-powered agent for incident management and resource optimization in production; the entire focus of the session.
- **GitHub Copilot** — AI coding assistant cited in customer velocity/modernization stats and deeply integrated with the SRE Agent (actions logged as GitHub issues).
- **GitHub Copilot CLI** — terminal-based Copilot used to create, configure, and interact with the SRE Agent without the portal.
- **GitHub Copilot app modernization** — capability credited with Ford's up to 70% modernization efficiency boost.
- **GitHub** — code repository + GitHub **Actions** workflows (HTTP trigger) and **GitHub Issues** for incident tracking/remediation.
- **Azure DevOps** — alternative supported code repository for connecting the agent.
- **MCP (Model Context Protocol) server** — the SRE Agent endpoint is exposed as an MCP server so tools like Copilot CLI can connect; "anything connectable via MCP" can integrate.
- **Recipes (Microsoft SRE Agent repo)** — pre-packaged bundles of connectors, tools, and skills to bootstrap an agent without configuring from scratch.
- **Skills & custom agents / sub-agents** — natural-language instructions (markdown) + YAML prompt/spec that teach the agent to perform specific workflows.
- **Dynatrace** — observability/telemetry connector used in both demos.
- **Datadog** — supported third-party observability connector (OAuth-based).
- **Azure Monitor** — first-party alerting/telemetry source for reactive incident response.
- **Log Analytics workspace** — Azure telemetry source connected to the agent.
- **Azure activity logs** — used by the agent to detect the password-rotation event in Demo 2.
- **Application Insights** — stores the full KQL-queryable audit trail; also a connectable telemetry source.
- **ServiceNow** — incident platform connected in Demo 2 (triggers the agent on incidents).
- **PagerDuty** — supported incident platform alternative.
- **Azure App Service** — example app-hosting service the recipe was customized to understand.
- **Azure PostgreSQL** — example backend database in the demo app architecture.
- **Azure Container Apps** — the "container app" whose revision needed updating after the password rotation (and was verified healthy post-remediation).
- **User-assigned managed identity** — per-agent identity; eliminates secrets/API keys.
- **On-behalf-of (OBO) flow** — temporary credential elevation for actions beyond standing permissions.
- **microVM sandbox** — Azure dedicated compute environment isolating each agent run and its Python tools.
- **Egress proxy / Bring-your-own VNet** — validates and controls all outbound agent network access.
- **Command-validation hooks** — inspect/validate every command and tool call before execution/return.
- **KQL (Kusto Query Language)** — used to query the agent's audit trail in Application Insights.
- **Cron expressions** — schedule proactive autonomous runs (health/compliance/security scans).
- **Microsoft Teams / Outlook** — optional channels to receive the agent's incident outputs.

## 🚀 Announcements / What's New
None explicitly announced. The session is a capabilities walkthrough and live demonstration of Azure SRE Agent (incident-prevention PR gating, autonomous incident response, governance/security model, and the three usage modes). No release/preview/GA milestones or roadmap dates were called out. The presenters note MCP-server access to the SRE Agent endpoint "has been available for a while now," and direct viewers to **sre.azure.com** to get started.

## 💡 Demos
- **Demo 1 — PR canary gating from the CLI (outer loop):** Created an SRE Agent entirely from the terminal/Copilot CLI using a recipe (GitHub + Dynatrace, customized for App Service + PostgreSQL), wired it to a GitHub Actions HTTP trigger, authored a skill + sub-agent, then opened a real PR (changing a URL). The agent auto-deployed the change to **staging**, ran a **5-minute synthetic/canary test**, detected that **staging mock responses differed from production**, **flagged the PR high-risk**, and **commented on it** — proving the agent can automatically prevent risky code from reaching production at team velocity, without leaving the developer's tools.
- **Demo 2 — Autonomous ServiceNow incident response (inner loop):** Reused the same agent connected to **ServiceNow**, then simulated a real failure by **rotating a backend DB password without updating the app** (breaking the order service). On **incident #3**, the agent autonomously read its **knowledge base**, leveraged **memory of past incidents**, correlated **logs + Azure activity logs**, found the **~3-minute-old password rotation**, confirmed the **"credential desync" root cause**, opened a **GitHub issue**, **autonomously remediated** (updated credentials, flowed them to the app), and **verified the new revision was healthy** — all in minutes, proving end-to-end autonomous diagnosis → RCA → mitigation → documentation. (Noted: autonomy is configurable; the agent can be set to analysis-only with no automated actions.)

## 📊 Notable Stats / Quotes
- **Gartner:** ~**90% of enterprise software engineers** will use some form of AI coding or ops assistance by **2028**.
- **AstraZeneca:** **+40% developer velocity** when adopting GitHub Copilot for writing code.
- **Ford:** up to **+70% modernization efficiency** boost using GitHub Copilot app modernization.
- **Alert reduction:** a customer/lab cut SRE daily alerts from **30–40/day to under 10/day** using Azure SRE Agent.
- **Time-to-insight:** RCA reduced **from hours to minutes** (multi-path transparent RCA).
- **Evals:** "intent met" quality score auto-calculated per completed thread, rated on a **1–5 scale**.
- **Regions:** **3 Azure regions** supported for hosting the agent (at time of recording).
- > *"What happens when AI agents don't just observe incidents but actually act on them?"* — the framing question for the whole session.
- > *"The real change in the AI-agent era isn't what you're responsible for. It's the scale, it's the speed, and it's how much of that responsibility you can now offload, orchestrate, and automate with agents."*
- > *"If this is the only thing you use the agent for [interactive co-pilot mode], you're probably missing 90% of the value."*
- > *"Imagine a teammate that never sleeps."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Deploy an Azure SRE Agent from a **recipe** in the Microsoft SRE Agent repo entirely via **Copilot CLI** (MCP), targeting a test prod + staging RG pair.
  - Wire an **HTTP trigger** to a GitHub Actions workflow to **canary-test PRs** in staging and auto-comment risk verdicts.
  - Stand up the **reactive** flow against **Azure Monitor alerts** (or ServiceNow) and test a **credential-desync** style incident end-to-end.
  - Try **review mode** vs **autonomous mode** and inspect the **KQL audit trail** in Application Insights.
  - Explore the **DIY hands-on labs** at **sre.azure.com**.
- [ ] Questions:
  - Which **3 regions** are currently supported, and what's the GA/preview status of the SRE Agent and its recipes?
  - What exactly counts as an **"Azure AI unit"** for agent-consumption billing, and how is it priced?
  - How are **microVM sandboxes** isolated/limited (runtime, resource caps, network), and what Python tooling is preinstalled?
  - What are the precise scopes of the **reader/standard/administrator** roles and the **reader vs privileged** managed-identity levels?
  - How robust is the **memory of past incidents** — is it per-agent, shareable, and how is it seeded vs. learned?
- [ ] Relevant to:
  - Azure production reliability / SRE & DevOps incident-response automation.
  - Reducing operational toil and MTTR for teams already on GitHub + Azure Monitor/Dynatrace/Datadog/ServiceNow.
  - Agentic AI governance patterns (managed identity, OBO, human-in-the-loop, audit trails).

## 🔗 Related
- 