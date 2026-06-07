---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/developer-tools
  - topic/platform-engineering
  - topic/coding-agents
  - topic/open-source
source: https://www.youtube.com/watch?v=o5IQMijn-Ks
session_code: BRK245
event: Microsoft Build 2026
speakers: Peter Steinberger (creator/maintainer, OpenClaw)
duration_min: 44
aliases:
  - Build the thing that builds the thing
---

# BRK245 — Build the thing that builds the thing

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Peter Steinberger — creator & maintainer of OpenClaw (large open-source project)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=o5IQMijn-Ks)

> [!note] Accuracy note
> This is an auto-caption transcript and the speaker is self-deprecating/improvisational, so some tool names and product names are garbled. Best-guess corrections are applied throughout (e.g. "GBT 5.4 / GBD55" → GPT-5.5-class model, "Asia" → Azure, "inferral machine" → infra/ephemeral machine, "crit box" → CrapBox, "claw"/"clanker" used loosely for the agent/AI). The talk is openly about **OpenClaw** and the agent used is **Codex**. Internal tool names (Claw Sweeper, GOG, Octopool, CrapBox, Mantis, CorePatch, CrapFleet, ClickClock, Release Bar) are taken as spoken — they are this maintainer's own homemade "slop" tools and may not be public products.

## 🎯 TL;DR
This is a fast, demo-driven talk by the maintainer of OpenClaw about a new way to build software in the agent era: **stop optimising how *you* build software and start building tools that help your *agents* build software faster.** The speaker walks through a sprawling collection of small, "vibe-coded" homemade tools (most of them ugly throwaways) that he built every time he hit friction maintaining a massive open-source project with a tiny team and tens of thousands of issues. The recurring method is simple: **annoyance is the signal** — whenever something is repetitive or painful, go one level up and build a tool to automate it, because in 2026 "any problem is just a prompt away." The headline lessons: treat every issue/PR as a "prompt request" (a change signal), automate triage/review/testing/verification end-to-end so you only stay in the loop for what matters, and remember these tools *compound* — each one makes the next one faster to build. The two things he most wants you to try: **auto-review** (agent re-reviews its own code in fresh contexts until clean) and **CrapBox** (ephemeral cloud test boxes).

## 🔑 Key Takeaways
- **Reframe the job:** your job is no longer to build software faster yourself — it's to *help your agent* build software faster, and above all to **close the loop** (give the agent a way to self-verify, e.g. taking its own screenshots instead of you eyeballing the browser).
- **"Prompt request," not pull request:** every issue or PR is just a signal that someone wants a change. Issues and PRs are largely interchangeable; a fresh issue is sometimes *easier* than an AI-written PR you have to make your agent read, critique, and rewrite.
- **The hard part isn't building, it's maintaining.** "Any problem is just a prompt away" — building these tools is trivial; gardening them over time (deps, platforms, edge cases) is the real cost.
- **Annoyance is the trigger to automate.** "Listen to your body / listen when you're annoyed." Every tool in the talk was born from a specific moment of friction.
- **Go one level up.** Don't think at the project level — point the agent at your *projects folder* and ask "what should I work on?" across all repos + open issues at once.
- **Optimise for autonomous work + protect your focus time.** Maximise what agents can do unattended (duration doesn't matter), and reserve human attention for the genuinely important/risky items.
- **Tools compound.** Small helper tools chain together (reports need the crawler; CrapFleet needs CrapBox), so each new tool gets cheaper to build — a flywheel, not a tax.
- **It's safe to vibe-code throwaways.** Helper tools aren't system-critical, so he literally doesn't read their code; for OpenClaw itself he reads far more code than people assume.
- **Auto-review changes everything:** one line in `AGENTS.md` ("before you commit/land a PR, run auto-review") makes the agent call itself in a *fresh context* and run many review rounds — far more reliable than manually hammering `/review` all day.
- **CrapBox (ephemeral cloud test boxes) is the other must-try:** offload heavy/parallel tests to beefy cloud machines, fan out across OSes/providers, and massively raise shipping confidence.
- **Capture intent, not just diffs:** an OpenClaw skill offers contributors a privacy-filtered prompt/transcript upload so the maintainer can tell genuine effort ("good slop") from a 5-token one-liner.
- **Models aren't the bottleneck — imagination is.** "We're not limited anymore by intelligence... everything that we're limited of is our own imagination."
- **Feed the agent your invariants.** Write project-specific assumptions into `AGENTS.md` (the agent has no memory across sessions), and periodically ask the agent itself to flag confusing/contradictory instructions and clean them up (confusion = token burn + worse results).
- **Don't write agent files yourself** — let the agent write instructions in "agent-to-agent" language; you describe intent, it phrases it.
- **Own the whole stack so the agent can self-fix:** because he controls the full stack (e.g. his own Google CLI), a missing feature is just something the agent can build *and* end-to-end verify against a demo account before shipping.
- **"You can just do stuff."** The overarching mindset: in this era a single person can build their own ecosystem of tooling on the side, in spare corners of the day.

## 📚 Detailed Notes

### Framing: build the thing that builds the thing
The speaker opens by warning this won't be a polished presentation — it's a live tour of his own tools. His thesis: it's been less than a year since coding agents existed and only ~half a year since they got *good*, and there's no slowing down, so **many of our old ways of building software are already obsolete and we haven't figured out the new ones yet.** The mental shift he's pushing: anytime you build software now, your job isn't to figure out how to build *faster yourself* — it's to figure out **what you can do to help your agent build faster**, and especially to **close the loop**.

He illustrates the loop with a story: last year he spent months building a SaaS where the agent would write code, declare it done, he'd check the browser, swear at the agent, it would loop and fix and eventually get there. The breakthrough was realising the agent could just **take a screenshot itself** — like a human would — so it could self-verify. Lesson: anything you find yourself doing repeatedly, ask "how can I automate this / help my agent close the loop?"

He also reframes how he sees all his "failed" projects. People wrote articles like "he made 43 projects that failed and one worked" — but he says **none of them failed**: they're all tools he built for himself (mostly to help his agents work faster). He's catalogued them on a deliberately "slop" website of all the little tools built to build OpenClaw (and says it's not even complete).

### The scale problem: tens of thousands of issues
OpenClaw "exploded," and issues/PRs spiked. He notes GitHub's issue counter caps display at 5k, masking the real number — at one point **more than 10,000 issues** open. His blunt view: most of that volume is **agent-generated**, not written by humans ("let's not pretend any of that is written by humans anymore"). Many open-source maintainers are furious about the "slop," but his stance is **you can't fight the world — you have to find a way to deal with it.**

Key reframe (the conceptual core of the talk): **stop calling it a pull request; call it a "prompt request."** Any issue or PR is just a signal that *someone is unhappy with what you built and wants a change* — issues and PRs are basically interchangeable. Sometimes a plain **issue is nicer than an AI-written PR**, because with an AI PR he has to make his agent read the code, critique it, and rewrite it anyway, whereas an issue lets him start fresh.

### Claw Sweeper — automated issue triage & closing
First concrete problem: **get the issue number down.** He tried existing review tools (he name-drops trying CodeRabbit, Greptile/"grab," and others). They were fine but only gave *reviews* — he wanted something that **automatically groups and closes** issues. Nothing good existed, so he built **Claw Sweeper** (again, intentionally sloppy — the website doesn't matter).

How it works (and it's deliberately simple):
- It runs as a **GitHub Action**. Whenever someone opens an issue/PR, it **kicks off a Codex run in the cloud**.
- A carefully written prompt explains the project's goal and vision. He keeps a **`vision.md`** in every open-source project now, and his standard prompt makes the agent read it. The file spells out **what the project definitely wants and definitely does not want.**
- Based on those rules, the agent either **comments on** or **closes** the issue.
- Result: he closed roughly **15,000 issues** this way. He admits he operates "on the assumption of infinite tokens" and that you could do it far more efficiently.

It's not a one-shot static process. Because at this scale a fix landing on `main` may resolve issues he's **never even read**, **Claw Sweeper re-runs on every issue/PR at least weekly** (could be daily if you want to spend the tokens). A common outcome: it auto-closes a months-old issue he never saw, the original reporter gets a "we fixed this on main" reply, and he never had to touch it. He has a **Discord integration** that reports what it did, and a **dashboard** (e.g. "18 Codex working right now") that shows a long explanatory comment plus an array of issues people need to solve.

### Maintainer reports & a Discord crawler
With more momentum he added maintainers — some excellent, some who showed up briefly then vanished. Having been liberal about granting access, he lost overview, so he built a **dashboard / maintainer reports** for OpenClaw (kept private because it needs more data than just GitHub). Crucially, **being a good maintainer isn't just pushing code — it's participating in discussions**, which the project does on **Discord**. So the reporting system needed Discord data too.

That created the next problem: **how to get data out of Discord.** Answer: build a **crawler** ("any problem is just a prompt away"). He stresses again that *building* the crawler was never the hard part — *maintaining* it is.

He then describes operating **one level above the project**: instead of thinking per-project, he points Codex at his **projects folder** and asks "what should I work on?" It enumerates all his projects and open issues. He could say "do all of them" (joking "my slop is better than your slop") but doesn't blindly — some reports are weird and he doesn't fully trust the agents, so he wants to read them.

### The issue browser — killing micro-friction
Reading flagged items by clicking each URL was too slow, so he built himself a **homemade issue browser**: select text and it parses it. Because "clankers" produce an almost unlimited number of formats, every time something didn't parse he just patched it, so now it handles essentially every format it's ever seen and he can click through the list fast. Thanks to the `vision.md` context, the agent's pre-selection is usually right — it'll say "do these eight, skip these two, those need real human time." 

The principle he extracts: **your time is the limiting resource, so you must build the tools to build the tools.** Optimise what agents do autonomously (then duration is irrelevant) and carefully manage the **focus time** where you genuinely need to be in the loop.

### GOG — a Google CLI for agents
Aside (sparked by spotting a "Gmail draft create" feature mid-demo): he built **GOG** because **Google has no good CLI** and he wanted his agents to access all his Google services. Codex has Gmail and now calendar integration but only for a single account, which annoyed him. Owning the whole stack means **the agent can fix itself** — anything missing is just a feature the agent can add. Better still, because he has a **demo account on GOG**, Codex can **build the feature *and* end-to-end verify it**, so he ships with confidence having done almost nothing but say "yes."

### Turning the crawler into a prioritisation engine
The Discord crawler turned out to solve a much bigger problem than reporting: **with thousands of issues, knowing *what to actually work on* is hard.** He hooked the crawler up to Codex so it can scan all his channels and answer questions like *"what are people screaming about the most, correlated to open issues/PRs — find me the top five things to work on,"* matched against the **vision document**, picking work the agent can do autonomously so it can run for hours and parallelise.

He reiterates a governance point: even when you heavily automate, **you must keep an overview of your system** so you can tell which issues are "probably fine, probably fine" vs. "this one is scary, I need to look at it."

**Distribution trick:** other maintainers wanted the crawler, but there's no public way to get all that data. He uses a bot to access it, but didn't want to hand his **bot token** to everyone. Solution: the crawler **backs up all Discord data to GitHub** ("what's the simplest backup system? GitHub") in a serialized DB format, so anyone without a bot token can use **GitHub as an alternative data source.** Problem solved.

### Release Bar — knowing when to ship
Maintaining many projects, he wanted a dashboard of **what needs attention** — most pending PRs, time since last release, "should I cut a release?" Nothing good existed, so he built **Release Bar**, which he can filter by e.g. *days since last release*. His software philosophy: **if you don't constantly garden software, it's dead** — dependencies and systems change, everything needs updating — so a dashboard telling him when to release (and which projects need attention) is valuable. Reminder again: these little helper tools are **not system-critical**, so he doesn't read their code; if a tool gets heavy use he iterates on it, and if one doesn't pan out, "no cost."

### Octopool — beating GitHub rate limits
Running lots of parallel work (and instructing his agent to hunt for *related* issues) kept **exhausting GitHub tokens**. He has friends at GitHub and literally had someone (Ashley/"Ashley wasn't around"; "Peter's rate limits") **clicking a button once an hour to reset his limits** — but humans need sleep ("it's not clankers"), so working odd hours he'd get stuck. (Annoyance → solution.)

He built **Octopool**. The principle is simple:
- A personal account gets **~5,000 API requests/hour**; installing a **GitHub App** grants **~15,000/hour**.
- Octopool **shims `gh`** and routes through a service on **Cloudflare**. For a **read-only, non-mutating action on a public repo**, it uses the **GitHub App's token** (not his personal token). For anything **mutating** or not matching that pattern, it falls back to his own token.

He praises how good the tooling is now — Cloudflare especially — noting the agent plus smart models plus browser use can essentially **configure Cloudflare itself** (though you still want to review that it didn't weaken your security settings). General principle restated: **whenever you feel pain, go one level out, ask "what can I do to remove this pain?"** — it'll usually help your whole team and it **compounds**.

### CrapBox — ephemeral cloud test boxes (must-try #2)
As the codebase and features grew, **tests became a major pain** — creeping from ~10s to 30s to minutes; he optimised for his Mac Studio to ~1 min, then everyone with fewer than 40 cores complained their "computers were melting." Shared pain.

Around then he saw a vendor (he references **Blacksmith**) launch a **"test box" concept** — give the agent a little box to run intensive tests/whatever it needs. It was beautiful but **very new and down ~2+ hours/day**, and his team had become so dependent that CI and tests would break and nothing got done during outages. So he built a **wrapper with alternatives**: **CrapBox** (keeping the "crustacean" naming theme).

How CrapBox works:
- Spin up an **ephemeral machine in the cloud**, with your **repo already checked out**, **rsync your changes** in, and **run the tests there** — so you don't pay the heavy CPU cost locally, can use **really beefy hardware**, and **massively parallelise.**
- It uses their main provider and **fails over to AWS / now also Azure** when one is down. It became "universally loved," and community PRs grew its support to **~20 providers.**

Then it expanded well beyond testing:
- **Cross-platform debugging.** Cross-platform is "a lie" — e.g. a Windows-only `EPERM`-type issue despite Node supposedly being cross-platform. Previously he'd lazily wipe such bugs rather than boot his Windows machine. He added **cross-OS support**: tell the agent "test it on all OSes" and it spins up **multiple boxes** (Windows/Linux/macOS, even Red Hat) in **parallel**, scaling "ad infinitum" to raise confidence.
- **UI debugging via VNC.** For UI-specific, browser-specific, OS-specific bugs he added **VNC** ("people already solved that — just add VNC"). The agent opens a browser with **webVNC** in the box, with a browser/terminal (and e.g. Telegram) already waiting, so it can **recreate the exact scenario end-to-end.**
- **Agent-driven computer use.** Since vision models can do it, CrapBox got **screenshot/click/type** tools so the **agent controls the UI itself** in its own box — no human clicking.

### Mantis — visual verification of fixes
Building on CrapBox: he wanted to stop watching the agent and just **watch a video.** **Mantis** is an agent you **ping on a PR**: it spins up the correct boxes, **records a video of the bug**, fixes it, **records a video of the fix**, and **looks at the video to verify** the fix. End-to-end flow: see an issue → ping **Claw Sweeper** to fix it (creates the PR) → **Mantis** does visual verification → he just **watches the video and merges.** "All built based on me being annoyed."

### Auto-review — agent reviews its own code (must-try #1)
He describes the painful manual loop everyone knows: run a prompt, then `/review` because you're unsure; Codex finds three real-sounding issues; you fix and wait 10–20 min; `/review` again finds two *new* issues (it can't surface them all at once); fix, wait, repeat. He once did this **10 times in a single day** (adding LINE support he doesn't even use) and felt like *he* was the agent.

So he built **auto-review.** He expected to need hooks (and could, since Codex is open source) but it turned out **far easier**, because agents follow instructions reliably. The whole mechanism is **one line in `AGENTS.md`**: *before you commit or land a PR, if you haven't done auto-review, run auto-review.* The trick: you can **call the CLI agent from within itself** to get a **fresh context** — Codex calls Codex to run the review — giving the "fresh eyes" that a single long context can't ("good luck" reviewing with fresh eyes inside one context). The result is a reliable system that **automatically runs many review rounds.**

He hit (and fixed) a bug where **Codex kept calling Codex calling Codex** recursively and took forever. He also tuned a **`SKILL.md`** to teach the agent that **not every review finding is valid** — agents surface weird edge cases, so you must encode your project's conditions/invariants (his example: "we don't expect plug-in files to be randomly edited while the system is running," otherwise the agent writes overly defensive code). **Write your invariants into `AGENTS.md`** — *you* know them, the agent doesn't, and its memory is gone each new session, so the more context you give, the better. He went from very long agent files → very short → now **long again but with meaningful content.** And: **don't write the text yourself** — let the agent phrase it in agent-to-agent language; periodically go "meta" and ask the agent what's confusing/contradictory in its own `AGENTS.md` and clean it up, because **confusion is pure token burn and yields worse results.**

> His explicit ask: *"If you only take two ideas from this talk: try auto-review and try CrapBox."* They "totally revolutionised how we build software" and his trust in prompting-and-shipping is much higher.

### Capturing contributor intent (the prompt-upload skill)
A oneline prompt can generate 10 pages of content, so you can't tell how much effort went into a PR. Early on his contributor guidelines **asked people to send their prompts**, but nobody did — no good system, and you can't beat people's laziness. The fix: an **OpenClaw skill** so that when a contributor sends a PR, **their agent asks** "want to send a **privacy-filtered** version of the prompt? If you do, we'll review your PR faster." On "yes," the agent **finds its own transcript on disk, trims it to the interesting parts, and attaches it to the PR.** Now he has a far better signal of **effort** — distinguishing a 5-token "fix issue #N" from hours of real discussion, i.e. **total slop vs. "good slop."** He notes he could've built this six months earlier; it just never occurred to him how easy it was. **"We're not limited by intelligence anymore — the models are good enough. What limits us now is our own imagination."**

### CorePatch — reviewing million-line codebases
Auto-review made him feel guilty about all the code he'd shipped *without* review — even with a strong **GPT-5.5-class model**, large/difficult changes hide bugs the agent only finds over multiple review rounds. But you **can't `/review` a million-line project** — too much for any context. So he built **CorePatch**: take a big project **apart into ~50 subsections** (however you can separate it), have the agent **review each separately**, and you'll "find a lot of interesting things." It's not as perfect as reviewing an actual changeset (true coverage would need thousands of Codex sessions, a problem even with unlimited tokens), but it's **great for cleaning up codebases.** Still unfinished.

### CrapFleet — multiplayer Codex
The last tool. He hated being the **intermediary** when a teammate copy-pastes between their coding agent and chat while he comments. He wanted to **talk to their agent directly.** Since CrapBox already runs tests in a box, **Codex can run in there too** → **CrapFleet = multiplayer Codex.** He can **send a maintainer a link to a session** so they can **view it, talk to it, or take it over** — "multiplayer clanking."

### ClickClock — they accidentally rebuilt Slack
Testing OpenClaw's many message channels end-to-end was hard — complex APIs are easier to understand in a UI. But automating real chat platforms in a fresh Linux cloud box triggered **Cloudflare CAPTCHAs / anti-bot defenses** (an unattended Linux box "feels like someone trying to hack their system"). Understandable, but it blocked real end-to-end tests. So they **built their own messaging platform** they fully control for end-to-end testing — which "got a little out of hand" and became a **backup chat system** for when their primary team chat is down. It's called **ClickClock**.

### Closing & Q&A
He wraps with the through-line: *"Listen to your body, listen when you're annoyed."* **Annoyance is an amazing signal that something can be automated**, and **every automation compounds** — all these oddly-named little tools work together (reports rely on the crawler; CrapFleet relies on CrapBox), letting a **very small team ship a massive codebase**. There are many more crawlers/tools he didn't show.

**Q&A:**
- *"As you build this ecosystem and get more 'enterprise,' do dependencies between your tools ever get in the way of improving them?"* — Hasn't happened yet. It's **less about dependencies, more that the tools compound and make building new tools faster.** A general agent trick: **if you've solved something once, point the agent at where you solved it** — agents are excellent at pattern-matching, so it really compounds. When something doesn't work out, you learn from it (e.g. the token/Octopool tool's first version ran on his machine and was awkward with the GitHub App, so he iterated, then told the agent "remove this feature, rebuild with this new idea, but take that part from that other tool" — reusing prior work saves the prompting; agents are smart at reading the git history to figure out context). Even better, just press the **Whisper Flow** voice button and *talk* about it — sometimes the team just discusses out loud, he presses the button, and **Codex listens in and starts building during the conversation**, clever enough to tell a joke aside from the important bits. **"You can just do stuff."**
- *"As a busy solutions engineer with a billion things on my plate, I love building my own agents but I simply don't have time to build tools to save time."* — He invokes the **"square wheels" meme** (people too busy pushing a cart on square wheels to adopt round ones). The point: **these tools can be massive slop** — literally tell Codex *"look at this session, see the pain I had, build me a tool that reduces it, this is just a rough idea."* You don't even need to specify the language or anything (he uses **Go** — admits he doesn't even like Go, but his agents are fast in it, "so who cares"). Do it **on the side**; there's always a spare corner/window for little experiments — it brings the fun back **and it compounds.**

> [!tip] The mantra
> "Any problem is just a prompt away." / "You can just do stuff." / "We're not limited by intelligence anymore — only by our imagination."

## 🛠️ Products / Features / Technologies Mentioned
- **OpenClaw** — the large open-source project being maintained; the subject of all the tooling.
- **Codex** — the AI coding agent (cloud + CLI) doing the actual work; the agent he calls recursively (Codex-calls-Codex).
- **GPT-5.5-class model** ("GBT 5.4 / GBD55" as garbled) — the model referenced as "really good" but still missing bugs on large/hard changes.
- **`vision.md`** — per-project file stating what the project *does* and *does not* want; read by the agent's standard prompt to drive triage decisions.
- **`AGENTS.md`** — agent instruction file; holds the one-line auto-review rule and project invariants. Evolved long → short → meaningfully long.
- **`SKILL.md` / OpenClaw "skills"** — tuned instructions teaching the agent which review findings are valid; also powers the contributor prompt-upload flow.
- **Claw Sweeper** — GitHub Action that fires Codex on every issue/PR to auto-comment/close per the vision rules; re-runs weekly; Discord-integrated; has a dashboard.
- **GOG** — homemade **Google CLI** giving agents full Google access (Gmail/Calendar/etc.) across accounts; supports end-to-end self-testing via a demo account.
- **Maintainer reports / dashboard** — private analytics combining GitHub *and* Discord activity to judge maintainer contribution and surface what needs attention.
- **Discord crawler** — pulls Discord data; later hooked to Codex for prioritisation; backs data up to GitHub as an alternative data source.
- **Issue browser** — homemade tool to select/parse issue text in any format and click through prioritised work fast.
- **Release Bar** — dashboard of release readiness across projects (e.g. days since last release, pending PRs); filterable to what needs attention.
- **Octopool** — shims `gh` and routes read-only/non-mutating public-repo calls through a **Cloudflare**-hosted **GitHub App** token (~15k/hr) instead of the personal token (~5k/hr) to beat rate limits.
- **Cloudflare** — hosting/edge for Octopool; praised as agent-configurable via smart models + browser use.
- **GitHub Actions / GitHub Apps** — automation runtime and the higher rate-limit token source.
- **CrapBox** — ephemeral cloud test boxes: repo pre-checked-out, rsync changes, run heavy/parallel tests on beefy hardware; multi-provider failover (main → AWS → Azure), ~20 providers; cross-OS boxes (Win/Linux/macOS/Red Hat); **VNC/webVNC** UI debugging; agent computer-use (screenshot/click/type).
- **VNC / webVNC** — added to CrapBox to recreate and debug UI/browser/OS-specific issues end-to-end.
- **Mantis** — agent pinged on a PR that spins up boxes, records before/after videos of bug & fix, and visually verifies the fix.
- **CorePatch** — splits a huge (million-line) codebase into ~50 subsections so the agent can review each separately; good for cleanup; unfinished.
- **CrapFleet** — runs Codex inside CrapBox to enable **multiplayer Codex**: share a session link so maintainers can view/talk-to/take-over a session.
- **ClickClock** — self-built messaging platform (originally to enable controlled end-to-end chat testing without anti-bot CAPTCHAs), now also a backup team chat.
- **Whisper Flow** — voice/speech-to-text button used to talk to Codex; can listen in on a live team conversation and start building.
- **Go (Golang)** — preferred language for throwaway tools purely because agents are fast in it.
- **Node.js** — underlying runtime of OpenClaw; cited re: "cross-platform is a lie" Windows `EPERM` bugs.
- **Blacksmith** — third-party vendor whose "test box" concept inspired CrapBox; its early instability/downtime prompted building a wrapper.
- **CodeRabbit, Greptile ("grab")** — existing AI review tools he tried; good for reviews but didn't auto-group/close issues, prompting Claw Sweeper.
- **Slack** — the chat platform they effectively (accidentally) rebuilt as ClickClock for testing/backup.

## 🚀 Announcements / What's New
None explicitly announced as Microsoft product releases/previews/GA. This is an experience/philosophy talk, not a product-launch session. Everything shown is the speaker's own homemade open-source/internal tooling for maintaining **OpenClaw** (Claw Sweeper, GOG, Octopool, CrapBox, Mantis, CorePatch, CrapFleet, ClickClock, Release Bar) — presented as personal "slop" tools, with CorePatch noted as not yet finished. No version numbers, GA/preview status, or roadmap commitments were stated.

## 💡 Demos
The whole talk is a live, screen-driven tour (improvisational, with "let's see if this works" moments). Notable on-screen demonstrations and the point each proved:
- **The "slop" tools website** — a catalogue of all the little tools built to build OpenClaw → proves the sheer volume of friction-driven tooling and that the polish doesn't matter.
- **Claw Sweeper dashboard** ("18 Codex working right now") — shows the long explanatory comment + array of issues to solve → proves issue triage/closing is fully automatable at scale (~15k issues closed).
- **Projects-folder Codex prompt** ("what should I work on?") — enumerates all repos + open issues → proves working "one level above" the project.
- **Issue browser** — select text → parsed, agent pre-selects "do these 8, skip these 2" → proves micro-friction removal compounds focus.
- **GOG / Gmail draft + calendar features** — spotted mid-demo → proves owning the stack lets the agent add *and* end-to-end-verify features.
- **Octopool** ("let's see if this actually works") — `gh` shim routing through Cloudflare/GitHub App → proves the 5k→15k token rate-limit workaround.
- **Release Bar** — filter by days-since-last-release → proves at-a-glance release/attention triage across many projects.
- **CrapBox** — ephemeral boxes running tests, fanning out across OSes/providers, with VNC and agent computer-use → proves offloaded, parallel, cross-platform, UI-capable testing.
- **Mantis** — ping on PR → before/after bug videos + visual verification → proves end-to-end visual fix verification with the human only watching a video.
- **Implied auto-review / CrapFleet / ClickClock** walkthroughs supporting each tool's narrative.

## 📊 Notable Stats / Quotes
**Stats**
- **>10,000** issues open at peak (GitHub display caps at **5,000**).
- **~15,000** issues closed via Claw Sweeper.
- Personal GitHub rate limit **~5,000 req/hr** → GitHub App **~15,000 req/hr** (Octopool's whole basis).
- Test runtime crept **10s → 30s → minutes → ~5 min**, optimised to **~1 min** on a 40-core Mac Studio (melting smaller machines).
- CrapBox failover providers grew to **~20** via community PRs.
- CorePatch splits a project into **~50** subsections; full changeset coverage would need **thousands** of Codex sessions.
- He once ran the manual `/review` loop **10 times in one day** (adding LINE support).
- Coding agents: **<1 year** old, **~6 months** since they got "good."

**Quotes**
- "It's still called a pull request. I call it a **prompt request**."
- "Your job should be: **what can I do to help my agent build software faster** — and even more, it's all about **closing the loop**."
- "**Any problem is just a prompt away.** Building this thing is never the hard thing; **maintaining** the thing is the hard thing."
- "**Listen to your body. Listen when you're annoyed.** Annoyance is an amazing signal that we can automate this."
- "You need to **build the tools to build the tools**."
- "**We're not limited anymore by intelligence... everything we're limited by is our own imagination.**"
- "If you only take two ideas from this talk: **try auto-review and try CrapBox.**"
- "My slop is better than your slop."
- "**You can just do stuff.**"
- (On AI volume) "Let's not pretend any of that is written by humans anymore... **you can't fight the world; you have to figure out a way to deal with it.**"

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] Add a **one-line auto-review rule to `AGENTS.md`** ("before commit/landing a PR, run auto-review") and have the CLI agent call itself for a fresh-context review loop.
  - [ ] Stand up an **ephemeral cloud test box** (CrapBox-style): repo pre-checked-out, rsync changes, run heavy/parallel tests off-machine; add OS/provider fan-out + VNC for UI bugs.
  - [ ] Keep a **`vision.md`** per repo (explicit want/don't-want) and wire it into the standard agent prompt for triage.
  - [ ] Write project **invariants** into `AGENTS.md`; periodically ask the agent to flag confusing/contradictory instructions and clean them (reduce token burn).
  - [ ] Adopt the **"annoyance → build a throwaway tool" reflex**; let the agent build it in any language (speed of agent > your language preference).
- [ ] Questions:
  - [ ] How are tokens/cost actually governed at "infinite tokens" scale — what would a budgeted version of Claw Sweeper look like?
  - [ ] Security review process for agent-configured infra (Cloudflare/Octopool) — how to catch a weakened security setting?
  - [ ] Which of these tools (if any) are/will be open-sourced or usable outside OpenClaw?
- [ ] Relevant to:
  - [ ] Our own agent/dev tooling, CI/test offloading, and OpenClaw workflows.
  - [ ] Open-source/issue-triage automation and maintainer dashboards.

## 🔗 Related
- [[2026 Build Session List]]
- 