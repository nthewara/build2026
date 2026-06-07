---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/engineering
  - topic/ai
  - topic/devex
source: https://www.youtube.com/watch?v=QyX2w7Mr-iE
session_code: BRK244
event: Microsoft Build 2026
speakers: Swyx (Shawn Wang) — Founder, Latent Space & AI Engineer; Advisor, Cognition
duration_min: 36
aliases:
  - Agent supervision is the new senior engineering skill
---

# BRK244 — Agent supervision is the new senior engineering skill

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Swyx (Shawn Wang) — Founder of Latent Space & the AI Engineer community/conferences; advisor to Cognition; host of the Latent Space podcast  
> **Duration:** ~36 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=QyX2w7Mr-iE)

## 🎯 TL;DR
Swyx argues that the unit of work for engineers has shifted from writing code to **supervising swarms of coding agents**, and that the entire industry has independently converged ("carcinized") on the same UI — the **agent command center / conductor** form factor. The real differentiator is no longer the model (you can leak Claude Code's source and nothing changes) nor the harness, but your ability to **orchestrate many agents and achieve human↔agent "mind meld."** He walks the audience through what he considers *guaranteed* over the next ~2 years — agents writing the majority of code, the death of code review (the "dark factory"), spec-driven development as the new programming, a coming **CPU shortage**, and hardware delivering **hundreds of thousands of tokens/sec** — versus what is still *speculative research* (real-time/low-latency interaction, memory & continual learning, world models, agentic video/everything). His through-line: what happened to coding last year is now happening to *all* knowledge work, and "agent supervision" is the senior skill that survives.

## 🔑 Key Takeaways
- **Everything is converging on the "conductor" / agent command center.** Conductor pioneered the form factor; Cursor, Windsurf, Codex, GitHub Copilot (new app) and even Cognition all rebranded into the same thing — "convergent evolution," like how nature reinvented the crab ~7 times.
- **The moat is neither the model nor the harness.** Leaking Claude Code's full source changed nothing — Anthropic still becomes a trillion-dollar company; rival harness makers said the leak only *validated* they had the same approach. The moat is **multi-agent orchestration + human↔agent alignment.**
- **"Model religion" is over → it's now model + harness.** Developers gain real influence by *shaping the harness* (MCPs, skills, workflows) — not just prompts — which demands new UIs beyond chat.
- **A real economic/capability phase transition happened ~late 2025.** Agent autonomy jumped from ~1–2 hour tasks to **10–12h and even 20–24h tasks** (a ~10x in autonomous capability), which unlocks entirely new UX. Swyx frames it like a new "WTF happened in 1971" inflection.
- **Agent-written code is exploding.** Claude Code's attributable share of GitHub commits hit ~4–5% (Feb), likely ~10% now, on track for ~50% by end of year. The GitHub COO cited **~14,000x (14,000×) year-on-year commit growth** from agent attribution.
- **The SDLC is collapsing stage by stage:** the *idea* is dying (Steve Yegge's prediction), **PRs → "prompt requests"** (maintainers want intent, not your code), and code review itself is next.
- **The "dark factory" is coming:** a software factory with **no human reviewers** in the loop — scary but demanded by multi-agent scale. Today it's fringe; "fringe last year becomes normal this year."
- **We have superhuman *coders* but not superhuman *reviewers*** — mostly a *communication* bottleneck (no high-bandwidth neural link), so agents guess intent and sometimes guess wrong. The fix is **fast cycles → fast feedback → strong alignment** (e.g. enforce <1 min compile times).
- **Spec-driven development is the new programming.** OpenAI's open-sourced **Symphony** is ~2,000 lines of markdown prompts — a "gold-standard spec" focused on the **"narrow waist"** (API contracts, module surfaces, types/data structures) to contain model entropy.
- **"Goal/Ralph loops" redefine instruction:** you don't tell the agent *how* to do the task — you tell it *how you'll evaluate it and when to stop.* This enables closed-loop self-verification.
- **An infrastructure shift is mathematically locked in:** GPU:CPU ratio moving from ~8:1 toward **1:1** as agents do massive CPU-bound work → a **coming CPU shortage**, not just GPU (per Intel CEO Lip-Bu Tan; Sam Altman: now an "inference company").
- **Inference speed is about to 10x repeatedly.** Today ~50–100 tok/s; Cerebras and others already do thousands; **Tâlus demoed ~17,000 tok/s** (vs H200/B200/Groq/Cerebras). Swyx is "highly convinced" a **300,000 tok/s** world for commodity tokens is coming — this is **hardware/optimization, not research.**
- **Chips now last longer; their terminal value is rising.** Old amortization ~3–4 years → now ~8; people still run GPT-4.1 / Llama 3 because working open-weight apps "only get cheaper and faster." H100 average price has *melted up*.
- **Model sizes keep creeping up:** "small" went 2B → 7B → **24B (Mistral Small)**; "small" may eventually mean ~100B. Top-end went from ~1T params (GPT-4 class) to **10T+** — but we're running out of orders of magnitude.
- **Coding is just the preview — the real story is *all* knowledge work.** Agents are generalizing into unverifiable domains (browsing/computer use, design, video). Developers are "privileged" to live this future first.
- **The frontier research grand prizes (speculative):** **real-time / low-latency interaction** (the GPT-4o voice we were promised but never got), **memory & continual learning**, **world models** (theory-of-mind of what *you* want), and **agentic everything** (video agents orchestrating video models).
- **The "agent work paradox":** agents do more work than ever, yet humans work harder than ever — and that's normalized. Swyx's self-serving thesis: **AI engineering is "the last job"** because you're the one automating all the others.

## 📚 Detailed Notes

### Framing: everything is becoming a "conductor" (carcinization of agent UIs)
Swyx opens (semi-provocatively) by poking fun at Microsoft's recently launched **GitHub Copilot app** — the big rebrand of what Copilot can be *beyond VS Code* — noting it looks strikingly similar to other recently launched apps. His thesis: **Conductor** was first to the "agent's command center" form factor, and then **Cursor, Windsurf, Codex, and GitHub** all rebranded into the same shape. Even **Cognition** (the company he advises) shipped its own agent command center *the day before* the talk, complete with **local-to-cloud handoff** features.

He frames this not as a failure of imagination but as **convergent evolution** — "everything becoming a crab." Carcinization: nature independently reinvented the crab body plan at least ~7 times; the industry has independently reinvented the agent command center because it's simply **the form factor everyone agreed to converge on.**

The deeper point: the **level of abstraction is shifting from managing individual agents to orchestrating many.** The progression he describes:
1. Autocomplete →
2. Managing individual terminals →
3. `tmux`-ing 12 terminals at once (chaotic) →
4. Something "more civilized and organized" — the command center, multiplexing across Cursor, Claude Code instances, etc.

(He jokes mid-talk that he just published his GitHub tokens on screen and needs to rotate them — a running gag, since the session is recorded.)

### Six core themes from the AI engineer community
Swyx has spent his career organizing the **AI engineer community** (Paris, London, Miami, Singapore) and has watched an "explosion" over the last year. He distills ~six contributing themes shaping where things are going:

- **Anxiety / "FOMAT" — Fear Of Missing Agent Time.** People do *polyphasic sleep*, waking at 2am to kick off another agent run before bed. The compulsion to keep agents busy is real.
- **Model religion is dead → model + harness.** The old "big model" belief gave way to a **model + harness combination**, which is *good for developers* because you can exert strong influence by **shaping the harness** — formerly via prompts, now via **MCPs, skills, workflows**, and more. This requires a **different UI than chat.**
- **Labs are shipping harnesses, increasingly swarm-oriented.** Model labs are transitioning from "ship the pure model" to shipping harnesses. Examples: **Kimi K2** putting out *hundreds of parallel swarms*; **Anthropic** releasing an "embarrassingly parallel" feature to port its **million-line Zig codebase into Rust.** A sign of things to come.
- **Lots of humans will still be employed here** — job security exists. Tellingly, **the agent codebase itself isn't the value:** you can leak the *entire* Claude Code source and *nothing changes.* Anthropic still becomes a trillion-dollar company; rival harness makers told Swyx (on his podcast) the leak just **validated** that they'd independently discovered the same things — "no secret sauce."
- **Therefore the moat is elsewhere:** not the model, not the harness, but **orchestrating multiple agents** and doing the **human↔agent "mind meld."**
- **Hands-off model work is newly possible** — the enabling shift (see below).

### The late-2025 capability phase transition
Swyx references **"WTF Happened in 1971"** (a famous economics site documenting sharp 50-year econ transitions) and argues **another such inflection just happened — around late 2025**, and we're now living its implications.

The mechanism: models moved from **requiring heavy human-in-the-loop** to autonomous long-horizon work. He cites **METR**-style measurement: capability jumped from **1–2 hour tasks to 10–12 hour and 20–24+ hour tasks.** That ~**10x in autonomous capability** is what unlocks fundamentally **different UX** — you can now dispatch work and walk away.

**Evidence in the wild (GitHub):**
- **Claude Code commit attribution** on GitHub rose to **~4–5% as of February**, "probably ~10% right now," on a trajectory to **~50% by end of year** (and that's *just* Claude Code — add Codex, Copilot, and other coding agents).
- The **GitHub COO** (Swyx's podcast guest the day before) cited **~14,000x (14,000×) year-on-year commit growth** attributable to agents.

He stresses this isn't only coding: agents are also tackling **unverifiable domains** — general browsing/computer use *and design* — and the training focus on **generalization** means these capabilities are breaking out of the "verifiable domains only" assumption.

### The collapsing SDLC: idea → PRs → code review
Swyx traces the software development life cycle being eaten stage by stage:

- **The idea is dying.** He curated a "prescient" talk by **Steve Yegge** (creator of "Gastown"/Gas Town; author of the legendary **Platform Rant**) predicting at end of 2026 that **"the idea" would die in 2026** — which Swyx says basically came true, with the "everything is a conductor" carcinization trend arriving right after. (He notes the irony of Yegge's Platform Rant lore alongside interviewing **Satya** about turning Microsoft into an **AI platform**.)
- **PRs → "prompt requests."** Pull requests exist because you "can't be trusted to review your own." Two flavors:
  - **Open source** (most at threat) — the vector for malicious or misaligned PRs.
  - **Internal teams.**
  Instead of pull requests, send **prompt requests**: maintainers adapt your **intent**, because "they don't need your code anymore."
- **Goal loops & self-verification.** With agents coding ~14x more than last year, the next frontier is **goal loops** — the **"Ralph Wiggum loop"** went viral last year and is now adopted by every major coding agent. This leads to a **closed loop where coding agents verify their own work** (work Cognition is doing).
- **Death of code review → the "dark factory."** Borrowing from manufacturing's "software factory / token factory":
  - **Light factory** = humans reviewing the output.
  - **Dark factory** = **no humans reviewing** — lights-off automated software production.
  Swyx calls the dark factory "very, very scary" yet inevitable, because human review is **the** remaining bottleneck for multi-agent orchestration.

### Q&A — hardening the dark factory (the external loop)
An attendee asks: in a dark-factory scenario, what's the **hardening at the end** — for audit/compliance, user acceptance, and change management? Swyx splits it into the **internal loop** (producing code) and **external loop** (user acceptance/validation):
- You need a **strong spec** defining what to converge to — the work shifts "one level above raw code delivery" because the hard problem becomes **how you validate.**
- He cites a **"Swiss cheese model"** (a top Latent Space contributor post of the year): combine a strong **specification** *and* a strong **test suite** to guard against regressions — but that's **not enough.**
- Add **online eval** of what you ship, plus **feature flagging** for **progressive rollouts.** These are "just good software engineering practices anyway," but they become **far more important** because a 10-person team is now shipping at **Uber/Facebook scale** — you've pulled forward large-org engineering discipline because you effectively *are* a large engineering org (made of agents).
- The audience pushes: you can only scale so far with humans in the room; there must be a **higher-order, more scalable** thing to evaluate. Swyx agrees this is the open frontier.

### Harness engineering & the OpenAI "Symphony" gold-standard spec
Swyx points to **Ryan (Apollo-/research-side, working on the dark factory)** — referenced as "Ryan Levesque/Apollo, OpenAI" in the captions — who wrote a piece on **harness engineering**: shipping **~1 billion tokens/day (~$10,000/day)** with **no human review.** OpenAI **open-sourced "Symphony,"** which has "a very strong structure." (He notes others innovating in dark-factory space too, e.g. **StrongDM**.)

Key reframing on **"goal":** *Goal is when you don't tell the agent how to do it — you tell it how you're about to evaluate it and when it should stop.* That's a primitive form of what a human reviewer does; you're just **taking the time to write it down** (the Ralph/goal loop).

**Why fast cycles matter:** despite a million LOC and a large app, the Symphony team **insists on <1-minute compile time** — something Swyx says he never had professionally. With agents you *can* take a daily "garbage-collection pause" to cut all build times, because **fast cycles → fast feedback → strong human↔agent alignment.** Critically: **"we have superhuman coders but not superhuman reviewers yet,"** and that's largely **not the agents' fault** — it's a **communication-bandwidth** problem (no "neural link" to plug intent into the machine), so agents guess and sometimes guess wrong.

**What Symphony actually looks like:** a **giant list of markdown files** — you "program with markdown and English." It tracks everything down to the list, focusing on the **"narrow waist"** of any program: **API contracts, surfaces between modules, types, and data structures** — because everything else can be derived from those. A narrow waist **contains the entropy** models inherently cause and gives you a way to verify you're not veering off course. It's **~2,000 lines of pure prompts** — a "**gold-standard spec.**" Most people (including Swyx) write ~200 lines "if lucky," but this is the **shape of fully-automated development.**

**The Microsoft vision (Swyx's read):** today you rent frontier models (GPTs, Claude), but ultimately you'll have **your own personal/company model trained on your spec**, so you won't need the expensive frontier models. A good **agent platform should be *your* friend, not OpenAI's friend** — "someone needs to be on your side." This is the crux of his **"agent labs vs. model labs"** debate.

### The eight levels of agent adoption (Steve Yegge / Gas Town → Gas City)
Swyx recommends Yegge's **Gas Town** post on the **eight levels of "fully LLM psychosis"** adoption. Rough progression:
1. Single coding agent →
2. **Multi-agent** (where *most people in the room* are, if up to speed) →
3. **Building your own orchestrator** (what Yegge is now doing with **"Gas City"** instead of Gas Town).

He stresses the timeline compression: Yegge said this in **November**, and it became **true around March** — "it's not that far ahead."

### Sandboxes: the unsexy but critical infrastructure need
Not a "sexy ML topic" like GRPO or RL — just: **agents need their own computers.** You must **fork agents into safe environments**; a new Git branch isn't enough — you need a **full fork of the entire environment.** Swyx calls this **"the Kubernetes problem on crack":** Kubernetes was built to **keep things alive**, but agent sandboxes need to be **extremely serverless / ephemeral** — fork, run, tear down. Current programming paradigms aren't well-adjusted for this.

### The coming CPU shortage (infrastructure ratios are flipping)
The compute mix is shifting. Historically: mostly **training**, a little **inference**, with a **GPU:CPU ratio ~8:1** (cited from **Intel CEO Lip-Bu Tan's** most recent earnings call). With agents, the ratio is moving toward **1:1 GPU:CPU** — which is why there's a **coming CPU shortage, not just a GPU shortage.** He backs this with **Sam Altman** (a few months prior) saying AI is now **"to a very significant degree an inference company," not just training.**

### Inference speed: the 10x staircase toward 300,000 tok/s
For massively parallel agents, you want them to **finish as fast as possible.** Reference points:
- **Typical inference today:** ~**50–100 tokens/sec** (know your own number).
- **Cognition + Cerebras** collaboration: thousands of tok/s (mentions versions ~31.5 / 32 coming).
- **Tâlus** (captioned "Talas") made a **public demo this year** plotting tokens/sec across **Nvidia H200, B200, Groq, and Cerebras** (the supposed "fast ones") — with **Tâlus at ~17,000 tokens/sec.** Swyx has *seen this himself*; not an exaggeration.
- **Projection:** a **300,000 tokens/sec** world is coming — **for commodity token logic, not frontier reasoning.** Current demos run **Llama 8B**, but this proceeds to **30B** and eventually **hundreds of B.** At some saturation point, intelligence becomes **functionally instant** for the vast majority of work.

Crucially: **none of this is research — it's all hardware/optimization** ("the highest-stakes poker game I've ever seen," played with billions of dollars). When asked "what pushes us from here — the next model or hardware?" Swyx is firm: **all hardware.** The most interesting *speed* research actually comes from the **image/video-gen community**; the language/coding side is mostly quantization and numerical-precision work. Every **10x changes usage habits, the products you can build, and your open-vs-closed-model choices** — so plan for "cool demo now, normal in a year."

### Q&A — etching models onto silicon (and chip longevity)
An attendee (referencing **Mark's** talk on specializing vs. generalizing) asks: if you **etch a model onto silicon** but hardware life cycles are 5–6 years while the model is irrelevant in ~1 year, how does that reconcile? Swyx clarifies a common misconception:
- **Most fast-inference players are NOT burning weights onto silicon** — **only Cerebras** is etching actual weights right now.
- There were **three generations** of specialized-inference companies: a **first generation that largely failed**, a **second generation** (**Cerebras, Groq**) "getting paid," and a **third generation** doing it "white hat" by **not** taking the short-term win of **burning weights in.**
- **The tail is very long:** people still run **GPT-4.1** and **Llama 3.** The whole point of **open weights** is that **you own them and no one moves your cheese** — if the app works, why change it? It only gets **cheaper and faster.**
- Therefore the **terminal value of a chip is increasing.** Old "tokenomics" (Latent Space, ~2 years ago) put chip amortization at **3–4 years; now closer to 8.** The **average H100 price has melted up** (old norm was rapid chip deprecation — a "hot potato" you'd never start a cloud on; now a ~4-year-old chip holds value because software keeps extracting more inference from general-purpose hardware).

### Model sizes keep creeping up
There's a **fundamental limit to compression**, so models keep getting larger. "Small" has drifted: **2B → 1B → 7B → 24B** today (**Mistral Small is 24B**, per Mistral's Chief Scientist on the podcast), and may eventually mean **~100B.** At the top end, we've gone from **~1 trillion params (GPT-4 class)** to **10T+** (Mistral-class top end) — but **we don't have many orders of magnitude left to go.**

### The research frontier (the speculative ~4-minutes)
Everything above is "guaranteed — set your clock by it for ~2 years." The **research agenda** (un-equally weighted) is what's *uncertain*:

- **Memory & continual learning** — you'll *hear about it for 5 years* but likely **not see huge change soon**; very speculative.
- **Real-time / low-latency interaction (the king, happening NOW).** This is the **low-latency voice promised by the GPT-4o demo that we never got.** Swyx wrote about the **"semi-async valley of death"**: an **uncanny-valley latency zone** where you sit watching the AI without really thinking or adding value, unable to context-switch. The cure is to live at the **two extremes**:
  - **Stay in flow / very fast** (deep work, your highest-value main thread), or
  - **Go fully async** (dispatch background agents, with a good system to work with them).
  There's "no room in between." All recent model progress has been **more reasoning** (2h → 15h autonomy), but **nobody has driven latency from 2,000ms → 200ms → 20ms.** The few people doing truly-interactive small models (he highlights interaction-focused small models, not yet released — only demo videos) prove there's *alpha* here. You can partly *cheat* on latency with hardware (buy a 300,000 tok/s chip), but that's **not truly interactive** — it still tries to inference ~100,000 reasoning tokens before answering. **Truly interactive** means **micro-batches of interaction are modeled in the training data itself**, enabling live **human↔machine mind meld**; it'll *seem* smarter simply because it better aligns with what you wanted.
- **Agents are eating everything (agentic everything).** From an XAI podcast: people think video generation = prompt → single forward pass through a video model. It's about to become **video agents** — agents *orchestrating* the video model. It sounds trivial ("I could do that") but most underestimate what it takes to **train the orchestrator for specific domains** like video agents — and similarly for **all other modalities.**
- **World models (the dark horse).** Models currently predict what the **median RLHF person / RL environment** is likely to reward. A **world model of what *you* specifically want/like** is the **second-level intelligence** — **presence of mind / theory of mind** — that's largely missing today. Solving any of these research directions changes how we use models.

### Closing: the "agent work paradox" and the last job
Swyx ends on the **agent work paradox**: **agents are doing more work than ever, yet we're working harder than ever** — and that's **okay and normal.** He explicitly **normalizes the stress** ("I'm also stressed out; you all feel it too"). It's rewarding precisely because **we're first to feel it** — bearing the brunt of the **compression of the future.** His (admittedly self-serving) conclusion: **AI engineering is "the last job,"** because **you're the ones automating all the other jobs away** — so "you guys are in good hands." [applause]

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot app** — Microsoft's new standalone Copilot app (beyond VS Code); the rebrand that prompted Swyx's "everything is a conductor" framing.
- **Conductor** — first mover on the "agent command center" form factor that everyone copied.
- **Cursor / Windsurf / Codex** — coding tools that all rebranded into the agent-command-center form factor.
- **Cognition** — AI agent company Swyx advises; shipped its own agent command center (with local↔cloud handoff) the day before the talk; building closed-loop self-verifying coding agents; partnering with Cerebras on fast inference.
- **Claude Code (Anthropic)** — coding agent with clear GitHub commit attribution (~4–5% in Feb → trending toward 50%); its full source was leaked yet changed nothing competitively.
- **OpenAI Codex** — coding agent; OpenAI announced merging Codex into ChatGPT.
- **OpenAI Symphony** — open-sourced harness/spec framework; a giant set of markdown files (~2,000 lines of prompts) representing a "gold-standard spec."
- **Kimi K2 / K2.5 (Moonshot)** — model running hundreds of parallel swarms; example of fast open-weight inference potential.
- **MCPs / skills / workflows** — harness components that let developers shape agent behavior beyond prompts.
- **Ralph Wiggum loop / goal loops** — autonomous goal-driven self-verification loops now adopted by major coding agents.
- **Gas Town / Gas City (Steve Yegge)** — Yegge's agent-orchestration projects; Gas Town post documents the eight levels of agent adoption.
- **Cerebras** — fast-inference hardware doing thousands of tok/s; the only player currently etching actual weights onto silicon.
- **Groq** — fast-inference chip company ("second generation" getting paid).
- **Tâlus** (captioned "Talas") — public 2026 demo hitting ~17,000 tok/s, beating H200/B200/Groq/Cerebras.
- **Nvidia H100 / H200 / B200** — GPUs referenced for inference speed and chip-pricing/longevity discussion.
- **Llama 8B / Llama 3** — small open model used in fast-inference demos; Llama 3 still in production use (long tail).
- **GPT-4.1 / GPT-4 / GPT-4o** — frontier models referenced for long tail (4.1 still used), top-end param counts (GPT-4 ~1T), and the unfulfilled low-latency voice promise (4o demo).
- **Mistral Small (24B)** — example that "small" models are now 24B; Mistral's top end cited at 10T+ params.
- **StrongDM** — cited as another company innovating in the dark-factory space.
- **METR** — referenced for the autonomy-time measurements (1–2h → 10–24h tasks).
- **Latent Space / AI Engineer** — Swyx's publication, podcast, and conference/community.

## 🚀 Announcements / What's New
This was an opinion/trends + Q&A talk, not a product-launch session. Items *referenced* as recent news (announced elsewhere, not by Swyx here):
- **OpenAI merging Codex into ChatGPT** — announced by the OpenAI team the day before (Swyx relays it as a "fun fact," not his own announcement).
- **Cognition's agent command center** — shipped the day before the talk (with local-to-cloud handoff).
- **GitHub Copilot app** — launched "a couple weeks ago."
- **OpenAI Symphony** — recently open-sourced harness/spec framework.
- No *new* Microsoft product/feature was announced within this session itself. **None explicitly announced by the speaker.**

## 💡 Demos
This was a discussion/Q&A talk rather than a build-along, but Swyx pulled several artifacts up live on screen to make his points:
- **OpenAI Symphony spec walkthrough** — opened the open-sourced Symphony repo live and scrolled its "giant list of markdown files," highlighting that the structure tracks the **narrow waist** of a program (API contracts, module surfaces, types/data structures) and that the example spec is "like 2,000 lines of just prompts" — a "gold standard" spec versus the ~200 lines most people write.
- **Tâlus inference-speed chart** — showed a tokens/second comparison chart pitting Tâlus against NVIDIA H200/B200, Groq, and Cerebras, with Tâlus at **~17,000 tok/s** (on Llama 8B), used to argue a near-future of **~300,000 tok/s** commodity-token inference.
- **H100 price time series** — pulled up a blog chart of average H100 pricing "melting up," illustrating that chip terminal value/amortization has stretched from ~3–4 years toward ~8 years.
- **Steve Yegge "Gas Town" 8-levels visual** — displayed the progression-of-agent-adoption graphic (single coding agent → multi-agent → building your own orchestrator / "Gas City"), placing "most of the room" at the multi-agent stage.

## 📊 Notable Stats / Quotes
- **Agent autonomy:** ~**1–2 hour** tasks → **10–12h** and **20–24h+** tasks (a ~10x jump, ~late 2025).
- **Claude Code GitHub commit share:** ~**4–5%** (Feb) → "~**10%** now" → trending to **~50%** by end of year.
- **GitHub COO:** **~14,000× (14,000x)** year-on-year commit growth attributable to agents.
- **Harness engineering scale:** ~**1 billion tokens/day ≈ ~$10,000/day** with **0% human review.**
- **Compile-time discipline:** Symphony enforces **<1 minute** compile time on a **million-LOC** app.
- **GPU:CPU ratio** shifting from **~8:1 → ~1:1** → a **coming CPU shortage** (Intel CEO Lip-Bu Tan).
- **Inference speed:** typical **~50–100 tok/s**; **Tâlus ~17,000 tok/s** demo; projected **~300,000 tok/s** for commodity tokens.
- **Chip amortization:** **3–4 years → ~8 years**; H100 average price has **"melted up."**
- **Model sizes:** "small" = **2B → 7B → 24B** (Mistral Small); top end **~1T (GPT-4) → 10T+** (Mistral class).
- **"You can leak the entire source code of Claude Code and nothing changes."** — the moat isn't the harness.
- **"We have superhuman coders but we don't have superhuman reviewers yet."**
- **"FOMAT — fear of missing agent time."**
- **"Goal is... you don't tell the agent how to do it. You tell the agent how you're about to evaluate it and when it should stop."**
- **"AI engineering is the last job... because you're the ones to automate all the other jobs away."**
- **"Everything is Conductor."** / **"We've independently reinvented the crab at least seven times."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Read OpenAI **Symphony** on GitHub to study its markdown-spec structure (focus on the "narrow waist" — API contracts, module surfaces, types). Experiment with a **goal/Ralph loop** (define evaluation + stop conditions rather than step-by-step instructions). Stand up an **ephemeral sandbox** pattern (full-env fork, serverless teardown) for agent isolation. Adopt **<1-min build times + online eval + feature-flagged progressive rollouts** as the "large-org practices at small scale" baseline.
- [ ] Questions: Where's the realistic ceiling on the **dark factory** for regulated/compliance-heavy software? What does a practical **"agent labs vs. model labs"** stack look like (own spec-trained company model vs. renting frontier)? How soon does **truly interactive (micro-batched) low-latency** ship vs. just faster hardware? Is the **CPU-shortage** thesis already showing up in cloud pricing?
- [ ] Relevant to: Building/scaling **multi-agent orchestration** workflows; spec-driven / harness engineering for our own coding agents; infra capacity planning (CPU vs GPU); evaluating fast-inference vendors (Cerebras/Groq/Tâlus); broader "agents for all knowledge work" strategy beyond coding.

## 🔗 Related
- [[BRK229 - From Skeptic to Superpower]]
- [[BRK247 - Scott and Mark learn how agents reshape software engineering]]
- [[ODSP906 - Apply orchestration patterns for production AI agents]]
- [[BRK241 - From prototype to production build and run agents at scale]]
- [[BRK200 - Why your AI code doesnt ship Closing the gap to production]]
- [[BRK233 - Software Defensibility in the era of AI coding]]
- [[DEM305 - GitHub Copilot Anywhere Remote CLIs to Cloud Sandboxes]]
- Source list: [[2026 Build Session List]]