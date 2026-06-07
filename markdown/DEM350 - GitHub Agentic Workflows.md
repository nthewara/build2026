---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/github
  - topic/github-copilot
  - topic/automation
  - topic/devops
source: https://www.youtube.com/watch?v=0XTyicuhdKE
session_code: DEM350
event: Microsoft Build 2026
speakers: Ari Lovignee, Alejandro Menocal
duration_min: 17
aliases:
  - GitHub Agentic Workflows
---

# DEM350 — GitHub Agentic Workflows: Automation That Actually Reads the Room

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ari Lovignee (Senior Learning Advocate, GitHub) · Alejandro Menocal (Senior Service Delivery Engineer, GitHub)  
> **Duration:** ~17 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=0XTyicuhdKE)

## 🎯 TL;DR
GitHub Agentic Workflows let you define repository automation in **Markdown instead of YAML**, then compile it into a runnable GitHub Actions workflow. Instead of brittle, syntax-heavy CI/CD, you describe what you want in natural language — and an AI agent (Copilot, Claude, Codex, or Gemini) executes the toil: triaging test failures, opening PRs, generating daily reports, or keeping content up to date. Security is enforced by giving the agent **read-only** access and routing all write actions through a separate post-run step called **"safe outputs,"** so the agent can never directly mutate your repo. The feature ships in **public preview the week after Build**, with a hands-on **GitHub Skills exercise** (a fictitious "Mona" Astro website kept current from GitHub blogs/changelogs) that anyone can run on their own handle.

## 🔑 Key Takeaways
- **Workflows-as-Markdown:** Author automation in `.md` files rather than learning Actions YAML; Copilot can even generate the Markdown for you.
- **Compile step → lock file:** The Markdown is *compiled* into a YAML **lock file**, which is the actual GitHub Actions workflow that runs. Markdown = human-controlled source; lock file = generated runtime artifact (both checked into the repo).
- **Model-agnostic agents:** The agent behind a workflow can be **Copilot, Claude, Codex, or Gemini** — pick the model that suits the task.
- **Security via least privilege + "safe outputs":** The agent gets only **read** access. Any write action (create issue, open PR) is performed by a *separate* post-agent step, segregating responsibilities so the agent can't hallucinate, delete code, or remove files.
- **Human stays in control:** Output lands as a **PR you review** (ideally peer-reviewed) before merge — you decide whether generated changes are useful or thrown away.
- **Self-scaffolding install:** Installing agentic workflows creates a PR that drops in the needed files under `.github/` — an **agent file** (defines the installed agent), a **skill**, and even an **MCP server** — so you start from a working framework, not from scratch.
- **Two-agent pattern:** There's a meta "agentic-workflows agent" whose job is to *help you build other agentic workflows* — it scaffolds new workflows using the bundled skill.
- **Familiar runtime:** Compiled workflows are "GitHub Actions on steroids" — run on a **schedule** or **on demand**, exactly like any Actions workflow.
- **Iterate like Copilot Chat:** You can refine the agent and the workflow over time (e.g. add directives such as "don't auto-compile," or business logic), and the step-by-step execution view mirrors Copilot Chat in the IDE.
- **Public preview ships the week after Build**, plus a deep existing **ecosystem** of prebuilt agentic workflows on a dedicated website.
- **Real use cases:** auto-fix CI/CD, triage/diagnose test failures, daily repo reports, dependency/stack version updates, and keeping a website current from upstream sources.

## 📚 Detailed Notes

### The problem: CI/CD is rigid and full of toil
Traditional automation/CI is **very rigid** — it depends on exact YAML syntax, and when there are syntax errors they're hard to identify. Day-to-day, developers shoulder a lot of **mundane, repetitive toil** on their repos. The pitch for agentic workflows is to *automate that toil* (test-failure triage, issue creation, daily repo reports, opening PRs) while making the authoring experience far more forgiving.

### What Agentic Workflows are
- You **define workflows in Markdown** rather than Actions YAML. You can even use **Copilot to generate the Markdown** files.
- Those Markdown files are **compiled into an agentic workflow**.
- Behind each workflow sits an **AI agent + model**. Supported models called out: **Copilot, Claude, Codex, Gemini** (and "any of the models").
- The agent can **dynamically diagnose test failures**, **open PRs** to make changes, or **update your stack** and give recommendations.
- There is already a **deep ecosystem** of different agentic-workflow types, with a **dedicated website** to browse them.

### Security model — least privilege + "safe outputs"
This was emphasised as the core differentiator:
- For agentic workflows to be secure, the **agent itself is given only read access** to the repository.
- All **write actions** are handled by a mechanism called **"safe output"** — a step that runs **after the agent finishes**. That post-run step is what actually holds the permission to perform the action (create an issue, create a pull request, etc.).
- This **segregates responsibilities**: the agent never has broad write access, so it "can't hallucinate or delete your code base or remove files."
- Net effect: the automation does the heavy lifting, but **you remain in control** — you decide whether the generated result is useful or discard it. When compiling, write permissions on `contents` are explicitly rejected ("write is not allowed… use safe output create-issue to perform write"), forcing the safe-output pattern.

### The Skills exercise: keeping the "Mona" website current
The demo is delivered as a **GitHub Skills exercise** you can take on your own handle:
- A **fictitious "Mona" website** (a basic **Astro** site) is tasked with surfacing the latest GitHub updates.
- Sources it watches: GitHub **blogs**, **changelogs**, and **notes written in the repo** itself.
- On a chosen **frequency**, the workflow pulls updates and produces a **PR** showing proposed changes. You can merge directly, but ideally **peer-review** with teammates first, then merge.
- The static site initially showed a date of **March 17th** (when the exercise was first built) — the whole point of the agentic workflow is to keep that content fresh automatically as new announcements land (e.g. the GitHub Copilot features/agents announced at Build would be pulled from the blog/changelog). The same pattern applies to **out-of-date stack versions** in your repo → auto-PR with updates.

### Install → scaffold (what gets created)
Because a full run takes longer than the session slot, the presenters had **pre-started** the process. Installation flow:
- Running an install command **creates a PR** that initializes the repo and sets up completions.
- The PR drops files under the **`.github/` directory**, including:
  - the **Markdown** workflow file,
  - an **agent file** (labeled "agentic workflows") that **describes the installed agent** — analogous to a custom agent / cloud agent that normally lives in your repo,
  - a **skill** installed as part of agentic workflows,
  - an **MCP server** (installed as part of the package).
- It also pre-populates things like the **Copilot setup steps** automatically, so you don't start from scratch — you get a framework to **build business value on top of** (e.g. auto-fix CI/CD, auto-update your website). The setup is "self-contained, already ready to go" scaffolding.

### Using the agent to author a new workflow
- They **merge the install PR** to see it in action, then **pick the "agentic-workflow agent"** and give it directions to create the workflow.
- Directions given to the agent (natural language):
  - ensure you're on the **latest `main`** branch,
  - **create a new branch**,
  - **update the info file** used by the website so it pulls the latest GitHub updates from the **blog, changelog, etc.**,
  - then **create the workflow file** — and **compile** it.
- Key nuance: the agent **sometimes auto-compiles**, but the team deliberately added an instruction to **show the compile step explicitly**. You can also add standing directives to the agent (e.g. compile behavior) so it always does specific things for your workflows.
- The execution view shows each step (prepare → generate file), and **looks just like Copilot Chat in the IDE**.
- Conceptually: this **meta-agent's job is to help create other agentic workflows** — it uses the **bundled skill** (from the scaffold) to generate the *new* workflow that updates the website.

### Anatomy of the generated workflow file
- The produced file (e.g. `update-github-info.md`) is the **agentic workflow**, and it's **very basic**.
- It has **front matter** at the top: this is the compiled-down, structured form of the **natural-language directions** you gave (when it runs, what access is granted, tools allowed, safe-output target, etc.).
- Front-matter fields seen/edited during the demo included: **schedule**, **`tools` allowed**, **`site-contents`**, **`safe-output` → assigned to user**, **`web-fetch`/`edit`**, and **permissions on `contents`**.

### The compile step and the lock file
- Because the source is "just a Markdown file," you must **compile** it so it **generates a YAML file — called a lock file** — that tells Actions exactly what to do.
- **Lock file = the actual Actions workflow that runs.** The **`.md` file = the natural-language, human-controlled, checked-in source.** The lock file is **generated as part of compilation.**
- Compilation enforces the **security guardrails**: the demo hit errors where the compiler **rejected `contents: write`** ("write is not allowed for secret… use safe output create-issue to perform write"), and flagged the word **"allowed"**. Fix was to change **`contents` to `read`** and keep **write only where legitimately needed** (e.g. pull-request permission), then **re-compile**. After tweaking the front matter, the file submits and the lock file is generated.

### Runtime & iteration
- Once compiled, it runs like **any GitHub Actions workflow** — on a **schedule** *and* **on demand** (they asked it to support both). "GitHub Actions kind of on steroids."
- Just like anything with Copilot/agents, you can **iterate**: add comments/directives (e.g. a "complete" comment telling it **not** to compile), modify the agent to work better for you, or modify other pieces of the workflow you've created.

### Try it yourself
- A **QR code / link** points to the **GitHub Skills exercise** so attendees can run it on their own GitHub handle, modify it, and learn the mechanics firsthand. The team will keep **iterating and improving** the exercise.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Agentic Workflows** — define repo automation in Markdown; compiled into runnable Actions workflows driven by an AI agent. (Core subject of the talk.)
- **GitHub Actions** — the underlying CI/CD runtime; compiled lock files are standard Actions workflows.
- **GitHub Copilot** — AI agent option; also used to generate the Markdown workflow files; setup steps auto-scaffolded.
- **Claude / Codex / Gemini** — alternative model/agent options selectable behind an agentic workflow.
- **"Safe outputs"** — post-agent step that holds write permissions and performs actions (create issue, create PR), enforcing least-privilege security.
- **Lock file** — the YAML Actions workflow generated by compiling the Markdown source.
- **Agent file** — file under `.github/` describing the installed agent (custom/cloud-agent style).
- **Skill (bundled)** — installed with agentic workflows; the meta-agent uses it to author new workflows.
- **MCP server** — installed as part of the agentic-workflows package.
- **GitHub Skills** — the interactive, exercise-based learning platform delivering the hands-on lab.
- **Astro** — static-site framework used for the demo "Mona" website.
- **GitHub Blog / Changelog** — upstream content sources the workflow pulls from to keep the site current.
- **Markdown front matter** — structured config block at the top of the workflow file (schedule, tools allowed, permissions, safe-output target, etc.).

## 🚀 Announcements / What's New
- **Public preview the week after Build** — GitHub Agentic Workflows will be released in **public preview "next week,"** so attendees can use it themselves.
- **GitHub Skills exercise available** — a self-serve, hands-on exercise (the "Mona"/Astro website use case) reachable via a session QR code/link; the team will keep iterating on it.
- **Existing ecosystem** — a dedicated **website** already catalogs many prebuilt agentic-workflow types to browse and adopt.
- *(Status note: this was a demo/enablement session — preview was the explicit release milestone called out; no GA date was given.)*

## 💡 Demos
- **Install & scaffold:** Ran the install command → it created a PR initializing the repo and adding the Markdown workflow, an **agent file**, a **skill**, an **MCP server**, and pre-built **Copilot setup steps** under `.github/`. **Proved:** installation is self-contained scaffolding — you start from a working framework, not a blank page.
- **Authoring a workflow with the agent:** Selected the **agentic-workflow agent** and gave natural-language directions (use latest `main`, new branch, update the website info file from blog/changelog, create + compile the workflow). It generated `update-github-info.md`, with execution steps mirroring Copilot Chat. **Proved:** you can build automation in plain language; an agent scaffolds and writes the workflow for you.
- **The website target:** Showed the basic **Astro** "Mona" site displaying a static **March 17th** date. **Proved:** the workflow's job is to keep such content auto-updated from upstream GitHub sources via a reviewable PR.
- **Compile → lock file + security guardrails (live troubleshooting):** Compiling the Markdown surfaced errors — the compiler **rejected `contents: write`** and the word "allowed," instructing the use of **safe-output create-issue**. They fixed the front matter (`contents` → `read`, keep write only where appropriate) and re-compiled to generate the **lock file**. **Proved:** (1) the Markdown→YAML lock-file compile step is real and required; (2) the **least-privilege / safe-output security model is enforced at compile time**, not just advisory.
- *(Candid note: the live demo was time-pressured and bumpy — a window was accidentally closed and front matter needed several tweaks — but the end-to-end flow and guardrails were demonstrated.)*

## 📊 Notable Stats / Quotes
- **"GitHub Actions kind of on steroids with the agentic workflows."** — on how compiled workflows relate to plain Actions.
- **"So it can't hallucinate or delete your code base or remove files from your repository. It's always going to be where you're in control."** — on the safe-outputs / least-privilege security model.
- **"This is where you add basically the business value of what you want to build."** — the scaffold handles boilerplate; you supply the intent.
- Compiler guardrail message paraphrased live: **"write is not allowed for [contents]… use safe output create-issue to perform write."**
- Website static date stamp: **March 17th** (date the exercise was first authored), illustrating the staleness the workflow fixes.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Run the **GitHub Skills "agentic workflows" exercise** on my own handle (Mona/Astro site) once public preview lands the week after Build; inspect the generated `.github/` files (agent file, skill, MCP server, `.md` + lock file).
- [ ] Things to try: Build a real agentic workflow for one of my repos — e.g. **auto-PR for out-of-date dependency/stack versions**, or **daily repo report / test-failure triage**.
- [ ] Things to try: Experiment with swapping the backing model (**Copilot vs Claude vs Codex vs Gemini**) for the same workflow and compare results.
- [ ] Questions: What exact **safe-output action types** are supported (create-issue, create-PR — others)? Where's the canonical docs/website for the agentic-workflow ecosystem and front-matter schema?
- [ ] Questions: How does the **compile/lock-file** step fit into branch protection and PR review — is the lock file regenerated on every change, and how are drifts between `.md` and lock file handled?
- [ ] Questions: How are **secrets and tool allow-lists** scoped per workflow, and what's the blast-radius if an MCP server is added?
- [ ] Relevant to: Automating repo toil across my Azure/GitHub projects; CI/CD modernization; reducing manual changelog/dependency upkeep.

## 🔗 Related
- 
