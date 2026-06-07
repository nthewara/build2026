---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/performance
  - topic/profiling
  - topic/agents
  - topic/ai
  - topic/dotnet
  - topic/visual-studio
source: https://www.youtube.com/watch?v=VF0M8QwIRIs
session_code: DEM300
event: Microsoft Build 2026
speakers: Nick Karpinski (Software Engineer, Microsoft — Visual Studio Profiler)
duration_min: 23
aliases:
  - Supercharged profiling Finding performance bugs with agents
---

# DEM300 — Supercharged profiling: Finding performance bugs with agents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Nick Karpinski — Software Engineer, Microsoft (≈12.5 years at Microsoft, entire career on Visual Studio, most of it on the Visual Studio Profiler)  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=VF0M8QwIRIs)

## 🎯 TL;DR
Nick Karpinski demos the new **Visual Studio Profiler agent** in GitHub Copilot (`@profiler`), which automates the real-world performance-optimization workflow: understand the issue → write a benchmark → enter the measure/change/measure optimization loop → confirm improvement. Using the popular open-source **CsvHelper** NuGet package (51M downloads, #16 most downloaded) as a realistic target, he shows Copilot autonomously writing a BenchmarkDotNet benchmark, installing the VS profiler diagnoser, running the benchmark to capture a profiling trace, and using actual profiling data (not just grep) to guide source-level optimizations. The core message: **measuring with data is what turns refactoring into optimization** — and Copilot can not only invoke these tools but teach you *why* optimizations work, helping you grow as an engineer.

## 🔑 Key Takeaways
- The **profiler agent** is invoked in Copilot chat via `@profiler` — it knows how to write benchmarks, run the profiler, and analyze traces.
- Optimization is a **loop, not a one-shot**: understand → benchmark → measure → change → measure → improve? If yes, done ("cake"); if no, try another optimization or pick a different hotspot.
- **"A benchmark is a unit test for performance."** Unit tests pair with the debugger; benchmarks pair with the profiler.
- **"Measure twice, optimize once"** — always re-measure after a change. *If you're not measuring with data, you're not optimizing — you're just refactoring.* Data is what makes it an optimization.
- The agent reads **existing benchmarks** in the project unprompted and writes new ones in a matching style, avoiding duplicate coverage.
- BenchmarkDotNet **diagnosers** let external tools pull diagnostic data during a benchmark run; Microsoft publishes a VS diagnoser package (`*.Diagnostics.Hub` / BenchmarkDotNet diagnosers) that lets the profiler hook in and collect traces.
- The agent uses the profiler's **go-to-source** functionality and line-level profiling data to guide investigation — not just text search through the codebase.
- You can **steer** the agent: if it targets a hotspot you don't want (e.g. `expression compile`), redirect it to the next-biggest item (e.g. `ShouldQuote` logic).
- Real wins are usually **small "paper cuts"** across the codebase, not magical 10x single-line fixes. A 25% improvement (1.1ms → 0.8ms) on one method is a meaningful result.
- The benchmark becomes a **reusable, durable artifact** committed with the repo — usable for future profiling and as a learning tool.
- You can ask Copilot **"why is this not faster?"** to learn JIT quirks and deepen your performance knowledge (e.g. the JIT stops inlining after a certain number of IL instructions).
- **Functionality safety:** tell Copilot which tests to run after each optimization so it uses them as a validation layer (you optimize for speed but must not break behavior).
- The profiler's **"Analyze" / Top Insights** feature flags known bad .NET/C++ patterns (e.g. `IndexOf` on a linked list, `Contains` on a list → suggest a set); **"Generate Top Insights"** has Copilot read the trace and propose ideas when none auto-fire.
- ⚠️ Caveat: when analyzing a trace, the agent doesn't always recognize it ran inside a benchmark and may try to optimize the surrounding benchmark harness — steer it back to user code.

## 📚 Detailed Notes

### Speaker & Framing
Nick Karpinski is a Microsoft software engineer of ~12.5 years, having spent his entire career on Visual Studio and most of it specifically on the **Visual Studio Profiler**. He opened by polling the room: a good number were .NET developers, many had used the VS profiler, a couple had used **BenchmarkDotNet**, but only one person had used the **Visual Studio integration with BenchmarkDotNet** — the feature he was there to showcase. The session is deliberately demo-heavy with a single supporting slide.

### The Optimization Flowchart (the one slide)
Nick's mental model for how you optimize code in the real world. You move left → right; succeed and "you get cake."

1. **Understand your issue.** Not vague ("I think serialization is slow"), but concrete: know *specifically* where time is spent, so you invest effort where it yields the most improvement. If you don't know the issue, just **run the profiler in Visual Studio** — it shows where time is actually being spent, and you decide where to dig.
2. **Create a benchmark.** Taking general traces makes optimization hard. A benchmark gives a **reusable, durable test harness** to test performance against. *"I like to think of a benchmark as a unit test for performance."* Unit tests ↔ debugger; benchmarks ↔ profiler.
3. **The optimization loop** (his favorite, "the fun part"): **measure → change code → measure again → see the delta.** "Measure twice, optimize once."
4. **Improve block — did you actually improve?** If yes: success/cake. If no: fall back into the loop and try a *different* optimization (it's experimental, not one-and-done). If you've maxed out one benchmark, return to step 1 and pick a different issue from the original trace.

### Choosing a Realistic Target — CsvHelper
Nick dislikes demos where someone puts an obvious bug in a console app and the tool "finds" it — that's not realistic software engineering. Instead he goes to a popular real repository. His method: browse **nuget.org**, scroll the most popular packages, and pick one to try to optimize. For this talk: **CsvHelper** — the **16th most downloaded** NuGet package at **51 million downloads**. Optimizing something that popular has the potential to help many people.

He cloned it and opened the solution in Visual Studio. It already contained:
- The **CsvHelper** project
- A **CsvHelper Benchmarks** project (added by Nick himself in a previous talk — he's reused this repo several times)
- **Tests** — useful for the optimization loop so you can confirm you didn't break functionality
- The **website**

### Anatomy of the Existing Benchmark (reading records)
For those new to BenchmarkDotNet, he walked the existing benchmark, which resembles a unit test:
- It has a **`[GlobalSetup]`** that runs initialization *before* the benchmark, so you can extract the parts you're **not** trying to measure.
- The benchmark measures **enumerating records** — i.e. how fast CsvHelper can read a CSV file. It needs test data, so `GlobalSetup` builds a CSV file into a **`MemoryStream`** — meaning the benchmark measures the library, not the test-data setup.
- Inside the benchmark, it sets the **stream position to 0** at the start. Because the CSV was written into an in-memory stream during setup, resetting the position (and keeping it in memory) avoids paying the cost of constantly expanding buffers / flushing to disk, isolating the actual enumeration code.

### Demo 1 — Copilot Writes a New Benchmark (writing records)
Goal: add a counterpart benchmark for **writing** a CSV (he already had reading). Steps shown:
1. In **Copilot chat**, type **`@profiler`** to address the profiler agent ("knows about benchmarking, knows how to run the profiler, knows how to write benchmarks"), then: **"Write me a benchmark for writing a CSV file."**
2. The agent **reads the existing benchmark unprompted** — Nick didn't tell it about it. It reasoned: "I'm writing benchmarks; I should look at the others in this project and write similar code."
3. It noted **no existing benchmark covers CSV writing** (so no duplication needed), searched the project, and wrote a new benchmark.
4. It then needed to **install the VS profiler diagnoser package** (BenchmarkDotNet diagnosers / Diagnostics Hub). Nick clicked **Confirm**. This is the VS↔BenchmarkDotNet integration: BenchmarkDotNet's **diagnoser** concept lets tools pull diagnostic info while a benchmark runs, and Microsoft's published NuGet diagnoser lets the profiler interact and pull data.
5. The benchmark **compiled cleanly** and was written in a matching style: a simple class, a `[GlobalSetup]`, a `WriteRecords` method, and it set the **position** (not the length) of the stream — he wanted to reset position each iteration but not reset the whole stream.

### Iterating on the Benchmark with Inline Copilot
Nick refined the generated benchmark's test data. The record being serialized had a `Name` field of random characters. He selected it, hit **Alt + /** (inline Copilot), and asked it to **update so half the records contain a comma delimiter** — making the data more interesting/realistic (commas inside fields force quoting logic). Copilot took a simple approach: **mod by 2** and drop a comma in. This showed you can iterate conversationally on the benchmark itself.

### Demo 2 — Entering the Optimization Loop
With the benchmark ready, Nick moved into optimization:
1. The profiler agent proactively asked whether to **run it to establish a baseline.** Nick used a **`#` slash-context menu** to provide additional context, instructing: **"Run the WriteRecords benchmark and optimize the code that it calls."** Better context → more likely the agent does what you want.
2. The agent read his files (e.g. `benchmark.main`) and noticed that previously there was only a **single** benchmark (so the project ran it directly). Now that there are multiple, it **switched to BenchmarkDotNet's `BenchmarkSwitcher`** so it can select which benchmark to run at runtime.
3. Behind the scenes it **ran BenchmarkDotNet.** Normally a terminal window pops up spewing per-iteration timings (he noted ~**1.4–1.5 ms** per iteration); the agent **captures all that output**, collects it, and at the end produces a **profiling trace**, saves it to a directory, and **automatically opens it in Visual Studio** to begin optimization.
4. At this point you have: the reusable benchmark (test harness) **and** a trace showing where time is spent.

### Demo 2 (cont.) — Steering the Agent & the ShouldQuote Optimization
Nick hit **stop** because "sometimes the agent gets a little excited" and tries to fix the problem immediately even though they've tried to tell it not to. The agent's analysis identified the biggest hotspots:
- **`Expression.Compile`** (top hotspot)
- **`ShouldQuote`**
- a **dynamic multicast delegate**

The agent wanted to optimize the topmost item (most CPU). But Nick has tried optimizing `Expression.Compile` before and always failed, so — per his pipeline's "if you can't improve it, pick the next biggest thing" rule — he instructed: **"Optimize the ShouldQuote logic."** The agent acknowledged ("user wants me to investigate this other thing") and pivoted.

Key insight on *how* it investigates: it does **not** just grep the source — it uses the profiler's **go-to-source** functionality and the **profiling data** to see exactly which lines take the most time, then uses that to guide the investigation.

Its conclusion: the best optimization is to **combine the character checks into a single pass.** The `ShouldQuote` method had a tidy Boolean-logic block doing many operations in few lines; Copilot reasoned it may be **iterating too many times** and proposed a **single pass** to avoid multiple iterations.

Crucially, as soon as it applied the change, it stated **"I need to rerun the benchmark to measure the improvement."** This is the heart of the loop: establish baseline → change code → re-measure to see impact. *"If you're not actually measuring with data, you're not optimizing — you're just refactoring code. The data is what turns it from a refactoring into an optimization."*

### Result — A Non-Win (and why that's fine)
The re-run result:
- Baseline: **1.4 ms** → after: **1.4 ms** — **no meaningful overall improvement.**
- However, **`ShouldQuote` dropped from 13% → 7%** of time, and other code began taking up more of the time (the bottleneck shifted).

Nick treated this as a normal, expected outcome — the loop allows you to try the next thing. Possible follow-ups he listed: optimize the **CreateWriteDelegate**, run a **memory profile** to inspect allocations, or view the create-write-delegate implementation.

### The Pre-recorded Real Win + Philosophy on Improvements
He admitted he'd run this **before the talk** and they actually **created a PR** because Copilot meaningfully improved it — though it didn't reproduce live (he'd need to dig into the logic to learn why). That earlier win moved metrics from **~1.1 ms → ~0.8 ms**, a **25% improvement.** His lesson: software wins are rarely a magical "one line, 10x faster." They're usually **small paper cuts all over the codebase** that add up and hurt you. With the Copilot agent, you can have it run through and optimize these as you have time.

### Copilot as a Learning Tool
Beyond invoking tools, you can use the agent to **learn and grow as an engineer.** Example: ask "since we did a single pass instead of multiple passes, why is this not faster?" Nick recounted Copilot finding interesting optimizations he didn't understand and, when asked, explaining JIT quirks — e.g. the **JIT stops inlining a method after a certain number of IL instructions.** He learned something new. The reusable benchmark artifact (committed with the repo) supports both future profiling and this kind of learning.

### Next Steps / Resources (from the closing slide)
- Try to **reproduce the same** — ideally reproducing a *win*, not the non-win he got live.
- **CsvHelper library** — a resource; uploaded in the session's **GitHub repo.** Its author is "a super nice guy" who will work with you.
- The **CsvHelper optimization PR**.
- The **profiler agent documentation**.
- **Related session:** later that day, **Mads** and Nick present **Breakout Session 207** on the main stage (at **4:00 PM**), showing not just the profiler agent but also the **debugging agent** and **creating unit tests**, and how they used these to improve the **performance and reliability of Visual Studio itself**.

### Q&A
- **Q: When is the breakout session?** → 4:00 (PM).
- **Q: How do you inject functional testing into the loop if Copilot broke functionality?** → Tell Copilot which tests you have and to run them after any optimization; it uses them as a **validation layer.** In Session 207 they use the profiler's ability to **profile a unit test** — improving the optimization while the unit test simultaneously validates functionality.
- **Q: Can the profiler help you interpret the results in a trace?** → Yes. Use the **Analyze** button → "suggest optimizations for this trace." It looks at top functions, call path / hot path, and caller-callee to digest ideas. The main trace surfaces **Top Insights** that fire on known bad .NET/C++ patterns. Example CPU insight: calling **`IndexOf` on a linked list** or **`Contains` on a regular list** → suggestion to use a **set** (hashed, direct access) instead of iterating. If no insights fire, click **Generate Top Insights** and Copilot reads the trace to propose ideas — e.g. removing repeated null checks, avoiding an `IEnumerable` with a concrete type to **remove the boxed enumerator**, or constructing the **`StreamWriter` with a large buffer** to save on buffer costs. ⚠️ Caveat: when you run Analyze on a benchmark trace, it doesn't always realize it ran in a benchmark and may try to optimize the **surrounding benchmark code** — be careful and steer it to optimize **user code** instead.

## 🛠️ Products / Features / Technologies Mentioned
- **Visual Studio Profiler** — Microsoft's performance profiling tooling inside Visual Studio; shows where time is spent in an app.
- **Profiler agent (`@profiler` in Copilot chat)** — Copilot agent that writes benchmarks, runs the profiler, captures traces, and drives optimization.
- **GitHub Copilot (chat + inline)** — AI assistant; chat agents via `@`, inline edits via **Alt + /**, context via the **`#`** menu.
- **BenchmarkDotNet** — the .NET benchmarking framework; concepts used: `[GlobalSetup]`, `BenchmarkSwitcher`, and **diagnosers**.
- **BenchmarkDotNet diagnosers / VS Diagnostics Hub diagnoser package** — NuGet package (BenchmarkDotNet diagnosers) that lets the VS profiler hook into a running benchmark and pull diagnostic/trace data.
- **CsvHelper** — popular open-source .NET CSV read/write library; the optimization target (#16 most downloaded NuGet package, 51M downloads).
- **NuGet / nuget.org** — package registry; used to find a popular, realistic optimization target.
- **.NET / C#** — the platform and language throughout.
- **Memory profiler** — VS profiling mode for inspecting allocations (mentioned as a follow-up path).
- **Trace "Analyze" / Top Insights / Generate Top Insights** — VS profiler features that surface known-bad-pattern insights and Copilot-generated optimization suggestions from a trace.
- **Profiler go-to-source** — feature the agent uses to map line-level profiling data back to source for guided investigation.

## 🚀 Announcements / What's New
- **Visual Studio Profiler agent in GitHub Copilot** — showcased as a new capability: `@profiler` writes benchmarks, runs BenchmarkDotNet, captures profiling traces, opens them in VS, and drives source-level optimizations. (Presented as a new/featured workflow rather than an explicit GA/preview status call-out.)
- **Generate Top Insights** — Copilot-powered trace analysis that reads a profiling trace and proposes optimizations when no built-in insight fires.
- **Roadmap / related:** Breakout Session 207 (same day, 4:00 PM, with Mads) to demo the **profiler agent + debugging agent + unit-test creation** used internally to improve Visual Studio's own performance and reliability.
- **Note:** No explicit version numbers, GA dates, or preview/GA labels were stated in this demo.

## 💡 Demos
- **Demo 1 — Generate a writing benchmark:** `@profiler` "Write me a benchmark for writing a CSV file." The agent read the existing reading benchmark unprompted, confirmed no write-benchmark existed, wrote a style-matched benchmark, installed the VS diagnoser package, and compiled cleanly. *Proves:* the agent has project awareness and produces idiomatic, integration-ready benchmarks with minimal prompting.
- **Demo 1b — Inline iteration:** Selected the `Name` field, **Alt + /**, asked to add commas to half the records (Copilot used `% 2`). *Proves:* you can conversationally refine benchmark data to make it realistic (commas trigger quoting logic).
- **Demo 2 — Baseline + optimization loop:** `#`-context "Run the WriteRecords benchmark and optimize the code it calls." Agent switched to `BenchmarkSwitcher`, ran BenchmarkDotNet (~1.4–1.5 ms/iteration), captured the trace, and auto-opened it in VS. *Proves:* end-to-end automation of measure → trace → open.
- **Demo 2b — Steering + ShouldQuote single-pass optimization:** Redirected the agent off `Expression.Compile` to `ShouldQuote`; it used profiling data + go-to-source to find hot lines and combined character checks into a single pass, then auto-re-measured. Result: overall 1.4 ms → 1.4 ms (no net win) but `ShouldQuote` 13% → 7%. *Proves:* the agent uses real profiling data (not grep), can be steered, and always re-measures — and that non-wins are a normal part of the loop.
- **Pre-recorded win (shown via conversation history):** an earlier run optimized `CreateWriteDelegate`, improving ~1.1 ms → ~0.8 ms (**25%**) and producing a real PR. *Proves:* meaningful, mergeable wins are achievable even if any single live run may not reproduce.

## 📊 Notable Stats / Quotes
- **51 million downloads** — CsvHelper, the **16th most downloaded** NuGet package.
- **~1.4–1.5 ms** — per-iteration time of the WriteRecords benchmark; baseline and post-change both **1.4 ms** (the live non-win).
- **13% → 7%** — `ShouldQuote` share of time after the single-pass optimization (bottleneck shifted elsewhere).
- **~1.1 ms → ~0.8 ms = 25% win** — the pre-recorded `CreateWriteDelegate` improvement that produced a PR.
- **~12.5 years** — Nick's tenure at Microsoft, all on Visual Studio.
- **4:00 PM** — Breakout Session 207 (with Mads).
- 💬 *"I like to think of a benchmark as a unit test for performance. Unit tests work with the debugger; benchmarks work with the profiler."*
- 💬 *"Measure twice, optimize once."*
- 💬 *"If you're not actually measuring with data, you're not optimizing — you're just refactoring code. The data is really what turns it from a refactoring into an optimization."*
- 💬 *"It's these small little paper cuts all over your code base that are really tripping you up... With the Copilot agent, you can just have it go through and optimize as you have time."*
- 💬 *"You can use Copilot to not only achieve the results you're looking for, but also to learn and grow as a software engineer."* (e.g. learning the JIT stops inlining after a certain number of IL instructions.)
- 💬 *"If you're successful, you get cake."*

## 🧠 My Notes / Follow-ups
- [ ] **Things to try:**
  - [ ] Try `@profiler` in Copilot chat on a real repo — have it write a BenchmarkDotNet benchmark from an existing one and capture a trace.
  - [ ] Reproduce the CsvHelper exercise and aim for an *actual* win (e.g. `CreateWriteDelegate` 25% improvement); compare against the live `ShouldQuote` non-win.
  - [ ] Use the trace **Analyze → Generate Top Insights** on an existing app trace and see which known-bad patterns fire.
  - [ ] Run a **memory profile** path on the write benchmark to inspect allocations (the follow-up Nick listed but didn't demo).
  - [ ] Practice the `#`-context menu to give the agent a precise "run this benchmark and optimize what it calls" instruction.
- [ ] **Questions:**
  - [ ] What's the exact diagnoser NuGet package name to add for the VS↔BenchmarkDotNet integration?
  - [ ] Is the profiler agent GA, preview, or insiders-only — and which VS version is required?
  - [ ] How does the agent decide when to switch a project to `BenchmarkSwitcher` automatically?
  - [ ] Can the validation-layer (run-my-tests-after-each-change) be made a standing rule per repo rather than per prompt?
- [ ] **Relevant to:**
  - [ ] Any .NET performance work / perf reviews where benchmarks + profiling traces are needed.
  - [ ] Demos showing Copilot agents driving real tooling (not toy bugs).
  - [ ] Follow-up: watch **Breakout Session 207** (profiler + debugging agents + unit-test creation, used on VS itself).

## 🔗 Related
- **Breakout Session 207 (Build 2026)** — Mads + Nick Karpinski: profiler agent + debugging agent + unit-test creation, used to improve Visual Studio's own performance & reliability.
- [CsvHelper](https://github.com/JoshClose/CsvHelper) — the optimization target library (session GitHub repo also hosts the resource + optimization PR).
- [BenchmarkDotNet](https://benchmarkdotnet.org/) — the .NET benchmarking framework used throughout.
- Visual Studio Profiler agent documentation (linked from the session's closing slide / GitHub repo).
- [[Build2026]] — Microsoft Build 2026 session notes index.