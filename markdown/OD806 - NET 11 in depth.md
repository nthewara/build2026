---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/runtime
  - topic/sdk
  - topic/performance
  - topic/ai
source: https://www.youtube.com/watch?v=dgPJwHXDj0o
session_code: OD806
event: Microsoft Build 2026
speakers: Chet Husk, Rich Lander
duration_min: 44
aliases:
  - .NET 11 in depth
---

# OD806 — .NET 11 in depth: Runtime, libraries, and SDK for the AI era

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Chet Husk (Product Manager, .NET SDK & MSBuild teams) · Rich Lander (Product Manager, .NET runtime & libraries team)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=dgPJwHXDj0o)

## 🎯 TL;DR
A two-part survey of what's coming in **.NET 11**, framed around the AI/agent era. Chet Husk covers the **SDK & tooling** side: three workstreams — new capabilities/UX, end-to-end performance, and lighter acquisition. Headliners include first-class `dotnet run` device deployment for MAUI, making the CLI **agent/LLM-aware**, an ambitious push to make the **entire .NET CLI native AOT** (with bundled tools like user-secrets already AOT in preview 6), **multi-threaded MSBuild**, a new cross-platform install tool **`dotnet up`**, and ~80 MB shaved off SDK payloads via tarball hard-link deduplication. Rich Lander then goes lower in the stack: a redesigned **Process API** (deadlock-free convenience methods), Unicode/text-processing improvements, System.Text.Json policies + JSON Lines, integrated **Zstandard** compression, and two enormous multi-release runtime projects — **runtime async** (state-machine-free async, opt-in in .NET 11, default likely in .NET 12) and **memory safety** (redesigning `unsafe` into a reviewable contract, JIT bounds-check/inlining wins, and memory-safe SIMD). The overarching message: install the previews and give feedback on GitHub before the **GA this fall**.

## 🔑 Key Takeaways
- **.NET SDK has three .NET 11 workstreams:** new capabilities/UX, performance throughout the stack, and lightening acquisition/management of tools — all heavily motivated by the rise of agents and fast multi-agent inner loops.
- **`dotnet run` now deploys to devices** (MAUI contribution): pick a target framework, pick a valid device, build the install payload, push, and launch on a simulator — all from `run`. The protocol is **extensible** beyond MAUI (Uno, Avalonia, etc.).
- **The CLI is now agent/LLM-aware** (heuristic-based). It changes output rendering (e.g. disables the terminal logger's token-noisy live-updating section under an LLM) and adapts internal behavior to who's driving it.
- **Build resource contention** from agent-spawned git worktrees is being addressed via a proposed **central MSBuild "gatekeeper"** that routes all builds and delegates resources so the machine stays responsive.
- **Native AOT for the entire .NET CLI is the North Star.** Bundled tools (`user-secrets`, `dev-certs`, `user-jwts`) are native AOT as of preview 6. Example: `dotnet user-secrets` ran in ~54 ms total, only ~14 ms of which was the app itself (rest is managed CLI overhead).
- **AOT is also an ecosystem play:** the effort forced core libraries (templating, NuGet, parts of MSBuild) to become more trim-friendly, unblocking the whole ecosystem to build trimmed/AOT apps.
- **The CLI now emits OpenTelemetry (OTEL)** — you can trace CLI commands in the **Aspire dashboard**. Telemetry was migrated to OpenTelemetry and old COM patterns made trim-friendly as part of the AOT migration.
- **Multi-threaded MSBuild** is coming in .NET 11 (threads, not just the current multi-process model) to cut IPC and CoreCLR JIT-loading overhead. Not usable today but will be by launch; task authors should read `aka.ms/msbuild/mttasks`.
- **`dotnet up`** — a new native-AOT tool to acquire/manage .NET toolchains consistently across platforms, supports nightlies, reads `global.json`, user-level installs (no admin). Previews "coming soon."
- **SDK download size cut ~80 MB+** per platform by deduplicating identical files into tarball **hard links** — big win for the many SDK downloads, especially container image builds.
- **New Process API** eliminates a classic deadlock and adds correct, fast convenience methods: `RunAndCaptureTextAsync`, `ReadAllLinesAsync`, `CreateAnonymousPipe` (for piping), fire-and-forget, plus a trim-friendly `SafeProcessHandle`.
- **Text/Unicode improvements:** `IsValid` + `IndexOfInvalidSubsequence` for UTF-8/UTF-16, a new `RegexOptions.AnyNewLine`, and **rune-aware** string methods (correct for multi-`char` code points like emoji).
- **System.Text.Json:** per-type and per-property naming/null-handling policies (e.g. type-wide "ignore nulls" + PascalCase default with a camelCase override on one property), and **JSON Lines** async writing from `IAsyncEnumerable` via top-level-values.
- **Compression:** **Zstandard** APIs are now integrated into the product; improvements across multiple algorithms. (In one text-only sample, Brotli edged out a very-close Zstandard.)
- **Runtime async:** a new async **optimization** (not a new model) — no new keywords, no source changes, fully compatible both directions. Opt in with `<Features>runtime-async=on</Features>`. New code has **no state machines** (the runtime owns suspension/resumption). Opt-in in .NET 11, likely default in .NET 12; benefits = cleaner stack frames, smaller binaries, and faster async.
- **Memory safety:** a two-release (.NET 11 + 12) project redefining `unsafe` as a **reviewable contract** rather than an unsafe context; JIT bounds-check elimination & inlining improvements that remove the need for hand-written unsafe code, culminating in **memory-safe SIMD**.
- **Call to action:** install .NET 11 previews, try the features, file feedback on GitHub discussions/issues and blog posts ahead of **GA this fall**; some features land in **.NET 12**.

## 📚 Detailed Notes

### Session framing — .NET 11 for the AI era
Chet Husk (SDK/MSBuild PM) and Rich Lander (runtime/libraries PM) split the talk: SDK/tooling first, then the runtime/libraries the tooling builds on. The SDK has **three major .NET 11 workstreams**:
1. **New capabilities & user experiences** — net-new CLI features plus reworking well-used features to be more workable/efficient in an **LLM context**.
2. **Performance through the whole stack** — driven by agents and the accelerated, repeated inner loops of multi-agent scenarios; the goal is for *every* command to be as fast as possible.
3. **Lightening acquisition & management** of the tools.

### SDK / tooling — UX improvements

**`dotnet run` → first-class device deployment.** `dotnet run` has long been the inner-loop backbone. .NET 10 added ways for projects to **hook how they run** (e.g. Azure Functions in the emulator). One gap was **MAUI / device-specific** running: normally you must build the product *and* an install payload, push it to a device, and run it there. In .NET 11 the **MAUI team contributed** enhancements so device flows are first-class in `dotnet run`, expanding the MAUI targets so `run` handles device deployment end-to-end:
- Pick the **target framework** to deploy to.
- Pick a **device valid** for that TFM.
- Upload the device payload and **launch on the simulator**.
- `run` now also knows how to **query available devices**, and the whole protocol is **extensible** — not MAUI-only; it could support Uno, Avalonia, or any UI framework.

**Making the CLI agent/LLM-aware.** The CLI now detects (heuristically) when it's being run **under an agent**. That knowledge enables two categories of work: (a) change how output is rendered to available streams, and (b) understand who's driving and adapt internal behavior. Concrete example: the **terminal logger** (default build display since .NET 10) has a static section for project output plus a **dynamic, constantly-updating** section showing per-project targets. LLMs read that live region as a **token-inefficient stream of constant changes**, so when run in an LLM context the CLI now **disables the live update**. The simple example illustrates a broader principle being applied across the CLI.

**Build resource contention from agents.** Agents increasingly spawn **git worktrees** (shallow clones at different branches) to work in parallel. But `dotnet build` isn't normally aware of other concurrent builds, causing resource **contention** that hurts machine responsiveness. The team is exploring a **central MSBuild gatekeeper** that all builds route through and that **delegates resources** to each build. Historically the tooling was "one-shot" focused; parallel agent work makes this necessary. Expect more of this category in the CLI.

### SDK / tooling — Performance & native AOT

**The CLI's AOT journey.** Because the CLI runs so often, performance multiplies. Status:
- **Bundled standalone tools** — `user-secrets`, `dev-certs`, and `user-jwts` (user JSON Web Token) — are **native AOT** as of ~2 weeks before the talk, shipping in **preview 6**, with improved responsiveness.
- **Benchmark (Damian Edwards' Windows machine, ~1 week prior):** AOT `dotnet user-secrets` averaged **~54 ms total**, of which only **~14 ms** was the actual app; the rest was managed **.NET CLI overhead** (which the AOT effort is attacking).
- Even shaving **~100 ms** off each command yields real gains given command frequency.

**Why AOT — also an ecosystem play.** Many Microsoft tools depend on Microsoft libraries that weren't AOT/trim-friendly. Setting "the CLI must be AOT" as a milestone forced those blockers down. Over the .NET 11 cycle, **templating, NuGet, and parts of MSBuild** became more trim-friendly. Unblocking these core libraries makes trimmed/AOT apps more feasible for the **entire ecosystem** (NuGet libraries especially).

**The whole CLI is on an AOT arc.** Some blockers were **complete replacements** — e.g. migrating telemetry to **OpenTelemetry**, and making old **COM patterns** trim-friendly (much of which the runtime already provided; the CLI just hadn't adopted it).

**Observability win — OTEL + Aspire.** Now that the CLI **emits OTEL**, you can trace it in the **Aspire dashboard** with familiar Aspire tools. In an example trace, the **top five spans** came from the **native** portion of the CLI and the **bottom five** from the **managed** portion. Commands move into native space as their blockers clear; the team prioritizes commands that are **relatively dependency-free** and **frequently used**. Current focus: **solution management** commands; next on Chet's list: **template-related** and **tool-management** commands. This even opens the door to things like the **`dnx`** command being a standalone native-AOT app.

**Multi-threaded MSBuild.** Today's MSBuild is **multi-process** — great for isolation/safety but with high **inter-process communication** overhead and **CoreCLR JIT-loading** costs. A **multi-threaded mode** (worked on for a while) is **not ready today but will be by .NET 11 launch**. It's promising for performance and enables further optimizations layered on top. **Task authors:** see `aka.ms/msbuild/mttasks` for the changes needed to adopt it. More announcements + measurement numbers to come.

### SDK / tooling — Acquisition

**`dotnet up`.** A new **native-AOT tool** to give a **consistent way to acquire & manage .NET toolchains** across platforms / across team members on different platforms. It supports **nightlies**, uses **`global.json`** if present, and does **user-level installs** (no admin). **Previews coming soon** ("Blizzard-style soon"). Chet recorded a **dedicated deep-dive for Build** on it.

**Smaller SDK downloads via tarball hard links.** The SDK is downloaded constantly — not just by end users but heavily for **containers** (a primary build path). The team found that **tarballs support hard links** (like symlinks: multiple identical-content files point to one canonical resource). By **inspecting the SDK layout** at packaging time and doing **automated unification/deduplication**, they've shaved roughly **80-ish MB per platform** (and more) off SDK payloads across the .NET 11 previews. Smaller payloads = faster delivery + less network I/O (big for SDK containers). This built on the runtime's improved **tarball support since .NET 7**, confidence gained via the **SDK containerization** feature, then applied to their own packaging.

---

*(Handoff to Rich Lander for runtime & libraries — "everything I just showed you wouldn't be possible without the runtime work.")*

### Libraries — the new Process API (Process v2)

Announced in **preview 4**, a major update to the **Process API** (used to start a process, capture results, etc.). The old API is **difficult and a long-standing source of bugs**, so new **convenience APIs** do the common things **correctly and fast**.

- **The "bad case" (deadlock demo).** Running `dotnet build` with full diagnostics produces both **stdout and stderr**. Code that calls `ReadToEnd` on **stdout first**, then stderr, deadlocks: the **stderr buffer fills up**, so the writer (`dotnet build`) **blocks** because it can't write more — while the reader is still waiting on stdout. Classic deadlock; the old fix was to restructure the code.
- **`RunAndCaptureTextAsync`** — returns a **`ProcessTextOutput`** object with everything you'd want: **all stdout, all stderr, and exit code**, ready to use.
- **`ReadAllLinesAsync`** — similar but a **streaming** model: `foreach` over lines and ask **each line whether it's stderr** (or stdout) and act accordingly.
- **`CreateAnonymousPipe`** — to replicate shell piping (e.g. `dotnet help | grep ...`) in C#: it gives **read & write sides**; pass the **write** side to the first command's stdout and the **read** side to the second command's stdin, start both processes, and **wait on the second** to exit — resources are released correctly. This is the whole program.
- **Fire-and-forget** — start a process, let it run, release resources correctly, and **don't collect results**. Optionally **kill the process on parent exit** (or not), per your use case.
- **`SafeProcessHandle`** — a separate type that **trims better** than `Process`; use it when trimming/AOT is a concern.

### Libraries — text processing & Unicode

Mostly **Unicode conformance**:
- **`IsValid`** and **`IndexOfInvalidSubsequence`** — two pairs for **UTF-8** and **UTF-16**. Validate text coming from a file/over the wire, and if invalid, learn **exactly where the bad code starts** (great for diagnostics/error messages).
- **`RegexOptions.AnyNewLine`** — handles the cross-OS pain of newline management (`\r`, `\n`, `\r\n`, and other newline variants).
- **Rune-aware string methods.** UTF-16 `char` can't hold every Unicode "character": many code points (notably **emoji**) need **two or more** `char`s (surrogate pairs). A **rune** describes a **Unicode code point** (letter, number, or emoji), and these string methods now work **correctly** with them.
- **Demo:** analyze Chet's GitHub review comments — split text by newline (`AnyNewLine` regex), iterate lines, detect "ship it"–style approvals (including **emoji** ones), and print surrounding context. Rich's aside: in real code he'd likely reach for the **`SearchValues`** APIs instead (he's a big fan), but the demo showcased the new rune/newline APIs.

### Libraries — System.Text.Json

Rich has worked on System.Text.Json for ~6–7 years; continued investment.
- **Naming / null policies** (also useful with agents): set policy for what to serialize and how.
  - For a whole type (e.g. `EventData`): **don't write properties when null** for the entire type.
  - `JsonSerializerOptions` set to **PascalCase** as the default; serialization uses that option.
  - **Per-property override:** e.g. `EventName` overridden to **camelCase** — finer control while keeping the convenience.
- **JSON Lines** (one JSON document per line; the very-similar variant is **NDJSON**). Used by some **AI agent conversation logs**. You can **async-write** the set of JSON documents produced by an **`IAsyncEnumerable`** method; opt in with **top-level-values = true**.

### Libraries — compression
A batch of compression work. The **biggest change: Zstandard (Zstd) APIs are now integrated** into the product, plus improvements across **several algorithms**. In a **single, text-only sample** (compressing the System.IO.Compression C# files from the runtime repo — "a bit meta"), tested at both **optimal** and **smaller-size** settings: **Brotli came out best, with Zstandard very close and competitive.** (Heavy caveat: one body of text only; source size uncertain, "maybe ~15 MB" — they weren't sure.)

### Runtime project #1 — Runtime async
Two "enormous" runtime projects follow. **Runtime async** is a **new optimization for async code — not a new model**:
- **No new keywords, no source changes.** It's a **fast path decided at compile time** when you build (e.g. `dotnet build`).
- **Fully compatible both directions:** new can call old, old can call new — **no compatibility break ever**.
- **No state machines** in your output. With the traditional model ("**compiler async**"), the **C# compiler owns the state machine** — each async method is rewritten into a state machine. With **runtime async**, the code is **not rewritten**; the **runtime owns** suspension/resumption, so **N source-level state machines collapse to one runtime-managed system**. (Wry note: runtime async is "almost all implemented in the **JIT**," which is itself a compiler — so both are "compiler async" of a kind; the naming is imperfect.)
- **Opt-in** in .NET 11; **likely the default / new normal in .NET 12** — but even when default, you can keep doing what you did before (no break).
- **How to opt in:** the `<Features>` property → set **`runtime-async=on`**. That's it.

**Benefits (why do it):**
- **Cleaner stack frames**, mainly for **production diagnostics**.
- **Small binary size** win.
- **Performance** was a large motivation — async can be faster, **especially when the whole stack is runtime async** (turn it on for all projects).
- **Improvement without recompiling:** since the async machinery lives in the **runtime**, upgrading the runtime (e.g. to .NET 13) could make your already-runtime-async code **faster without rebuilding** it.

**Evidence — preview 4 size win.** Runtime async was turned on for the product in **preview 4** (released **May**; off in preview 3). Several heavy-hitter libraries got **smaller** in preview 4, largely from **removing state machines** they previously contained.

**Stack-frame demo.** A sample app nests `OuterAsync → MiddleAsync → InnerAsync`. Rich deliberately used `Task.CompletedTask` so the stack frames are **purely the async machinery**, not app logic. `InnerAsync` writes `Environment.StackTrace`; `MiddleAsync` throws an exception (to land in a different frame).
- **.NET 10:** the `Environment.StackTrace` output **shows the state-machine frames** — messy but **perfectly accurate**. (`Exception.ToString()` was already cleaned up to convey **intent**, whereas `Environment.StackTrace` is meant to be **perfectly accurate**.)
- **.NET 11:** `Environment.StackTrace` is **just as accurate but the state-machine frames are gone** — it now matches the cleaned-up form. Overlaying the two slides shows exactly which frames were removed (you enter `InnerAsync`, start the state machine, return to `InnerAsync` — and with state machines you'd re-enter **multiple times** if there were multiple awaits).

**Native AOT compatibility.** Runtime async **works perfectly with native AOT**. Native AOT has no traditional runtime but uses **RyuJIT** as its code generator, so the whole system "just works" with AOT by architecture — nothing special to do.

### Runtime project #2 — Memory safety
A **massive, two-release project (.NET 11 + .NET 12)**, somewhat like runtime async (though runtime async is *supported* in .NET 11, just not default; **memory safety is in preview** in .NET 11). Rich wrote a **blog post (~a week prior)** with much more detail.
- **This release** (.NET 11): define a set of **language changes**, apply them to **`System.Private.CoreLib`** (the bottom-most managed library), and make changes so the team — **and everyone else** — needs `unsafe` **less**.
- **.NET 12:** finish it off.
- **Core idea:** redesign the **`unsafe`** keyword to mean a **reviewable contract** (a "color" contract) rather than establishing an **unsafe context**. APIs like `Unsafe` and `MemoryMarshal` will be **marked with this contract** when done.

**JIT improvements that remove the need for `unsafe`** (bounds-check elimination + better inlining — places people wrote unsafe code because the JIT couldn't reason well):
- **Bounds-check (related-index) example:** a guard like `if (i + 2 < length)` proves the next two indexes are safe. In **.NET 10 and earlier**, the JIT only matched the check to the **exact** index (`i + 2`) and would **still bounds-check `i + 1`**. Now it recognizes `i + 1` falls within the `i + 2` guard, so **`i + 1` gets faster**.
- **Tail-slice example:** a check like "is the span at least 4 bytes (past the size of an `int`)?" followed by a `span.Slice(...)` of the same size **from the end**. The JIT previously handled this **tail-slice pattern** poorly; now it works.
- **Inlining example:** previously, inlining `GetLength` into a method left **two null checks** on `s` (both run), and an inline **`throw new ArgumentNullException`** could **pessimize** the surrounding code (having an actual `throw` in the stack frame). Now, after inlining, you're left with just the single **`s is null → return -1`** path: cleaner, less code.

**Memory-safe SIMD (the payoff).** These wins are nice but don't "change the game" alone — so they were applied to **SIMD** (Single Instruction, Multiple Data — vector instructions), which is used **pervasively** across the product and relies on **lots of unsafe code**. Making SIMD memory-safe **removes a whole category of unsafe code** from the product. The "before" code is full of **`MemoryMarshal` and `Unsafe` calls** (clearly not safe); in the "after," **all those API calls are gone** — the JIT does the right thing, partly by leaning on the bounds-check/inlining improvements above. This memory-safe code can now be **deployed across the product**, and it's better.

### Closing / call to action
Install the **.NET 11 previews**, try the new features, and **file feedback on GitHub** (discussions and issues) and on the blog posts — the team watches these constantly. **The earlier you get hands-on, the better the GA this fall will be**, and the better the features still landing in **.NET 12**.

## 🛠️ Products / Features / Technologies Mentioned
- **.NET 11** — the release this whole session previews (SDK, runtime, libraries); GA targeted for **fall**.
- **.NET 12** — next release; destination for runtime-async-by-default and the completion of memory safety.
- **.NET SDK** — the toolchain; three .NET 11 workstreams (capabilities/UX, performance, acquisition).
- **.NET CLI (`dotnet`)** — the command-line driver being made agent-aware and native AOT.
- **`dotnet run`** — inner-loop run command; now does first-class MAUI/device deployment.
- **.NET MAUI** — UI framework whose team contributed the `dotnet run` device-deployment flow.
- **Uno / Avalonia** — other UI frameworks the extensible device-run protocol could support.
- **Azure Functions emulator** — example of a .NET 10 `dotnet run` hook.
- **Terminal logger** — default build display (since .NET 10); its live region is disabled under LLMs.
- **MSBuild** — the build engine; gaining a resource gatekeeper and a multi-threaded mode.
- **Git worktrees** — shallow per-branch clones agents use for parallel work (source of build contention).
- **Native AOT** — ahead-of-time compilation; target for the CLI, bundled tools, `dotnet up`.
- **Trimming** — removing unused IL; core libraries made more trim-friendly for the AOT effort.
- **`dotnet user-secrets` / `dev-certs` / `user-jwts`** — bundled CLI tools, now native AOT (preview 6).
- **OpenTelemetry (OTEL)** — telemetry standard the CLI migrated to and now emits.
- **Aspire dashboard** — used to trace the CLI's OTEL spans (native vs managed portions).
- **CoreCLR / RyuJIT** — the runtime and its JIT/code generator (RyuJIT also powers native AOT).
- **`dnx`** — a command that could become a standalone native-AOT app.
- **`dotnet up`** — new native-AOT tool to acquire/manage .NET toolchains (nightlies, `global.json`, user-level, no admin).
- **`global.json`** — pins SDK version; respected by `dotnet up`.
- **Tarballs + hard links** — packaging format/technique used to dedupe SDK files (~80 MB+ saved).
- **SDK containers / containerization feature** — major SDK download consumer; benefits from smaller payloads.
- **`Process` API / `ProcessTextOutput`** — redesigned process-launching API and its result type.
- **`RunAndCaptureTextAsync` / `ReadAllLinesAsync` / `CreateAnonymousPipe`** — new process convenience APIs.
- **`SafeProcessHandle`** — trim-friendlier alternative to `Process`.
- **`IsValid` / `IndexOfInvalidSubsequence`** — UTF-8/UTF-16 validation APIs.
- **`RegexOptions.AnyNewLine`** — regex option handling all newline variants.
- **Rune (`System.Text.Rune`)** — Unicode code point abstraction; string methods now rune-aware.
- **`SearchValues`** — efficient multi-value search APIs (Rich's preferred real-world choice).
- **System.Text.Json / `JsonSerializerOptions`** — JSON serializer with new per-type/per-property naming & null policies.
- **JSON Lines / NDJSON** — one-JSON-doc-per-line formats; async write from `IAsyncEnumerable` via top-level-values.
- **`IAsyncEnumerable`** — async stream source for JSON Lines writing.
- **Compression: Zstandard (Zstd), Brotli** — Zstd APIs now integrated; improvements across algorithms.
- **Runtime async** — JIT-based async optimization removing state machines; opt in via `<Features>runtime-async=on`.
- **Compiler async** — the traditional compiler-owned state-machine async model (contrast term).
- **`Environment.StackTrace` / `Exception.ToString()`** — used to demo cleaner runtime-async stack frames.
- **Memory safety project** — redesign of `unsafe` into a reviewable contract; memory-safe SIMD.
- **`Unsafe` / `MemoryMarshal`** — low-level APIs to be marked with the new reviewable `unsafe` contract.
- **`System.Private.CoreLib`** — bottom-most managed library where memory-safety changes are first applied.
- **SIMD** — vector instructions; target of memory-safe rewrites removing unsafe code.
- **`aka.ms/msbuild/mttasks`** — docs link for adapting MSBuild tasks to multi-threaded mode.

## 🚀 Announcements / What's New
- **`dotnet run` device deployment for MAUI** — first-class device build/push/launch via `run`; extensible protocol. (.NET 11)
- **Agent/LLM-aware .NET CLI** — detects agent context; disables terminal-logger live updates under LLMs; adapts behavior. (.NET 11, ongoing)
- **MSBuild resource gatekeeper** — proposed central broker to manage cross-build resource contention. (exploratory)
- **Native-AOT bundled CLI tools** — `user-secrets`, `dev-certs`, `user-jwts` are native AOT in **preview 6**.
- **Whole-CLI native AOT** — in progress; solution-management commands first, then templates & tool management; emits OTEL now.
- **Multi-threaded MSBuild** — coming in .NET 11; **not usable today, ready by launch**; task-author guidance at `aka.ms/msbuild/mttasks`.
- **`dotnet up`** — new cross-platform native-AOT acquisition tool; **previews "coming soon."** A dedicated Build deep-dive recording exists.
- **SDK payload size reduction** — ~**80 MB+ per platform** via tarball hard-link dedup, across the .NET 11 previews.
- **Process API v2** — announced in **preview 4**; deadlock-free convenience methods + `SafeProcessHandle`.
- **Unicode/text APIs** — `IsValid`, `IndexOfInvalidSubsequence`, `RegexOptions.AnyNewLine`, rune-aware string methods. (.NET 11)
- **System.Text.Json policies + JSON Lines** — per-type/per-property naming & null handling; JSON Lines async writing. (.NET 11)
- **Zstandard integrated** into the product, plus broader compression improvements. (.NET 11)
- **Runtime async** — **opt-in in .NET 11**, on by default in the product since **preview 4**; **likely default in .NET 12**; AOT-compatible.
- **Memory safety** — **in preview in .NET 11**, completing in .NET 12; redesigns `unsafe` as a reviewable contract; memory-safe SIMD; accompanying blog post.
- **GA timing** — .NET 11 **GA this fall**; some features deferred to **.NET 12**.

## 💡 Demos
- **`dotnet run` MAUI device flow (slide/image):** picks a TFM, picks a valid device, uploads the payload, and launches on a simulator — proving device deployment is now first-class and extensible in `run`.
- **Aspire dashboard CLI trace:** top five spans from the native CLI portion, bottom five from the managed portion — proving the CLI now emits OTEL and is observable like any Aspire app, and showing the native/managed split.
- **Process deadlock "bad case":** `dotnet build` with full diagnostics, reading stdout `ReadToEnd` before stderr → stderr buffer fills → writer blocks → deadlock; motivates the new APIs.
- **Anonymous pipe in C#:** replicating `dotnet help | grep` with `CreateAnonymousPipe` (wire write→stdout, read→stdin, wait on second process) — the entire program, with correct resource cleanup.
- **Rune / AnyNewLine GitHub-review analysis:** split Chet's review comments by `AnyNewLine`, detect emoji "ship it" approvals with rune-aware handling, print surrounding context — proves correct multi-`char`/emoji handling (though `SearchValues` would be the real-world pick).
- **System.Text.Json policy code:** type-wide ignore-nulls + PascalCase default with a camelCase override on `EventName` — proves fine-grained naming/null control.
- **JSON Lines async write:** stream JSON docs from an `IAsyncEnumerable` via top-level-values — proves first-class JSON Lines support.
- **Compression benchmark (one text sample):** compressing the runtime's System.IO.Compression C# files at optimal vs smaller-size settings — Brotli best, Zstandard a very close second.
- **Runtime async stack-frame comparison:** nested Outer/Middle/Inner async (using `Task.CompletedTask`) printing `Environment.StackTrace` and throwing — .NET 10 shows messy-but-accurate state-machine frames; .NET 11 is equally accurate but **frames removed**; an overlay slide shows exactly which frames disappeared.
- **Memory-safe SIMD before/after:** a SIMD block full of `MemoryMarshal`/`Unsafe` calls → an "after" with all those calls gone — proves the JIT can now make SIMD memory-safe.

## 📊 Notable Stats / Quotes
- **`dotnet user-secrets` (AOT) ≈ 54 ms total**, of which only **~14 ms** is the actual app — the rest is managed CLI overhead (Damian Edwards' Windows machine).
- **"Even shaving 100 ms off every command"** translates to real benefits given how often developers run commands — the rationale for the AOT push.
- **~80-ish MB** shaved off SDK payloads **per platform** via tarball hard-link deduplication.
- **Tarball support landed in .NET 7** (the runtime knowledge this SDK win builds on).
- **Runtime async turned on for the product in preview 4** (released **May**); measurable **binary size reductions** from removed state machines.
- **Compression sample:** **Brotli best, Zstandard very close/competitive** (one text-only body; source size uncertain — "maybe ~15 MB").
- **Memory safety = a two-release project** spanning **.NET 11 and .NET 12**.
- **"There's no compatibility break in any direction"** — recurring promise for runtime async (old↔new interop, even when it becomes default).
- **Previews "coming soon"** for `dotnet up` — "the Blizzard-style soon, if you're a gamer."
- **GA this fall**; get hands-on early so the team can "ship the right thing."

## 🧠 My Notes / Follow-ups
- [ ] Things to try: enable `<Features>runtime-async=on</Features>` on a sample async-heavy project and compare stack traces / binary size between .NET 10 and .NET 11; try the new `Process` convenience APIs (`RunAndCaptureTextAsync`, `CreateAnonymousPipe`) to replace hand-rolled process wrappers; install preview 6 and benchmark native-AOT `user-secrets`/`dev-certs`; trial `dotnet up` once previews drop; measure SDK container image size delta on .NET 11.
- [ ] Questions: When exactly does multi-threaded MSBuild flip on by default, and what's the task-migration effort (`aka.ms/msbuild/mttasks`)? What's the perf delta from runtime async in real workloads (not just size)? How does the new `unsafe` reviewable-contract surface in analyzers/code review? Which CLI commands are native AOT by GA?
- [ ] Relevant to: anyone building .NET in CI/containers (SDK size + CLI speed), agent/LLM tooling authors (agent-aware CLI, JSON Lines logs), MAUI/cross-platform device devs, perf-sensitive library authors (runtime async, memory-safe SIMD), and MSBuild task authors.

## 🔗 Related
- [[2026 Build Session List]]
- Rich Lander's **memory safety** blog post (referenced, ~1 week before the talk) — redesigning `unsafe`.
- Chet Husk's dedicated **`dotnet up`** Build recording.
- `aka.ms/msbuild/mttasks` — multi-threaded MSBuild task migration guide.
- 