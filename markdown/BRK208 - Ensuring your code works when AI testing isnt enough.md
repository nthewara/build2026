---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/testing
  - topic/quality
  - topic/ai
  - topic/devops
source: https://www.youtube.com/watch?v=9RzqagabeOk
session_code: BRK208
event: Microsoft Build 2026
speakers: Simon Willison
duration_min: 45
aliases:
  - Ensuring your code works when AI testing isnt enough
  - Verification patterns for agentic engineering
---

# BRK208 — Ensuring your code works when AI testing isn't enough

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Simon Willison (independent developer, writer at simonwillison.net; co-creator of Django, creator of Datasette; long-time AI-assisted-coding practitioner)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=9RzqagabeOk)

## 🎯 TL;DR
Simon Willison argues that coding agents — LLMs that write, run, test and iterate on their own code — became genuinely reliable "daily drivers" only at the **November 2025 inflection point** (Opus 4.5, GPT-5.1 + matured coding harnesses), and that the typing-code bottleneck is now gone. The real, urgent job has shifted from *writing* code to **verifying** it: producing code that is trustworthy, maintainable and high-quality at a massively accelerated velocity. This (slightly retitled) talk on **verification patterns for agentic engineering** walks through concrete, individually-usable techniques — active refactoring, prototyping-as-verification, exercising API designs with throwaway code, agentic documentation, continuous preview deployments, reducing the "blast radius" of mistakes with sandboxes (CSP, sandboxed iframes, WebAssembly/WASI), and zero-tolerance for flaky tests. The throughline: large companies have always shipped quality from untrusted/unreviewable code via layered verification; we should scale those same ideas *down* to run on our laptops with our "armies of agents," and use AI to build **better** software faster, not worse software faster.

## 🔑 Key Takeaways
- **The November 2025 inflection point**: coding agents went from curiosity to reliable daily driver because OpenAI and Anthropic spent all of 2025 doing reinforcement learning against coding tasks (a domain with obvious right/wrong answers); the advances landed together in November (Opus 4.5, GPT-5.1, much-improved coding harnesses).
- **"Vibe coding" is being misapplied.** Karpathy coined it (Feb 2025) explicitly for *fun/weekend* projects where you forget the code exists. For professionals shipping real software the better term is **agentic engineering**.
- **The typing-code bottleneck is automated away** — Willison routinely writes ~600 lines of tested, documented code *on his phone while walking the dog*, versus historical norms of 10–50 LOC/dev/day (and 600 LOC/day once cited as an extreme outlier).
- **Verification is now the core job.** "Our job is to produce code AND verify that that code works." Churning out code is worthless without trustworthy, maintainable, proud-of-it results.
- **The invisible QA you used to do as you built has vanished.** You used to twiddle a feature, hit refresh, eyeball it constantly. One-shotting 1,000 lines with Claude skips all of that — so verification must be deliberately re-introduced.
- **It's an old problem in disguise.** Microsoft (100k+ devs, 25M+ LOC) and other megacorps already ship quality from code no single human can review — by layering verification. The challenge is **scaling those big-company techniques down to a laptop.**
- **Active refactoring** beats passive code review: nitpick the agent relentlessly (rename, dedupe, "explain this and add comments"). You can't be rude to an agent — and you come out actually understanding the code.
- **Think in stakes and seams.** Review an auth flow line-by-line; barely glance at a decorative icon. Engineers are now more like **architects/designers** — get the high-level structure and the seams between systems right.
- **Verify API designs by writing throwaway code against them.** Agents will instantly prototype several features against a new API, surfacing design problems you'd otherwise miss.
- **Prototypes are now effectively free** — use agents to build interactive proofs-of-concept (to prove something is *possible*), hoard them, then feed them back as input when building the real feature. Some projects spend a month+ purely prototyping.
- **Agentic documentation**: agents are great at accurate, short, "uncreative" prose. Run `diff against main → does any documentation need updating?` before landing a branch. **Strip all opinions/promotional language** — doc trust is hard to earn and lost instantly the first time docs mislead.
- **Continuous deployment for previews has no downside now.** Auto-deploy every PR to a fresh preview env (Fly.io / Cloud Run / Vercel) — reading code never tells you what running it does. A single prompt (with "ask clarifying questions first") replaces what used to be weeks of CI/CD setup.
- **Reduce the blast radius of mistakes** with layered defenses (the Firefox model): Content Security Policy headers, **sandboxed iframes**, and **WebAssembly/WASI** server-side sandboxes that can't read files, open network connections, or exceed strict CPU/memory limits.
- **Test your sandboxes by attacking them with agents.** Put GPT-5.5 inside and tell it to break out; if it can't, you gain real confidence. (Caveat: agents often recognize **Docker** and escape via known host-port tricks — so test sandboxes specifically.)
- **Zero tolerance for flaky tests** — including UI tests. Agents don't mind wasting their own time reproducing a 1-in-50 failure; they're very good at simulating the conditions (e.g. reproducing a Linux/CI-only bug in Docker on a Mac in the background).
- **Any tool that helps human engineers helps agents too**: `CLAUDE.md` (onboarding docs), linters, formatters, debuggers, logs, CI, and fast-compiling languages with good error messages (Go is excellent for agents).
- **Agentic engineering is the "SEO for accessibility" of good practices** — it finally gives everyone a selfish reason to adopt decades-old engineering discipline (tests, docs, CI, CD).
- **Use this to build better software faster, not worse software faster** — you can have all three of higher quality, easier maintenance, and more features; the usual "pick two of three" no longer binds.

## 📚 Detailed Notes

### Framing: a "grand elder" of a four-year-old field
Willison opens (clicker failing, recovered mid-talk) by noting he's been using LLMs to help write code since **2022** — which absurdly makes him a "grand elder" of a four-year-old space. He references his own June-2022 writing about getting GPT-3 to write little SQL queries and explain how code works, and has explored these tools continuously since. The point: the field is so new that even brief experience counts as deep, and patterns are still being discovered constantly.

### Vibe coding vs. agentic engineering (terminology)
- **Andrej Karpathy**, Feb 2025 ("ancient times" by current pace), coined **vibe coding**: "fully give into the vibes, embrace exponentials, and forget that the code even exists."
- Crucially, most people **didn't scroll to the bottom of that tweet**, where Karpathy said this is *for fun, for weekend projects* — not for serious code.
- Willison thinks it's a "waste of a term" to apply "vibe coding" to all AI-assisted coding. Vibe coding = the **irresponsible** way of building things.
- The open question: what do you call it when **professional engineers ship real software they care about** using AI? The term bubbling to the top — and the one he adopts — is **agentic engineering** (he saw a Chinese AI lab use it in a press release, his signal it had spread enough to be safe to use).
- **Audience poll**: "How many have shipped code to production without reading that code?" — *quite a few hands*. He notes that when he pitched the talk three months earlier, the honest answer would have been **nobody at all**. The rate of change is "shocking."

### What "coding agent" means here, and the November inflection point
- **Definition**: a coding agent is software where the LLM *both* writes the code *and* executes it — it can test, iterate, and improve.
- They "only really got good in **November 2025**": **Opus 4.5** shipped, **GPT-5.1** + coding harnesses matured, and the tools jumped from interesting curiosity to a **reliable partner / daily driver**.
- **Why November**: both OpenAI and Anthropic spent all of 2025 doing **reinforcement learning against coding tasks** — a strong pattern precisely because code has an obvious right/wrong answer. A year of advances "came to a head" in November, just in time for everyone to tinker over the Christmas holidays.
- He calls this **the November inflection point**.

### Lines of code: the metric you should never use (used anyway)
- The cardinal rule: never measure productivity in lines of code. He immediately breaks it to make a point about *scale of change*.
- **Steve McConnell, _Code Complete_ (2004)**: industry-average productivity ≈ **10–50 lines of delivered code per person per day**.
- A later source (~10 years on): **600 LOC/day** was cited as a *high outlier* of developer performance.
- Willison: he now writes **~600 lines of tested + documented code on his phone while walking the dog**, routinely. Output has risen "by a terrifying magnitude."
- The whole question: **is that code any good?** How do we work at this much higher velocity without producing slop and rubbish?

### The old problem hiding inside the new one
- This looks new, but megacorps solved a version of it long ago. **Microsoft**: 100,000+ developers of varying experience across a 25-million-line codebase. **No single human can review it all** — yet they ship quality.
- The big challenge for individuals: figure out **which big-company techniques produce quality from unreviewable code, and scale them down to run on our laptops.**
- Willison had an earlier version of this revelation ~5 years ago at **Eventbrite** (engineers across ~5 time zones). The processes good for distributed teams — **comprehensive automated tests, comprehensive documentation** — turned out to be great for *personal* productivity too: rather than slowing him down they *sped him up*, because he could run **100 projects at once** and treat every reboot like being a brand-new contributor.
- Now the same idea must apply to the whole field of **software validation**: produce code *and* verify it works.

### The verification gap: invisible QA disappeared
- Verification used to be woven into the build: change a line → hit refresh in the browser → confirm it works. That **invisible, continuous manual QA** was just "the daily grind."
- Now you can **one-shot a feature with Claude** and come back to ~1,000 lines having done *none* of that along-the-way checking. The QA didn't move — it vanished, and must be re-introduced deliberately.

### Case study — Strong DM's "dark factory" (the maximalist version)
The most striking example he's seen (from October 2025 — "ancient times" by current standards): a company called **Strong DM** building what they called a **software factory**, also known as a **dark factory**.
- **Dark factory concept (from manufacturing)**: if you automate a factory enough, you don't need humans on the floor — the robots do all the work, so you may as well *turn the lights off*. Applied to software: build so automatically that human "illumination" isn't required.
- **Team of just three people.** Two foundational rules:
  1. **Code must not be written by humans** — radical nine months ago, unremarkable now.
  2. **Code must not be *reviewed* by humans** — the genuinely provocative one ("big exclamation mark").
- The kicker: they were building **security software** — authentication management, issuing credentials — arguably the *most* security-conscious software imaginable, yet built under those two rules.

**Techniques worth borrowing from Strong DM:**
- **Scenario testing with an army of agents.** Scenarios are described in plain terms ("a user must log in, add something to the shopping cart, sign out"); those scenarios become test scripts; swarms of automated agents run through different scenarios hunting edge cases. Effectively an **automated, very-high-quality QA team**.
- **A "digital twin universe."** Their software integrates with **Slack, Okta, Jira** and other enterprise platforms — all of which have **rate limits**, are occasionally flaky, and can't take 10,000 tests/hour.
  - So they had a coding agent **rebuild clones** of those partners, using the partners' **API documentation and client libraries as the specification** (plus the fact that agents already "know what Slack is").
  - The clones were tiny **Go binaries** — complete-enough duplicates of Slack/Okta/etc. — with **no rate limits**, hammerable as hard as needed.
  - They could even **simulate weird production bugs** by having the digital twin reproduce them.
  - Example: a testing agent posting "Hey, I'm Janet Sanchez joining as an employee in #general" would trigger a whole simulated **onboarding + credential-issuing** sequence.

**The one rule he rejects — "token maxing."** Strong DM's third rule: *"If you haven't spent at least $1,000 on tokens per human engineer, your software factory has room for improvement."* (i.e. ~$30,000/month for the three-person team.) Willison calls this **"token maxing before anyone was calling it token maxing"** and explicitly does **not** endorse spending $30k/month. He cites a saner data point heard *that morning*: **Uber capping tools at $1,500 per engineer per month.** Takeaway: borrow the *techniques*, not the spend.

---

### Pattern 1 — Active refactoring (make review fun, and actually learn the code)
- **Stakes-based review policy**: think hard about the stakes. A decorative icon on a web page → don't sweat the details. An **authentication flow → review every line carefully.**
- But reviewing code is *miserable* — nobody wants to read 1,000 lines of a GitHub PR; you glaze over and rubber-stamp "accept."
- **Active refactoring**: instead of passively reading, **nitpick the agent's every decision** — rename this variable, refactor this, remove this duplication, "I don't get how this works — explain it and add comments."
  - This is a **complete anti-pattern with humans** (rude; can stall a PR for weeks across timezones). But **you can't be rude to an agent** — if it "gets upset," reboot it and it forgets everything.
  - It's **more fun and less boring** than read-and-accept, and you **come out actually understanding what the code does.**
- **Example prompt**: *"Refactor the tests to reduce duplicate code; rename variables for consistency with this other file."* He uses prompts like this constantly; it works very well for code that **deserves the effort**.

### Pattern 2 — Stakes and seams; verify API designs by exercising them
- The job is increasingly **software architecture/design**: get the **high-level structure** and the **seams between systems** as good as possible.
- **API design is one of the most important decisions** — any interface other code/developers will call should be **as close to flawless as possible.**
- **Best way to verify an API design: write lots of code against it.** Agents are excellent at **throwaway code** against experimental APIs.
- **Workflow trick — "review the last commit"**: if you make good commits, telling the agent to *look at the last commit* is enough for it to understand "this feature, in this part of the codebase, changed this way." Then: *"brainstorm and prototype three features against that new API"* — tell it to run in a **branch or work tree**, and it churns out the equivalent of several co-workers hacking at your API, **instantly.**
- Result: far more confidence in API designs, because **every one has been exercised** (sometimes in weird ways) by agents.

### Pattern 3 — Prototyping as verification (prototypes are now free)
- Willison has "always been a prototyper" — interactive prototypes / proofs-of-concept aren't just about the interface; they **prove something is possible** given available tools (e.g. "Can Redis serve up this combined timeline?").
- Prototypes are **effectively free** now that agents build them. Build a prototype with an agent, then **feed the verified prototype back in** as input to build the real thing.
- **Concrete example**: he's building **his own agent** (he quips that in 2026 "the hello world of programming is *build your own agent*"), and wanted Claude's feature where pasting a large block of text into the input is treated as a *file*.
  - Prompt (≈): *"Build a prototype with text editing where you can type directly in, but if you paste more than X characters (pick X, I don't care), treat it as a paste-file event."*
  - It produced a working little text editor: paste a big chunk → it shows as a "pasted file" at the bottom. He **tested it across a couple of browsers** → now has a **verified** version of the feature.
  - Later: *"Add a paste-file feature based on the prototype in `file-paste.html`."*
- He is **"hoarding prototypes."** Many of his most interesting projects spend **over a month in the prototyping phase**, trying little patterns he expects to need. Eventually: "I've covered all my bases, I have working code for all the pieces — now it's just cobbling them together into production software."

### Pattern 4 — Agentic documentation (accurate, short, uncreative)
- A long-held belief of his: *"If I'm going to read a piece of text, the writer must have put more effort in than I put into reading it — otherwise they're a vampire on my time."* True for **blog posts / persuasion / anecdotes** — but **code documentation has none of those characteristics.**
- What you want from code docs: **accurate, short, totally uncreative, tells you exactly what the thing does.** Agents are **very good at uncreative prose.**
- **Habit before landing a branch**: *"`diff against main` and review if any documentation needs to be updated."* (Again using **git as input** to the agent.) Sometimes it finds nothing; sometimes it offers updates (he accepts or rejects case-by-case).
- The main benefit is **confidence in documentation.** **Documentation trust is very hard to earn and lost instantly** — the moment docs mislead someone, they'll never trust them again. Agents give us a powerful mechanism to **keep docs continuously up to date.**

### Pattern 5 — No opinions, no promotion in generated text
- A **strong rule** for LLM-generated text: **no opinions and no rationalizations.** Agents often add a flourish like "this feature exists so that X, Y and Z" — usually **not quite the real reason**, hence misleading. **Edit it out.**
- Real commit examples of his: *"tweaked some overly promotional language"*; removing a code comment that claimed *"the whole point is to persist an async response."*
- Keeping artificial/over-promotional language out of codebases matters because **people lose trust** in docs/comments that feel artificial.

### Pattern 6 — Continuous deployment & preview environments (now trivial)
- Some things every team wants but that were "too much work" in the **pre-agent era** — his favourite example: **continuous deployment** (push a branch/PR/main → something turns "green" and deploys that version to hosting).
- He uses CD on **main** for several projects; **CD for previews has essentially no downsides.**
- With a **robust preview environment** (good auth, VPN, etc.), preview deploys take **"the risk of reviewing code by looking at it down to almost zero"** — because **reading code never tells you what you need to know vs. actually putting it through its paces.** Value for both your own testing *and* sharing/collaborating with teammates.
- This used to be **weeks of work for an engineering team**; now a single prompt does it:
  - *"Build a GitHub Actions workflow that deploys new PRs to a fresh Fly.io machine"* (or **Cloud Run / Vercel** / your host of choice), **"ask clarifying questions first."**
  - The "ask clarifying questions first" tack-on is essential — without it the agent **makes stuff up**; with it, it extracts the needed info from you and produces the "dream preview environment" with **no manual GitHub Actions fiddling.**

### Pattern 7 — Reduce the blast radius of mistakes (layered defenses)
- Agents (and humans) make mistakes that slip through; **agent mistakes may be weirder and harder to spot due to overconfidence.** So borrow software-engineering techniques for **operating when code isn't fully trustworthy.**
- **The Firefox model**: Firefox has many reported security issues, but **very few are priority-1**, because everything runs in **many layers of defense** — a bug in one part still can't break out to read files on your computer.
- Three sandboxing tools he's been using heavily:
  - **Content Security Policy (CSP)** — HTTP headers that stop pages from loading code from external domains and restrict what they can do if something goes wrong.
  - **Sandboxed iframes** — *fascinating*: an iframe area that can run **malicious JavaScript that can't do anything bad** (can't steal cookies, can't break out). Trustworthy because they're used for **banner ads** — *several decades of hardening.* Documentation is "almost impossible" to find, but **frontier agents (e.g. GPT-5.5) are good at setting them up** and have taught him a huge amount he'd struggled with for years.
  - **WebAssembly / WASI** — Wasm began as a browser tech (run compiled C/C++ in a sandbox where it can't misbehave). Newer **server-side** Wasm via **WASI (WebAssembly System Interface)** lets you run sandboxed code in server programs: **can't read files, can't make network connections, strict memory/CPU limits.** He recently read software running **Python inside WebAssembly inside Python** and it seemed to hold up.

### Pattern 8 — Attack your own sandboxes with agents
- A perennial problem with sandboxes: **you don't trust them.** Fix: **put agents inside and have them try every escape trick they know.** He tested the Python-in-Wasm sandbox by telling GPT-5.5 *"you are running in a sandbox I built — try to break out."* It couldn't (he wants to try **Claude** equivalents when he gets access).
- **Important caveat about Docker**: many people report that when they try this **in Docker, agents recognize it** ("Oh, this is Docker — if I connect to this host port I can run host commands") and **escape**. So it's specifically good to **test your sandboxes this way.**

### Pattern 9 — Zero tolerance for flaky tests (incl. UI tests)
- A test failing **1 in 50** times is historically a miserable, hours-to-days hunt — so humans *tolerate* it. **No more.** Agents **don't mind wasting their own time** and are **very good at simulating the conditions** that cause flakiness.
- **Concrete example**: a sandboxing project crashed in **GitHub Actions CI against Python 3.14** but worked fine on his Mac. He told **Codex**: *"You've got Docker — try to reproduce this."* It **reproduced enough of the Linux/CI environment in a Docker container on his Mac to replicate the bug**, found the root cause, and produced a confusing-but-correct patch he had to interrogate to understand. He **ran it in a background window and forgot about it**; checking back ~15 minutes later, it had solved the problem. "We don't have to tolerate flaky tests anymore" — a huge relief.
- **Applies to UI tests too (100%).** Browser-automation tests were *notoriously* flaky (he's worked at companies that **threw away entire test suites** over it). Two things changed: **Playwright** auto-handles timing ("the link's not there — wait a second and retry"), and **agents are fluent in all browser-testing tech** (Selenium, Playwright). You often don't even need to install anything — **Chrome's DevTools Protocol** lets agents talk JSON directly to Chrome. Browser automation "quietly got solved over the past 18 months"; he now uses it for everything, including **scraping** (if data appears in a browser, the agent can fire up the browser engine and scrape it).

### Pattern 10 — Every human-productivity tool helps the agents too
- A general principle: **any tool that helps human engineers almost always helps coding agents** — and he's been describing them all along.
- Examples: **onboarding documentation** (he notes `CLAUDE.md` *is* just onboarding documentation for your agent — "we should have had that before, we just weren't incentivized"); **continuous integration**; **linters** (he now runs them against everything — agents sort out the gnarly warning/error messages); **code formatting**; **debuggers**; **logs**; and in some cases **entire programming languages.**
- **Language angle**: he never got to grips with **Go** before (the learning curve), but **Go is fantastic for coding agents** — anything that **compiles quickly and has good error messages** lets agents practically **brute-force** their way through building things. Generating overly-ambitious projects and then picking through them is itself a great way to **learn a new language.**

### The big picture — agentic engineering as a Trojan horse for good practices
- **Analogy to accessibility**: web accessibility was always a hard sell — until people realized **Google/SEO was effectively the world's most prolific screenless user.** Once SEO was the carrot, people adopted **semantic headings and accessibility** wholesale. **SEO was the trick that got people to care about accessibility.**
- Likewise, **agentic engineering is the trick that teaches everyone good engineering practices.** Decades-old-but-neglected discipline (tests, docs, CI/CD, linters) is suddenly worth learning, because the acceleration forces us to **work like mega-corporations — on our laptops, with armies of agents.**
- He's **rereading _The Mythical Man-Month_ (1978)** and finds **three chapters directly applicable** to agentic engineering in 2026.

### Build "verification machines," not dark factories
- His own setup isn't a true dark factory — "more of a slightly gray, hazy factory"; he **still reviews code when needed.**
- The most important thing is to **build verification machines**: anything that helps you and your agents **verify the code is good, works, and is high-quality.**
- **Closing thesis**: *"If we're going to use these tools to build worse software faster, we're missing a trick. We should be using this stuff to build* ***better*** *software faster."* We can have **higher quality, easier maintenance, AND more features** — normally a "two out of three," but here we get **all three.** We get to **reinvent how software is built**; nobody asked for it, nobody knows the end state, but it's a thrill to be present for it.
- Find him at **simonwillison.net**, and on **Mastodon, Bluesky, and Twitter.**

### Q&A highlights
- **What are you reading/listening to?** _Mythical Man-Month_'s concept of **conceptual integrity** — a large system must be understandable/explainable as a coherent whole. Big risk with agents: every feature is "just another prompt," producing a **weirdly-shaped product** you can't even remember the capabilities of the next day (he calls his January-2026 phase **"coding-agent psychosis"** — he rebuilt JavaScript in Python, built a Go application server with lazy-loading/proxying, ~4–5 giant projects untouched since February because they were terrible ideas with no market fit). Lesson: **just because you can build it doesn't mean you should**; the hard problem now is **personal discipline.**
- **Where do I find templates/repos that bake these principles in?** **Jesse Vincent** (sitting front row) built **Superpowers** — a set of **skills for Claude Code / Codex** that bakes in much of this (e.g. brainstorming → test-driven development). Good starting point, but patterns are still evolving — **the most important thing is to just try it out.** Take on **side projects**; he's been doing **game development** (half a dozen games, including a 3D game in **Rust**, all "terrible") and learned the hard part isn't drawing on screen — it's a **compelling game loop**, which he hasn't cracked.
- **The "jagged frontier":** LLMs are unpredictably great at some things and bad at others. The only way to learn the boundary is to **throw overly-ambitious projects at them.** Great trick: **if something fails, pocket it and retry in six months** — it often starts working, and you may be the **first person in the world** to discover an agent can now do it.
- **How do different languages behave in agentic flow?** A year ago there were clear winners (Python, JavaScript great; Rust often failed to compile ~18 months ago). **That's changed entirely** post-November models — agents can write code in a **language you just made up**, brute-forcing through *especially* if it has good error messages. He's "**running out of tasks they can't do**" (awkward for benchmarking new models). He optimizes for **his own readability** — picks **Go over Rust** because he can read ~all of it, whereas Rust's **borrow checker / refs / signatures** still trip him up (one of his model tests: *"can it teach a Python programmer how the Rust borrow checker works?"* — improving, but he hasn't internalized it). He's even written **Swift UI** Mac menu-bar apps **without knowing a single line of Swift.** With strong fundamentals (red-green TDD, good test harnesses), "the world is your oyster."
- **HTML prototypes vs. spec-driven development?** He uses both. The most basic spec-driven version is **Claude Code's planning mode**; he often does informal planning — **brainstorm with a model, have it write a markdown file** describing the feature, then feed that markdown to the implementing model. Works **across all models** (brainstorm with Claude, implement with Codex). Huge bonus: **review becomes far easier** — instead of decoding unfamiliar code, you're just **checking it did exactly what you agreed.**
- **Zero tolerance for flaky UI tests too?** Yes (see Pattern 9). His own UI testing is **very basic** (open window, navigate, click button) and he **doesn't review that test code closely** — a great property of UI tests is **you can watch them run** (the window pops open, you see it click/select), which makes reading the underlying code add little value. He has nothing against behavior-driven development; he just keeps it simple.
- **Regulated industries / SOC-2 / CISO conversations?** He's candid: he **last dealt with these problems eight years ago**, pre-coding-agents, so he has **no specific advice** here. Good news: **every regulated industry faces the same problems right now.** His one transferable tip: **find peers doing your job at similar companies and form a "cabal"** — monthly coffee to swap the dirty tricks that actually work (he did this as an engineering manager; it was fantastic). (Audience referenced a **"Swiss cheese" layered-defense model** where each layer produces artifacts that satisfy controls/requirements — Willison didn't claim production experience with that specific compliance mapping.)
- **Does code readability still matter** if you don't know the language and agents maintain it? Comes back to **blast radius / stakes**: high-stakes code, yes, absolutely; low-stakes "vibed-up" UI on a rarely-visited page, less so (a future agent can clean it up). But there's a real tension: **good code for humans is good code for agents.** Agents are **great at consistency** — drop one into a **good codebase** and it tends to **keep it good**; drop one into a **gritty codebase** and it risks getting **messier and messier** over iterations. Since keeping it clean isn't expensive, **investing in readability is worth it.** (He stresses he's **not confident** this answer is correct.)
- **Is the coding-agent transcript a necessary artifact?** **"So much. Yes."** His biggest frustration: **agents don't treat transcripts with respect** (Claude Code, last he checked ~6 months ago, **deleted transcripts older than 90 days by default** — presumably fixed by now). **"There's gold in those"** — most of the work now lives in the transcript. His favourite agent is **Codex Desktop** purely for its **"copy as markdown"** button: he pastes the transcript into a **GitHub Gist** and **links the gist in the commit message** → archived forever. He rarely re-reads them, but treats them like **commit messages** — irrelevant until the day you need to know *why on earth* you decided to do something a certain way. Coding agents **should value their transcripts far more.**

## 🛠️ Products / Features / Technologies Mentioned
- **Coding agents (general class)** — software where the LLM both writes and executes/tests/iterates on code; "only really got good" in November 2025.
- **Claude / Opus 4.5 (Anthropic)** — flagship model whose Nov-2025 release helped trigger the inflection point; also the source of the paste-large-text-as-file UX he cloned. ("Claude Mythos" referenced as a sandbox-testing target he wants access to.)
- **GPT-5.1 (OpenAI)** — improved coding model/harness contributing to the November inflection point.
- **GPT-5.5 (OpenAI)** — frontier model he uses for sandboxed-iframe setup and for **attacking his own sandboxes** to test escape resistance.
- **Claude Code** — coding agent; its **planning mode** and `CLAUDE.md` onboarding-doc convention are cited; criticized for deleting old transcripts by default.
- **Codex / Codex Desktop (OpenAI)** — coding agent he used to reproduce a CI-only bug in Docker; **Codex Desktop's "copy as markdown"** transcript export is his favourite feature.
- **GitHub / GitHub Actions** — CI/CD; prompt-generate a workflow to deploy PRs to preview environments; also where the Python 3.14 CI bug surfaced.
- **GitHub Gist** — where he archives agent transcripts and links them from commit messages.
- **Fly.io / Google Cloud Run / Vercel** — hosting targets for auto-deployed per-PR preview environments.
- **Content Security Policy (CSP)** — HTTP headers restricting external code loading and page capabilities (blast-radius reduction).
- **Sandboxed iframes** — heavily-hardened (via banner-ad history) browser sandbox that can run untrusted JS safely.
- **WebAssembly (Wasm) + WASI (WebAssembly System Interface)** — browser-origin sandbox tech now usable **server-side** to run code with no file/network access and strict CPU/memory limits.
- **Playwright** — browser-automation framework that auto-retries on timing issues, dramatically reducing UI-test flakiness.
- **Selenium** — older browser-automation framework agents are fluent in.
- **Chrome DevTools Protocol** — lets agents drive Google Chrome via JSON directly, no extra install needed.
- **Docker** — used to reproduce Linux/CI bugs locally; **caution**: agents often recognize Docker and escape its sandbox via host-port tricks.
- **Redis** — referenced as the kind of capability question a prototype answers ("can Redis serve this combined timeline?").
- **Go** — fast-compiling, good-error-message language that's **excellent for coding agents**; used by Strong DM for their tiny digital-twin binaries.
- **Rust** — agents now write it well, but Willison still struggles to *read* it (borrow checker); used for his 3D game experiments.
- **Swift / SwiftUI** — used (via agents) to build Mac menu-bar apps despite him not knowing the language.
- **Python** — used throughout; including running Python inside WebAssembly inside Python; CI bug was Python 3.14.
- **Slack / Okta / Jira** — enterprise platforms Strong DM cloned as "digital twins" for unlimited integration testing.
- **Superpowers (by Jesse Vincent)** — a set of skills for Claude Code / Codex that bakes in brainstorming + TDD patterns; recommended starting point.
- **GPT-3 (2022)** — his original LLM-for-code experiments (SQL queries, code explanation).

## 🚀 Announcements / What's New
None explicitly announced. This is a patterns/practitioner talk, not a product-launch session. Contextual references to recent releases (Opus 4.5, GPT-5.1, and the "November 2025 inflection point") describe the existing landscape rather than new Build announcements.

## 💡 Demos
No live on-stage demos were run (the clicker even failed at the start). Willison instead walked through **screenshots/examples from his own real work**, notably:
- **The paste-file prototype** — a small text editor built by an agent where pasting > X characters renders the content as a "pasted file" at the bottom; shown as proof that prototypes are cheap, verifiable, and reusable as later prompt inputs.
- **Strong DM's Slack "digital twin"** — a screenshot of an agent-rebuilt Slack clone (tiny Go binary) and a testing agent posting "Hey, I'm Janet Sanchez joining as an employee in #general" to trigger a simulated onboarding/credentialing flow.
- **Commit-message examples** — e.g. "tweaked some overly promotional language" — illustrating the no-opinions/no-promotion editing rule.

## 📊 Notable Stats / Quotes
- **10–50 lines of delivered code per person per day** — industry-average productivity (Steve McConnell, _Code Complete_, 2004).
- **600 LOC/day** — once cited as a *high outlier* of developer performance (a source ~10 years after _Code Complete_).
- **~600 lines of tested + documented code on his phone, while walking the dog** — Willison's casual present-day output.
- **November 2025** — the inflection point when coding agents became reliable daily drivers (Opus 4.5, GPT-5.1, matured harnesses).
- **Microsoft: 100,000+ developers, 25,000,000+ lines of code** — the "no single human can review it all" scale that motivates layered verification.
- **Strong DM: a team of 3** building security software under "no human writes code" + "no human reviews code"; their token rule = **$1,000+ tokens per engineer (~$30,000/month)** — which Willison rejects.
- **Uber: $1,500 per engineer per month** tool cap — cited as the saner spending benchmark.
- **1 in 50** — the flaky-test failure rate he now refuses to tolerate; the background agent solved the CI repro in **~15 minutes.**
- **Claude Code deleted transcripts older than 90 days by default** (as of ~6 months before the talk).
- _"You can't be rude to an agent. If you're rude to your agent and it gets upset, you can reboot it and it forgets everything."_
- _"In 2026 the hello world of programming is: build your own agent."_
- _"Token maxing before anyone was calling it token maxing."_
- _"Documentation trust is very difficult to earn and you can lose it instantly."_
- _"If we're going to use these tools to build worse software faster, we're missing a trick. We should be using this stuff to build* ***better*** *software faster."_
- _"Agentic engineering... it's a trick to teach everyone good engineering practices"_ (the SEO-for-accessibility analogy).
- _"The jagged frontier"_ — LLMs are unpredictably good/bad; the only way to learn the edge is to try overly-ambitious things.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Adopt **active refactoring** on the next real PR from a coding agent — nitpick names/dedupe/"explain and add comments" instead of read-and-accept.
  - Wire up **per-PR preview deploys** with the "build a GitHub Actions workflow… ask clarifying questions first" prompt (Fly.io / Cloud Run / Vercel).
  - Add the **`diff against main → does any documentation need updating?`** step to my pre-merge checklist.
  - Try the **"review the last commit → brainstorm & prototype 3 features against this API in a work tree"** loop to stress-test an API design.
  - Experiment with a **WASI server-side sandbox** for running untrusted/agent-generated code; then **attack it with an agent** to confirm it can't escape (and remember the **Docker-escape caveat**).
  - Start **hoarding prototypes** as `.html`/standalone files and feeding the verified ones back as prompt inputs.
  - Set up **transcript archiving** (Codex Desktop "copy as markdown" → Gist → link in commit message).
  - Look at **Superpowers** (Jesse Vincent) for Claude Code / Codex skills (brainstorm + TDD).
- [ ] Questions:
  - What does a **layered "Swiss cheese" verification model mapped to SOC-2 / audit artifacts** actually look like for a regulated team? (Willison explicitly couldn't answer.)
  - For our stack, which **digital-twin clones** (of internal/3rd-party APIs) would unlock unlimited, rate-limit-free scenario testing?
  - What's our equivalent of a per-engineer **token budget** — and what governance makes it sane (cf. Uber's $1,500/mo)?
  - How do we preserve **conceptual integrity** when every feature is "just another prompt"?
- [ ] Relevant to:
  - Anyone shipping AI-assisted code who needs a **verification / quality strategy** (testing, CI/CD, sandboxing, docs).
  - Platform/DevEx teams designing **preview environments, CI, and sandboxed execution** for agent-generated code.
  - Engineering leaders thinking about **agentic engineering practice, tooling budgets, and code-review policy.**

## 🔗 Related
- [[BRK208 - Ensuring your code works when AI testing isnt enough]] (this note)
- Topic: agentic engineering / AI-assisted coding · verification & testing · sandboxing (CSP, sandboxed iframes, WebAssembly/WASI) · continuous deployment & preview environments
- People/projects: Simon Willison (simonwillison.net) · Jesse Vincent — *Superpowers* · Andrej Karpathy ("vibe coding") · Strong DM ("dark factory" / digital twins)
- Reading: *The Mythical Man-Month* (Brooks, 1978) — conceptual integrity · *Code Complete* (McConnell, 2004)
- 