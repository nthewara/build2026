---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/github-copilot
  - topic/app-modernization
  - topic/azure
  - topic/dotnet
  - topic/java
  - topic/mainframe
source: https://www.youtube.com/watch?v=SgTw85Cwtm8
session_code: BRK220
event: Microsoft Build 2026
speakers: Jeff Fritz, Nish, Hassam
duration_min: 43
aliases:
  - Using AI tools to teach old apps new tricks
---

# BRK220 — Using AI tools to teach old apps new tricks

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jeff Fritz (Principal Program Manager, GitHub Copilot Modernization team) — host & narrator; Nish & Hassam — solution engineers / demo presenters  
> **Duration:** ~43 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=SgTw85Cwtm8)

## 🎯 TL;DR
Microsoft is reframing application modernization as a **continuous, agentic, AI-driven** process rather than a one-off migration project. The pitch centres on **GitHub Copilot modernization** (for developers/architects in the IDE & CLI) working alongside **Azure Copilot** (for IT ops in the Azure portal) to deliver the "first end-to-end agentic modernization solution" across three pillars: **scale, customization, and governance**. The session announces the modernization agent and custom skills as **generally available**, plus a **Command Center** and **Rulebooks** in **private preview**, and demonstrates a wide span of scenarios — mainframe COBOL→Java, Java Struts→Spring Boot (Java 21), and ASP.NET Web Forms→Blazer→.NET 10 with Aspire — all executed by parallel cloud coding agents with human-in-the-loop control. The core message: modernize estates "in days, not months" while keeping your own standards, libraries, and governance baked in.

## 🔑 Key Takeaways
- **Modernization is now urgent + AI-led:** A Forrester Q1 2026 survey cited claims **94% of IT leaders rank app modernization as a top investment** for the next 6–12 months; **over a third of modernization projects stall** because monoliths are complex, resources tight, and security concerns pile up.
- **Three customer-demanded pillars: scale, customization, governance** — Forrester data cited at **87%+ of organizations** agreeing they need all three.
- **Two complementary products:** **Azure Copilot** (preview) is the **IT-led entry point** (discovery, inventory, dependency/topology mapping, ROI, 6R wave planning, landing zones); **GitHub Copilot modernization** is where developers/architects do the **actual execution** (assess, upgrade, migrate, refactor, replatform, deploy).
- **Modernization agent is now GA** — operated from the **CLI**, it orchestrates **multiple assessments and migration plans in parallel**, then hands plans to developers to execute/validate in the IDE. **Java and .NET Framework upgrades are automated end-to-end** from the agent CLI.
- **Custom skills are now GA** — encode your team's migration patterns and proprietary libraries **once, reuse across the portfolio** ("write once, reuse at scale") from a centralized skill library.
- **Command Center (private preview)** — a **self-hostable portal** bundled with the modernize CLI giving a **portfolio-level dashboard** (assess/plan/execute phases, project timeline, what's in flight/blocked/ready for review, ownership, auditability).
- **Rulebooks (private preview)** — encode policy, security, and architectural standards as markdown that the agent optimizes into structured files; **guardrails apply automatically to every plan regardless of language/tech stack**, with auto-generated compliance reports.
- **Parallelization is the unlock:** coding agents running in parallel can tackle estates of **tens of thousands of applications** — versus the old "hand-to-hand combat, a few apps at a time."
- **Proof points / ROI:** **70% reduction in modernization time**, **50%+ reduction in tech-debt effort**, internal customers **Xbox and Teams saw 88% time/effort savings**; internal Microsoft projects saved **10,000+ engineering hours**; cross-customer reductions of **88/80/70/60%** in migration effort.
- **Built where developers already work** — VS Code, Visual Studio, IntelliJ, the CLI, GitHub, and the Command Center (**76% of developers** live in these tools).
- **Holistic estate approach** — covers VMware, Windows/Linux workloads, .NET & Java apps, Oracle, SQL Server, and **mainframes** (via a **hybrid concierge** model pairing agents with partner experts). Ships with **60+ specialized skills out of the box**.
- **Seamless Azure Migrate ↔ GitHub Copilot handoff** — start discovery from on-prem infrastructure in Azure Migrate, export a config file, and bootstrap it into the modernize CLI; reports flow back to both developer (GitHub) and IT (Azure Migrate storage).
- **Expanded scenarios** newly supported: **mainframes, .NET Aspire, and ASP.NET Web Forms** (Web Forms in private preview).
- **Human-in-the-loop everywhere** — manual execution mode creates a **GitHub issue** with the assessment, plan, rulebook, and a staged branch so developers retain full control of code transformation.

## 📚 Detailed Notes

### Framing: Why modernization, why now
Jeff Fritz opens by positioning AI as a change to **modernization itself** — not just how you write code, but how you remove the day-to-day friction of upgrades, migrations, and tech-debt backlogs. The argument:
- Modernization isn't new, but AI makes it **more urgent than ever**.
- **94% of IT leaders** (Forrester Q1 2026 survey) rank app modernization as a top 6–12 month investment — "basically everybody."
- There is huge **friction (FUD/toil)** in keeping legacy systems alive. **Over a third of modernization projects stall** because monoliths are complex, resources are tight, and security concerns accumulate.
- When modernization stalls, **tech debt grows "like a fungus"**, eating time that should go toward AI-ready work.
- Key reframe: **"Modernization by itself isn't the goal — it's what it unlocks"** (innovation, new capabilities). The *toil of getting there* is the real blocker, which is why teams turn to **agents**.

### The three pillars: scale, customization, governance
Customers consistently ask for the same three things (Forrester: **87%+** agree they need all three):
- **Scale** — you can't modernize one app at a time in an editor. The **entire modernization lifecycle** (assessments → migration plans → version upgrades → framework changes) must scale and execute together.
- **Customization** — every app is different; you didn't write the same source for each one. Agents are **provisioned per-application** to assess and transform code to each app's specific needs and objectives.
- **Governance** — transformation must be **safe**: human-in-the-loop review, policies for approval/banned patterns, compliance rules baked in, plus **monitoring and audit trails** throughout.

### Product tenets / design principles
- **Work where you work** — **76% of developers** live in VS Code, Visual Studio, IntelliJ, the CLI, and GitHub. Bring agents to those tools rather than forcing a new console app.
- **Build with any workload** — already serving **16M+ .NET and Java developers**; positioned as **the only vendor taking a holistic estate-level approach**. Enterprise modernization requires understanding **apps, data, and infrastructure together** — VMware, Windows/Linux, .NET/Java, Oracle, SQL Server, and **mainframes** (hybrid concierge = agents + partner experts).
- **Customize and govern your tools** — "no black-box handoffs; you modernize your way." Ships with **60+ specialized skills**; layer your own **custom skills and rulebooks** so the agent learns how your org actually works.

### The vision: continuous, intelligent, collaborative
Modernization should be **continuous, intelligent, and collaborative**. **Azure Copilot + GitHub Copilot together = the first end-to-end agentic modernization solution**, unifying IT and developer workflows.

**Azure Copilot (preview)** — for IT operations folks in the Azure portal:
- Integrates directly into Azure; standardizes migration/modernization across the estate.
- Capabilities: **rapid discovery & inventory, topology & dependency mapping, ROI analysis, 6R-aligned wave planning** so leaders prioritize the right infra/apps/databases first.
- Spins up **Cloud Adoption Framework–aligned landing zones** with compliance guardrails, ready to receive workloads.
- Plans generated by central IT **flow downstream** to app/database teams — top-level decisions translate into coordinated execution at scale.

**GitHub Copilot (modernization)** — for developers/architects in the editor & CLI:
- Where the actual work happens: **code assessment, version/framework upgrades, migration planning + execution, refactoring, replatforming, reimagining** across apps, databases, and mainframe.
- Deploy outputs to **modern managed services on Azure**.

### The continuous modernization loop
The lifecycle is a **loop, not a one-and-done migration**, captured by: **plan → execute → innovate → observe → troubleshoot → optimize**.
- **Modernization side (left):** Azure Copilot's **migration agent** = IT-led entry point (planning, discovery, dependency mapping, business cases, 6R wave planning). **GitHub Copilot drives execution** (assess, transform code, upgrade frameworks, containerize, deploy to Azure).
- **Innovation stage:** refactor/reimagine apps for **AI readiness** — **.NET Framework → modern .NET**, **legacy Java → current**, swapping old dependencies for **modern Azure SDKs**.
- **Operations side (right):** keep modernized apps healthy — **observability, incident response, cost & performance optimization**.
- **Security is woven throughout:** **CVE scanning, deprecated/AI API detection, remediation** built into the workflow.
- **Why it works now = parallelization:** coding agents in parallel can take on **tens of thousands of applications**, versus the old "hand-to-hand combat."

### GitHub Copilot modernization — the three GA/preview capabilities
1. **Modernization agent — GA.** Scales assessments and upgrades across the whole portfolio. Operated from the **CLI**; orchestrates multiple assessments + migration plans **simultaneously**, then hands plans to developers to execute/validate in the IDE. **Java and .NET Framework upgrades automated end-to-end** from the agent CLI.
2. **Custom skills — GA.** Encode your team's migration patterns once, reuse across the portfolio ("write once, reuse at scale"). Developers keep business-specific logic/goals while hitting enterprise-scale speed.
3. **Command Center + Rulebooks — preview.** Command Center = portfolio-level oversight; Rulebooks = baked-in policies → human-in-the-loop at every step + full auditability.

Available everywhere teams already work: favorite editors, CLI, Command Center, and GitHub. **Link:** `aka.ms/GHCP modernization` → entry point for Microsoft Learn docs.

### Demo walkthrough (pre-recorded "modernization journeys")
Jeff brings on **Nish and Hassam**. Hassam is challenged to start not with Java/.NET but with the hardest case — **mainframe modernization**.

#### 1) Mainframe assessment & documentation (COBOL/JCL/BMS/DB2/VSAM)
- Demo app = a **terminal green-screen application** built on **COBOL, JCL scripts, and BMS screen maps**.
- **Mainframe modernization is now part of GitHub Copilot modernization** — designed to be **succinct, cautious, step-by-step** because mainframes are core business systems.
- Open the app in the **modernize CLI** and **assess**: the assessment reads the source (**COBOL, JCL, BMS, DB2, VSAM files**) and **identifies missing dependencies early** to avoid downstream modernization issues.
- Beyond catching dependency issues, it **documents the mainframe** (customers say they must understand what the mainframe does *before* modernizing):
  - **Holistic overview / executive summary** of what the app does, **user personas**, **functional modules & key capabilities**, **application architecture**.
  - **User journeys** fanned out (e.g., the green-screen options), **key business processes** and **major decision points**.
  - **Program-level detail:** per-program overview, **purpose of every data field**, program structure, and most importantly the **business logic** (the step-by-step process).
  - **Visualizations:** **call graph** + **data lineage** (data inputs/outputs) to understand how the mainframe behaves.
- Nish summarizes: effectively **reverse-engineering COBOL into documentation** that can then be re-architected into a Java app.

#### 2) Mainframe → modern app (data layer first, then app)
- **Step 1 — modernize the data layer to native SQL:** a report **maps every mainframe data field → equivalent SQL field**, viewable in VS Code, with **table relationships** generated. At this stage you inject **business-requirement changes**, which **carry over** to the next step.
- **Step 2 — application transformation:** Importantly, this is **not just generating specs and feeding Copilot** — there's **built-in mainframe-modernization knowledge** so nuances of migrating *from a mainframe* are included. Output includes **setup instructions** (database setup, build) and a **native Java implementation** of the mainframe app as an **interim step**, which is then customized to the target requirements.

#### 3) The legacy estate (the "Zava Bank" sample app)
- Nish opens a typical **"Zava Bank"** app, in production "for 20–25 years," in VS Code. The repo is a **mixed portfolio**: a **Java Struts app** (early-2000s) with components like an **account/connection manager** and a **fraud detector**, plus **.NET apps** (with `web.config`, default files, **ASP.NET Web Forms**) — "a mix of all the apps in a portfolio."
- The **GitHub Copilot modernization agent in VS Code / Visual Studio** lets you start from the IDE: run **assessments**, do **runtime & framework upgrades**, **migrate to Azure (cloud-native)**, or start with **security issues (CVEs/CWEs)**.
- That works for a **single app/single developer**, but the real problem is **~20 applications** — hence the **CLI** at scale.

#### 4) Modernize CLI at scale (now GA)
- First shown a **JSON configuration file** listing **multiple projects/teams/repos** (GitHub repo URLs the architect can modernize).
- The **modernize CLI** offers commands for **assessment, planning, execution**, plus **upgrade** (technical debt at scale) and **model selection** (pick a model that fits the scenario, or the default).
- **Assessment flow:** start from the config file with exact repo URLs → confirmation prompt ("ready to modernize/assess all these?") → choose **assessment domains** (upgrades, cloud readiness, security) → choose **analysis coverage** from **issue-only to full analysis** (general insights, diagrams, API contracts) → optionally set **target Java/.NET runtimes** and **target compute services** for cloud readiness.
- **Local vs. cloud execution:** assess **locally** or **delegate to cloud agents** to work **in parallel at scale** (chosen here). Also supports **headless execution** so you can wire it into a **CI/CD pipeline** for a continuous loop.
- On execution it **clones the apps, sets up needed skills**, and surfaces an **assessment dashboard**. In **GitHub Agents HQ** you watch **multiple agents working in parallel**.
- Drill into a completed item → **view pull request** → **files changed**: includes **assessment overview, architecture documents, everything in markdown** — "the kind of documentation that takes months for a dev team," now produced by agents at scale.

#### 5) On-prem starting point — Azure Migrate handoff
- For orgs starting from **on-prem infrastructure / production code** (not code-first): a **seamless handoff between Azure Migrate and the GitHub Copilot modernization agent**.
- In **Azure Migrate**, central IT sees assessed apps and their infrastructure (e.g., web server = **IIS**). Choose **"add code insights to GitHub Copilot modernization"** → select **at-scale code assessment with automated report upload** → get a **config file** (similar to before but with extra Azure Migrate info + where to send the report back).
- Result: developers get reports in **GitHub**; IT gets reports back in **Azure Migrate storage**.
- A **consolidated HTML report** (shareable) shows: **issue summary**, all assessed apps, **wave-planning recommendations** (which apps to modernize first), **cost estimates** (based on **Azure retail pricing**; **usage-based billing** info planned), **portfolio overview**, **effort distribution by application**, **languages**, security findings (e.g., **hard-coded sensitive data / connection strings in `web.config`** → flag need for **Key Vault** in cloud), and **architecture diagrams**.

#### 6) Command Center (private preview)
- Announced as a **self-hostable portal** bundled with the modernize CLI (spun up via a command).
- Solves "we started modernizing but don't know where we are / who owns what." Provides a **dashboard** across phases (**how many apps assessed / planned / executing**), a **project timeline** (start, deadline, where agents are today), and **assess/plan/execute** detail.
- Assessments that previously ran on the **architect's machine** now **surface in the Command Center** so the **whole company can share reports**, **compare two assessment reports**, and make informed migration decisions. Same report content (CVE/CWE checks, etc.), different apps.

#### 7) Rulebooks (private preview)
- For org-specific **policies and guidelines** when modernizing to cloud. **"The agents now have rules too."**
- Created in the **Command Center** or the **modernize CLI**. Start by pasting a **markdown** file of rules/policies/guardrails (with plans to add more documentation sources to generate the rulebook).
- A generated rulebook includes a **charter / high-level principles** (e.g., **"cloud-native authentication must use DefaultAzureCredential"**), **security requirements**, **guardrails / hard boundaries** (things agents should *never* do), **observability requirements** (e.g., **OpenTelemetry**), and **approved SKUs** (e.g., **Azure Container Apps**).
- **Plan creation with rulebooks:** Nish creates an **execution plan** to rewrite the **Zava payment gateway from Struts → Java 21 (Spring Boot)** — a major rewrite — optionally including the **assessment report** and selecting the **rulebook**. A **plan document** is generated.
- **Cross-stack consistency:** compares **two completely different plans** — (a) **Struts → Spring Boot**, (b) **Web Forms → Blazer → Aspire on Azure Container Apps**. The plans differ by stack but **both honor the rulebook** (e.g., **OpenTelemetry implemented in both**).
- **Manual execution mode:** chosen so the developer keeps **full control** of code transformation. From the Command Center, manual mode **creates a GitHub issue** containing the **assessment, plan, and rulebook**, and **stages everything in a branch**. The developer pulls it into **VS Code**, reviews with architects, makes changes, and executes. The pasted markdown is **optimized for agents** and split into **specific structured files**.

#### 8) Custom skills (GA) — proprietary libraries/components
- For special internal libraries a generic coding agent wouldn't know to use. **Custom skills** let you inject company-specific knowledge.
- In VS Code's **skills library**, a **"manage repositories"** option lets you configure a **central repository** of organizational skills, then search and include them. Examples shown:
  - A **"Kafka → Azure Event Hubs"** custom skill (custom implementation, written like standard agent skills but with internal library/config details).
  - A **PII-handling** custom skill tied to the OpenTelemetry/logging rule — **ensures no PII is logged**.
- Running the (fast-forwarded) plan does a **complete rewrite Struts → Spring Boot**, and the transformed code shows evidence the agent **respected the customizations**: a **`PIIUtil`** (from the custom skill), the **Event Hubs** custom implementation, **Key Vault config** (from the rulebook), and — because the plan targeted Azure — generated **infrastructure-as-code** files to review and provision.

#### 9) .NET path — ASP.NET Web Forms → Blazer → .NET 10 → Aspire → Azure
- Opens an old **ASP.NET Web Forms** app (default files, `runat="server"` components).
- Start modernizing from the **Command Center plan** or **directly from the IDE**. Prompt: **"upgrade my project to .NET 10; my project has Web Forms."**
- Agent offers a **target framework (.NET 10)** and a **Blazer hosting model** (**Blazer Server** chosen), plus a **flow mode** — **automatic flow mode** chosen for **minimal prompts** ("I trust this agent for legacy modernization"). Work happens on a **separate branch** so nothing breaks.
- Output: the **Web Forms project is converted to Blazer**, **containerized**, with a log showing **`Microsoft.AspNetCore`** (the **new pipeline**, not the old ASP.NET pipeline).
- **Add .NET Aspire:** described as a **code-first layer** adding **orchestration and observability** — recommended for new cloud-native apps and far easier to maintain than Docker Compose files. Scaffolds an **app host for Aspire**; the **Aspire dashboard** shows **service discovery** and the **URLs of running services**. Aspire is **polyglot** — Java + .NET can coexist (the Java Bank had Java/.NET) and be managed in one place.
- **Deploy:** use the **Aspire CLI deploy command**, choose a **region**, and the app lands on **Azure Container Apps** with a live **application URL** — "a legacy Web Forms app brought to Blazer, Aspired, and deployed to the cloud."
- Aside: the agent could even modernize the **dated '90s UI** in a future modernization program ("probably add some emojis and fix it for you").

### Recap (Jeff)
The full set of expanded GitHub Copilot modernization capabilities:
- **Portfolio assessment & migration planning — GA.**
- **Custom skills — GA** — apply app-specific guidance + Azure best practices; **centralized skill library**; agents understand your architecture, dependencies, standards, and migration strategy **without hard-coding or forking the platform**.
- **Rulebooks — private preview** — centrally encode governance/security/architectural standards; **policies apply automatically to every plan**; agent **auto-generates a compliance report** for traceability.
- **Command Center — private preview** — one view of modernization across the portfolio: what's in flight / blocked / ready for review, with **auditability, clear ownership**, and the ability to scale execution — "enterprise oversight at agentic speed."
- **Expanded scenarios** — **mainframes, Aspire, and ASP.NET Web Forms** (Web Forms in private preview). For mainframes: **reverse-engineer COBOL into high-level + per-program documentation**, then **reimagine as a native Java app with the data layer in native SQL**, delivered **in partnership with mainframe modernization partners**.
- **Big idea:** not a one-size-fits-all refactoring engine, but a **governed, extensible system** reflecting how each organization modernizes at scale. "Modernization isn't a per-app assignment anymore — it's a landscape"; as customers strive to be **AI-ready, all layers of the estate must come along**, and **agents are how that happens**. Closing call: **"modernize in days, not months."**

### Customer proof & partners
- **Java — SAP Labs China** modernized Java apps at scale, reducing complications and saving significant time. **Dr. Richard Kai (SAP Labs China)** called the modernization agent **"an essential pillar of our modernization effort."**
- **.NET — Jordan Clay, Staff Platform Engineer at FMG:** GitHub Copilot modernization **"has completely changed how we think about .NET upgrades"** — fully automated, customized, cloud-driven upgrades that **"just work,"** making it **"the first tool any team should reach for."**
- **Internal Microsoft:** projects that took **weeks now done in a few hours**; **10,000+ engineering hours saved** across projects.
- **Mainframe modernization partners:** Amdocs, TCS, Infosys, Kyndryl, Accenture, Capgemini, Avanade, NTT Data, Sonata ("Sono"), and Hitachi.

### Closing / where to go next
Blog posts, a **private preview sign-up**, and a **virtual deep-dive event (~2 weeks out)** with hands-on guidance from the teams that built the tools (QR code on screen). Get started via the **GitHub Copilot modernization documentation**: `aka.ms/GHCP modernization`.
## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot modernization** — end-to-end agentic modernization system for developers/architects (IDE + CLI); ships with 60+ specialized skills.
- **Azure Copilot (preview)** — IT-ops-focused modernization in the Azure portal: discovery/inventory, topology & dependency mapping, ROI analysis, 6R wave planning, landing zones.
- **Modernization agent (GA)** — orchestrates parallel assessments & migration plans; automates Java and .NET Framework upgrades end-to-end from the CLI.
- **Modernize CLI** — command-line driver for assessment/planning/execution/upgrade; model selection; headless mode for CI/CD.
- **Custom skills (GA)** — reusable, centralized org-specific migration patterns/proprietary-library knowledge (e.g., Kafka→Event Hubs, PII handling).
- **Rulebooks (private preview)** — markdown-defined governance/security/architecture guardrails optimized into structured files; auto compliance reports.
- **Command Center (private preview)** — self-hostable portfolio dashboard (assess/plan/execute phases, timelines, ownership, auditability).
- **GitHub Agents HQ** — where parallel cloud coding agents are monitored.
- **Azure Migrate** — on-prem discovery/inventory; seamless config-file handoff to GitHub Copilot modernization; receives reports back.
- **.NET Aspire** — code-first orchestration + observability layer for cloud-native apps; polyglot (Java + .NET); Aspire dashboard (service discovery); Aspire CLI deploy.
- **Blazer (Blazor) Server** — target hosting model for migrated ASP.NET Web Forms apps. *(transcript auto-caption spells it "Blazer"; product is Blazor.)*
- **.NET 10** — target framework for the Web Forms upgrade demo.
- **Spring Boot / Java 21** — target for the Java Struts rewrite.
- **Azure Container Apps** — managed deployment target (approved SKU example in rulebooks).
- **Azure Key Vault** — recommended for secrets when moving connection strings off `web.config`.
- **DefaultAzureCredential** — rulebook principle for cloud-native authentication.
- **OpenTelemetry** — observability standard enforced via rulebooks.
- **Azure Event Hubs** — custom-skill migration target from Kafka.
- **Legacy/source technologies referenced:** COBOL, JCL, BMS screen maps, DB2, VSAM (mainframe); ASP.NET Web Forms, `web.config`, IIS; Apache Struts; VMware; Oracle; SQL Server; Windows/Linux workloads.
- **VS Code, Visual Studio, IntelliJ, GitHub** — supported developer surfaces.
- **Cloud Adoption Framework (CAF)** — landing zones aligned by Azure Copilot.
- **6R framework** — wave-planning model for migration disposition.
- **"Zava Bank"** — fictional sample legacy portfolio app used across demos.

## 🚀 Announcements / What's New
- **Modernization agent — Generally Available.** Scales assessments/upgrades across the portfolio from the CLI; **Java and .NET Framework upgrades automated end-to-end.**
- **Custom skills — Generally Available.** Centralized, reusable org-specific skills/library knowledge.
- **Portfolio assessment & migration planning — Generally Available.**
- **Command Center — Private Preview.** Self-hostable portfolio oversight dashboard.
- **Rulebooks — Private Preview.** Centralized governance/security/architecture guardrails with auto-generated compliance reports.
- **Mainframe modernization — newly introduced** as part of GitHub Copilot modernization (COBOL→docs→native Java + native SQL data layer), with partner delivery.
- **.NET Aspire support — expanded scenario.**
- **ASP.NET Web Forms modernization — Private Preview** (Web Forms → Blazor → .NET 10).
- **Azure Migrate ↔ GitHub Copilot modernization seamless handoff** (config-file bootstrap; bidirectional reports).
- **Roadmap signals:** usage-based billing for cloud-readiness cost estimates ("coming"); additional documentation sources to auto-generate rulebooks; a virtual deep-dive event ~2 weeks after Build.

## 💡 Demos
*(All pre-recorded "modernization journeys" on a demo machine, presented by Nish & Hassam.)*
- **Mainframe assessment & documentation** — Assessed a COBOL/JCL/BMS green-screen app via the modernize CLI; produced executive overview, personas, modules, architecture, user journeys, business processes/decision points, per-program detail (every data field's purpose + business logic), and call-graph/data-lineage visualizations. **Proves** agents can reverse-engineer opaque mainframes into shareable documentation *before* any code change — de-risking the journey.
- **Mainframe → native Java + native SQL** — Mapped every mainframe data field to SQL (viewable in VS Code with table relationships), allowed business-requirement injection that carries forward, then transformed to a native Java app using **built-in mainframe knowledge** (not just spec→Copilot). **Proves** the platform encodes domain-specific migration nuance, not generic codegen.
- **At-scale CLI assessment with parallel cloud agents** — From a JSON config of ~20 repos, ran multi-domain assessments (upgrades/cloud/security) with full analysis (diagrams, API contracts), delegated to cloud agents watched in GitHub Agents HQ, output as PRs containing markdown assessment/architecture docs. **Proves** "months of documentation" and portfolio-scale assessment now happen in parallel automatically.
- **Azure Migrate handoff** — Exported an on-prem assessment config from Azure Migrate (IIS-hosted apps) into the modernize CLI; produced a consolidated, shareable HTML report (issue summary, wave-planning recommendations, Azure retail-price cost estimates, effort distribution, security findings like hard-coded connection strings, architecture diagrams). **Proves** infra-first/IT-led starts integrate cleanly with developer-led code modernization, with reports flowing to both audiences.
- **Command Center** — Spun up the self-hostable portal showing assess/plan/execute phases, project timeline, and comparison of two assessment reports company-wide. **Proves** centralized visibility/ownership for large teams running many concurrent modernizations.
- **Rulebooks + cross-stack plans** — Generated a rulebook (DefaultAzureCredential, OpenTelemetry, approved SKUs, hard guardrails), then created two very different execution plans (Struts→Spring Boot/Java 21; Web Forms→Blazor→Aspire on Azure Container Apps) that **both honored the same rulebook**. **Proves** governance is enforced uniformly regardless of language/stack.
- **Manual execution → GitHub issue + staged branch** — Manual mode created a GitHub issue bundling assessment + plan + rulebook and staged a branch for review in VS Code. **Proves** human-in-the-loop control over actual code transformation.
- **Custom skills in a real rewrite** — A fast-forwarded Struts→Spring Boot rewrite produced code containing `PIIUtil` (PII custom skill), an Event Hubs implementation (Kafka→Event Hubs skill), Key Vault config (rulebook), and generated IaC for Azure. **Proves** the agent respects proprietary libraries + governance simultaneously.
- **.NET Web Forms → Blazor → .NET 10 → Aspire → Azure** — Upgraded an ASP.NET Web Forms app to .NET 10/Blazor Server in automatic flow mode on a separate branch, containerized (new `Microsoft.AspNetCore` pipeline), added Aspire (dashboard, service discovery, polyglot Java+.NET), and deployed to Azure Container Apps with a live URL via the Aspire CLI. **Proves** an end-to-end legacy-to-cloud-native journey for a notoriously hard stack.

## 📊 Notable Stats / Quotes
- **94%** of IT leaders rank app modernization as a top 6–12 month investment (Forrester Q1 2026).
- **87%+** of organizations agree they need all three of scale, customization, and governance (Forrester).
- **Over one-third** of modernization projects stall (complexity, resources, security).
- **76%** of developers live in VS Code / Visual Studio / IntelliJ / CLI / GitHub.
- **16M+** .NET and Java developers served.
- **60+** specialized skills out of the box.
- ROI: **70%** reduction in modernization time; **50%+** reduction in tech-debt effort; **88%** time/effort savings for **Xbox and Teams** internally; **10,000+** engineering hours saved internally; cross-customer reductions of **88 / 80 / 70 / 60%** in migration effort.
- *"Modernization by itself isn't the goal. It is what it unlocks."* — Jeff Fritz
- Tech debt *"grows kind of like a fungus and eats into the time you'd be spending on the AI-ready work."* — Jeff Fritz
- *"Before agents, this was hand-to-hand combat. A few apps at a time."* — on pre-agent modernization.
- *"An essential pillar of our modernization effort."* — Dr. Richard Kai, SAP Labs China.
- GitHub Copilot modernization *"has completely changed how we think about .NET upgrades… the first tool any team should reach for."* — Jordan Clay, Staff Platform Engineer, FMG.
- *"Modernization isn't a per-app assignment anymore. It's a landscape."* — Jeff Fritz.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Run the **modernize CLI** against a small mixed .NET/Java repo and inspect the generated assessment PR (markdown architecture docs).
- [ ] Things to try: Author a **rulebook** (DefaultAzureCredential + OpenTelemetry + approved SKUs) and confirm it applies across two different stacks.
- [ ] Things to try: Build a **custom skill** for an internal library and verify the agent references it in a transformation.
- [ ] Things to try: Test the **Web Forms → Blazor → .NET 10 → Aspire → Azure Container Apps** path on a throwaway legacy app.
- [ ] Things to try: Exercise the **Azure Migrate → GitHub Copilot** config-file handoff end-to-end.
- [ ] Questions: What's GA vs. private-preview availability/region gating, and what licensing/billing applies (usage-based billing timing)?
- [ ] Questions: How deep is mainframe coverage (COBOL dialects, CICS/IMS, beyond DB2/VSAM)? Which partners for the hybrid concierge?
- [ ] Questions: How are secrets/PII actually validated in transformed code — is the PII skill enforced or advisory?
- [ ] Questions: How self-hostable is the Command Center (infra footprint, auth, multi-team RBAC)?
- [ ] Relevant to: Azure/.NET modernization labs; any legacy ASP.NET Web Forms or Java Struts apps in the estate; AI-readiness planning.

## 🔗 Related
- [[Build2026]] (event index)
- `aka.ms/GHCP modernization` — Microsoft Learn entry point for GitHub Copilot modernization
- Topics: #topic/app-modernization #topic/github-copilot #topic/dotnet #topic/java #topic/mainframe #topic/azure
