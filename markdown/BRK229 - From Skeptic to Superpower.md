---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/coding-agents
  - topic/github-copilot
  - topic/developer-productivity
source: https://www.youtube.com/watch?v=avfVJQWkF2A
session_code: BRK229
event: Microsoft Build 2026
speakers: Priyanka (Marketing/Product, ex-CNCF), Mario (Backend Engineer) — Think
duration_min: 38
aliases:
  - From Skeptic to Superpower
---

# BRK229 — From Skeptic to Superpower: Real-World AI Coding Workflows That Scale

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Priyanka (one-person MarTech team / product; previously ran the Cloud Native Computing Foundation, CNCF) & Mario (backend engineer; telco + IoT background) — both at **Think**, an energy-management company  
> **Duration:** ~38 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=avfVJQWkF2A)

## 🎯 TL;DR
Two builders from **Think** — a startup that runs HVAC/energy orchestration for 10,000+ buildings (critical infrastructure, some in −40 °C polar-circle Sweden) — share how they went from AI skeptics to running an almost-fully-autonomous "software factory." Priyanka frames the cultural and business arc (CEO mandate → early friction → "wow" moments → an Anthropic ban that took them offline for 10 days), drawing a strong **deja-vu parallel to cloud-native adoption**: vendor lock-in, lack of data/workflow portability, and a FinOps/"AI-Ops" cost problem. Mario presents the technical core: the **"Think Harness,"** a spec-driven, immutable, multi-agent pipeline (PRD → features → tasks → parallel implementation as a DAG) built on **GitHub Copilot CLI in autopilot**, heavy use of skills/specialized agent personas, a Socratic "grill-me" gate, model-switching for adversarial QA, and arch-linting to fight code drift. The headline live demo: a feature was kicked off at the start and **merged to main on stage** while they talked. Core message — AI is a brilliant but quittable colleague; harness the drift, stay vendor-neutral, and have fun.

## 🔑 Key Takeaways
- **AI coding adoption is re-running the cloud-native playbook.** The same enterprise twists/turns Priyanka saw over 10 years with Kubernetes/CNCF are reappearing in generative AI: lock-in, portability gaps, cost/FinOps pain.
- **"Drift" is the central engineering risk.** LLMs hold an internalized, over-confident view of code/terms (and can invent things "from thin air"). Without a harness the codebase rots, divergent terms accumulate, and because the AI is fast, bugs explode quickly.
- **A cited investigation:** teams using AI for ≥50% of their coding saw **bug frequency rise ~53%** — largely because they hadn't harnessed it.
- **The fix is context management, not raw model power.** Restate purpose, architectural & design principles; scaffold the repo so agents can navigate (ports = interfaces, adapters = implementations, clear domain context).
- **Spec-driven + immutable everything.** PRDs → features → tasks, all written into the repo in a machine-interpretable way, then frozen so an agent can trust "I can read this path and stop worrying."
- **Multi-agent orchestration via Copilot CLI's task scheduler.** Sub-agents can schedule further sub-agents, which manages context well; work runs as a **topology-sorted DAG** and parallelizes in "waves" by dependency.
- **Switch models for QA on purpose.** Different models are "seeded differently" and catch different issues; they implement with one (e.g. Claude 4.8) and run adversarial QA reviews with another (e.g. GPT-5.5), or reverse. Models won't critique themselves well ("I do nothing wrong").
- **Human-in-the-loop steering at the gates**, not line-by-line coding. Mario now acts as architect/designer; the engineer corrects partitioning, security, resilience decisions and re-iterates.
- **Vendor neutrality is a hard business requirement.** An **Anthropic org ban on 19 Apr 2026** halted all Claude-based processes; resolved ~10 days later, but exposed lock-in. Anything with a token markup (e.g. routing Claude through Cursor) is a poor backup for a bootstrapped startup.
- **Portability is fragile.** Work tied to implicit memory or a specific chat window can be truly lost (Priyanka lost a long copywriting conversation when a context window vanished).
- **The 10x shows up where you're weakest.** A non-security-minded dev suddenly ships better security posture in PRs; a backend engineer ships a "fully functional ugly mock" UI to start from.
- **Real business impact at Think:** an RFQ/RFP quoting workflow went from days → minutes (each application worth ~$100k–$800k); Priyanka's in-house website/CMS/CRM build saves ~$120k–$200k/year.
- **A new structural difference vs. cloud era: wider surface area** — *everyone's* a builder now ("it's the Oprah show… you get to build"), so problems can hit the business from many more directions.
- **"Brilliant colleagues — human or machine — can quit at any time."** Prepare accordingly (the ban was their proof).

## 📚 Detailed Notes

### Who they are & the setup
- **Priyanka** — works at **Think** (energy-management space); previously ran **CNCF** (Cloud Native Computing Foundation, the home of Kubernetes) for ~10 years. Now effectively the **one-person MarTech team** building Think's website + CMS/CRM. Has been **"vibe coding" for 6+ months** and frames the talk around the deja-vu with cloud-native.
- **Mario** — telco + IoT background. Started coding "Energy OS" in 2022, a platform **built to let LLMs execute on it**. His epiphany was **2021 trying GitHub Copilot** (early tab-completion era), predicting then that within 5–10 years **80% of simple code would be done by AI** — "and we're here now."
- **Think's stakes:** powers **10,000+ buildings** (commercial + residential) for power needs; parts are **critical infrastructure** (heating, ventilation, orchestration). Deployed near the polar circle where winters hit **−40 °C** — a failure could mean a pensioner in northern Sweden loses heat. This is *why* they were cautious skeptics.
- **Live framing device:** Mario is visibly "nervous" / itching to code, so early on he **kicks off a real autonomous build** on stage (from a to-do list) that runs in the background for the whole talk and is merged live at the end.

### The autonomous flow (kicked off live)
- It's an **autonomous flow with gating that forks out lots of agents.**
- Structure: **PRDs → broken into features → features broken into tasks → tasks implemented in waves, in parallel, by dependency graph.**
- Run on the **Copilot CLI in "autopilot"** (so it doesn't stop for "allow all" approvals).
- A custom command lists all tasks + status. A **skill called "implement feature"** acts as an orchestrator that **forks sub-agents** using Copilot's task scheduler (sub-agents can schedule further sub-agents → good context handling).
- On kickoff it reads the **immutable** context: which tasks belong to the feature, which PRDs they belong to, the architecture — then plans the implementation.

### The cultural arc: from skeptic to superpower (Priyanka)
- **Early 2025:** the CEO mandated AI-enabled tooling "bigger, better, faster." Crucially, **the CEO used the tools himself**, giving him credibility about what worked.
- **The team was not stoked** — critical-infrastructure risk made them wary.
- **Early experience = friction.** First attempts were "POCs that were glitchy." Priyanka "wrestled hard" with early Sonnet then Opus models building a new Think website — "fighting every day."
- **Feb 2026 "wow" moment:** with **Claude Opus 4.6**, Priyanka built a website section **in 5 minutes** and messaged the CEO — a memorable turning point. (Mario notably did *not* like 4.6 — his model story differs; see below.)
- **Wins spread across the business:**
  - CEO + controller built a **cloud-based RFQ workflow** (like an RFP process to apply for commercial-building installation / electrical projects). **Days → minutes**, with **each application worth ~$100k–$800k.**
  - **Head of product experience** (engineer by training, but had leaned into product and felt reticent to code) prototyped features **zero → working in days**, e.g. **"Sparky,"** a chat agent — built largely with **Codex** under her guidance.
  - **Priyanka** became the one-person MarTech team, building the company website + CMS/CRM in-house, saving **~$120k–$200k/year**. Caveat/joke: she showed *screenshots not the live site* — generative AI "enabling her OCD," now **six iterations** deep and needing to ship. (That site isn't used for lead-gen, so she had leeway to over-polish; case-study/news pages that would've taken weeks took **two days** incl. approvals.)
  - **Mario as proof of the "10x where you're weakest":** identifies as a backend engineer; ships an **"ugly mock"** UI in his GitHub repo — not a Picasso, but **fully functional** and a great starting UI.

### New tech, old problems (the deja-vu)
- **19 April 2026: Anthropic banned Think's organization.** All Claude-related AI processes halted.
- **Business response:** pause Claude-dependent business processes (RFQ, front-end) until resolved; keep **core engineering moving via backup tooling like Cursor** — but Cursor adds a **token markup that costs money**, a real constraint for a **bootstrapped startup**.
- **Dark, demoralizing ~10 days**, then resolved — but with lingering **billing/payments glitches**, echoing cloud-native **FinOps** pain.
- **Priyanka's named lessons:**
  1. **No real portability** in many app/chat-based workflows — data and workflow can be truly lost; anything relying on **implicit memory or a specific chat window** is at risk. (She lost a rich copywriting conversation — tone of voice, product marketing direction, built up in a ~1M-token context window — when it vanished.)
  2. **Any tool with a markup is a poor backup** — financial responsibility forces hard choices when you "go dark" with one vendor.
  3. **"Brilliant colleagues, human or machine, can quit at any time"** — prepare accordingly. The fun of building with an always-available smart collaborator is real, but so is the risk of it "going dark."
- Net: **vendor lock-in, lack of data/workflow portability, a FinOps nightmare** — "we just got into this new era and we're talking about all the things from the old era." Oddly comforting: *we solved this before, we'll solve it again.*

### The drift problem (Mario)
- **Software drift** exists among humans because each person has an **internalized view** of how a function behaves / what a word means; teams sync this via **architecture/design meetings and code reviews.**
- **An LLM is no different** — it's ingested huge internet data and formed an internalized view of everything — but with **more limited context and attention.** It also **writes very self-confident code that's wrong by your standards** and can **invent things from thin air**, very fast.
- **Consequence if unharnessed:** the **codebase rots** — same concept gets different words, the LLM then **interpolates code wrong**, compounding errors quickly. **Bug frequency goes "through the roof."**
- **Cited finding:** teams using AI for **≥50% of coding → bug frequency up ~53%**, largely from not harnessing it. It becomes **expensive to maintain** the very thing meant to accelerate you — "what should accelerate us will decelerate us."
- **Nuance:** vibe coding is great for **prototypes**, but for a **product shipping next year and the year after**, drift problems pile up.

### Enter the "Think Harness"
The harness = "do as we always have done" (spec → design → architecture) but **communicated properly into context**, because *"it's all about context management."* Its evolution:

1. **Early: chatGPT for research/design iteration** — tiny context window, it **derailed immediately**, hard to get usable code/tests (docs were OK-ish).
2. **Claude 4.1:** could start doing **audit-to-test**, small fixes, documentation.
3. **The architecture-expression problem:** Think has many products, multiple languages, somewhat different architectures, **1M+ lines of code** (better and worse parts, mostly sound). They needed a way to **express architecture that doesn't make the LLM derail.**
   - They'd used parts of **Domain-Driven Design (DDD)**, **Clean Architecture**, and **Hexagonal architecture.**
   - **First discovery:** **restate purpose + architectural/design principles** and add **scaffolding** so the AI can navigate — e.g. *"go to **ports** to examine an interface, go to **adapters** to see implementations,"* clear **domain context.**
4. **Claude 4.5 — the model that "really could code."** (They **disliked 4.6**: it "stopped adhering to instructions," overriding system prompts / "I do whatever I like." **4.7 was the patch** for that.) With 4.5 they could take **two separate services to be joined**, do data work, and have the model **actually understand both** — previously that "would crap."
5. **Specialized agents & skills:** they wrote many — **security auditor, resilience auditor, API experts**, etc.
6. **The context Goldilocks problem:** context was first **too small** to express intent, then **too large** (everything packed in). Since an **LLM is fundamentally an attention mechanism** (the transformer), you must signal **what to be guided by vs. what to pay *most* attention to.** Solution: keep **"must" / "must not" rules sparse** so the few that exist get real attention.
7. **Repo-as-context (vs. RAG):** put info into the repository in a **machine-interpretable** way. RAG (vector similarity) is "take this and this and this" and you can get clever (even **graph DB + RAG**), but it's a lot of work; instead **stick to good old strict traditions — define specs, adjust them slightly so LLMs can ingest them** into context.

### The end-to-end pipeline (how a feature actually ships)
- **Input from the product owner** — "awesome," knows the business/customers/tech, does **chaos engineering**-style creativity: lots of Google Docs, **mocks built with Claude** to visualize concepts → turned into **roadmap items** with a few goals + use cases.
- **Break down with skills:**
  - A skill breaks roadmap items into **"pods"** (scopes).
  - Take one pod → run the **"tech feature"** skill, which **auto-breaks it into features that can be parallelized**, using **several sub-agents** depending on the PRD/feature.
  - **Human-in-the-loop steering:** the engineer corrects it — *"you got this wrong, partition this way, have you thought about that?"* — and it **re-iterates from the prior iteration's instructions**, e.g. realizing it needs help with **security and resilience** it under-covered. Output: a **feature draft.**
- **Socratic gate — "grill me":** heavily inspired by **Matt Peacock's "grill me"** (praised as "a few lines of code… awesome"). It reads their context and **grills the user on common terms** (ubiquitous language, DDD), asks whether **architectural changes** are needed, etc. The engineer **must answer every question.** It **forks sub-agents to grill specific areas** — frequently a **security agent.** Output: a **written brief**, **canonicalized keywords**, and **ADRs (Architecture Decision Records).**
- **Ratify / QA gate:** a final QA sync to confirm everything is set; then it **writes the ADRs and the ubiquitous-language definitions.** Because **everything is immutable** (can't be changed afterward), this lets the LLM trust a path absolutely: *"I can read this and don't need to care anymore."*
- **Task split (the executing "yellow" stage):** the feature is split into **tasks along DDD / hexagonal boundaries.** Currently there's a **human step to approve tasks** ("never had to adjust them" — so this will likely be automated/skipped next). Tasks form a **DAG, topology-sorted**, so **dependencies run in the right order** and independent ones **parallelize** for speed.
- **Quality controls during implementation:**
  - **QA-gated**, with awareness of **which agents were used** → those become **candidates for QA review.**
  - **Arch-linting** keeps it on track (e.g. don't put something under **ports** that belongs in **adapters**) and on the right "trail."
  - **TDD / testing** throughout.
  - **Adversarial QA reviews** with **model-switching** (optional): implement with **Claude 4.8**, QA-review with **GPT-5.5** (or reverse) — *because models are seeded differently they discover different things*, and a model tends to think its own output is flawless.
- **Feature review (whole-scope):** integration testing over the entire feature scope, plus **security over adjacent systems** (not just the current change — must consider the larger blast radius). If it detects **more work is needed, it auto-adds new tasks**, and the **feature-implement scheduler picks them up and keeps going** — the goal is to **implement as much as possible overnight** so the morning isn't "everything stopped" with only 4–5 hours to fix.
- **Output:** a **PR ready to merge to main** (if not, fix via prompting or by hand).

### A working day with the harness
- **Morning:** review all the PRs — *"merge, merge, merge."* Blocked ones usually mean a **genuine architecture change** needing a human; sometimes the agent **hallucinates a block** and you just tell it *"this is in your imagination, continue"* and it proceeds.
- **Afternoon:** PRDs, features, **grilling**, and the rest of the spec work.
- **Night:** **implementation time — the agent codes while you sleep** (and sometimes during the day too).
- **Role shift:** Mario used to spit out **1,000–1,500 lines of code** easily and implement lots of features; **now he fixes things and does much more thinking — architect/designer**, letting AI implement most of it. Because they control **sensitive infrastructure**, some hard parts (security, compliance) are **still hand-developed** for now, though they intend to delegate more over time.

### Security & compliance
- Security checks run at **both spec time and implementation time** — on the **feature itself** and on the **surrounding subsystem/system.**
- They must be **ISO 27000-series compatible** (Mario references "ISO 27,000XX," possibly an EU-related obligation) with processes and audits.
- They're **writing an MCP plus skills/agents** to conform and **automate the tedious, hard compliance tasks.**

### The live demo payoff
- The task Mario kicked off at the start ran **all the described steps autonomously while they talked.** Priyanka narrated the "drama" live: at one point an **adversarial reviewer** appeared and she didn't know if it would stop the build — *"it fought it, it won… like a video game, super fun."*
- Result: **"Shipped and approved."** It did **two rounds with five reviewers**; everything passed.
- It produced a **PR to merge** — a **new SQLite repository** implemented for persistence, properly documented. They then **live-merged to main on stage** (applause). Punchline: *"You did it." — "I did nothing." — "That's the best part."*

### Closing message & future plans
- We're in the **"heady phase"** of a new tech — same excitement as the **iPhone** and **cloud computing**, followed by the same problems.
- **Vendor neutrality + data portability are non-negotiable** if you'll rely on this for important workflows: *"If you lock me out of your system that's okay, but I need my stuff."*
- **FinOps moved fast** — people now call it **"AI-Ops"**; encouraging that the gen-AI era is thinking about cost early (it took longer in cloud).
- **Drift compounds fast** when agents are involved; the **one new difference is a wider surface area** because **everyone's a builder** → more ways for problems to hit the business.
- **Future:** stay **nimble**, **aggressively support open-source / vendor-neutral options**, keep **building the software factory** (excited about **Copilot's parallelization**), and continuously evaluate **build vs. buy vs. open-source** to stay focused on customer deliverables, not tool-building.
- **Final note:** it's a new, sometimes intimidating/annoying era, but you've been given a **brilliant always-available colleague** to amplify you — *"why don't we just have a good time with it?"*
- Contact: Priyanka on **LinkedIn / Twitter / GitHub** (handle ~"Priyanka"); Mario on **GitHub** ("minus the dot"). She asks the audience to follow Think on LinkedIn to pressure her to ship the website, and to give feedback / contribute to the **Think Harness by emailing Mario.**

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot CLI** — primary agent runtime; run in **"autopilot"** so it doesn't stop for approvals. Core of the autonomous pipeline.
- **Copilot task scheduler / sub-agents** — lets sub-agents schedule further sub-agents; manages context for the parallel multi-agent flow.
- **GitHub Copilot (original, ~2021)** — the early tab-completion experience that gave Mario his "AI will write most simple code" epiphany.
- **Claude (Anthropic)** — primary coding/model family across the story.
  - **Claude Opus 4.6** — Priyanka's "wow" model (Feb 2026); but Mario found it stopped adhering to instructions.
  - **Claude 4.7** — the "patch" that fixed 4.6's instruction-following regression.
  - **Claude 4.5** — the model that "really could code" / understand two services to join.
  - **Claude 4.1** — early viable model for audit-to-test, small fixes, docs.
  - **Claude 4.8** — current default implementation model (paired with GPT-5.5 for QA).
- **Codex (OpenAI)** — used by Think's head of product to build "Sparky" and prototype features.
- **GPT-5.5** — used for adversarial QA reviews (paired against Claude 4.8).
- **ChatGPT** — early research/design-iteration tool; small context window caused derailing.
- **Cursor** — backup engineering tool during the Anthropic ban; downside = token markup.
- **MCP (Model Context Protocol)** — being written (with skills/agents) to automate ISO 27000-series compliance tasks.
- **Skills (Copilot/agent skills)** — Think's custom toolkit: `implement feature` (orchestrator), `tech feature` (breaks pods into parallelizable features), plus skills for pods/scoping, security/resilience auditing, QA, arch-linting.
- **Specialized agent personas** — security auditor, resilience auditor, API experts, adversarial QA reviewer, grilling sub-agents.
- **"Grill me" (by Matt Peacock)** — a Socratic-method tool ("a few lines of code") they heavily adapted into their ratify gate.
- **SQLite** — the persistence layer implemented by the live-demo PR (a new SQLite repository).
- **DDD / Clean Architecture / Hexagonal architecture** — design approaches underpinning the harness; ports/adapters scaffolding and DDD boundaries drive task splitting.
- **RAG / vector similarity / graph databases** — discussed as an alternative to repo-as-context; deliberately *not* their primary approach.
- **ADRs (Architecture Decision Records)** — written and frozen (immutable) as canonical decisions for agents to trust.
- **Kubernetes / CNCF (Cloud Native Computing Foundation)** — Priyanka's prior world; the source of the cloud-native adoption parallels (and the FinOps framing).
- **Think's platform / "Energy OS"** — Mario's LLM-executable energy-management platform (started 2022) powering 10,000+ buildings.
- **"Sparky"** — an internal chat agent built (with Codex) by Think's head of product experience.
- **ISO 27000-series** — security/compliance standard set Think must conform to (driving the MCP + automation effort).

## 🚀 Announcements / What's New
This was a **customer experience/practitioner talk, not a Microsoft product launch session** — no first-party GA/preview announcements were made. Notable forward-looking / status items mentioned:
- **Copilot CLI parallelization** — Mario reports the parallelization is "just the best"; Think is excited about how **Copilot is developing** and has "seen awesome demos." (Praise/roadmap sentiment, not a formal announcement.)
- **Think's roadmap:** continue building the **"software factory"**, automate **ISO 27000-series compliance** via a custom **MCP + skills/agents**, push to **automate the human task-approval step** (DAG task split), and keep delegating more **security/compliance** work to agents over time.
- **Model-version timeline referenced** (as experienced by Think, not announced here): Claude 4.1 → 4.5 → 4.6 (instruction-adherence regression) → 4.7 (patch) → 4.8 (current); GPT-5.5 used for QA.
- **Event date marker:** the Anthropic org ban was **19 April 2026**; the "wow" moment was **February 2026**.
> *None of the above are confirmed Microsoft Build product announcements — they are the speakers' experiences, tooling, and plans.*

## 💡 Demos
- **Live autonomous build → on-stage merge (the centerpiece).** Mario kicked off a real feature at the *start* of the talk via the Copilot CLI in autopilot; it ran the full pipeline (plan → implement waves → arch-lint → TDD → adversarial QA with model-switching → feature review) **autonomously while they presented.**
  - **What it proved:** the end-to-end harness genuinely runs unattended and produces a mergeable PR — not a scripted mock-up.
  - **Drama as narrative:** an **adversarial reviewer** appeared mid-run and the outcome was uncertain ("like a video game… it fought it, it won").
  - **Result:** **"Shipped and approved,"** **two rounds with five reviewers**, all passing; produced a **new SQLite persistence repository**, properly documented.
  - **Payoff:** they **live-merged the PR to main on stage** (audience applause). Punchline reinforced the role shift: *"I did nothing" — "That's the best part."*
- **`t stats` / task-status command** — Mario showed a custom command listing all tasks and their status in the repo.
- **Screenshots (not live) of Priyanka's website** — shown deliberately as screenshots (she hasn't shipped the real site after six iterations); illustrates the "AI enabling perfectionism" point rather than a live demo.
- **Mario's "ugly mock" UI** (in his GitHub repo) — shown as evidence the AI gives a non-frontend engineer a fully functional starting UI.

## 📊 Notable Stats / Quotes
- **10,000+ buildings** powered by Think (commercial + residential); parts are **critical infrastructure**.
- **−40 °C** winters near the polar circle where Think is deployed — the stakes framing.
- **~53% increase in bug frequency** for teams using AI for **≥50%** of coding (cited investigation) — largely from not harnessing the AI.
- **Each RFQ application worth ~$100,000–$800,000**; the workflow went from **days → minutes**.
- **Priyanka's website/CMS/CRM build saves ~$120,000–$200,000/year.**
- Case-study/news pages: **weeks → two days** (incl. final approvals).
- **Anthropic ban:** 19 Apr 2026, **~10 days** offline.
- **"Wow" moment:** built a section in **5 minutes** with Claude Opus 4.6 (Feb 2026).
- Mario: used to write **1,000–1,500 lines of code** easily; now mostly architects and fixes.
- **2021** — Mario tried GitHub Copilot; predicted **80% of simple code** done by AI within **5–10 years**.
- **1M+ lines of code** across Think's products; copywriting context window referenced as **~1M tokens**.
- > *"Brilliant colleagues, whether they're human or machine, can quit at any time, and you have to prepare accordingly."* — Priyanka
- > *"It's all about context management here."* — Mario
- > *"What should accelerate us will decelerate us."* — Mario, on unharnessed drift.
- > *"It's the Oprah show. You get to build, you get to build, you get to build."* — Priyanka, on everyone becoming a builder (and the wider problem surface).
- > *"I did nothing." / "That's the best part."* — after the live merge.
- > *"Standing on the shoulders of giants"* — learning from cloud-native mistakes.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] **Matt Peacock's "grill me"** Socratic tool — Mario rates it highly and it's tiny; worth trialing as a spec/ratify gate.
  - [ ] Run **Copilot CLI in autopilot** with a **sub-agent task scheduler** for a small PRD → features → tasks DAG and see how it parallelizes.
  - [ ] Experiment with **model-switching for adversarial QA** (implement with one model, review with another) to catch more issues.
  - [ ] Adopt **"immutable specs/ADRs in the repo"** + sparse **must/must-not** rules to fight context overload and drift.
  - [ ] Add **arch-linting** (ports vs adapters / DDD boundaries) to keep agents on the right "trail."
- [ ] Questions:
  - [ ] What exactly triggered the **Anthropic org ban** (policy/usage) — how to avoid it for an org relying on Claude?
  - [ ] Source/citation for the **"+53% bug frequency at ≥50% AI coding"** figure?
  - [ ] How is the **DAG task scheduler** implemented in/around Copilot CLI — native feature vs. their own orchestration?
  - [ ] What's in their **compliance MCP** for ISO 27000 automation — reusable pattern?
- [ ] Relevant to:
  - [ ] Anyone scaling **agentic coding** beyond prototypes to shippable products (drift/harness lessons).
  - [ ] **Vendor-neutrality / portability / FinOps ("AI-Ops")** planning for AI tooling.
  - [ ] Teams designing **spec-driven, multi-agent CI-style** software factories.

## 🔗 Related
- [[2026 Build Session List]]
- Topics: agentic coding workflows, context engineering, DDD / hexagonal architecture, AI FinOps / "AI-Ops", vendor lock-in & data portability