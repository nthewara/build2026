---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/github-copilot
  - topic/security
  - topic/nvidia
  - topic/agents
source: https://www.youtube.com/watch?v=0mLL3aS9Wxw
session_code: DEMSP387
event: Microsoft Build 2026
speakers: Ali Golshan, Alexander Watson (NVIDIA / Gretel)
duration_min: 22
aliases:
  - Secure agent workflows in GitHub Copilot with NVIDIA OpenShell
  - DEMSP387
---

# DEMSP387 — Secure agent workflows in GitHub Copilot with NVIDIA OpenShell

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ali Golshan (Sr. Director, AI Software @ NVIDIA; co-founder/CEO of Gretel) & Alexander "Alex" Watson (co-founder of Gretel, now NVIDIA)  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=0mLL3aS9Wxw)

> [!note] Naming
> The auto-captions render the product as "Open Shell". The actual NVIDIA project name is **OpenShell** (one word) — corrected throughout these notes.

## 🎯 TL;DR
OpenShell is an open-source (Apache 2.0) **runtime for long-running, autonomous AI agents**, started by Ali Golshan and Alex Watson at NVIDIA. Its core idea is **out-of-process, "secure by design" governance**: every agent (plus its harness/model/sub-agents) runs in a **zero-trust sandbox**, a **gateway outside the sandbox** holds all credentials/tokens (so a prompt-injected agent has nothing to leak — the sandbox is the blast radius), and policy is enforced at the **kernel/infrastructure layer** where the agent can't touch, override, or reason around it. Unique pieces include a **policy prover** (formal/SMT verification that mathematically proves what an agent *can still do* under a policy, running in single-digit milliseconds) and a **privacy router** (built on Gretel synthetic-data / differential-privacy tech) that keeps PII local while still using frontier models. The session demos using **GitHub as a persistence/audit layer** for fan-out agents and an agent **negotiating its own access** (getting blocked, drafting a policy proposal, the prover/gateway auto-approving, hot-reloading the policy). The goal: cut ~90% of human approvals for enterprise fleets running thousands-to-millions of sandboxes, while keeping a full audit trail.

## 🔑 Key Takeaways
- **OpenShell = an agent-native runtime, not just a sandbox.** Thesis: as agents become long-running, stateful, and persistent, they need a whole new stack built for *machine speed* and a *trusted runtime* everyone can confidently run agents, models, and harnesses inside.
- **Zero trust by default.** Every sandbox/environment starts **completely closed down**; the agent is only granted access incrementally as it earns it.
- **Architectural departure: the agent runs *inside* the sandbox.** With Copilot/Claude Code today, the agent runs outside and only executes code inside a sandbox, so governance lives at the Copilot layer. In OpenShell the agent itself (and its I/O) runs inside the sandbox, so **one policy language governs any agent** across your infrastructure.
- **Credentials never touch the agent.** A **gateway outside each sandbox** holds all secrets/tokens/keys and authenticates to services on the agent's behalf. Prompt injection therefore has nothing to steal; the **blast radius is a single sandbox**.
- **Governance is lifted to the kernel/infra layer**, out of the agent's probabilistic loop — *intentionally* out of the agent's path and reach so it can't bypass, override, or reason about it.
- **Policy prover** is the signature feature: policies (OPA/Rego/YAML) are translated to **formal logic** and checked with **SMT solvers / formal verification** to produce a **mathematical proof** of what the agent can still do (e.g. "can it reach the internet? can it write to this repo?"). It **cannot be fooled** (assuming the logic description is correct), unlike a human or another reviewer-agent.
- **Speed matters:** the prover runs in **single-digit milliseconds**, so adding security doesn't double token cost or latency the way "another agent reviews every call" does.
- **Privacy router** (three modes): (1) PII detected → route to a **local model**; (2) no PII → route out to a **frontier model**; (3) hybrid → use planner models / **differentially-private fine-tuned models (low epsilon)** to synthetically rewrite the query, preserving utility but stripping PII, then **rehydrate** locally. Keeps context/PII local while leveraging global compute.
- **Per-sandbox isolation of agentic behavior**, not just process/kernel isolation (vs gVisor / hardened containers / micro-VMs which just add layers between process and kernel).
- **Agents can negotiate their own access.** Global org policies are visible to the sandboxed agent; from zero-trust it can request "give me X, Y, Z and I can finish" — the **policy prover validates no exfiltration path is created**, then the policy is granted, **hot-reloaded** (no sandbox restart), and the agent proceeds.
- **GitHub as a persistence/audit layer** works cleanly for ephemeral, concurrent agents (artifacts, notes, full audit trail) with built-in concurrency and no risk of agents stomping each other.
- **Drivers** let you choose the under-the-hood sandbox perimeter (Firecracker, hardened container, trusted computing, Kubernetes gVisor-style primitives); OpenShell enforces its runtime on top of whatever you pick.
- **Logs in OCSF** (Open Cybersecurity Schema Framework) → compatible with Splunk / Datadog / any security data tooling.
- **Scale framing:** even a 1% human-approval rate across millions of sandboxes = thousands of prompts/day; aim is to reduce ~**90%** of approvals down to one or two human sign-offs per piece of work.
- **Status:** alpha; first released at **GTC (San Jose), March 2026** (~3 months prior); **beta targeted in the next couple of months**; long-term intent to **donate to CNCF or Linux Foundation**.

## 📚 Detailed Notes

### Origin & first principles
- OpenShell was started by **Ali Golshan and Alex Watson** at NVIDIA as a **20%-time project ~8 months ago**. The two previously founded **Gretel** (synthetic data), joining NVIDIA ~a year ago.
- Built on two first principles:
  1. **Agent-native software stack.** As the world moves to agents, what does an agent-native stack look like? Agents are becoming **long-running, stateful, persistent** sessions — that needs a different environment/stack to manage persistence than human-oriented software.
  2. **Machine-speed tooling.** If the stack is agent-native, the tooling should be built for machine speed, not human pace.
- The unifying goal: instill a **trusted runtime** — **secure by design** — so anyone can confidently run agents, models, and harnesses inside it.
- Motivating question (Alex): *what happens when you run 500 or 1,000 agents at once?* You can't depend on humans approving every action. The aim is to approve as many agent actions as possible, in an enterprise-grade secure way, **at agent speed**, without human-in-the-loop bottlenecks.

### Zero-trust environment
- Every sandbox/environment **starts completely closed** (not permissive). Access is granted incrementally as the agent moves through its task.
- Big categories of customer/partner/ecosystem concern about long-running autonomous agents drove the design. A key observation: most controls/governance today are enforced **at the agent/model layer, inside the probabilistic loop** — which is unreliable.
- OpenShell's answer: take those policies and create a **deterministic** way to control/govern the agent by pushing policy/governance down to the **infrastructure / kernel layer**.
- **Prompt-injection example:** the agent should hold **no credentials/secrets/tokens/keys**. The **gateway outside the sandbox** holds them. So if the agent is injected/compromised, there's nothing for it to leak; the **blast radius is one sandbox**.
- Cloud-native analogy: like the shift from **stateful monolithic VMs → container microservices on Kubernetes**, you can treat these sandboxes more like **cattle than pets**, which makes them far easier to govern.

### Architecture & core primitives
OpenShell is a **runtime**. Everything (architecture, roadmap, code) is open source under **Apache 2.0** on the GitHub repo. Core primitives:

- **Gateway** — sits **outside every sandbox**; communicates/interacts and **holds credentials, tokens, keys**. The agent has its session but no path to leak anything else.
- **Dedicated sandboxes** — every agent (and its sub-agents and tooling) runs in its **own sandbox**. An agent that spawns sub-agents gets a sandbox each, with **cross-sandbox communication**.
- **Agent runs *inside* the sandbox (key departure)** — normally (Copilot, Claude Code) the agent runs outside and only executes code inside a sandbox, so governance is at the Copilot layer (not the model layer). In OpenShell the agent runs inside the sandbox and **every input/output is enforced**, enabling **one policy language across any agent**.
- **Policy prover** — see below.
- **Privacy router** — see below.

### Policy prover (signature feature)
- Goal: answer not just "what does this policy enforce?" but **"if I enforce this policy, what can the agent *still* do?"**
- Implementation: takes the policy language — **OPA + Rego** (or YAML) — and **describes it in formal logic**, then uses **formal verification / SMT solvers**. Uses **technology that originally came from Microsoft**.
- This goes beyond simple `if` statements ("can this agent access the internet / write to a repo?") — it creates a **mathematical proof**, enabling complex, robust reasoning about capabilities.
- **Why it beats reviewer-agents:** OpenAI and Anthropic are moving toward using **another trusted agent to review sandbox changes** (e.g. "auto-approver" for Codex, "managed agents" for Claude). But a reviewer agent is **susceptible to the same risks** — it can be fooled, just like a human. The **policy prover cannot be fooled** (given a correct logic description). If you open a new hole in the sandbox (e.g. allow writing to a new GitHub repo), there is **no way to fool the prover into not seeing it** — it flags it.
- **Performance:** runs in **single-digit milliseconds**, so it's often not even necessary to do a second-level (reviewer-agent) run. Avoids the failure mode where reviewing every agent call with another agent **doubles token cost and time**.

### Privacy router
- OpenShell isolates the usual constructs — **system, file, network, memory** — but its differentiator is **isolation around *agentic behavior***, which manifests very differently from traditional encapsulation (gVisor, hardened containers, micro-VMs just add layers between process and kernel to reduce attack surface).
- The privacy router **borrows heavily from Gretel's synthetic-data work** (and work Microsoft itself did). Three use cases:
  1. **PII present → local inference.** Agent submits a query riddled with PII; router detects PII and **routes to a local model**.
  2. **No PII → frontier model.** Agent needs multi-turn orchestration/tasking/reasoning and a frontier model; router sees no PII and **lets it route out**.
  3. **Hybrid (combination of 1 & 2).** Use **planner models** or **differentially-private fine-tuned models (DP with low epsilons)** to **synthetically rewrite the query** — preserving utility, removing PII — so it can go to a frontier model, reason, and come back to be **rehydrated** locally. Net effect: **keep context + PII local while leveraging global compute.**

### Demo 1 — GitHub as a persistence/notepad layer (map-reduce / fan-out)
- Problem framed: ephemeral agents are great (spin up, do the job, spin down) but how do they **communicate and store data/persist**? OpenShell uses **GitHub as a persistence layer** for artifacts, notes, and the full audit trail.
- This example ships in the repo: **OpenShell → examples**.
- Pattern shown: a **map-reduce / fan-out** — fire up **five sandboxes**, each works a task, each stores its notes, then a **synthesis/summarization agent** reads across all the notes and combines them into one result. All stored in GitHub.
- Sandboxes can be **restarted as many times as you want**; **concurrency is built-in** — no risk of agents stomping each other's notes in GitHub.
- **Policy shape:** the demo shows an **OPA Rego policy scoped to a single agent execution** for GitHub — it lists the **specific REST endpoints** the agent may use. Need more → it must **negotiate**. This minimal scoping is the key security construct.
- The **agent never sees credentials** — all managed at the **supervisor** level. The terminal UI shows credentials being hidden from the agent.
- Observed run: five sandboxes spun up, each with a coding agent inside (**Copilot or Codex**), four running on tasks; they use granted credentials to write directly to GitHub; the synthesis agent merges results. Each agent is **isolated in its own sandbox** so you can reason precisely about what it's doing security-wise, while still coordinating.
- Mention: **Google's A2A** ("agent-to-agent") protocol enables fast, high-rate inter-agent communication for agents working tightly together — a more advanced option to build on. But for storing an **audit trail / notes / execution**, GitHub still makes a lot of sense.
- Result: sandboxes are **closed down and deleted**; everything is written out to GitHub. In the repo you can see **each agent wrote to exactly one file** (so **no destructive actions are possible**), then all were summarized into a single output.
- **Hot-reloaded policies:** every time policies are loaded on the network-stack / file-system stack, they are **hot reloaded** — no need to restart the whole sandbox and eat that latency (unlike traditional containers). Designed for machine speed because **every millisecond of delay compounds downstream**.

### Demo 2 — An agent negotiating its own access (auto-approval loop)
- This functionality was **"all of about 3 days old"** — a big piece of in-progress work.
- Setup: OpenShell terminal on the left, demo on the right. A **Codex agent** is spun up inside a sandbox with **read access to GitHub but no write access**, and told to write to GitHub.
- Flow:
  1. Agent tries to **write to GitHub → gets blocked** by OpenShell (policy block at drafting). A **denial** appears.
  2. OpenShell **passes the agent an explanation**: "you got blocked because you don't have access to this repo; there's a **local skill** you can use."
  3. The agent uses that **local skill** to **enumerate the sandbox policies** and **extend the policy** — it **drafts a proposal** requesting access to **write to a specific repo endpoint** (a network rule).
  4. The **policy prover runs against the proposal** and reports **one finding**: it's **expanding the agent's credential write scope** — but that's deemed **okay**, so it's **automatically approved** and let through, **all logged**.
  5. The policy is **hot-reloaded**, and the agent can then **write to GitHub directly**.
- **How policy visibility enables this:** all **global org policies** (allowed/disallowed actions) are made available to the sandboxed agent. From zero-trust, the agent can say "if you give me X, Y, Z I can complete my task." This is **not granted blindly** — agents can **chain capabilities** to problem-solve, so the **policy prover checks for accidental exfiltration paths** before granting.
- **Logs:** emitted in **OCSF (Open Cybersecurity Schema Framework)** — compatible with Splunk / Datadog / any security tooling. The trail shows: first write **denied** → agent **authored a new proposal** → **gateway approved** → **policy hot-reloaded** → **write to GitHub succeeded**.
- Value: set a security policy once and **let agents evolve** without granting a giant maximalist "here's everything you can do" policy. Keep each sandbox at the **minimal policy required**; the agent **negotiates up** from there.

### Ecosystem, go-to-market & roadmap
- Built **with an ecosystem of partners**, Apache 2.0; long-term intent to **donate to CNCF or the Linux Foundation**.
- **Microsoft** (announced "yesterday" relative to the talk): OpenShell **embedded into Windows native WSL, Azure, GitHub** (and **MXC**, as spoken).
- Available via **Canonical on Ubuntu**, **Red Hat on OpenShift**, and **Docker**.
- Partners running their agents inside OpenShell for trust include **SAP, Workday, ServiceNow**.
- Vision: embed OpenShell as a **trust layer** everyone can build on; NVIDIA drives it but hopes the **community picks it up and pushes it forward**. Call to action: visit the GitHub repo, give feedback, experiment.
- **Timeline:** **alpha** today; first released at **GTC San Jose, March 2026** (~3 months prior); **beta targeted in roughly the next couple of months**.
- **Drivers** (new, powerful concept): when launching OpenShell you **pick the sandboxing perimeter under the hood** — **Firecracker**, a **hardened container**, **trusted computing**, or **gVisor-style ("SIG") primitive sandboxing from Kubernetes**. OpenShell relies on whatever tech is under the hood and **enforces its runtime on top**.

### Q&A
- **Q: How far can the agent negotiate before it stops?**
  - Goal (a "finger-in-the-air" estimate) is to reduce ~**90% of the approvals** a human would typically need — ideally wrapping a piece of work into **one or two required human approvals**. Ultimately it depends on the **constraints the security team** chooses.
  - In the project, **providers** (Codex, Claude, Copilot, etc.) are where **central teams / IT / security run global policies**. Every sandbox starts at **zero trust** (none granted), so the **ceiling is whatever the central teams' global policies allow**.
  - Two ways to do this: (a) a single **maximalist policy** signed off by security ("everything you could possibly do") — **bad** security posture; not every agent should start with that. (b) OpenShell's approach — a **dynamic** way for the agent to grow into **exactly what it needs and no more**, with **negotiation allowed up to the point the security team says "that's it — anything more needs a human."**
  - Enforcement is at the **kernel / infrastructure layer intentionally**, to keep policy **out of the agent's path and reach** so it can't bypass/override/reason about it.

## 🛠️ Products / Features / Technologies Mentioned
- **NVIDIA OpenShell** — open-source (Apache 2.0) runtime for long-running, autonomous agents; the subject of the talk.
- **Gateway** — out-of-sandbox component that holds credentials/tokens/keys and authenticates to services on the agent's behalf.
- **Sandbox** — per-agent (and per-sub-agent/tooling) zero-trust isolated execution environment; the blast radius.
- **Policy prover** — translates OPA/Rego policy to formal logic; uses SMT solvers/formal verification to mathematically prove what an agent can still do; runs in single-digit ms. Built on tech originating from Microsoft.
- **Privacy router** — routes inference (local vs frontier) based on PII/cost/privacy policy; can DP-rewrite queries; built on Gretel synthetic-data tech.
- **OPA (Open Policy Agent) + Rego** (and **YAML**) — the policy languages used to express what an agent may do.
- **Drivers** — pluggable under-the-hood sandbox perimeters (Firecracker, hardened container, trusted computing, Kubernetes gVisor-style primitives).
- **OCSF (Open Cybersecurity Schema Framework)** — log format used; compatible with Splunk / Datadog / security tooling.
- **GitHub** — used as a persistence/notepad/audit-trail layer for ephemeral, concurrent agents; also the host of the OpenShell open-source repo + examples.
- **GitHub Copilot / OpenAI Codex** — coding agents run *inside* OpenShell sandboxes in the demos.
- **Anthropic Claude / Claude Code** — referenced; their "managed agents" reviewer-agent approach contrasted with the policy prover.
- **Google A2A (agent-to-agent) protocol** — for fast, high-rate inter-agent communication when agents work tightly together.
- **Gretel** — synthetic-data company co-founded by the speakers (now NVIDIA); source of the privacy router's DP/synthetic-data tech.
- **Differential privacy (DP) / differentially-private fine-tuned models (low epsilon)** — used to synthetically rewrite queries, preserving utility while removing PII.
- **Firecracker, hardened containers, micro-VMs, gVisor, trusted computing, Kubernetes** — sandboxing/isolation primitives referenced (some as "drivers", some as contrast for "just adding layers between process and kernel").
- **Splunk / Datadog** — example security/observability tools OCSF logs integrate with.
- **WSL (Windows native), Azure, Canonical/Ubuntu, Red Hat/OpenShift, Docker** — integration/distribution targets.
- **SAP, Workday, ServiceNow** — partners running agents inside OpenShell for trust.
- **CNCF / Linux Foundation** — potential future home for the project (donation intent).

## 🚀 Announcements / What's New
- **Microsoft integration announced (the day before the talk):** OpenShell embedded into **Windows native WSL, Azure, GitHub** (and "MXC" as spoken).
- **Availability via partners:** **Canonical on Ubuntu**, **Red Hat on OpenShift**, **Docker**.
- **Agent-negotiates-its-own-access loop** (Demo 2) — brand new, **"about 3 days old"** at the time of the talk; an in-progress capability where a blocked agent drafts a policy proposal, the prover/gateway auto-approves it, and the policy hot-reloads.
- **Drivers** — pluggable sandbox perimeters (Firecracker / hardened container / trusted computing / Kubernetes gVisor-style primitives) presented as a current, "very cool and powerful" concept being matured.
- **Status / roadmap:** Project first released at **GTC San Jose, March 2026** (~3 months before this talk); currently **alpha**; **beta targeted in roughly the next couple of months**; long-term intent to **donate to CNCF or the Linux Foundation**.

## 💡 Demos
- **Demo 1 — GitHub as a persistence/notepad layer (map-reduce / fan-out).** Spun up **five sandboxes**, each with a coding agent (Copilot/Codex) working a task and writing its notes to **exactly one file** in a GitHub repo (so no destructive actions are possible); a **synthesis agent** then read across all notes and merged them into a single result. Showed: credentials hidden from the agent (managed at supervisor), minimal per-execution Rego policy scoped to specific REST endpoints, built-in concurrency, sandboxes restartable and then auto-deleted, and policies **hot-reloaded** without sandbox restarts. **Point proved:** ephemeral, concurrent agents can persist, coordinate, and leave a clean audit trail using GitHub — under strict, minimal, isolated policy.
- **Demo 2 — Agent negotiating its own access (auto-approval loop).** A **Codex agent** with read-only GitHub access was told to write to GitHub. It got **blocked**; OpenShell returned an explanation + pointer to a **local skill**; the agent used the skill to **enumerate and extend the sandbox policy**, **drafting a proposal** for a specific write endpoint. The **policy prover** flagged one finding (credential write-scope expansion), deemed it okay, **auto-approved**, **hot-reloaded** the policy, and the agent then wrote to GitHub. The **OCSF audit log** showed deny → proposal authored → gateway approved → policy reloaded → write succeeded. **Point proved:** agents can dynamically negotiate up from zero-trust to exactly the access they need — provably safe and fully logged — without humans approving every step or granting a maximalist policy.

## 📊 Notable Stats / Quotes
- **~8 months** — how long ago OpenShell was started (as a 20%-time project at NVIDIA).
- **~1 year** — how long ago the speakers (ex-Gretel founders) joined NVIDIA.
- **500–1,000+ agents at once** — the motivating scale question that framed the design.
- **Five sandboxes** — fan-out fleet size in Demo 1.
- **Single-digit milliseconds** — policy prover run time (so a second-level reviewer-agent pass is often unnecessary).
- **"About 3 days old"** — age of the access-negotiation functionality in Demo 2.
- **~90%** — target reduction in human approvals ("finger in the air"), ideally down to one or two human approvals per piece of work.
- **Even 1% human approval across millions of sandboxes = thousands of prompts/day** — the scale argument for automation.
- **~3 months** — since first release at GTC San Jose (March 2026).
- **4 minutes left** — time remaining when they paused for Q&A (talk ~22 min).
- *"You can have one policy language that works across any type of agent that you're running across your infrastructure."* — Alex Watson, on the in-sandbox architecture.
- *"The approver cannot be fooled — assuming our description of the logic of the policy is correct... there's no way to fool an agent into not seeing that you're doing it."* — Alex Watson, on the policy prover.
- *"We intentionally want that policy to be out of the path and reach of the agent, so it can't bypass it or override it or reason about it."* — Ali Golshan, on kernel-layer enforcement.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: clone the **NVIDIA OpenShell** GitHub repo and run the `examples/` GitHub-notepad fan-out demo; test the access-negotiation loop with a Codex/Copilot agent; try a **driver** swap (Firecracker vs hardened container).
- [ ] Things to try: wire OpenShell **OCSF** logs into a Splunk/Datadog sink and inspect a deny → propose → approve → write trail.
- [ ] Questions: How mature is the **privacy router**'s DP-rewrite path (modes 1–3) in alpha, and what's the utility/latency cost? How are **A2A** and GitHub-persistence meant to coexist? What exactly is "MXC" from the Microsoft integration list (caption-ambiguous)?
- [ ] Questions: What's the relationship between OpenShell, **NemoClaw**, and the broader **NVIDIA Agent Toolkit** (mentioned in NVIDIA blog/press, not deeply in this talk)?
- [ ] Relevant to: secure agent platforms; GitHub Copilot / Codex enterprise rollouts; agent governance & policy-as-code (OPA/Rego); zero-trust runtime design; DP/synthetic-data privacy routing; Azure/WSL/GitHub agent integrations.

## 🔗 Related
- [NVIDIA Technical Blog — Run Autonomous, Self-Evolving Agents More Safely with NVIDIA OpenShell](https://developer.nvidia.com/blog/run-autonomous-self-evolving-agents-more-safely-with-nvidia-openshell/)
- [build.nvidia.com/openshell](https://build.nvidia.com/openshell)
- NVIDIA Agent Toolkit / NemoClaw / Nemotron (broader stack OpenShell is part of)
- Topics: OPA + Rego policy-as-code · SMT solvers / formal verification · differential privacy (Gretel) · OCSF · Google A2A protocol · Firecracker / gVisor sandboxing
- 