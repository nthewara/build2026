---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/github-copilot
  - topic/visual-studio
  - topic/debugging
  - topic/profiling
  - topic/dotnet
  - topic/ai
source: https://www.youtube.com/watch?v=Nt87zSqfk-o
session_code: BRK207
event: Microsoft Build 2026
speakers: Mads Kristensen (Visual Studio team), Nick (Visual Studio team, former profiler dev lead)
duration_min: 44
aliases:
  - GitHub Copilot in Visual Studio Agents That Debug Profile Test
---

# BRK207 — GitHub Copilot in Visual Studio: Agents That Debug, Profile, and Test

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mads Kristensen (PM, Visual Studio team) & Nick (Visual Studio team, former dev lead for the VS profiler)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=Nt87zSqfk-o)

## 🎯 TL;DR
Visual Studio is positioning itself as **the** tool for professional C# and C++ developers on Windows in the new agentic world — built for teams who treat code as a long-lived **asset** (quality gates, security, compliance, governance) rather than a throwaway artifact. The talk is demo-heavy: the team dogfoods Copilot *on Visual Studio's own source* (the 160-project Diagnostics Hub / profiler solution) to fix a real crash via test-first development, then uses a new **debugger agent** and **profiler agent** to autonomously debug an off-by-one bug and nearly double the speed of a file-decode hot path. The core message is *guardrails + agents*: you write a failing test (or capture a profiling trace) to create a durable harness, then "let the agent cook" while staying in the loop — you steer, it executes against real runtime **data**, not guesses. The back half is a roadmap reveal: web-forms→Blazor modernization, auto-applied agent skills, AI merge-conflict resolution, faster builds, a move onto the shared **GitHub Copilot CLI SDK**, and **bring-any-model** support (local/on-prem/cloud) with enterprise lock-down — most landing in **Visual Studio 2026 Insiders next week**.

## 🔑 Key Takeaways
- **Visual Studio's identity in the agentic era:** the premier tool for *professional C#/C++ developers on Windows*. Other stacks (Python, Node.js) are better served by VS Code and other tools — VS doubles down on the pro segment.
- **Asset vs. artifact framing:** if code is an **asset** (maintained for years, by a team, where standards/formatting/quality matter) → Visual Studio is for you. If code is an **artifact** (a throwaway PoC/internal tool you don't need to read) → you may not need that rigor. This distinction frames all their investment.
- **Code quality matters *more* in agentic dev, not less:** you may not write the code, but you definitely **review** it — VS focuses on quality gates, security, accessibility, compliance, governance, IT-admin control (group policy across a fleet).
- **Governance over YOLO:** Copilot's MCP tool calls require explicit confirmation; it uses *your* credentials. Nick deliberately stays "in the loop" rather than autopilot — though full autopilot is available if you want it.
- **Test-first is reborn because of Copilot:** Nick (a TDD skeptic for years) now writes a failing test *first* to reproduce a bug, creating a durable test harness/guardrail, then lets Copilot author the fix. The test stays in the repo as a durable artifact for future refactors.
- **New debugger agent:** a specialized agent (distinct from regular agent mode) that *knows how to use the debugger* — sets/hits breakpoints, evaluates expressions, inspects memory, forms a hypothesis, applies a fix, then re-runs the test **under the debugger** to validate. Invoked via right-click → **"Debug this test with Copilot."**
- **New profiler agent:** right-click → **"Profile with Copilot."** It runs a unit test with the profiler attached (CPU/allocation, static + dynamic instrumentation), reads the trace, finds the hot path, proposes and applies a low-level optimization, then **re-profiles to validate the improvement** — a proper before/after scientific measurement.
- **"If you're not using data, you're not profiling — you're just refactoring."** The agents optimize from *executed runtime data*, not by eyeballing code, which is a far stronger basis for a fix.
- **VS Test Performance Collector (NuGet):** add it to your test runs and every CI/Azure DevOps run auto-captures a profiling trace (a `.diagsession`) as a test attachment — making performance regression detection part of the inner loop / CI instead of an afterthought.
- **Real, dogfooded wins:** doubled `.diagsession` read perf via 6–7 PRs; the profiler agent found **800,000 allocations** in VS startup (XML deserialization of an Azure DevOps cache file) → trimmed **~50 MB off the initial heap**; also improved Azure App Service and the Roslyn compiler (a new switch-case optimization, found by an SDE2 as their first Roslyn contribution).
- **MCP servers in Copilot** (esp. a new **Azure DevOps / ADO** connector) let Copilot fetch a work item from a pasted bug link, find a CI test run, locate its `.diagsession`, and analyze it — pulling external context directly into the loop.
- **Why VS gets Copilot features "late":** VS has its *own* Copilot backend implementation (talks to the Copilot API itself) and must wire it into the profiler/debugger/modernization agents. Fix: moving onto the shared **GitHub Copilot CLI SDK** so VS, VS Code, and the CLI share one base and ship features in lockstep.
- **Your expertise still matters:** "the better you are at your job as a developer, the better you are at managing your agent." The human steers; non-deterministic agents need a skilled hand.
- **Progressive enhancement model:** like HTML5 → Ajax → React, the manual experience is the base layer — you can do everything by hand — and Copilot is the optional layer on top to push further. You choose when to use it.
- **Roadmap (mostly Insiders next week):** web-forms→Blazor app modernization (with Aspire + cloud uplift), auto-applied agent skills authored by feature teams, AI merge-conflict resolution, smarter/faster builds, Copilot CLI SDK migration, and **any-model** support (local/on-prem/cloud) with an enterprise security/management layer. Also shipping next week: Git **work tree** support and **Git submodule** support.

## 📚 Detailed Notes

### Framing: How Visual Studio fits the agentic world
Mads opens by addressing the recurring booth/conference question: *where does Visual Studio fit now that agents are everywhere?* Answer — it works great, and it has a clear position: **the tool for professional C# and C++ developers on Windows**, today and tomorrow, whether you're hand-coding all day or orchestrating a fleet of agents. For Python/Node.js etc., Microsoft has other tools (VS Code is "fantastic") — VS isn't trying to be everything; it's laser-focused on the pro C#/C++ segment.

What makes VS especially good for *professional* developers is the surrounding rigor that pros care about:
- **Quality gates** — what does the code actually look like?
- **Security & accessibility**
- **Compliance & governance**
- **Administration** — IT admins / group policy deciding how VS behaves across an org's fleet.

This is a continuing high priority and is where investment is going.

### Asset vs. artifact — the central mental model
The talk's organizing idea. In agentic development you "don't always write the code, but you definitely review it." So how do you maintain quality, standards, and formatting when an agent wrote it? It depends on what the code *is*:
- **Code as an asset:** something you maintain for years, possibly across a whole team. Coding standards, formatting, and quality all matter because the code itself has lasting value. → **This is who Visual Studio is for.**
- **Code as an artifact:** proof-of-concepts or internal tools where the code is just *the thing you're producing*; you don't need to read it carefully or maintain it, and you're fine letting the agent own it. → Less of that rigor needed.

VS's "very, very serious" investment is squarely aimed at developers who see **code as an asset**.

### Demo 1 — Fixing a real crash in Visual Studio's own profiler (test-first)
Nick frames the demo around realism: rather than a toy app, he works **on Visual Studio inside Visual Studio**. The open solution is **Diagnostics Hub** — the code name for the **Visual Studio profiler** itself, which gets built and packaged into VS and powers all the profiling tools. It's a genuinely large, polyglot component: **C++, C#, JavaScript, plus some assembly and IL**, totaling **160 projects** (just for the profiler + the diagnostic-tools window). (When VS migrated from TFS to Git, the repo was ~**400 GB** of data.)

**The bug:** an internal telemetry crash — `IndexOutOfRange` in the **hybrid dictionary enum keys iterator**. A new profiler feature exercised a previously-unused code path, so internal dogfooders hit crashes that code review never caught (the path had no tests). The bug was filed and routed to Nick.

**The agentic workflow:**
1. Nick copies the bug link into **Copilot chat** and leans on **MCP servers** — specifically a new **Azure DevOps (ADO)** connector — saying, in effect: *"We're getting this crash (here's the bug link) — write me a unit test that demonstrates it."*
2. Copilot calls the MCP tool. Crucially it **prompts for confirmation** (`get work item`) — it can't go full autopilot/YOLO without permission, and it uses Nick's credentials (it grabs an auth token). Mads notes you *could* enable autopilot, but Nick prefers staying in the loop to understand what's happening — tying back to the governance theme.
3. Copilot fetches the work item, reads the stack trace, inspects the **HybridDictionary** source and existing test structure, identifies the problem area, finds the relevant tests, and **authors two new test methods** (one enumerating keys, one enumerating values) in the **data warehouse managed suites** test project.
4. First **build fails (1 failed)**: *"The type 'string' must be a non-nullable value type"* — the dictionary key needs a **struct**. Nick just tells Copilot "those don't compile, looks like the wrong key type," and it investigates the generic key constraints and fixes it. Build succeeds.

**Why test-first (the discussion):** Mads probes the approach. Nick admits he *"never believed in test-driven development until Copilot came along"* — it felt awkward; he preferred writing code then adding a few tests. Now he writes tests first to build a **test harness / guardrail**, then lets Copilot **author the fix** against those tests. Mads reframes it: the harness gives you the *safety* to "let loose the agent" on your code. Bonus — it's a **durable artifact** that lives with the repo, protecting future Copilot-driven refactors and dependency swaps.

**Running the test — real-world messiness:** Nick runs the new test expecting it to fail and reproduce the crash. On large enterprise software (hundreds of projects) nothing is instant. The test fails — *"This is a success!"* — but the **test detail summary** reveals it's failing in an **assert**, *not* throwing the expected `IndexOutOfRange`. This is the realistic moment: writing a repro reveals *other* problems. Nick iterates with Copilot. A telling slip: when he says "yes" to a suggested fix, Copilot starts **fixing the code** when he only wanted the **test** fixed — *"Not supposed to fix the code yet."* He re-steers: "fix the test so it fails with index out of range." Both speakers note the **non-deterministic / probabilistic** nature of agents — you get different runs each time, which is "the fun of it." Mads' key point: Nick's **expertise** let him see what was happening and guide the agent — *"the better you are at your job as a developer, the better you are at managing your agent."*

**Letting the agent cook with the debugger agent:** With a solid failing test (now correctly throwing `IndexOutOfRange`) as a guardrail, Nick right-clicks the test → **"Debug this test with Copilot."** This switches from regular agent mode into the **debugger agent**, which *knows how to use the debugger*: set/hit breakpoints, evaluate expressions, inspect memory, and genuinely understand the code. It states a hypothesis — *"the bug is clear"* — pinpoints an **off-by-one error** (very specific about the element count in the collection), applies the fix, **re-runs the unit test under the debugger** (so it could catch any new problem), and confirms the test now passes.

**Real impact:** this was a genuine bug, caught internally (in the **18.5 / April update** range) before it reached customers; Copilot authored and pushed the fix. Mads underlines that off-by-one errors — simple but sometimes maddening to find — are exactly the kind of thing this accelerates.

### Demo 2 — The profiler agent: nearly doubling a hot path on stage
Nick introduces the **VS Test Performance Collector**, a recently added **NuGet package** you add to your test runs. They added it to their **Azure DevOps** test runs so that *every* unit-test run **automatically captures a profiling trace** and attaches it to the test result.

**What a profiling trace is (explained):** when a test runs, the profiler turns on, periodically samples *where the program is* throughout the run, then at the end saves all that data plus auxiliary data — **debugger symbols, .NET metadata** — and produces a report of where the program spent the most time. It can capture **CPU data and allocation/object-allocation data**. The format of the trace file is a **`.diagsession`** (`.diagsession` files contain the ETL trace; opening one in VS reads it into memory). The demo uses both **static instrumentation** and **dynamic instrumentation** — the test hooks into the profiler, which **instruments the code with start/stop around method calls** to get exact per-method performance.

**The target:** a CI run flagged a `decode large file` / `verify my large file` unit test (which compresses/decompresses a `.diagsession` containing an ETL file) as spending most of its time in a particular spot. So Nick right-clicks → **"Profile with Copilot"** (again, the "make a clicky button for the thing we do over and over" theme — and again, you can just choose **"Profile"** to do it all yourself and get your hands dirty; Copilot doesn't *need* the UI to pop, but VS shows it so you can explore and **steer the conversation**).

**A teaching superpower:** after an optimization, you can ask Copilot **"why is this faster?"** and *learn* — about the **JIT**, the **GC**, why one collection/list/dictionary type beats another, unsafe C# tricks you wouldn't otherwise know. Mads (knows C# but not unsafe C#) calls this hugely helpful.

**The run:**
- Initial trace: the test takes exactly **3.88 seconds**. The hot path is dominated by an **Express stream** frame repeatedly hitting a **`CheckReadEnoughBits`** function. Nick wrote this code himself, was the profiler dev lead, profiled it "over and over" for years — and there were *still* optimizations to find.
- Copilot suggests: *"optimize this Express stream read block to buffer reads and reduce the binary reader overhead."* Nick clicks **"go for it."** It reads the source context, matches **line information** to the **profiling report**, and knows exactly what to optimize — i.e. it's grounded in **actual executed data**, not guessing from the code (a stronger scientific case for the change).
- The change reads the input stream into a **new byte array** to read from directly, reducing calls into the **byte/binary reader** (already "the fastest way to access a byte stream in .NET" — yet the agent still improved it). It touches low-level **Huffman table read** / compression code used for these large `.diagsession` files.
- **Measure twice, optimize once:** the agent then **rebuilds, re-runs the tests** (to ensure no regression in behavior), and **re-profiles** to validate. Mads stresses this is *the* scientific method for perf — establish a baseline, change, measure again to see real impact. ("Optimize twice / measure twice, optimize once.")
- Real-world hiccups on stage: 160-project builds take a while; unrelated projects throw errors; **Test Explorer also kicks off its own build** — "as real as it gets."
- **Result:** the new green-er chart shows **~2 seconds**, down from **3.88s** — they **almost doubled** the performance of decoding a large file, live on stage.

**Inner loop, not afterthought:** historically profiling was something you did *after* coding; even opening a trace took minutes, so it became an afterthought outside the build/run/test inner loop. Now it's fast enough to run *as part of the inner loop* — start a session, check for regressions, know within ~a minute. With the NuGet collector feeding CI, you get `.diagsession` files on every run, can spot regressions, download the file, and open it in VS to see exactly what's wrong — or use the **ADO MCP tools** to have Copilot *find* the diagnostic sessions from a pipeline/test-run URL and analyze them automatically. Mads' aside: improving performance is one of the few things developers can do **without asking permission** — no Jira/GitHub ticket needed; everyone just benefits.

### Real-world results beyond the demos
Switching back to slides, Nick recaps where they've pointed the **profiler agent**:
- **Visual Studio startup:** found **800,000 allocations** caused by **XML deserialization of an Azure DevOps cache file** when loading the version-control library. He set up a rough loop — *"run devenv, allocation-profile it, see what you can do"* — and it **trimmed ~50 MB off the initial heap** and removed 800k allocations, dramatically reducing GC work.
- **`.diagsession` reader:** **6–7 PRs** that **more than doubled** the performance of reading these files in the latest VS.
- **Azure App Service:** ran the agent against it (not just VS) to **reduce the cost of running Azure App Services** by optimizing performance.
- **Roslyn compiler (~2–3 weeks ago):** Roslyn has tons of benchmarks and has been optimized for years, yet the agent found an optimization in **switch-case evaluation**. An **SDE2** downloaded Roslyn, ran the profiler agent over its tests, and landed their **first-ever Roslyn contribution**.

Takeaway: this works across a wide variety of app types — UI, APIs, DLLs/libraries, `.NET`, C++ — "across the board."

### Roadmap — what's coming (much of it in Insiders next week)
Mads runs through upcoming features. (Git **work tree** support and **Git submodule** support are also landing next week but he sets those aside to focus on Copilot.)

- **App modernization: Web Forms → Blazor.** A real pain point — fewer developers remain who can maintain old WinForms/Web Forms apps (some on **.NET 3.0**), and managers won't fund "6 months to convert to Blazor / .NET 10." Recent breakthroughs let the **modernization agent** convert Web Forms — including **user controls, server controls, components** — into **Blazor**, modernize onto a current stack, add **Aspire**, and even **uplift to run in the cloud**. Big for enterprises sitting on legacy apps.
- **Agent skills, auto-applied.** Agent skills (just **markdown files** in plugin/marketplace repos) make agent workflows far more powerful, but discovery is a real problem — how do you know which skills apply to WinForms or a given `.NET` scenario? VS will **automatically detect what you're working on** and inject the relevant skills into context. These skills are authored by the **actual feature teams** (Azure team, WinForms team, etc.) — the absolute experts — are **open source**, take **community contributions**, and are "skills you can trust," applied automatically.
- **Faster builds during agent runs.** Agents frequently trigger builds. Today VS may see errors in the error list yet still kick off a ~2-minute build before failing on an error it could have known about upfront. First optimization: **check the error list and other indicators before kicking off a build** — skip or defer the build when it's obviously going to fail. One of many perf optimizations coming to the chat window and broader experience.
- **AI merge-conflict resolution** (one of Mads' favorites). Developers report real fear/anxiety/frustration around committing when they're behind HEAD and must pull first ("almost shaking moving the mouse to the pull button"). Soon: **click a button and let the AI resolve merge conflicts.** When they test "what would a human do?" vs. the agent, the agent is *very* capable and nearly matches a human; if it can't, you still do it manually. Often only one (or none) of several conflicts actually needs your input — it "takes the heartache away."
- **Why VS lagged on Copilot features — and the fix.** Audience knows the pain: VS often gets Copilot features later. Reasons: VS has its **own Copilot implementation** — it talks to the **Copilot API itself** and must integrate with the **profiler, debugger agent, app modernization**, etc. that other tools lack; and it has its **own backend implementation**. **Fix (rolling out next week on VS Insiders):** move onto the **GitHub Copilot CLI SDK**, so **Visual Studio, VS Code, and the CLI all share the same base/SDK** and get features **at the same time**. They're still *implemented* differently — e.g. when the agent kicks off a build in VS, it uses VS to build (**MSBuild already warm, Roslyn already running**), which is **faster than building on the command line**. So VS keeps doing its VS-specific things atop the shared SDK. Mads has run it full-time for ~a month and "absolutely loves" it.
- **Bring any model.** Today VS offers a model list — **Opus, Sonnet, GPTs**, plus add-your-own (**xAI/Grok, Gemini**, etc.) with **bring-your-own-key** from an approved provider list — but you must still sign in with **GitHub Copilot credentials**. Coming "very soon": use **any model in Visual Studio**, whether **local, on-prem, or cloud, anywhere** — huge for enterprises with strict security needs who can't use cloud models (run it on your machine, on-prem, your own server room, no restrictions). Because VS targets pro developers who care about **trust boundaries**, there's a **security/management layer**: orgs can **lock it down** and mandate only specific models/providers (e.g. only a local model, or only one cloud provider). Start checking it out **next week in VS 2026 Insiders**.

### The throughline — progressive enhancement + human-in-the-loop
Mads ties it together with a **progressive-enhancement** analogy: like the web went from basic HTML (click a link, full page reload) → **Ajax** (partial page loads) → **React/Angular** and more on top — each layer usable only as browsers became more capable — Copilot in VS works the same way. The **manual experience is the base layer**: you can be the driver and do *everything* by hand, fully in control, exactly as you always have. Copilot is the **optional layer on top** to push the limits. Sometimes you want the Copilot experience; sometimes you don't — **you decide**. Combined with the recurring "your expertise makes you a better agent manager" point and the explicit, credential-scoped MCP confirmations, the consistent philosophy is **agents as a powerful, opt-in enhancement under human control**, anchored to real runtime data and durable guardrails (tests, profiling traces).

Mads closes encouraging everyone to grab **VS 2026 Insiders next week** for the upcoming features.

## 🛠️ Products / Features / Technologies Mentioned
- **Visual Studio (2026)** — the IDE; positioned as the premier tool for professional C#/C++ developers on Windows.
- **GitHub Copilot in Visual Studio** — the AI assistant; agent mode, chat, and specialized agents inside VS.
- **Copilot chat** — conversational interface where Nick drives the bug-fix and profiling workflows.
- **Agent mode (regular)** — the default Copilot agent that gathers context, writes tests/code, and applies changes.
- **Debugger agent** — specialized agent that uses the debugger (breakpoints, expression eval, memory inspection) to diagnose/fix bugs and validate under the debugger.
- **Profiler agent** — specialized agent that runs tests with the profiler attached, analyzes traces, applies perf optimizations, and re-profiles to validate.
- **MCP servers (Model Context Protocol)** — pluggable tool endpoints Copilot can call; require user confirmation, use your credentials.
- **Azure DevOps (ADO) MCP connector** — fetches work items from a bug link, finds CI test runs, locates `.diagsession` files, etc.
- **VS Test Performance Collector** — NuGet package added to test runs that auto-captures a profiling trace as a test attachment on every (CI) run.
- **`.diagsession`** — the Visual Studio profiler trace file format (contains the ETL trace + symbols + .NET metadata); opening one reads it into memory.
- **Diagnostics Hub** — internal code name for the Visual Studio profiler itself (the demo solution; 160 projects; C++/C#/JS/assembly/IL).
- **Diagnostic Tools window** — the debugging window with live graphs; part of the same component.
- **HybridDictionary** — the .NET collection whose enum-keys iterator had the `IndexOutOfRange` crash.
- **Test Explorer** — VS test runner UI used to run the repro test.
- **Static & dynamic instrumentation** — profiling techniques inserting start/stop around method calls for exact per-method timing.
- **CPU & allocation profiling** — trace types capturing time spent and object/memory allocations.
- **Express stream / Huffman table read** — the low-level compression code path optimized in Demo 2.
- **Binary/byte reader (.NET)** — "fastest way to access a byte stream" — yet further optimized via a direct byte-array read.
- **MSBuild** — the build engine; kept "warm" inside VS so agent-triggered builds are faster than CLI builds.
- **Roslyn** — the C#/VB compiler; profiler agent found a switch-case evaluation optimization.
- **JIT / GC** — runtime internals Copilot can explain when you ask "why is this faster?".
- **App modernization / modernization agent** — converts Web Forms (incl. user/server controls, components) → Blazor, adds Aspire, cloud uplift.
- **Web Forms / WinForms** — legacy UI stacks (some on .NET 3.0) targeted by modernization.
- **Blazor** — modern .NET web UI stack; modernization target.
- **.NET Aspire** — added to modernized apps for cloud-ready composition.
- **.NET 10 / .NET 3.0** — modern target vs. legacy starting point referenced.
- **Agent skills** — markdown files in plugin/marketplace repos; VS auto-detects context and injects team-authored skills.
- **GitHub Copilot CLI SDK** — shared base that VS, VS Code, and the CLI will all move onto for feature parity.
- **AI merge-conflict resolution** — one-click AI resolution of Git merge conflicts (upcoming).
- **Git work tree support / Git submodule support** — VS source-control features landing next week.
- **TFS → Git migration** — historical context; the profiler repo was ~400 GB at conversion.
- **Models:** Claude **Opus** & **Sonnet**, OpenAI **GPT** models, **xAI/Grok**, **Google Gemini** — selectable; bring-your-own-key; upcoming any-model (local/on-prem/cloud) support.
- **Group policy / enterprise management layer** — admin controls to mandate/restrict which models an org may use.

## 🚀 Announcements / What's New
*(Most items are roadmap/upcoming; many land in **Visual Studio 2026 Insiders next week**. Treat as previews unless noted.)*
- **Debugger agent** — "Debug this test with Copilot" right-click flow; debugs, hypothesizes, fixes, validates under the debugger. *(Shown live; appears current/near-current.)*
- **Profiler agent** — "Profile with Copilot" right-click flow; profiles → optimizes → re-profiles to validate. *(Shown live.)*
- **VS Test Performance Collector (NuGet)** — auto-captures profiling traces in CI as test attachments. *("Recently added.")*
- **App modernization: Web Forms → Blazor** (incl. controls/components, Aspire, cloud uplift) via the modernization agent. *(Recent breakthrough / upcoming.)*
- **Auto-applied agent skills** — VS detects your project type and injects relevant team-authored, open-source skills automatically. *(Upcoming.)*
- **Faster agent builds** — check the error list/indicators before kicking off a build to avoid doomed ~2-min builds; part of broader chat-window perf work. *(Upcoming.)*
- **AI merge-conflict resolution** — one-click AI conflict resolution. *("Launching very soon.")*
- **Move to GitHub Copilot CLI SDK** — shared SDK across VS / VS Code / CLI for simultaneous features; VS still builds via warm MSBuild/Roslyn. *(Rolling out next week on VS Insiders.)*
- **Bring any model** — use any model (local / on-prem / cloud, anywhere) in VS, with an enterprise security/lock-down layer to mandate or restrict providers. *("Very soon"; check VS 2026 Insiders next week.)*
- **Git work tree support & Git submodule support** — landing **next week** in VS.

## 💡 Demos
**Demo 1 — Fix a real crash in VS's own profiler (test-first + debugger agent).** Working *on Visual Studio inside Visual Studio* (the 160-project Diagnostics Hub solution), Nick fixes a real `IndexOutOfRange` crash in the HybridDictionary enum-keys iterator. Copilot (via the ADO MCP connector, with explicit confirmation) fetches the bug work item, reads the stack trace, and writes two repro unit tests; a key-type/struct compile error is fixed by conversation; the test reveals an unexpected assert (not the expected exception), which Nick re-steers; once it correctly throws `IndexOutOfRange`, the **debugger agent** ("Debug this test with Copilot") pinpoints an **off-by-one** error, fixes it, and validates by re-running under the debugger. **Proves:** test-first creates a durable guardrail that lets agents safely "cook," the debugger agent can autonomously diagnose/fix/validate real bugs, governance (confirm MCP calls) is preserved, and developer expertise is what steers non-deterministic agents.

**Demo 2 — Profiler agent nearly doubles a hot path live.** A CI-flagged `decode large file` test (compress/decompress a `.diagsession`) takes **3.88s**, dominated by an Express stream `CheckReadEnoughBits` frame. Via "Profile with Copilot," the **profiler agent** matches profiling line data to source, optimizes the read path (direct byte-array read + Huffman table changes, reducing binary-reader calls), rebuilds, re-runs tests for no regression, and **re-profiles** to validate — dropping the test to **~2s** on stage. **Proves:** agents optimize from *real executed data* not guesses ("measure twice, optimize once"), find wins even seasoned experts miss, and keep guardrails (re-test + re-profile) so you can let them run.

## 📊 Notable Stats / Quotes
- **160 projects** in the profiler/Diagnostics Hub solution alone (C++, C#, JavaScript, assembly, IL).
- **~400 GB** of repo data at the TFS→Git migration.
- **3.88s → ~2s** — Demo 2 nearly **doubled** decode-large-file performance live.
- **800,000 allocations** found by the profiler agent in VS startup (Azure DevOps cache-file XML deserialization) → **~50 MB** trimmed off the initial heap.
- **6–7 PRs** more than **doubled** `.diagsession` read performance in latest VS.
- Roslyn: a **switch-case evaluation** optimization found by an **SDE2** as their **first Roslyn contribution**.
- Crash caught internally in the **18.5 / April update** range before reaching customers.
- Mads ran the new shared-SDK experience full-time for **~1 month**.
- *"If you're not using data, you're not actually profiling or improving performance — you're just refactoring."* — Nick
- *"The better you are at your job as a developer, the better you are at managing your agent."* — Mads
- *"You measure to establish a baseline, then you make changes, then you measure again."* (measure twice, optimize once)
- *"Let the agent cook"* — once guardrails (failing test / profiling trace) are in place.
- *"This is literally what my day-to-day looks like."* — Nick, on the messy, iterative repro process.
- Improving performance is *"one of the few activities we can do as developers without having to ask permission first"* — no ticket required.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Add the **VS Test Performance Collector** NuGet to a project's CI test runs and inspect the auto-captured `.diagsession` attachments.
  - Try the **debugger agent** (right-click test → "Debug this test with Copilot") and **profiler agent** ("Profile with Copilot") on a real repo.
  - Wire up the **Azure DevOps MCP connector** in Copilot and have it fetch a work item from a bug link and analyze a pipeline's diagnostic sessions.
  - Practice the **test-first** loop: write a failing repro test, then let Copilot author the fix; ask it **"why is this faster?"** after a perf change.
  - Grab **VS 2026 Insiders** to try the Copilot CLI SDK build, any-model support, and merge-conflict resolution.
- [ ] Questions:
  - When exactly does each roadmap item GA vs. stay in Insiders? (Talk only commits "next week" for several.)
  - For "any model," what's the exact list of supported local/on-prem runtimes, and how does the org lock-down layer enforce it?
  - Does the profiler agent support allocation + CPU traces equally in the agentic flow, and what overhead does dynamic instrumentation add?
- [ ] Relevant to:
  - Any C#/C++ team treating code as an **asset** (quality/compliance/governance) — internal tooling, perf-sensitive libraries, legacy modernization.
  - Anyone maintaining legacy **Web Forms/WinForms** apps eyeing Blazor/.NET 10 + Aspire.
  - CI/perf-regression strategy (shift profiling into the inner loop and PR gates).

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Build 2026 — Visual Studio / GitHub Copilot sessions
- Topics: GitHub Copilot agents, debugger agent, profiler agent, app modernization (Web Forms → Blazor), MCP, Copilot CLI SDK
