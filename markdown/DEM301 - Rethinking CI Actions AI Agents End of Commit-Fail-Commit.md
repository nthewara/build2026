---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ci-cd
  - topic/github-actions
  - topic/agents
  - topic/devops
source: https://www.youtube.com/watch?v=Mt11hZql5Kc
session_code: DEM301
event: Microsoft Build 2026
speakers: Cil (Product Manager, GitHub), Dennis (Product Manager, GitHub)
duration_min: 23
aliases:
  - Rethinking CI Actions AI Agents End of Commit-Fail-Commit
---

# DEM301 — Rethinking CI: Actions, AI Agents, and the End of Commit-Fail-Commit

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Cil — Product Manager, GitHub (presenter/driver) · Dennis — Product Manager, GitHub (co-presenter, supporting)  
> _(Both names are auto-caption transcriptions; "Cil" in particular is caption-uncertain. Dennis is also referred to once as "Denzon," likely the same person.)_  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=Mt11hZql5Kc)

## 🎯 TL;DR
GitHub Actions usage is exploding (550M → 850M jobs/week in 2026, much of it AI/agent-driven), and a recurring pain point is the **"commit-fail-commit" loop** — endlessly adding print statements, re-committing, and re-running just to figure out why a workflow failed or behaved oddly. This demo-heavy session shows two emerging tools that break that loop: (1) **Agentic Workflows** — markdown-authored workflows infused with agent logic, demonstrated via a pre-built **"CI Doctor" / "CI Failure Doctor"** template that auto-triggers on workflow failure, performs root-cause analysis, and files a GitHub issue with diagnosis and fix suggestions (going to **public preview next week**); and (2) a **sneak-peek Actions Debugger** — a real interactive debugger that connects to the live Actions runner over the **Debug Adapter Protocol (DAP)**, letting you inspect variables/contexts, run shell commands on the runner, and diagnose strange-but-passing workflows without any commit churn (still internal, no release date, gated on security).

## 🔑 Key Takeaways
- **Actions usage is accelerating massively**: ~2.8M jobs/week in early Jan, 550M/week at the start of 2026, 850M/week by early May — roughly a **60% jump in a few months**, driven heavily by AI and agents (though CI remains the primary use case).
- The **commit-fail-commit cycle** is the core problem being targeted: commit → run → something looks off → add a print statement → re-commit → re-run → repeat until you stumble onto the cause. It's slow and frustrating.
- Two complementary solutions: an **agent-based diagnostic** (good when there's clear failure data) and an **interactive runner debugger** (good when the workflow *succeeds but behaves wrong*).
- **Agentic Workflows** let you author workflows in **markdown** (expressing intent in natural language) instead of writing raw Actions YAML by hand; a compile step turns the markdown into runnable YAML.
- The **CI Doctor / CI Failure Doctor** is a pre-built agentic workflow template that **auto-triggers when a specified workflow fails**, runs an agent to do **root-cause analysis**, and opens a **GitHub issue** with the diagnosis, the offending data, and concrete fix suggestions — all in the background, no manual trigger needed.
- Agentic workflows are **fully customizable**: you can edit the markdown prompt directly, and you can use **Copilot to help write/modify** that prompt (e.g. the presenter added a custom `/slash` command protocol to feed the CI Doctor extra info mid-investigation).
- The authoring flow uses the **`gh aw` GitHub CLI extension** (`gh aw compile`) which compiles the markdown into a **`.lock.yml`** Actions file — deliberately named `.lock.yml` to distinguish agentic from traditional (non-agentic) workflows. You recompile whenever the markdown changes and commit the result.
- Agentic workflow files are **just files in your repo** — shareable across teammates and repos like any other file; recipients can recompile and/or further customize them.
- GitHub ships a **growing library of pre-built agentic workflow templates** (CI doctor, issue triage, PR triage, automatic/continuous documentation, continuous improvement, multi-repo coordination) addable via a wizard.
- Issues filed by the CI Doctor can be **assigned to a coding agent** (which starts a session and attempts the fix) or assigned to a human teammate — closing the loop from detection → diagnosis → remediation.
- The **Actions Debugger** is a genuine interactive debugger for **GitHub-hosted runners**, built on the **Debug Adapter Protocol (DAP)** so it works with any DAP-capable client (VS Code shown; the lead engineer uses Neovim).
- With the debugger you can **inspect the full GitHub context, environment variables, and (redacted) secrets**, **step through workflow steps**, and **run arbitrary shell commands directly on the runner** to test hypotheses live — no print-statement churn.
- **Availability:** Agentic Workflows → **public preview next week** (search "GitHub Agentic Workflows"). Actions Debugger → **internal/unreleased, no date**, held back specifically over **security/abuse concerns** because it grants direct runner access.

## 📚 Detailed Notes

### The problem: the "commit-fail-commit" loop
GitHub Actions adoption has been climbing at an unprecedented rate. The presenters cite concrete numbers: at the very beginning of January 2026 they were running ~**2.8 million jobs per week**; by the start of 2026 (the year) that was **550 million per week**; and just a month earlier (early May) it was **850 million per week** — described as nearly a **60% increase in only a few months**. A lot of the growth comes from AI and agents, but **CI remains the primary way people use Actions**.

The recurring friction users hit is the **commit-fail-commit cycle** (also said as "fail-commit, fail-commit"). The pattern: you commit a change, run a workflow, and something looks off — maybe it outright **fails**, or maybe it **succeeds but looks weird/wrong**. The only tool most people have is to make a small change (add a `print` statement, tweak something), **re-commit, re-run**, and keep iterating until they eventually break out of the loop by luck or persistence. A show of hands in the room confirmed it's a widely shared pain. The session presents **two ways to break out of this loop faster**:
1. An **agent-based solution** — using **agentic workflows** to let AI diagnose problems automatically when they arise.
2. An **Actions Debugger** (sneak peek) — to dig *inside the runner itself* to troubleshoot.

### What Agentic Workflows are
**Agentic Workflows** are a way to create an Actions workflow but **infuse agent logic into it**. Instead of hand-writing Actions YAML, you **author in markdown** — you express *what you want to do* in natural language markdown, and the system turns that into Actions YAML. A given agentic workflow file contains a small amount of **traditional YAML** (triggers/config) plus a body that is **mostly markdown** (the agent's instructions/prompt).

The presenter polled the audience — a good number had heard of and were using Agentic Workflows already, so they're gaining traction.

### Demo 1 — The CI Doctor diagnoses a failing workflow
The starting point is a **standard (non-agentic) Actions workflow**: it runs a Python script that reads a handful of files (each just a bunch of **key/value pairs**), sums them up, and returns a value. The presenter runs it and it **fails** — the Python error is essentially *"cannot concatenate string"* (a `TypeError` from mixing strings and integers).

The key move: going back to the list of workflow runs, there's a second workflow that fired **right after** the failure — the **"CI Failure Doctor"**, which is an **agentic workflow**. It's configured to **trigger automatically any time** a specified workflow (here, the "demo sum key counts from files" workflow) **fails**. When that happens it runs an agent that **analyzes what happened**, produces **root-cause analysis**, and suggests solutions.

Looking at the file backing it, you notice something distinctive about agentic workflows: instead of a plain workflow YAML file you see the **agentic workflow (markdown) file**. Opening it reveals a little traditional Actions YAML up top, then mostly markdown — e.g. *"You are the CI failure doctor. You are investigating failed GitHub Actions to identify root causes and patterns,"* followed by a lot of detailed instructions on **how to do the analysis, what steps/components to return, and how to work through the problem**.

This CI Doctor is one of several **pre-built templates** GitHub provides (findable online, addable via a **wizard**): CI doctor, **issue triage**, **PR triage**, **automatic documentation**, and others — including this one tuned to **identify and resolve open issues**.

**Customization (Q&A):** Yes, it's just an `.md` file you can edit freely, and editing it changes the behavior. Beyond hand-editing, you can use **Copilot to help build and edit the prompt**. The presenter, noticing the agent was producing some odd results, used Copilot to **add a custom `/slash` command protocol** so they could feed the CI Doctor **additional information mid-investigation** to steer it.

### From markdown to a runnable workflow: `gh aw compile` → `.lock.yml`
Q&A continues on what physically happens to the `.md` file. The flow:
- You put the `.md` file into your repo.
- You install **`gh aw`** — **"AW" is the Agentic Workflows extension for the GitHub CLI**.
- You run **`gh aw compile`**. This validates and may emit **warnings** (in the demo it warned that the workflow should be **restricted to the `main` branch** — the presenter had removed that restriction just for the demo).
- Compilation turns the markdown into an **Actions YAML file** that isn't really human-readable but that Actions knows how to execute. The output is committed as a **`.lock.yml`** file. The name `.lock.yml` was deliberately chosen to **differentiate agentic workflows from non-agentic ones** (since many people will still have traditional workflows).
- Whenever you change the markdown, you **recompile** and commit the regenerated lock file. (In the demo, since it was already compiled, recompiling added nothing.)

Mental model the co-presenter summarized: *"As a human I start with MD; the agentic-workflows process lets me convert that into an actual workflow — it converts to a `.lock.yml`."*

### Sharing agentic workflows across teammates and repos (Q&A)
Because agentic workflows are just files, you can **share any agentic workflow you've defined** with anyone in your org/repos exactly like any other repo file. Teammates can then **further customize it or just recompile it** and add it to their own workflows. They behave like any other file/workflow you work with. GitHub itself is **building more and more of these agentic workflows** to solve common problems it keeps seeing, and is continuously **adding to and iterating on** them.

### The CI Doctor's output: an investigation issue + agent assignment
When the CI Failure Doctor finishes, it pops up a **"CI Failure Investigation"** issue. In the demo it reports the failure was a **`TypeError`** because a particular file (referred to as "counts 13") contained **string values instead of integer values** — which is correct, since the presenter **deliberately introduced** that error to force the failure. The issue:
- Explains *why* it failed (strings instead of integers).
- Notes that the summing function **isn't doing any type casting**.
- Provides **suggested actions** — here, **adding a casting operation** to force the values to integers even when they're strings, plus adding a **data validation step** to the workflow.

From the filed issue you can then **assign it to a coding agent**, which **starts a session and attempts to fix all the errors** automatically. Alternatively you can **assign it to a human** teammate (the presenter jokes about assigning it to "Denzon"/Dennis to take a crack at it). The `/slash` customization also lets you **inject more context** into the issue once you've spotted an additional root cause, speeding things up — once you know the problem, you just assign it to an agent and it handles the fix.

**End-to-end recap (co-presenter):** An automated agentic workflow was **triggered by an event** (CI failing). The CI Doctor agentic workflow **immediately kicks off**, **produces an issue** for you to review, and you **didn't have to trigger anything yourself** — it all runs in the background.

### Where agents aren't enough: workflows that *succeed but misbehave*
The CI Doctor shines when a workflow has **failed with obvious data to diagnose**. But a nastier class of problem is when the **workflow doesn't fail — it succeeds, but in a strange way**; something doesn't add up. In those cases an agentic workflow surfacing information **might not be enough** — you need to **start rooting around** in the actual execution. That motivates the second tool.

### Demo 2 — The Actions Debugger (sneak peek)
**Setup:** There's an open **PR** with a workflow that runs on the PR. The workflow is supposed to **identify all the markdown (`.md`) files modified by the PR** and **add links to them in the PR description**, so reviewers can jump from the PR straight to a **well-rendered version** of each changed doc. (The team uses this on their own workflow because they write many docs in markdown.) So far one file, **`page two`**, has been added.

The presenter switches to **VS Code**, copies `page two` to create **`page three`**, makes a small edit, saves, commits, and pushes. Back on the PR, the workflow reruns — but instead of linking **both** `page two` and `page three`, it **only shows `page three`**. That's unexpected: the workflow **succeeded but produced the wrong result** — exactly the strange-but-passing scenario.

**The old way:** add a bunch of print statements, open the workflow, guess at the problem, iterate — slow.

**The debugger way:**
1. Open the workflow run / job and choose **Re-run**. (Normally you'd "re-run with debug logging," but instead you **enable the debugger**.) Note: this is **not released yet — still internal**.
2. The job kicks off and shows **"waiting for debugger client to connect."**
3. **Copy the link to the job**, go to VS Code, and run **`gh ... debug running job`** (paraphrased as a GitHub command), part of a **slightly modified version of the GitHub Actions extension**, pasting in the job. Within a second the client **connects to the running job**.

**Why DAP:** The debugger uses the **Debug Adapter Protocol (DAP)** — a **standardized protocol used by many debuggers** for debugging different applications. It was chosen because it lets you **tightly integrate with debuggers**, and crucially means **any DAP-supporting client works**. VS Code is the presenter's choice, but the **lead engineer prefers Neovim and does all of this in Neovim**; lots of DAP integrations exist and it's easy to add.

**What you can do once connected** (you're attached to the **runner's compute**):
- **Run commands directly on the runner** — e.g. `ls` to list files. *"You can run commands on the runner itself... that's the whole point of this."*
- In the debugger's **variables panel**, inspect all **context information**: open the **GitHub context** to see its values, view defined **environment variables**, and see **which secrets are defined** — though **secret values are redacted** (you can see that a secret exists, not its contents).
- **Step through the workflow steps.** The first two steps (checkout repo, set up Python) are unlikely culprits, so they're skipped over.

**Finding the bug:** The relevant step is **"collect changed files,"** which creates a **temp directory** and does a **`git diff` between two commits**, writing the result out to a value. Inspecting the variables:
- **HEAD sha** = `309c9…` — checking the PR, that matches the PR head. ✅
- **base sha** = `a07ff…` — but that's the commit **right before** the PR head, i.e. the workflow is **diffing the last two commits of the PR**, not the PR against `main`.
- The **actual head of `main`** is something **completely different**.

So the workflow is doing a **bad comparison** — comparing the PR's last two commits instead of PR-vs-base, which is exactly why only `page three` (the most recent commit's change) showed up and `page two` didn't. The two values set via environment variables are **wrong**.

**Verifying the fix live (without committing):** Rather than guess, the presenter hunts for the correct base sha *inside the runner*:
- Look in the **GitHub context → event context → `pull_request`**, which has a **`base`** object, which has a **`.sha`** — value `b49a57…`, which matches the real base. ✅
- To double-check before changing code, **run the command directly on the runner**: `git diff --name-only <base> <after>`, pasting in the correct base sha and the **`after`** sha (pulled from context). Because that particular base var isn't set, it's done **manually**, but that's manageable.
- Running it now returns **both files** — confirming the fixed comparison is correct.

From here you could **step through every remaining step**, inspect all values, regenerate the files, and even run all the steps at the end — but the problem is already understood. The presenter can now **go back, make the one change, commit, and be done** — *"the debugger has told me exactly where I was looking for. I didn't have to commit a bunch of stuff, do print statements, or add extra steps."* You **jump in, do some research, find what you need, make the change, commit — done.**

**Recap (co-presenter):** It's a **real debugger for the runners** — you can jump in, play around, run commands, and inspect everything **within the context of any DAP-accepting client**. DAP is designed for debugging, so it handles **stepping over** and **returning/inspecting variables** natively.

### Availability, security posture, and feedback
- **Agentic Workflows → public preview next week.** Search **"GitHub Agentic Workflows"** online to find the preview site, which includes a **CLI quick-start** and **many examples** (issue management, **continuous documentation**, **continuous improvement**, with **multi-repository coordination** in progress).
- **Actions Debugger → still internal, no release date.** It was shown only as a sneak peek of what the team is building. Because it allows **direct access to your runners**, the team is **very concerned about security and abuse** and is spending **extra time** ensuring the **appropriate level of protection** so teams get maximum value **without opening security holes**. No date because **security is paramount**, but they wanted to show it because it's compelling.
- **Feedback strongly requested** on both agentic workflows and the debugger via **GitHub's public forums** — it's the best channel for the team to track. For agentic workflows especially (actively iterated, public preview next week), feedback and **use-case stories** are valuable because they let GitHub **build more pre-built agentic workflows** to accelerate users' processes.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Actions** — CI/CD automation platform; the subject of the whole talk; usage scaling to ~850M jobs/week.
- **Agentic Workflows** — Actions workflows authored in **markdown** with embedded agent logic, compiled to runnable YAML; going to public preview next week.
- **`gh aw` (Agentic Workflows CLI extension)** — GitHub CLI extension for agentic workflows; **`gh aw compile`** turns the markdown into a `.lock.yml` Actions file.
- **`.lock.yml`** — the compiled, machine-readable Actions YAML output of an agentic workflow; the `.lock` suffix distinguishes agentic from non-agentic workflows.
- **CI Doctor / CI Failure Doctor** — pre-built agentic workflow template that auto-triggers on workflow failure, does root-cause analysis, and files a diagnosis issue with fix suggestions.
- **Pre-built agentic workflow templates** — library including issue triage, PR triage, automatic/continuous documentation, continuous improvement, and (in progress) multi-repository coordination; addable via a wizard.
- **GitHub Copilot** — used to help author/edit the agentic workflow markdown prompt (e.g. adding the custom `/slash` command protocol).
- **GitHub coding agent / issue assignment to an agent** — a CI Doctor issue can be assigned to an agent that starts a session and attempts the fix automatically (or assigned to a human).
- **Actions Debugger** (unreleased, internal) — interactive debugger that attaches to a live GitHub Actions runner to inspect state and run commands.
- **Debug Adapter Protocol (DAP)** — the standardized debugging protocol the Actions Debugger is built on; enables any DAP-capable client to connect.
- **GitHub Actions VS Code extension (modified)** — provides the `gh ... debug running job` command used to attach the debugger to a running job.
- **VS Code** — the presenter's DAP client of choice for the debugger demo.
- **Neovim** — the lead engineer's DAP client of choice; cited to show DAP client-agnosticism.
- **Python** — language of the demo CI script (reads key/value files and sums values; failed with a `TypeError`).
- **`git diff` (`--name-only`)** — the comparison the "collect changed files" step runs; the bug was a wrong base/head sha pairing.

## 🚀 Announcements / What's New
- **GitHub Agentic Workflows → public preview "next week"** (relative to Build 2026). Preview site (search "GitHub Agentic Workflows") includes CLI quick-start and examples; multi-repository coordination is actively being built.
- **GitHub Actions Debugger → previewed as a sneak peek; NOT released, no date.** Still an internal project; release gated on security/abuse hardening because it grants direct runner access.
- Ongoing: GitHub is **continuously adding new pre-built agentic workflow templates** for common problems.

## 💡 Demos
- **CI Doctor on a failing workflow:** A standard Python Actions workflow was made to fail with a deliberate `TypeError` (strings where integers were expected). The **CI Failure Doctor** agentic workflow **auto-triggered on the failure**, ran an agent, and **filed a "CI Failure Investigation" issue** correctly identifying the bad file, explaining the missing type casting, and suggesting fixes (add casting + a data-validation step). Demonstrated that the issue can then be **assigned to a coding agent** to auto-fix. *Point proved:* failures can be diagnosed and routed to a fix **automatically, in the background, with zero manual triggering** — replacing the first half of the commit-fail-commit loop.
- **Authoring + compiling an agentic workflow:** Showed the CI Doctor's underlying **markdown file** (the `You are the CI failure doctor…` prompt + a little YAML), live use of **Copilot to add a custom `/slash` command protocol** to the prompt, and **`gh aw compile`** turning the markdown into a committed **`.lock.yml`** (including a warning to restrict it to `main`). *Point proved:* agentic workflows are human-authorable, AI-assisted, customizable, and shareable like any repo file.
- **Actions Debugger on a strange-but-passing workflow:** A PR workflow meant to link all modified `.md` files in the PR description **only linked `page three`, not `page two`** — succeeded but wrong. The presenter **re-ran with the debugger enabled**, attached from **VS Code over DAP** (`gh … debug running job`), inspected the **GitHub context / env vars / (redacted) secrets**, and found the **"collect changed files"** step was diffing the **PR's last two commits** (wrong base sha `a07ff…`) instead of PR-vs-base. They located the correct base sha (`b49a57…`) in the **`pull_request.base.sha`** context, **ran `git diff --name-only` directly on the runner** to verify it returned **both files**, then concluded they could fix-commit once and be done. *Point proved:* you can fully diagnose runner behavior **interactively, without commit/print-statement churn** — killing the second half of the loop.

## 📊 Notable Stats / Quotes
- **Actions job volume:** ~**2.8M jobs/week** (early Jan) → **550M jobs/week** (start of 2026) → **850M jobs/week** (early May) — *"a 60% increase almost in only a few months."*
- *"The end of fail-commit, fail-commit"* — the framing for breaking the commit-fail-commit loop.
- *"You are the CI failure doctor. You are investigating failed GitHub Actions to identify root causes and patterns."* — the CI Doctor agentic workflow's opening prompt.
- *"You can even run commands on the runner itself… that's the whole point of this."* — on the Actions Debugger.
- *"The debugger has told me exactly where I was looking for. I didn't have to commit a bunch of stuff, do a whole bunch of print statements… I jumped in, I did some research, and I was able to find what I need. I can make my change, commit, I'm done."*
- *"Given that this is allowing direct access to your runners, we are very concerned about security and abuse…"* — on why the debugger is unreleased.
- **`.lock.yml` naming:** *"We just put `.lock.yml` because we wanted something to differentiate between non-agentic workflows."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **`gh aw`** CLI extension and add the **CI Doctor** template (via the wizard) to a test repo; deliberately break a workflow and watch it file a diagnosis issue.
  - Try the broader template set — **issue triage, PR triage, continuous documentation, continuous improvement** — and see which map to real repo pain.
  - Author a custom agentic workflow from scratch in markdown, then **use Copilot** to refine the prompt; practice the **`gh aw compile` → `.lock.yml` → commit** loop.
  - Experiment with the **issue → assign to coding agent** handoff to see how well auto-fix performs on real failures.
  - Watch for the **Actions Debugger** preview; if it ships, try the **DAP attach from Neovim** path (not just VS Code).
- [ ] Questions:
  - What are the **security guardrails** the team is building for direct runner access (who can attach, on which branches/repos, audit logging, time limits)?
  - How are **secrets redacted** in the debugger's variable view, and can that be bypassed — what's the threat model?
  - What does **multi-repository coordination** for agentic workflows look like in practice, and when does it land?
  - What **model(s)** power the CI Doctor agent, and how are token/compute costs of auto-triggering on every failure managed at scale?
  - Does the `.lock.yml` need to be **kept in sync manually** (recompile on every markdown edit), or is there CI enforcement to prevent drift?
- [ ] Relevant to:
  - Any team on **GitHub Actions** fighting flaky/opaque CI or the commit-fail-commit loop.
  - DevOps/platform engineers standardizing **reusable, AI-assisted CI diagnostics** across repos.
  - Anyone evaluating **agent-in-the-loop CI/CD** patterns (auto-triage → auto-fix) and the governance around agent runner access.

## 🔗 Related
- [[DEM350 - GitHub Agentic Workflows]] — deeper/companion coverage of the same Agentic Workflows feature from Build 2026.
- Microsoft Build 2026 — GitHub Actions / Copilot coding-agent sessions (CI/CD + agents track).
- GitHub Agentic Workflows preview site (search "GitHub Agentic Workflows") — CLI quick-start + template examples.
- Debug Adapter Protocol (DAP) — the standard underpinning the Actions Debugger; relevant to any DAP-based tooling (VS Code, Neovim).
