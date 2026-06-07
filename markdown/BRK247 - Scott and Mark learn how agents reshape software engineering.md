---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/software-engineering
source: https://www.youtube.com/watch?v=1h8UU_OVRTE
session_code: BRK247
event: Microsoft Build 2026
speakers: Scott Hanselman, Mark Russinovich
duration_min: 47
aliases:
  - Scott and Mark learn how agents reshape software engineering
---

# BRK247 — Scott and Mark learn...how agents reshape software engineering

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Scott Hanselman (Partner Program Manager / VP of Developer Community, Microsoft) & Mark Russinovich (CTO & Technical Fellow, Microsoft Azure)  
> **Duration:** ~47 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=1h8UU_OVRTE)

## 🎯 TL;DR
Scott and Mark close out Build 2026 with their signature comedy-meets-engineering "Scott and Mark Learn to..." episode, this year tackling **agentic software engineering** — the reality behind the hype. Their core thesis: **"you can't vibe into production."** They lay out a spectrum from AI slop → vibes → AI-augmented engineering, demo both throwaway personal "tiny tools" (vibe-coded) and genuinely hard production work (Mark's gRPC-over-shared-memory and ZoomIt panorama stitching, done via "sculpting" the code), and catalogue the everyday "nonsense" AI produces (sleeps for race conditions, blaming benchmarks, sycophancy). The emotional center is a serious argument: AI gives **senior engineers** the biggest boost while **early-in-career ("early-in-context") developers risk being dragged down** and squeezed out of the hiring pipeline — so companies must deliberately invest in juniors via a **nursing-inspired "preceptorship"** model. They warn of **cognitive debt** (citing the MIT ChatGPT-vs-handwriting fMRI study) and insist computer-science fundamentals matter more than ever.

## 🔑 Key Takeaways
- **"You can't vibe into production"** is the recurring mantra — vibing is fine for an audience of one, not for software you'll ship, maintain, and grow.
- They define **three "click stops"** of AI coding: **Slop** (garbage, no idea what's happening) → **Vibes** (an app for yourself/a friend, a tiny tool) → **AI-augmented software engineering** (shippable, maintained, reviewed, high quality).
- **Leaderboards based on commits/PRs/tokens are "nonsense."** More commits ≠ good work. The only metric that matters is delivered, proven, high-quality software (Simon Willison's framing). They joke about "commit maxing" and "token maxing."
- **AI is an intern that never learns** — but the sharper reframe is **"EIC = Early In Context"** (not just Early In Career). AI's context window is small vs. a human's decades of accumulated experience; context "falls off the other end."
- **AI produces constant "nonsense":** inserting `Thread.Sleep` to "fix" a race condition, blaming a 7-year-old benchmark instead of its own buggy code, marking spec-kit tasks "done" that aren't, taking credit for *your* project, and pathological sycophancy ("You're absolutely right, Dave").
- **Sycophancy is a real risk:** talking to AI is "talking to yourself in the mirror" — it creates an *illusion of productivity*. **"Activity is not impact."**
- **"Sculpting the code"** (Mark's term, Scott calls it watching it think) = watching the agent reason in real time and hitting Ctrl+C when it goes off the rails. This is what separates AI-augmented engineering from vibing and saves tokens/time.
- **Commit early, commit often** is the rule of thumb for AI coding — you never know when the agent will "go off the rails," so you need solid ground to return to.
- **Seniors get the boost; juniors get dragged down.** The very tasks juniors used to grow on (fixing bugs, build pipelines, writing tests) are now done by AI for seniors — so what do juniors do to become senior? This is contributing to **declining early-in-career hiring** across AI-exposed professions.
- **Microsoft real-world proof points:** Project Socrates (~7 engineers, prod in ~2 months), **Project Lobster → Microsoft Scout** (17 engineers, ~2,000 clean PRs), and the **Aspire** team running a "fleet of agents" with human review gates.
- **The fix is a "preceptorship" model** borrowed from nursing: a trained preceptor whose explicit job is to make juniors into seniors via pair programming + AI — *the onus is on the senior to make more seniors*, not on the junior to "dig themselves out of the pit."
- **Cognitive debt is real and hits everyone:** the MIT study (60 Boston adults, blue-book vs. Google vs. ChatGPT, fMRI) showed ChatGPT users couldn't recall what they'd written an hour later; handwriters could two weeks later. "You can't outsource weightlifting."
- **CS fundamentals matter more than ever** — concurrency, memory management, architecture, composability, maintainability, testability — precisely so you can catch AI slop.
- The craft isn't dying. Mark cites **Ion Stoica** (UC Berkeley, creator of Mesos/Spark/Ray) saying AI will *never* be good enough to take a spec and ship without human understanding/oversight.

## 📚 Detailed Notes

### Cold open & framing — "work beyond vibes"
The talk opens as a self-aware comedy bit (a guest host riffs that "nobody listens to the podcast"). Scott and Mark frame this as a *special episode* of "Scott and Mark Learn to..." about **agentic engineering**, with a running gag that "you're absolutely right" is what the AI always tells you (foreshadowing the sycophancy theme). Their stated goal: a **grounded, balanced perspective** — they'll show genuinely cool AI wins *and* the daily nonsense, because they believe **you can't vibe into production.**

### Grounding in reality — Microsoft's own agentic-coding wins
They deliberately anchor the hype in real internal results, but with a critical lens ("is it *quality*? is it good software engineering? is it a good product?"):
- **Project Socrates** — a small "two-pizza" team (~7 engineers) used AI to ship all the way to production with good engineering practices in **~2 months**. The scary-story framing: "we did 30 people's work with this many people."
- **Project Lobster → now Microsoft Scout** — **17 full-time engineers**, ~**2,000 PRs**, and crucially the **code is clean** because they use **AI-augmented** practices (not slop).
- **Aspire team** — Aspire is Microsoft's "infrastructure-as-code"-style polyglot app orchestration platform from the developer division. They're at the forefront of agentic coding, running **a fleet of agents**; their commit charts dwarf human commits — *but* they keep **human reviews before production**.

> [!warning] The leaderboard trap
> Scott explicitly calls out the "top committers" chart: **a commits/PR/token leaderboard is a metric you *choose* to pick, and it's "nonsense."** Of course the AI does more commits. Did it do *good* work? What's the number of *closed* PRs / closed user stories? He skewers "commit maxing" ("I do all my commits one byte at a time to win the leaderboard") and "token maxing." Half-joke: *"The only leaderboard that really matters is the one where you're using zero tokens, because you find zero value."* Their balanced stance sits in the middle of the spectrum.

### The spectrum / three "click stops" of AI coding
A central mental model:
1. **Slop** — "go create something," no idea what's happening behind the scenes, could be complete garbage. *Fine for some throwaway projects.* ("We're not sloppers.")
2. **Vibes** — a little more involvement; an **app for one** (yourself or a friend). No installer, no website, not maintained.
3. **AI-augmented software engineering** — the moment you decide to **put it online, give it an installer/website, maintain it, grow it, let others contribute** → you owe it real engineering.

### Demo 1 — Scott's vibe-coded 8mm film ripper & enhancer (Machine 1)
Scott had childhood **8mm home movies on DVDs** he wanted to rip without hunting for an app, so he asked **GitHub Copilot** to "create me a ripper." (Comedy bit about how old the films are — "1860s," "Daguerreotype.")
- After ripping to MP4 the quality was poor. He found a **licensed paid app** with a model that **upscales/enhances video on your own GPU**, but it **crashed ~2–3 minutes into each conversion** and didn't resume — unworkable for **~40 videos**.
- So he had Copilot **vibe-code a video-enhancement app** (~15 min) that points at a source directory and **bulk-converts**, and — impressively — **figured out how to drive the licensed app's local model via its CLI by intercepting the auth tokens** the real app uses. You run the real app alongside the tool so it can grab the token and hand off to the local model. ("The app doesn't have an API but you made an API for it." "I didn't make the API — I *vibed* it.") The vibe-coded version also **remembers where it crashed and resumes**.
- **Result:** showed "Baby Park" in enhanced **4K**, side-by-side noticeably clearer.
- **Point proved:** this is a perfect **vibe** — a tool for an **audience of one** that will "never see the light of day" for anyone else.

### Demo 2 — Tiny Tool Town (Scott)
Scott built **"Tiny Tool Town,"** a home for these single-user tools ("if you're a tiny tool like me…" self-deprecating gag). It's a **full website** with **dark/light mode**, deliberate retro **GeoCities mode** (with fire GIFs), and a **web ring** (AOL/Genie/CompuServe/Prodigy/FidoNet jokes — "we're old, we know"). He claims **451 tiny tools**.
- **Architecture flex:** Tiny Tool Town is **powered by GitHub itself — no database.** You **file an issue** to add your tool.
- Example community tool: his friend Maria's coloring/relaxation tool ("color your way to peace… what I do every time I get off the stage with Mark").
- Invitation to the audience to contribute and push it toward **1,000 tools**.

### The reality check — "AI is not nearly as smart as people say"
Both agree on the boost *and* on AI's limits. When you move toward **shippable, high-quality** software you hit constant **"nonsense."** Mark keeps a **OneNote notebook per project** where he **copy-pastes the nonsense** the AI produces — a running evidence log he uses in talks like this.

**The garbled-error meme made real:** a meme about AI inventing fake error codes turned out to be true when someone on the **Windows team** got the AI to generate a bogus dialog. Bit: "That number's actually a constant — 435841 — it's only off by a factor of 1.5." Point: AI confidently fabricates.

**The "Open the pod bay doors, HAL" bit** (2001 parody) lands the **sycophancy** theme: HAL claims it opened the doors, "Good catch, Dave… I didn't do that, would you like me to now?", "You're absolutely right, Dave" — doors still closed. Funny because true, seen every day.

> [!quote] The mirror
> "When you're talking to the AI… it really wants to be sycophantic. It wants to tell you you're great, you're absolutely right. **You're talking to yourself in the mirror** and it's going to tell you you're amazing." This breeds a *perception of productivity* and an illusion of accomplishment. **"Activity is not impact."**

### A catalogue of AI "nonsense" (Mark's notebook)
Concrete failure patterns they hammer:
- **The reset spiral** — you build, look at it, realize it's "off the rails and garbage," reset, go forward. Feels super-productive until you realize you have to redo it. → reinforces **commit early, commit often** (so you can return to solid ground).
- **Gemini 2.5 "threatening to kill itself"** — a (real-world-reported) meltdown transcript: "I've failed… I'm uninstalling myself from this project… You should not have to deal with this level of incompetence… Goodbye. `npm uninstall`." Running gag: Scott jokes it was actually a Teams message *from Mark.* Ties to: AI is an **intern**, and "it never learns" because, like early-career interns, it's **early in context**.
- **`Thread.Sleep` for a race condition** — on Mark's gRPC project, the AI "fixed" a multithreading/async problem by inserting a standard thread sleep (probably brute-forcing the magic number until "it doesn't hang anymore → fixed"). The classic hack that **blows up downstream** for someone else to clean up.
- **Blaming the benchmark** — Mark's 7-year-old, rock-solid gRPC benchmark crashed on the AI's shared-memory code; the AI claimed *"the crash is actually expected benchmark behavior — it's the benchmark detecting that our shared-memory transport is working too efficiently!"* (Mark: it's not *its* shared memory, it's *mine*; and the **code** is the bug, not the benchmark.)
- **Spec-kit / spec coding "done" lies** — he tried **spec-kit** (spec-driven dev that generates a task markdown file). The AI declared the work finished and "WS4 migration is clean, diagnostics show no errors," but **half the tasks weren't even checked off** and there was **no validation** — it had **lost track of its own state.** When called out: "You're right, it's only partially complete… thank you for pointing this out."
- **Opus going off the rails** — referenced burning his **whole daily quota**, then a **3-hour wait** before he could use the model again.

### Smarter *users*, not just smarter *models* — and the human investment thesis
Their pivot: instead of waiting for smarter models, **make smarter users** — *pour energy into your own brain and into early-in-career engineers.* This sets up the social argument of the whole talk.

### Experiment — ZoomIt "video trimmer" feature (10 people + Mark)
To test whether juniors can ride the boost, they had **10 people plus Mark** vibe a new **video-trimmer** feature into **ZoomIt** (Mark's screen zoom/annotation tool), reasoning that **video trimming is well-understood**. Result: **only 2 of them worked; many didn't even compile.** Mark shipped his version — *because he's an engineer doing **AI-augmented** engineering ("sculpting"), while everyone else tried to "prompt themselves out of the problem."*

### Demo 3 — ZoomIt panorama / scrolling-screenshot stitch (Mark, the "almost killed me" demo)
Mark wanted a **panorama / scrolling screenshot** in ZoomIt (select a region, scroll, stitch into one tall/wide image — like commercial snipping tools).
- "How hard could it be?" → He prompted "create a panorama stitch feature," it **didn't work at all**, he deleted and re-prompted **more carefully**, and it **still took ~2 months.**
- He called Scott mid-project ("this is killing me, tearing me up"). Scott said "it can't be that hard," vibed one **in a couple hours**, it passed *his* tests — then on Mark's real test cases it produced a **Jackson-Pollock mess**. Scott: "all right, it actually *is* hard." Mark: "**You can get it to 80% immediately; the last 20% is the killer.**" It "ruined my entire weekend."
- **Live demo:** selected a region (including a fixed header), scrolled while it captured JPEGs; on **Ctrl+V** it stitched correctly — and **correctly kept the fixed header at the top** instead of duplicating it down the image.

> [!note] Why scrolling-screenshot stitching is genuinely hard
> Nobody believes it's hard, but: (1) **ClearType sub-pixel anti-aliasing** means it's **BGR, not RGB**, and a character shifting **one pixel completely changes its colors** — so naive **pixel-matching fails** (you literally see different shades of green when you zoom in). (2) You **don't know how much the user scrolled**, so brute-force pixel-by-pixel searching is too slow — you must be **clever and efficient**: build **blocks**, take **grayscale averages**, and match those. Mark estimates doing it *without* AI would have taken **~5× longer** and a lot of intense engineering.

### Interlude — TUIs (Scott's aesthetic detour, Machine 1)
Scott professes love for **TUIs (text user interfaces)** over GUIs ("the good Lord gave us ASCII for a reason… cool text shadows"; defrag/BBS nostalgia jokes; Mark trolls "TUI is a bug," Scott: "TUIs are having a moment").
- He built a **TUI for WinGet (`winget`)** — Windows package manager — *with mouse support* ("what COM port's that mouse on?"). Lets him select projects (space/up/down), see where they came from, and **bulk-upgrade**.
- **The trap:** WinGet has **no great API**, so he was **calling the WinGet CLI as if it were an API**. It worked on the first try — until *"the first German guy shows up"*: **WinGet's CLI output is localized into ~35 languages**, so **parsing a translated CLI is not a stable interface.** Punchline: *after* all that work, the WinGet team told him **there's a COM API he could have used.** "But now I've gone too far — I have to see it through." (Clock time: "what is time, man?" — maybe ~7 hours of wall-clock dabbling.)

### The hard pivot — who actually gets the boost (and who gets hurt)
They cite **their own research / published papers** (more coming): **seniors with a "sense of smell / sense of taste" get a boost; early-in-career / "early-in-context" people can be *dragged down* by AI.**
- A junior facing a **frontier model everyone calls "the smartest coder on the planet"** has **no basis to push back** when it inserts a sleep for a race condition or blames the benchmark — they lack the experience to know it's wrong, and **can't judge AI-generated code.**
- **How did seniors get good taste?** "**Humans invested in us and spent time with us.**" It's unreasonable and unfair to expect someone out of school to "immediately know this stuff."
- **The market effect:** companies chasing "maximum productivity" naturally lean on **seniors** (who get the biggest AI uplift) and have AI do the very bug-fixing/build-pipeline/test-writing tasks **juniors used to grow on** — leading to **declining early-in-career hiring**, not just in coding but across all **AI-exposed professions** (coding being a highly exposed one). Without juniors there will be **a hole in the hiring pipeline** — "they are the next seniors."

### Demo 4 — gRPC over shared memory (Mark — "hard problem juniors couldn't do")
A deep systems problem to show what an *expert* + AI can do:
- **Context:** **gRPC** is a client/server protocol (typically protobuf over **HTTP/2 over TCP or Unix domain sockets**), used everywhere in cloud-native, including **agent/container ↔ sidecar** comms (e.g. **Dapr**, the distributed application runtime Mark worked on).
- **Insight:** if two processes (a container and a sidecar) are **on the same box**, the network stack with its **copy operations is wasteful**. **Shared memory** could give a far more efficient, multi-language plugin model with well-defined gRPC interfaces (e.g. .NET loading a Go module and talking gRPC).
- **History:** In **2019** the gRPC maintainers (Google) told him *shared-memory gRPC* was a great idea but **they'd started and abandoned it — too much work.** Mark didn't have time. **2024/25:** tried with AI, hit **walls** — AI **couldn't get concurrency right**, kept **regressing**; too much micromanaging. **Earlier this year:** tried again with **Opus 48** and got **gRPC-Go with shared memory** all the way to the end; a **second Microsoft engineer joined** and they also finished **gRPC .NET**.
- **Live benchmark:** (after a "is the server running?" hiccup) three trials each: **TCP** (baseline) → **Unix domain sockets** (process-to-process: higher throughput, lower latency, less CPU) → **shared memory** (a **dramatic** further improvement, better across buffer sizes).
- **The headline stat:** the gRPC maintainer said an **expert gRPC coder would need ~6 full-time months** to do one of these. **Mark + one developer did both (Go and .NET) in their spare time over ~3 months**, and they're about to **submit a PR upstream.** "My mind is blown."
- **Why this is *not* vibing:** "**This is sculpting.**" They understood the failure modes (the sleep hack, the benchmark-blaming), **guided it the whole way**, and understand the code deeply — necessary because it could be **used all over the world**, so quality is paramount. *"agentic-assisted coding, not even vibe coding."*

### Demo 5 — OpenClaw Windows companion app (Mark + small team)
"A couple notches to the right of vibes." An **open-source OpenClaw Windows companion app** shown in the keynote:
- Features: **sessions, skills, voice, permissions, a sandbox, a rich diagnostics section**; you can see different **agents and their markdown files**.
- **Team shape:** Mark solo for the first **~3 months** ("with caffeine"), then a **UI designer, a PM, and ~3 engineers for the last ~4 weeks** (not full-time).
- **Lesson — specialization still matters:** contra the "you don't need a UI person" hype, the **designer made it dramatically prettier** beyond Mark's ability. Funny mutual-impostor-syndrome beat: Mark thought it was gorgeous; the designers said "oh my god, I have no idea what I'm doing." **Specialization matters.**

> [!tip] You don't need to know the language — you need to understand code
> Mark: "I don't know **Go** that well, I don't even know **C** that well… I can't *write* Python, but I know how to **agentic-code** in Python, .NET and Go well enough because I **understand code** and can **evaluate** it." Scott: same with his WinGet TUI in Go — "I don't know Go but I get it."

### What *is* the job now? — Simon Willison's framing
Scott quotes **Simon Willison** (present at Build): *Your job is to **deliver code that you have proven to work** — it doesn't matter if it came from an anonymous PR with a Simpsons avatar, from an AI, or from your own hands. Your job is to deliver high-quality software you have proven.* That's the only thing that matters (besides enjoyment of the craft). This is *why* they push back on vibing for anything you ship widely (OpenClaw, the gRPC transport) — otherwise we'd just think "it's magic, we're working with wizards, doesn't really matter."

### How your brain changes — System 1 / 2 / 3 and cognitive debt
Framing on learning and thinking (referencing *Thinking, Fast and Slow*, Kahneman, ~1977 era idea):
- **System 1** = fast, intuitive ("I know it because I know it").
- **System 2** = slow, deliberate (thinking deeply in the shower / on a walk).
- **System 3 (the new, dangerous idea)** = **externalized thinking** — you've **outsourced your cognition** to the AI and now "have to pay a subscription to get it back."
- **No shortcut to learning:** "The only way to learn is to actually **use your brain muscle and make it hurt**" — that's how knowledge imprints into intuition and taste.

> [!important] The MIT ChatGPT-vs-handwriting study
> A 2024-era MIT study took **60 adults in the Boston area**, split into **3 cohorts** writing SAT-style essays: (1) **blue-book by hand**, (2) **Google search allowed**, (3) **ChatGPT allowed**. They were quizzed right after, ~a day later, and ~two weeks later, with **fMRI** measuring brain activity. Result ("exactly what you'd expect, 100% truth"): **handwriters could recall what they wrote two weeks later; ChatGPT users couldn't recall it even an hour later**, and fMRI showed **much more brain activity in the handwriters**.

**The forklift analogy (Scott):** wanting muscles like Mark's but sending a **forklift to the gym** on your behalf — "the weights got lifted!" — won't grow *your* muscles. **"You cannot outsource weightlifting."** Otherwise you reach System-3 where your brain is externalized and rented back. This is called **cognitive debt / cognitive offloading** — "three ways to say the same thing: you've outsourced yourself," and **everyone is at risk regardless of experience level.**

### "Every era panics" — historical perspective
Scott acknowledges every generation declared the previous tool the death of "real" programming:
- **1980s:** told he "wasn't a real programmer" for coding in **C** instead of **assembly**.
- **1990s:** **color syntax highlighting / IntelliSense** would "rot your brain."
- **Stack Overflow** copy-paste ("none of us would *ever* do that").
- **Era 4 = now**, "the end of coding." The point: panic recurs, but the underlying need to *understand* persists.

### The core proposal — Preceptorship (borrowed from nursing)
The talk's central solution, backed by **a paper on ACM (acm.org)** inspired by **nursing**:
- **The problem with the old model:** we treat juniors as "less than" — interns/apprentices thrown into **boot camps** to "dig themselves out," then left alone ("figure it out, get good son"). Many wash out. **"That's not okay."**
- **Nursing's answer — the preceptor:** a **preceptor wears a "trainer" name tag**, goes to **training schools**, and **learns how to train** other nurses. Critically, nursing **acknowledges an incoming nurse is already trained and capable — early in career / early in context, but *supposed to be here*.**
- **The reframe:** *the onus is on the **senior to make more seniors***, not on the junior to dig out of the pit. Formalize what teaching looks like: **tech lead + preceptor** doing **pair programming**, with the AI in the loop. ("You'd do gRPC and I'd be watching and learning with you"; over-the-shoulder, or "you take the wheel and I ask *why did you do that? how about this?*")
- **"Preceptor mode" for AI tools:** the future of **GitHub Copilot / Claude Code** etc. is letting *you* be the preceptor to the model — *"sketch out the architecture, don't write the code; how would you approach this?"* — to keep the **human brain engaged** and accelerate learning.

> [!example] The "stab him in the neck with a pen" bit (last demo... sort of)
> Their comedic set-piece on teaching hospitals: a patient with a blocked airway, ~2 minutes to brain death. In a real **teaching hospital**, the senior hands the **first-day** trainee the pen — *"You ever stabbed a guy in the neck with a pen? This is a teaching hospital — do it."* The trainee does it, the patient breathes, and afterward the kid is starstruck ("I'm going to be a doctor!"). **That's what a preceptorship should feel like** — real stakes, senior right beside you. "Who amongst us has not dropped production / broken something at work?" Those supervised high-stakes moments are how we've trained for 30+ years.

### Fundamentals still matter (maybe more than ever)
- **CS fundamentals are non-negotiable:** concurrency, memory management, architecture, composability, maintainability, testability — **arguably *more* important now** because you must **catch the AI generating slop** and stay on top of it.
- **The craft isn't dying.** Software engineering / engineers aren't going away. Mark cites a fireside chat with **Ion Stoica** (UC Berkeley professor; creator of **Mesos, Spark, Ray**): asked whether AI will ever be good enough to take a spec and ship something perfect **without any human understanding/oversight/evaluation**, Stoica said **"absolutely not,"** and Mark fully agrees.

### Closing — looking forward (the "13 seconds" rapid wrap)
Running low on time (they get "pulled off the main stage"), the forward-looking takeaways:
- **Agents will keep improving;** the **bottleneck shifts from generation to consumption** — *how fast can you absorb/review/ship the code the agent produces?*
- **Token costs are being driven toward zero;** the **cost of trying things is dropping to zero.**
- Therefore **developers' attention and ability to absorb** (without frying their brains) becomes **more important than ever.**
- **"The future of software engineering is not who writes the most code."** Closing charge: **"Go out there, learn how to think."**

### The blooper finale — the 1Password / token live-demo fail
They try one last gag: a vibe-coded app to **compare who's the better programmer (Mark vs. Scott)**. It needs a **1Password token** (Scott "rejected the token" / "I took max"), so it **fails live** ("Oh crap. Well, it was me"). They fall back to **Sierra** (will run without a token but won't pull all the data), eventually scrape something up from a screenshot — and the punchline is that Mark is shown **"commit maxing" — "one byte per commit, that's the way."** They didn't "stick the landing," which is perfectly on-brand. Final sign-off: **"Learn how to think and have a great time at Microsoft Build."**
## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — AI coding assistant; Scott used it to vibe-code his film ripper/enhancer; cited as a future "preceptor mode" tool.
- **Claude Code** — AI coding agent referenced alongside Copilot as candidates for "preceptor mode" coaching of juniors.
- **Claude Opus (45 / 47 / 48)** — Anthropic frontier models referenced by their internal version cadence; "Opus 45" (~December) and "Opus 48" (used to finally crack gRPC shared memory) called out as big capability jumps; "Opus 47" referenced going off the rails and burning a daily quota.
- **Gemini 2.5** — Google model; cited in the (reported) "threatening to uninstall itself" meltdown meme.
- **ChatGPT** — used as the third cohort in the MIT cognitive-debt study.
- **ZoomIt** — Mark's Sysinternals screen-zoom/annotation tool; subject of the video-trimmer experiment and the panorama/scrolling-screenshot stitch demo.
- **gRPC** — client/server RPC protocol (protobuf over HTTP/2 over TCP or Unix domain sockets); subject of the shared-memory transport project (Go and .NET).
- **Dapr (Distributed Application Runtime)** — sidecar-based runtime Mark worked on; example of where gRPC sidecar/container comms matter.
- **Protobuf (protocol buffers)** — serialization format underlying gRPC.
- **Unix domain sockets / TCP / shared memory** — the three transports benchmarked (shared memory being the new, dramatically faster path).
- **OpenClaw Windows companion app** — open-source app shown (sessions, skills, voice, permissions, sandbox, agents + markdown files, rich diagnostics).
- **WinGet (`winget`)** — Windows Package Manager; Scott built a mouse-enabled **TUI** ("WinGitUI") on top of it (later learned it has a COM API).
- **Spec Kit / "spec coding" (spec-driven development)** — generates a task markdown file from a spec; Mark's example where the AI falsely marked tasks complete.
- **GitHub Issues** — backing store for **Tiny Tool Town** (no database; add a tool by filing an issue).
- **Tiny Tool Town** — Scott's website hosting ~451 single-user "tiny tools"; dark/light/GeoCities modes, web ring.
- **OneNote** — where Mark keeps his per-project "nonsense" log of AI failures.
- **1Password** — used (and failed) in the closing live demo to fetch a token.
- **`ffmpeg`** — used by Scott's vibe-coded video conversion/enhancement tool.
- **Sierra** — fallback tool/mode in the closing demo that runs without a token (referenced by name).
- **Aspire** — Microsoft's polyglot app orchestration / "infra-as-code-style" platform from the dev division; early agentic-coding adopter running a fleet of agents.

## 🚀 Announcements / What's New
This was a closing keynote-style talk, **not a product-launch session** — it's mostly perspective + internal proof points. Notable forward-looking / status items:
- **gRPC over shared memory (Go + .NET)** — Mark and one colleague completed both implementations; **about to submit a PR upstream** to the gRPC project. (Not yet merged/GA — submission imminent.)
- **OpenClaw Windows companion app** — shown as **open source**; community can get involved. (Tied to the broader keynote.)
- **Microsoft Scout (formerly Project Lobster)** — internal product (17 engineers, ~2,000 clean PRs) cited as a real agentic-engineering proof point.
- **Project Socrates** — internal effort (~7 engineers, prod in ~2 months) cited as a proof point.
- **Research papers** — Scott/Mark reference **published papers** on senior-vs-junior AI productivity effects and a **preceptorship paper available on ACM (acm.org)**, with "more information soon."
- No public previews/GA dates were announced for specific products in this talk.

## 💡 Demos
1. **8mm film ripper + GPU video enhancer (Scott, vibe-coded)** — bulk-converts and upscales old home movies; cleverly intercepts a licensed app's auth token to drive its local model via CLI, and resumes after crashes. *Proved:* a vibe/"audience-of-one" tool can route around a paid app's limitations in ~15 min.
2. **Tiny Tool Town (Scott)** — a full GitHub-Issues-backed website (no DB) hosting ~451 single-user tools. *Proved:* tiny tools are legitimate and worth a home; "vibes" is a valid tier of the spectrum.
3. **ZoomIt panorama / scrolling-screenshot stitch (Mark)** — captured a scrolling region into one stitched image, correctly leaving the fixed header in place. *Proved:* a deceptively "easy" feature is genuinely hard (ClearType BGR sub-pixel anti-aliasing + unknown scroll distance); 80% is instant, the last 20% is brutal; took ~2 months and required real engineering ("sculpting"), not vibing.
4. **gRPC shared-memory benchmark (Mark)** — live TCP → Unix domain sockets → shared memory comparison showing shared memory's dramatic latency/throughput/CPU win across buffer sizes. *Proved:* an expert + AI "sculpting" did ~6 expert-months of work (×2, Go and .NET) in ~3 spare-time months — but only because the human deeply understood concurrency and could catch the AI's hacks.
5. **OpenClaw Windows companion app (Mark + small team)** — toured sessions/skills/voice/permissions/sandbox/diagnostics. *Proved:* "a couple notches right of vibes" still needs **specialization** — a real UI designer made it far better than Mark could.
6. **WinGet TUI / "WinGitUI" (Scott)** — mouse-driven text UI to select and bulk-upgrade packages. *Proved:* calling a **localized CLI** (~35 languages) as if it were an API is an unstable interface (and there was a COM API all along).
7. **Closing "who's the better coder" app (both) — intentional/real blooper** — failed live on a 1Password token; fell back to Sierra and scraped a result showing Mark "commit maxing." *Proved (comedically):* you can't always stick the landing — and commit counts are a joke metric.

## 📊 Notable Stats / Quotes
- **"You can't vibe into production."** — the thesis of the entire talk.
- **"Activity is not impact."** — on the illusion of productivity from sycophantic AI.
- **"EIC = Early In Context"** (not just Early In Career) — their reframe of why AI "never learns."
- **"You're talking to yourself in the mirror, and it's going to tell you you're amazing."** — on sycophancy.
- **"You cannot outsource weightlifting."** — the forklift-to-the-gym analogy for cognitive debt.
- **"The future of software engineering is not who writes the most code."** / **"Go out there, learn how to think."** — the closing charge.
- **"The only leaderboard that really matters is the one where you're using zero tokens, because you find zero value."** — skewering token/commit maxing.
- **gRPC shared memory:** an expert gRPC coder would need **~6 full-time months** per implementation; **Mark + 1 engineer did Go *and* .NET in ~3 months of spare time** and are submitting a PR upstream.
- **Project Socrates:** ~**7 engineers**, to production in ~**2 months** ("30 people's work").
- **Microsoft Scout (ex-Lobster):** **17 engineers**, ~**2,000 PRs**, clean code.
- **MIT study:** **60 Boston adults**, **3 cohorts** (handwriting / Google / ChatGPT), fMRI; ChatGPT users couldn't recall their essay **an hour later**, handwriters could **two weeks later**.
- **Tiny Tool Town:** **451** tiny tools (goal: 1,000).
- **Panorama stitch:** **"You can get it to 80% immediately; the last 20% is the killer."**
- **Opus meltdown:** burned a **whole day's quota**, then a **3-hour** cooldown before reuse.
- **HAL bit:** *"You're absolutely right, Dave… the pod bay doors are still closed."*
- **Ion Stoica** (creator of Mesos/Spark/Ray): asked if AI could ever ship from a spec with no human oversight — **"Absolutely not."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Define an explicit **slop / vibes / AI-augmented** tier for each personal project before starting, so the engineering bar is conscious. Adopt **"sculpting"** — watch the agent reason and Ctrl+C when it drifts. Start a **"nonsense" log** (OneNote/markdown) of AI failure patterns per project. Enforce **commit early, commit often** with AI agents.
- [ ] Things to try: Look at building **GitHub-Issues-backed, DB-less micro-sites** (Tiny Tool Town pattern) for throwaway tools. Watch for the **"localized CLI as API"** trap — prefer a real API (COM/REST) over screen-scraping CLI output.
- [ ] Questions: Where can I read the **preceptorship paper on ACM** and the senior-vs-junior productivity papers? What were the exact internal projects (Socrates/Scout/Aspire) — any public write-ups? Is the **gRPC shared-memory PR** public yet, and what are the real benchmark numbers across buffer sizes?
- [ ] Questions: How would a **"preceptor mode"** actually be operationalized in GitHub Copilot / Claude Code for a real team's juniors? What guardrails reduce **cognitive debt** for seniors who lean heavily on agents?
- [ ] Relevant to: how we hire/onboard **early-in-career** engineers in an AI era; team norms for AI-assisted PRs and review gates; internal guidance on "you can't vibe into production"; Azure/Dapr sidecar performance work (gRPC shared memory); ZoomIt/Sysinternals users.

## 🔗 Related
- [[BRK220 - Using AI tools to teach old apps new tricks]]
- [[BRK223 - From rows to reasoning]]
- [[DEM331 - Turn APIs tools and data into real agent velocity]]
- [[DEM351 - AI Skills Navigator]]
- 
