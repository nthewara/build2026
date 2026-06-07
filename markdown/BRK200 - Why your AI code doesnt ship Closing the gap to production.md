---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-coding
  - topic/devops
  - topic/production
  - topic/ci-cd
  - topic/agents
  - topic/github
source: https://www.youtube.com/watch?v=5YFPfuOhpwU
session_code: BRK200
event: Microsoft Build 2026
speakers: Mario Rodriguez (VP/Head of Product, GitHub), Evan Bole (Engineering Lead — Copilot CLI / SDK / App)
duration_min: 45
aliases:
  - "Why your AI code doesn't ship: Closing the gap to production"
---

# BRK200 — Why your AI code doesn't ship: Closing the gap to production

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mario Rodriguez (leads Product for GitHub) · Evan Bole (co-creator & engineering lead of the Copilot CLI, Copilot SDK and Copilot app)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=5YFPfuOhpwU)

## 🎯 TL;DR
The hard part of AI-assisted development is no longer *writing* code — agents now do that well — it's getting that code **over the line into production**: triage, CI, review feedback, security, merge conflicts, and deployment. GitHub's thesis is that since January 2026 "agents entered the workforce" and genuinely work, shifting developers from **micro-delegation** (constantly correcting an agent) to **micro-steering** (delegating whole tasks and only nudging). To close the last-mile gap, GitHub is building an **agent-native engineering system** spanning six pillars — surfaces, runtime, automation, quality, intelligence/memory, and enterprise trust — and demoed it almost entirely live ("demos, not memos"). The centrepiece is the new **GitHub Copilot app**, built to *finish* work rather than just start it, with **canvases** (agent-drivable custom UIs), **Copilot Cloud** sandboxes, **Chronicle** (cross-surface session memory with a SQL API), **agent merge** (an agent that babysits a PR to green), **automations** (morning brief, auto-repro of bug reports), **rubber duck** (advisor/critic mode), and **multimodel code + security review**. The unifying message: stop measuring *activity*, start measuring *output* — are you actually shipping?

## 🔑 Key Takeaways
- **The bottleneck moved from generation to shipping.** Agents can produce code; the gap to production is the "meta work" — review, CI, security, merge, deploy — and that's where velocity is lost.
- **Micro-delegate → micro-steer.** Since Dec 2025 / Jan 2026, you can hand an agent a whole task ("fix this issue") and only steer occasionally, instead of correcting every step. This is framed as a "complete new way of working."
- **"Agents entered the workforce and it's really working"** is Mario's framing for the inflection that makes an agent-native system necessary.
- **The SDLC is "more or less dead"** — it's merging with the product development lifecycle into one human + agent collaboration loop, end-to-end (idea → spec/plan → build → review → deploy → debug live issues).
- **Agent-native engineering system = 6 pillars:** Surfaces → Runtime → Automation → Quality → Intelligence/Memory → Enterprise (trust & scale). Each is being rebuilt "agent-first," needing new APIs and new agentic UX.
- **"Demos, not memos"** is GitHub's internal saying — the whole session is live demos to prove the system works, defects and all.
- **The Copilot app is built to *finish* work, not start it.** Most tools help you spin up endless parallel work; this app focuses on getting work delivered — "it's not about doing more, it's about finishing more."
- **Canvases** are agent-drivable custom full-screen UI surfaces (terminal, triage board, whiteboard, kanban, Miro) that you (or the agent) author, check into the repo, and share with the team — a bidirectional relationship where the agent drives the UI and the UI drives the agent.
- **A canvas marketplace** is coming, with official first-party and third-party canvas extensions (e.g. a Miro design canvas), beyond the hyper-personalised ones you build yourself.
- **Copilot Cloud** runs tasks on **GitHub sandboxes** — fast, stateful microVMs that spin up in seconds, are isolated, with tightly-scoped credentials — so you can "close your laptop and go home" while agents keep working overnight.
- **Chronicle** is per-user, private cross-surface session memory: it remembers every session, prompt and line of code across machines and Copilot products, and exposes a **direct SQL API** to the agent (full-text + structured SQL over a data lake of your sessions).
- **Agent merge** is an agentic automation that watches a PR and drives it to merge — resolving merge conflicts, getting CI green, and responding to review (CCR) feedback with justifications — but it pushes back sensibly on bad asks (e.g. refused an unsolicited 1000-line refactor).
- **Automations** can run locally (private "morning brief" at 6 a.m.) or in the cloud (e.g. on `issue created`, auto-attempt a repro + write a failing test + label + comment), turning noisy feedback firehoses into focused, actionable work.
- **Rubber duck** brings the "let me bounce this off a colleague" workflow to agents, with **advisor** and **critic** modes; available in the Copilot CLI and the GitHub app.
- **Multimodel review beats single-model.** Running code review across Gemini, Claude (Sonnet 4.6) and GPT (GPT-5.5) — models with different training distributions — yields better results than any one; a final "rubber duck" pass critiques the combined output before it reaches the human.
- **Security is first-class, not an afterthought.** A dedicated security-review sub-agent (built with GitHub Advanced Security) runs alongside code review, so quality and security are both automated on the path to production.
- **Trust & sandboxing are the gating requirement for "YOLO."** Mario stresses the live YOLO/autopilot demos only work because local (public preview) and cloud sandboxes keep agents isolated, credentials scoped, and prevent leaks/pwning.
- **A partner ecosystem closes the production loop:** Sonar (code quality), Endor (security), Miro (canvas/design), LaunchDarkly (safe production rollout) — so teams can ship to prod feeling safe.
- **The core question for every team:** are you optimising for *activity* or *output*? Everything in the Copilot app is aimed at output — bringing all the pieces together to actually deliver value to users.
- **Greenfield vs legacy caveat:** these frontier practices land easiest on greenfield apps; legacy/mainframe will move slower — but the talk is meant to spark curiosity about an agent-first future.

## 📚 Detailed Notes

### The inflection: agents entered the workforce (and it's working)
Mario Rodriguez (Head of Product, GitHub) opens by framing a step-change that happened "since January" 2026: **agents entered the workforce and started *really* working.** Previously you had to **micro-delegate** — hand the agent a tiny piece, then repeatedly correct it ("you got this wrong, you got this wrong"). From roughly December 2025 into Jan/Feb 2026, the behaviour changed: you can now **micro-delegate** a whole task and only **micro-steer** it — e.g. just say "fix this issue" (after a little spec/plan work) and let the agent run. He calls this "a complete new way of working."

The consequences he draws out:
- Developers spend more time on **creativity and judgment** (the pre-work) and delegate more of the execution.
- **Code review got better** — richer feedback from Copilot.
- Agents can now **deploy with the right guardrails into production** and even **debug live issues**.
- Because agents touch the whole lifecycle, **"the SDLC is more or less dead"** — it's merging with the product development lifecycle into a single **human + agent collaboration** loop. It's no longer the old hand-off chain.

The strategic question this raises: if agents can do all this work, **what's getting in the way of shipping?** Why is velocity not higher, and how do you prepare for a world where velocity is 10×/20×/100× and "anything your imagination can become a reality"?

### The agent-native engineering system (the 6 pillars)
This change "necessitates a system," and Mario argues it's not simple. GitHub historically optimised **human-to-human** developer collaboration; it must now evolve into **human + agent** collaboration. He frames the core primitives an agent-native GitHub needs as six pillars, flowing "from surface into enterprise":

1. **Surfaces** — where developers do their work: IDEs, the command line, and the newly launched **GitHub Copilot app**, plus "many places including your phone."
2. **Runtime** — a safe, trusted place for agents to execute, **both locally and in the cloud** (he ties this to keynote announcements around "ME MXC" — caption-uncertain phrasing).
3. **Automation** — to make the whole system **predictable** and to **scale**. Analogy: a **3D printer** — you give it a CAD drawing, it returns an object; you still must *verify* the result and discard defects. Just as CI/CD and DevOps/DevSecOps were "movements of automation," agentic engineering won't be different.
4. **Quality / verification** — a system that confirms your **intent** (the "CAD drawing") actually became the shipped software (the "object").
5. **Intelligence / memory** — a system with **continuous intelligence improving itself**.
6. **Enterprise trust & scale** — everything above must work with enterprise-grade trust.

Going "deep in each one" and making it agent-native/agent-first requires **brand-new APIs**, **brand-new UX** (which become "agentic experiences"), and a new way of doing automations — with the **power of agents *and* predictability**, which Mario calls "a hard problem to solve at scale." This system is **the agent-native engineering system** and is the spine the rest of the demos hang off.

> Greenfield caveat: these practices are "a little bit of the frontier." They're easiest on greenfield apps and harder on legacy/mainframe; the goal is to encourage curiosity about an agent-first future of software development.

### The GitHub Copilot app — built to *finish* work, not start it
Mario hands to **Evan Bole**, co-creator of the app and engineering lead for the **Copilot CLI, Copilot SDK and Copilot app**. Evan's core thesis: the Copilot app is **not just another session manager**. Most tools help you create lots and lots of *parallel* work; the Copilot app is built to help you **finish** it. The interesting part isn't implementation — it's all the **meta work** that delivers value to users: **issue triage, getting through CI, keeping it green, responding to review feedback, merging, and deploying to customers.**

He reframes the promise of agents: not "do more" but **"finish more"** — reclaim your focus, optimise for **outcomes** (did you actually deliver the thing and make users' lives better?) over **activity**. He's self-deprecating about being a "major procrastinator" on tedious tasks — and that everything he's about to show is the product of "procrastinating productively" by building new primitives instead of doing the tedious task (which takes ~10× longer but means millions of other engineers never have to do it).

### Inbox, batch triage & isolated work trees
Evan starts in a **customised inbox view** on the app homepage, filtered to public issues in the GitHub-app repo (lots of feedback since launch). He spots an issue about the **terminal canvas missing from quick chat** and decides to batch several related terminal items (UI improvements, tab switching). He hits **actions → new individual sessions**, which:
- Kicks off **three sessions** in the left nav at once.
- Creates **isolated work trees** per session.
- **Auto-attaches the relevant issue** as context.
- Lets the agent start working immediately.

This is the "on-the-rails" one-size-fits-all workflow (you can also kick off agentic PR review or issue/diagnosis sessions) — but the bigger story is **customisation**.

### Canvases — agent-drivable, custom, shareable UI surfaces
**Canvases** are the marquee concept: custom UI surfaces the **agent can drive**, and which can **drive the agent back** — "a rich bidirectional relationship." Evan demonstrates several:

- **Terminal canvas (built-in):** via voice, he asks the agent to *open the terminal canvas, run a web server that renders "hello canvas," then open the browser to that page.* The agent opens the terminal, sends commands, reads output, writes/runs a Python web server, does "a little extra verification," and opens the browser — all on the right-hand side of the app. Point: built-in surfaces the agent can fully operate (terminal, browser, automated testing).
- **Triage canvas (team-built, checked into the repo):** pulls recent issues, top thumbs-up issues, and common themes. A button (e.g. **"analyze sample"**) right-clicks a message to the agent instructing it to create **5–8 feedback buckets** — mirroring how Evan's team reviews customer feedback at daily standup. You can also **start sessions directly from the canvas**, which spawns **nested sub-sessions** (visible as a tree) that can talk back and forth — great for managing context and grouping work. Mechanism: the **`create session` tool** — "everything I can drive through the GitHub app, the agent can drive through the GitHub app."
- **Create-canvas skill (author a canvas live):** taking an audience suggestion ("whiteboard"), Evan dictates a request for a **whiteboard canvas** you can draw on, with a button to **export to JPEG and publish to a gist** (for design-meeting whiteboarding + sharing artifacts on GitHub). This triggers the **create-canvas skill**; the agent authors the extension **dynamically** into the repo's `.github` folder, so it can be **checked in and shared with all teammates**. (He sets repo scope and goes to autopilot; it takes a couple of minutes.)
- **Extension ecosystem (install from gist/URL):** while the whiteboard builds, he shows installing an extension from a gist/URL — an **agentic kanban ("kanban board") canvas**. If you think visually, you can have the agent add tickets/subtasks to the board for a bigger feature, then **start a task from the board** to kick off work in the left-hand chat. You can even ask for live changes (e.g. re-theming) and the agent **hot-reloads the extension**.
- **Miro canvas (first-party/partner):** a full Miro design canvas — sticky notes, feedback, the rich Miro features you'd expect — but now **agent-driven**: the agent can modify the board and you can kick off implementation from it.

**Canvas marketplace:** GitHub is launching a **marketplace** of canvas extensions — not just personal miniatures but **official first-party and third-party** canvases (Miro being an example partner). More official partner canvases are coming. The overarching idea: **hyper-personalised software for your team's and your personal workflows** — "build anything to your heart's content."

### Copilot Cloud — close your laptop, agents keep working
Evan addresses **"agent anxiety"**: it's 4:55pm, you're racing to get an agent set up and running before you leave, and the clock's running out. The fix is **Copilot Cloud**, built on **GitHub sandboxes** — **fast microVMs that spin up in a matter of seconds**. He enables it ("yolo on," autopilot) and kicks off cloud tasks. Properties of these sandboxes:
- **Stateful** — they persist, so you can come back to them.
- **Isolated** — keep risky PRs/changes separate from everything on your laptop.
- **Locked down with tightly-scoped credentials.**
- **No laptop / internet needed** — kick off a task, let it run all night, and it's ready in the morning.

The payoff: safely test PRs in a clean environment, or run long jobs unattended, and genuinely "shut your laptop and go home" — go to your family and enjoy your evening.

### Chronicle — cross-surface session memory with a SQL API
Developers work across many distinct surfaces — the cloud agent, **CCR** (Copilot code review), Visual Studio, VS Code, the CLI — and it's hard to remember *where* you did something. Evan introduces **Chronicle**: **per-user, private session memory** that gives you continuity across all surfaces. "Chronicle remembers everything that you've ever done — every session, every line of code, every prompt," across different machines and different Copilot products, and it's **scoped to your user / only accessible to you**.

Two demos:
- **`Chronicle search`** — he half-remembers fixing "a rather gnarly Rust bug the other day" and asks Chronicle to find it. It crawls his history, locates the context (what the bug was, how he fixed it), loads it into the session, and lets him finish the new task faster.
- **`Chronicle stand-up`** — a swipe at unproductive standups ("managers still living in the 80s"). It looks at all his work in the **last 24 hours** (build prep, bugs he filed while prepping demos) to auto-generate a standup summary, eliminating "TDM."

The technical reveal: **the agent knows SQL.** GitHub **exposes a direct SQL API to the agent**, and Chronicle works as a **combination of full-text search and structured SQL queries** over a **data lake of all your sessions**. You can watch the SQL queries execute and expand them to see rich structured data being returned.

### Agent merge — an agent that drives a PR to green
The last-mile problem: **getting work over the line.** On any PR, there's now an **`agent merge`** button. Once clicked, agent merge **periodically checks in on the PR** and works it until it's green and mergeable by:
- Detecting and resolving **merge conflicts**.
- Ensuring **CI is green**.
- Resolving **review feedback** — whether from an agent (CCR) or a human co-worker.

Evan walks through the **very first agent-merge PR** (from "Jeremy," dated **March 19th** — evidence they've been building the app for a while): Jeremy added a **CLI health check** and turned on agent merge, then **went and got lunch.** Over multiple rounds of **CCR feedback** (CCR gave an overview + a batch of five comments, then many more rounds), Jeremy's agent **resolved every thread tastefully**, replying with **justifications for what it fixed and what it deliberately didn't.** Only once it was clean did Jeremy send the PR to Evan — **"protecting my attention, my focus."**

Crucially, agent merge **isn't blindly obedient** — it makes good decisions and pushes back:
- When Evan ("like any good manager") demanded a docs link for a blocking case, the agent replied (paraphrased) **"did you read two lines below? It's already there."**
- When Evan tried to "send it off the rails" by demanding a **massive 1000+-line refactor**, the agent said **"fair concern, but I'm not going to do that as part of this change"** — and **merged the PR anyway.**

The lesson Evan hammers: stop optimising for **activity**; optimise for **output**. "Are you using agents to get that work over the line?" Everything in the Copilot app is about bringing the pieces together — the engineering *and* the meta-engineering — and "doing a great job at the five to ten [things] that really matter" instead of "50 things at once."

### Sandboxing & trust — the prerequisite for "YOLO"
Mario returns to underline **two things**. First, **sandbox**: all those live "YOLO"/autopilot moments only work because you have **trust and security** underneath. GitHub now offers **both a local sandbox story (public preview)** and a **cloud sandbox** (what Evan used via Copilot Cloud). The cloud sandbox capability is **also coming to the Copilot app**, so you'll be able to **delegate local sessions (and that one-shot canvas) into the cloud environment** and "multiplex yourself" — without fear of getting pwned or leaking information.

### Automations — local & cloud, to guard your focus
The second thing Mario flags is **automations** ("agent merge is itself a type of agentic automation, running locally"). Evan demos guarding focus against the **"firehose of noise"** that agents/feedback can create (public + private feedback, cross-team, Slack-connect channels):
- **Morning brief (local, private):** runs at **6 a.m. every day** on his machine, just for him. The prompt asks for a brief covering **PRs in flight he needs to land, critical un-reviewed PRs that are blocking other engineers, and new/critical issues**. Output: a **"focus morning brief"** with top-10 issues + links, PR details, and what needs his attention — "start your day with your first cup of coffee, focused." Because it's local, the team never sees the output.
- **Issue-repro automation (cloud):** he creates a cloud automation named **"issue repro"** triggered on **`issue created`** for the **private GitHub-app repo** (where GitHub employees file feedback). The prompt: if the issue is a bug report, **try to reproduce it**, **write a failing test case** (to confirm it's a real bug "not ghosts in the GPUs"), **add a label** indicating it's confirmed, and **add a comment with the repro steps + the verbatim failing test** to write and make green. This turns raw bug reports into **pre-triaged, repro-ready work** — "if there's already a repro, fixing them is usually trivial." He then files a test bug ("app won't start … shows a strange whiteboard canvas") to let the automation run during the talk.

Message: use agents not just to write code but for **all the meta-work around maintaining a high-quality project** and understanding customer signals.

### Rubber duck — advisor and critic modes
Mario highlights **rubber duck** (shown in the keynote, not re-demoed here). Because GitHub is now **multimodel, multi-agent and multi-surface**, it can give you a **second set of eyes** — the "hey, what do you think about this?" rubber-ducking you'd do with a colleague, but with agents. Rubber duck has **two modes**: **advisor** and **critic**. It's available in the **Copilot CLI** and the **GitHub app**. Mario says he uses it constantly — "mainly on critique mode," sometimes assistant mode to save tokens.

### Quality: multimodel code review + security review (orchestrated)
The final demo is about **quality** — the pillars sequence is restated: **surfaces → runtime → automation → quality → intelligence → enterprise** (intelligence and enterprise weren't demoed). Evan gives "inside baseball": prepping the demo, he hit a bug where **cloud support in the app didn't work** for cross-repo orchestration; a colleague ("Enrique") put together a fix PR right before launch, and Evan wants to **review it carefully for quality and security**.

He pastes the PR URL into the app (**Cmd-K**), and Copilot offers to **create a review session**, loading the diff. He can add comments and ask questions in a **private conversation with the agent** — "this doesn't go to github.com," it's just for building shared understanding of the code. Then he composes review workflows:
- **`/review`** for code review and **`/security review`** for security.
- **Multimodel code review** across **Gemini, Claude (Sonnet 4.6) and GPT (GPT-5.5)** — models with **different training distributions** that "don't all agree," which is the point: combining them yields the best results.

He issues one orchestration prompt asking the agent (via the **`create session` tool**) to:
1. **Session 1** — check out the branch and run a **multimodel code review** (code-review agent + Gemini / GPT-5.5 / Sonnet 4.6).
2. **Session 2** — pull the same branch and run a **security review**, also using **multimodel sub-agents** (the security sub-agent was **built in collaboration with GitHub Advanced Security**).
3. When both sub-sessions finish, they **message back to the parent session**, which then runs a **rubber-duck critique** of the combined output — a final critical pass — before surfacing a **final recommendation** and optionally **posting comments to the PR**.

The value: by the time it requires the human's attention, multiple models have agreed, the rubber duck has agreed, and the security review has found the issues — "the feedback it's giving me is actually helpful and legit." High quality, much faster.

### Partner ecosystem & the production loop
Mario closes the loop back to the **agent-native engineering system**: turning **idea → intent → production** via human + agent collaboration, with **trust** throughout. He name-checks partners that fill out the path to prod:
- **Sonar** — code quality.
- **Endor** — security.
- **Miro** — canvas/design (shown earlier).
- **LaunchDarkly** — deploy to production safely (feature-flag/rollout safety).

So GitHub isn't "leaving you hanging after coding" — it takes the work the rest of the way: code review + security + safe deploy. The session ends with the live security-review sub-agents still running ("three of these with Gemini"), a fitting demos-not-memos finish.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot app** — the new desktop app at the centre of the talk; built to *finish* work (triage → CI → review → merge → deploy), not just spawn parallel sessions.
- **Copilot CLI** — GitHub's command-line Copilot surface; hosts rubber duck and is part of the agent-native surface set.
- **Copilot SDK** — SDK Evan's team owns alongside the CLI and app (named as part of his remit).
- **Canvases** — custom, agent-drivable UI surfaces in the app (terminal, triage, whiteboard, kanban, Miro); authored as extensions, checked into the repo, shareable with the team, hot-reloadable.
- **Create-canvas skill** — a skill that authors a new canvas extension dynamically into the repo `.github` folder from a natural-language description.
- **Canvas marketplace** — forthcoming marketplace of official first-party and third-party canvas extensions.
- **`create session` tool** — the primitive that lets both the human and the agent spin up sessions / nested sub-sessions; underpins triage, orchestration and multi-repo work.
- **Isolated work trees** — each session gets its own isolated work tree with the relevant issue auto-attached.
- **Copilot Cloud** — run agent tasks in the cloud, built on GitHub sandboxes; lets you close your laptop while work continues.
- **GitHub sandboxes** — fast, stateful, isolated microVMs (spin up in seconds, tightly-scoped credentials) powering local + cloud agent execution.
- **Local sandbox** — on-machine sandboxed execution (public preview) for safe local YOLO/autopilot.
- **Chronicle** — per-user, private cross-surface session memory; full-text + structured SQL over a data lake of all your sessions, with a direct SQL API exposed to the agent (`Chronicle search`, `Chronicle stand-up`).
- **Direct SQL API for the agent** — the mechanism powering Chronicle; the agent writes/executes SQL over session data.
- **Agent merge** — agentic automation (a button on a PR) that drives a PR to green: resolves conflicts, gets CI green, answers review feedback with justifications, and pushes back on bad asks.
- **CCR (Copilot code review)** — GitHub's code-review agent; produces overviews + batched comments that agent merge responds to.
- **Automations** — scheduled/triggered agent jobs, runnable **locally** (e.g. 6 a.m. morning brief) or in the **cloud** (e.g. on `issue created`).
- **Morning brief** — a local daily automation summarising in-flight PRs, blocking un-reviewed PRs, and critical new issues.
- **Issue-repro automation** — a cloud automation that, on a new bug report, attempts a repro, writes a failing test, labels the issue, and comments repro steps + the test.
- **Rubber duck** — multimodel/multi-agent "second set of eyes" with **advisor** and **critic** modes; in the Copilot CLI and the GitHub app.
- **`/review`** — code-review command/agent in the app.
- **`/security review`** — security-review command; uses a security sub-agent built with GitHub Advanced Security.
- **Multimodel review** — running review across multiple models (Gemini, Claude Sonnet 4.6, GPT-5.5) for better coverage via differing training distributions.
- **GitHub Advanced Security** — the security product the security-review sub-agent was built in collaboration with.
- **Cmd-K (paste PR URL)** — quick action in the app to create a review session from a PR URL.
- **Models named:** **Gemini**, **Claude (Sonnet 4.6)**, **GPT (GPT-5.5)** — used for multimodel code/security review.
- **Partner integrations:** **Sonar** (code quality), **Endor** (security), **Miro** (canvas/design), **LaunchDarkly** (safe production deploy).
- **Agent-native engineering system** — GitHub's overarching platform vision: surfaces → runtime → automation → quality → intelligence/memory → enterprise.

## 🚀 Announcements / What's New
- **GitHub Copilot app** — newly launched ("we just launched this"); the session is effectively its showcase. Exact GA/preview wording not stated beyond "launched."
- **Canvases** — introduced as a new app capability (built-in + author-your-own + install-from-gist/URL).
- **Canvas marketplace** — announced as **coming** ("we're excited to share more … coming"); official first-party + third-party canvas extensions, with a Miro partner canvas shown. Not yet GA.
- **Copilot Cloud** — presented as available to use in the demo (built on GitHub sandboxes); the **cloud sandbox is also coming to the Copilot app** (delegate local sessions into the cloud) — framed as forthcoming for the app specifically.
- **Local sandbox** — explicitly called out as **public preview**.
- **Chronicle** — introduced as a new capability ("we now have something called Chronicle"); preview/GA status not stated.
- **Agent merge** — introduced as a new PR capability ("I now have this button called agent merge"); status not explicitly labelled.
- **Automations (local + cloud)** — demoed as available; status not explicitly labelled.
- **Rubber duck** — shown in the keynote and stated to be **available now in the Copilot CLI and the GitHub app** (advisor + critic modes).
- **Multimodel + security review orchestration** — demoed live; the security sub-agent built with GitHub Advanced Security. Status not explicitly labelled.
- *Note on GA vs preview:* the only **explicit** status given was **local sandbox = public preview**. Most other items were demoed as working/launched without a precise GA-vs-preview label, so treat them as "shown/launched" rather than confirmed GA.

## 💡 Demos
- **Batch issue triage** — filtered the inbox to terminal-related issues and fired **new individual sessions** for three of them at once, each in an isolated work tree with the issue auto-attached and the agent starting work. *Point:* group related agentic work for easier review.
- **Terminal canvas (voice-driven)** — asked the agent (by voice) to run a Python web server rendering "hello canvas" and open the browser to it; the agent drove terminal + browser end-to-end. *Point:* the agent can fully operate built-in surfaces (terminal, browser, automated testing).
- **Triage canvas** — "analyze sample" button instructed the agent to bucket issues into 5–8 feedback themes (the team's daily standup ritual), and **start sessions** straight from the canvas, spawning nested sub-sessions. *Point:* canvases drive the agent and organise/group work.
- **Create-canvas (live authoring)** — dictated a request for a **whiteboard canvas** with export-to-JPEG + publish-to-gist; the create-canvas skill authored the extension into `.github` at repo scope to share with the team. *Point:* you (or the agent) can build bespoke, checked-in, shareable canvases on the fly. (Paid off later — the whiteboard worked and successfully published to a gist.)
- **Install extension from gist/URL** — installed an **agentic kanban board** canvas, added it, opened it, and started a task from the board; asked for live theming changes that the agent **hot-reloaded**. *Point:* a portable canvas ecosystem + live bidirectional editing.
- **Miro canvas** — showed a first-party Miro design canvas, agent-driven, with the ability to kick off implementation from it. *Point:* official partner canvases.
- **Copilot Cloud** — turned on YOLO/autopilot and kicked off cloud tasks on GitHub sandboxes (stateful microVMs). *Point:* close your laptop; agents keep working safely overnight.
- **Chronicle search** — recovered the context of a half-remembered "gnarly Rust bug" fix and loaded it into the session. *Point:* cross-surface memory speeds up new work.
- **Chronicle stand-up** — summarised the last 24 h of work via live SQL queries over the session data lake (queries visible/expandable). *Point:* the agent uses a direct SQL API over your history.
- **Agent merge walk-through** — replayed the first agent-merge PR ("Jeremy," Mar 19): the agent resolved many rounds of CCR feedback with justifications while Jeremy ate lunch, pushed back on a redundant docs request and a 1000-line refactor demand, then merged. *Point:* an agent reliably drives a PR to green and exercises judgment, protecting reviewer focus.
- **Morning brief automation** — a local 6 a.m. automation produced a focus brief (top-10 issues + links, in-flight PR details, team blockers). *Point:* tame the feedback firehose; start the day focused.
- **Issue-repro automation (cloud)** — created a cloud automation on `issue created` to repro bugs, write a failing test, label, and comment; then filed a test bug to trigger it. *Point:* auto-pre-triage bug reports so fixes become trivial.
- **Multimodel code + security review orchestration** — from a pasted PR URL, orchestrated two sub-sessions (multimodel code review via Gemini/GPT-5.5/Sonnet 4.6; security review via multimodel sub-agents + GitHub Advanced Security), then a parent-session rubber-duck critique and final recommendation/PR comments. *Point:* high-quality, multi-perspective review + security as one composed workflow. (Live: the security sub-agents were still running at the end — "three of these with Gemini.")

## 📊 Notable Stats / Quotes
- **"Demos, not memos."** — GitHub's internal saying; the whole session lives by it.
- **"Agents entered the workforce and … it's really working."** — Mario, on the post-January 2026 inflection.
- **Micro-delegate → micro-steer** — the shift from constantly correcting agents to delegating whole tasks and only nudging.
- **"The SDLC is more or less dead"** — merging into the product development lifecycle as one human + agent loop.
- **"It's not about doing more. It's about finishing more."** — Evan, reframing the promise of agents around output, not activity.
- **"~10× longer"** — Evan's joke that building a new primitive to avoid a tedious task takes about ten times as long as just doing the task (but millions of engineers benefit).
- **"60% … telling the truth and … 40% are lying"** — recurring running gag about audience show-of-hands (procrastination; agents creating noise).
- **Velocity "10×, 20×, 100×"** — Mario's framing of the upside once shipping friction is removed.
- **GitHub sandboxes spin up "in a matter of seconds"** — the microVM performance claim.
- **Morning brief runs at 6 a.m. daily; Chronicle stand-up covers the last 24 hours.**
- **First agent-merge PR dated March 19th** — signalling how long the app's been in development.
- **Multimodel review uses Gemini + Claude Sonnet 4.6 + GPT-5.5** — "they don't all agree with each other … you get the best possible results."
- **"Are you focused on activity or are you focused on output?"** — the session's central challenge to every team.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Stand up an **agent-merge-style** PR babysitter in our own CI (resolve conflicts + drive to green + answer review bots) and measure reviewer-attention savings.
- [ ] Things to try: Prototype a **"morning brief" automation** (in-flight PRs, blocking un-reviewed PRs, critical new issues) and an **`issue created` auto-repro + failing-test** bot.
- [ ] Things to try: Pilot **multimodel code review** (route the same diff through 2–3 models + a final "rubber duck" critique pass) and see if disagreement surfaces real defects.
- [ ] Things to try: Build a small **canvas-style** internal tool (triage/kanban board the agent can drive) to test the bidirectional UI ↔ agent loop.
- [ ] Questions: What are the **GA vs preview** timelines for Copilot app, Copilot Cloud, Chronicle, agent merge, and the canvas marketplace? (Only local sandbox was explicitly called public preview.)
- [ ] Questions: How is **Chronicle** secured/scoped in enterprise (data residency, retention, who can query the SQL API), given it stores "every prompt and line of code"?
- [ ] Questions: Pricing/token implications of **multimodel** review + rubber duck running on every PR at scale?
- [ ] Questions: What exactly is **"ME MXC"** (caption-uncertain) referenced as the keynote runtime announcement?
- [ ] Relevant to: Platform/DevEx teams defining the **last-mile "AI code → production"** pipeline (review, security, CI, safe deploy) and agent governance/trust.

## 🔗 Related
- [[BRK233 - Software Defensibility in the era of AI coding]]
- [[BRK229 - From Skeptic to Superpower]]
- [[BRK223 - From rows to reasoning]]
- [[GitHub Copilot app]]
- [[Agent-native engineering system]]
- [[Chronicle (Copilot session memory)]]
- [[Agent merge]]
- Source list: [[2026 Build Session List]]
