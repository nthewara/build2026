---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/arm
  - topic/cobalt
  - topic/performance
  - topic/azure
  - topic/profiling
source: https://www.youtube.com/watch?v=J43ze2sO5-U
session_code: ODSP900
event: Microsoft Build 2026
speakers: David Heckney (Technical Product Director, Arm)
duration_min: 8
aliases:
  - Performance tuning on Cobalt with Arm Performix
---

# ODSP900 — Performance tuning on Cobalt with Arm Performix

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** David Heckney — Technical Product Director, Arm  
> **Duration:** ~8 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=J43ze2sO5-U)

## 🎯 TL;DR
Arm's David Heckney introduces **Arm Performix**, a new performance-analysis toolkit built in close collaboration with Microsoft's performance experts to help engineers observe and accelerate workloads running on **Azure Cobalt** (Arm-based) VMs. Performix frames performance work like a crime investigation — broad evidence-gathering first, then progressively deeper, hypothesis-driven dives — and packages that disciplined methodology into a unified UI (and equivalent CLI) built around two core concepts: **targets** (the Cobalt instances under test, added via SSH) and **recipes** (the experiments/workflows you run). A guided ladder of recipes takes you from validating the instance (system characterization), to seeing how it behaves under load (system utilization heat map), to finding hot code (code hotspots, language-agnostic incl. Java/.NET), to instruction mix and Arm top-down CPU microarchitecture analysis. The standout capability is an **MCP server** that couples Performix's profiling data, disassembly, target info, and source code to an LLM (demoed beside code in Visual Studio), turning analysis from passive sampling into active, confidence-based optimization suggestions. **Performix is available now, free to download and free to use.**

## 🔑 Key Takeaways
- **Arm Performix** is a new, free performance-analysis toolkit purpose-built to observe and accelerate workloads on **Azure Cobalt** Arm-based instances.
- It was **co-developed with Microsoft performance experts**, reflecting the strong Microsoft–Arm partnership; aimed especially at teams **migrating to Cobalt for the first time**.
- Core mental model: performance analysis is an **investigation** — suspects, leads, hypotheses, evidence, dead ends — **not** a linear process; expert workflow is consistent even though each case is unique.
- Method = **breadth-first, then depth**: get the overall picture, then dive into specifics; use **good science** (change one variable at a time, repeat runs for consistency, compare against baselines).
- Two foundational concepts: **Targets** (systems to test — Cobalt instances added via SSH: host, user, port, keys) and **Recipes** (the experiments/workflows; some still flagged **experimental** as the toolkit expands).
- **System characterization recipe** runs micro-benchmarks to validate the instance performs as expected (e.g. how **memory bandwidth varies with access size** = cache behavior).
- **System utilization recipe** shows behavior under load — e.g. a **CPU heat map across a 96-core system** over a 1-second interval (demo: ~2/3 cores busy, 1/3 idle) to surface investigation avenues (more threads? different instance size? lock contention?).
- **Code hotspots recipe** samples where time is spent and ties it back to source — **works across all languages including Java and .NET** — finding hot paths static analysis can't.
- **Instruction mix** reveals how well the app exploits the platform; demo **compared Arm NEON vs SVE** matrix-multiply instruction mixes across two runs.
- **CPU microarchitecture recipe** applies **Arm's top-down methodology** to attribute time across CPU layers — cache levels, pipeline stalls from **branch mispredictions**, etc.
- **Run comparison** is first-class: easily diff two runs against each other / against baselines.
- The **MCP server** integrates Performix with an LLM (shown in **Visual Studio**), feeding it profiling data + disassembly + target info + source code so it **actively suggests confidence-based improvements** — analysis becomes dynamic, not passive.
- Everything in the UI is **also available via the command line** for terminal-first workflows; **Performix is available now, free to download and free to use.**

## 📚 Detailed Notes

### Context: why this toolkit, and who it's for
David Heckney (Technical Product Director, Arm) presents a short walkthrough of **Arm Performix**, a brand-new performance analysis toolkit for observing and accelerating workloads on **Cobalt** (Azure's Arm-based compute). He stresses the **strong Microsoft–Arm partnership** — Performix was developed in **close collaboration with Microsoft performance experts**. The talk explicitly addresses people who may be **migrating to Cobalt for the first time**, nudging them toward the available migration resources before diving in. The motivating problem: performance engineers today must wrangle a **wide, complex, and fragmented tool set**, and Performix exists to unify that.

### The mental model: performance analysis as a crime investigation
Before the demo, Heckney sets the conceptual frame. Performance analysis is **like a crime investigation**:
- You have **suspects, leads, and hypotheses**.
- You **gather evidence** to support or disprove theories.
- Expect **blind alleys and dead ends**; **new evidence can force you to revisit prior assumptions**.
- It is **not a straightforward linear process**.

Crucially, while every investigation is unique, the **overall approach expert analysts take is consistent** — and that consistency is what Performix encodes into a guided workflow.

### The methodology: breadth-first, then depth, with good science
The disciplined approach Performix bakes in:
1. **Start broad** — acquire an overall picture before diving into detail.
2. **Run experiments with good science** — change **one variable at a time**, **repeat runs** to understand consistency, and **compare against previous baselines**.
3. Concretely, this means:
   - First understand **what the platform (the Cobalt instance) is capable of**.
   - Then understand **how the system behaves once the workload is applied** — which dictates **where analysis should be focused**.
   - Then **go deeper** with targeted analysis where the evidence points.

### Two core concepts: Targets and Recipes
The Performix UI (with full **CLI parity** for terminal users) is organized around two primitives:

- **Targets** — the systems you run workloads on; in this case **Cobalt instances**. Adding a target is simply supplying the relevant **SSH credentials**: host, user, port, and any required SSH keys.
- **Recipes** — the **experiments or workflows** you run against a target as part of analysis. There's a catalog of recipes; ones **still under development are marked "experimental"** as Arm continues to expand the toolkit.

When you run a recipe you **select the target** and **choose the benchmarks/options**; Performix then **ensures the target is set up and installs any dependencies on the target system on your behalf** — removing manual setup friction.

### Recipe 1 — System characterization (validate the instance)
The first step assesses the overall Cobalt target. The **system characterization recipe** runs a **series of micro-benchmarks** on the platform. Example output shown: **how memory bandwidth varies with access size** — i.e., **how the cache is performing**. The purpose is to **validate that the instance itself is performing at the expected level** before you start blaming your workload. (This is the "understand what the platform is capable of" step.)

### Recipe 2 — System utilization (behavior under load)
Next, see how the instance behaves with the workload running, via the **system utilization recipe**. It can:
- **Launch a new workload**,
- **Attach to an already running process**, or
- **Profile across all processes**.

Demo: focusing on the **CPU of a 96-core system**, Performix shows a **heat map of how busy each core is over a 1-second interval**. Roughly **two-thirds of cores are occupied, the remaining third relatively idle**. This **at-a-glance visualization generates investigation avenues**, e.g.:
- Could we **increase the thread count**?
- Would a **different instance size** help?
- Is there **lock contention** occupying these cores?

This is the pivot point that decides where to dig deeper.

### Recipe 3 — Code hotspots (find the hot code, any language)
To learn what those busy cores are actually running, use the **code hotspots recipe**. It **samples where time is being spent in the code** and **ties it back to the source code itself**. Key strengths:
- **Works across all languages, including Java and .NET** (i.e. managed runtimes, not just native).
- Ensures you **optimize the right places** — something **static analysis tools can't do**, because hotness is a runtime property.

### Recipe 4 — Instruction mix (how well you use the platform)
Another lens on where time goes is **instruction mix**, useful for understanding **how well the application is taking advantage of the platform's capabilities**. Because comparison is core to the methodology, Performix lets you **easily compare between runs**. Demo: comparing the **instruction mixes of two different matrix multiplications** — one using **Arm NEON** instructions, the other using **SVE** (Scalable Vector Extension) — illustrating how a code change shifts the instruction profile.

### Recipe 5 — CPU microarchitecture (Arm top-down)
For the deepest hardware-level view, the **CPU microarchitecture recipe** uses **Arm's top-down methodology** to characterize **where time is being spent at various parts of the CPU**. With it you can:
- Dig into **how the various layers of caching are performing**.
- **Detect pipeline stalls** caused by **branch mispredictions**.

This completes the "breadth-first across the whole system, then deep into specific aspects as the investigation unfolds" arc.

### Delivering insights: the MCP server + LLM integration (the headline)
For the final part, the focus shifts from analysis to **actually delivering improvements**. Performix **provides an MCP (Model Context Protocol) server** so the analysis can be **tightly coupled with an LLM**. Demo: working **next to code in Visual Studio**, Heckney **summons the analysis from all the runs just performed**. By feeding the LLM:
- the **profiling data**,
- the **disassembly**,
- **information about the target system**, and
- the **source code**,

Performix can **deliver dynamic insight and suggest confidence-based improvements** to accelerate the workload on Cobalt. This transforms performance analysis **from a passive activity** (sampling and profiling) **into a dynamic one** that **actively suggests optimizations**.

### Wrap-up
Summary of the arc: Performix uses **targets and recipes** to apply a **guided analysis approach** — start broad with **system characterization** and **utilization**, then enable **deeper analysis** with specialized recipes (code hotspots, instruction mix, CPU microarchitecture). The **MCP server integration** is the differentiator, turning profiling into active optimization. **Performix is available now, free to download and free to use** — Arm invites viewers to try it and share feedback. (Note: the transcript contains a stray caption artifact — "[snorts]" — mid-summary; it carries no content.)

## 🛠️ Products / Features / Technologies Mentioned
- **Arm Performix** — new (free) performance-analysis toolkit for observing and accelerating workloads on Cobalt; unifies a fragmented performance tool set; UI + CLI parity. The subject of the entire session.
- **Azure Cobalt** — Microsoft's Arm-based cloud compute; the "target" platform whose instances are analyzed and tuned here.
- **Targets (Performix concept)** — the systems/Cobalt instances under test, added via SSH (host, user, port, keys).
- **Recipes (Performix concept)** — the experiments/workflows; some flagged "experimental."
- **System characterization recipe** — micro-benchmarks to validate instance capability (e.g. memory bandwidth vs access size = cache behavior).
- **System utilization recipe** — launch/attach/profile-all-processes; CPU core-busy heat map over a time interval.
- **Code hotspots recipe** — runtime sampling tied back to source; language-agnostic, **incl. Java and .NET**.
- **Instruction mix** — analyzes how well code uses the platform; supports run-to-run comparison.
- **CPU microarchitecture recipe** — **Arm top-down methodology**; cache-layer analysis + branch-misprediction pipeline-stall detection.
- **MCP (Model Context Protocol) server** — Performix-provided server that couples analysis with an LLM for active, confidence-based optimization suggestions.
- **Visual Studio** — IDE where the LLM-driven analysis is summoned next to the user's code in the demo.
- **Arm NEON** — Arm SIMD instruction set; one matrix-multiply variant in the instruction-mix comparison.
- **Arm SVE (Scalable Vector Extension)** — Arm vector ISA; the other matrix-multiply variant compared against NEON.
- **SSH** — transport/credentials used to register Cobalt targets.

## 🚀 Announcements / What's New
- **Arm Performix is available now** — **free to download and free to use** (general availability framing; presented as released, not a preview). This is the session's principal announcement.
- Some Performix **recipes are still in development and marked "experimental"**, indicating the toolkit will continue to expand.

## 💡 Demos
The session is essentially one continuous product demo of the Performix UI:
- **Adding a target** — register a Cobalt instance via SSH (host/user/port/keys). *Proves setup is trivial.*
- **System characterization** — micro-benchmarks; output graph of **memory bandwidth vs access size** (cache performance). *Proves the instance performs at the expected level.*
- **System utilization** — **96-core CPU heat map** over a 1-second interval showing ~2/3 cores busy, 1/3 idle. *Proves you can spot utilization patterns and generate hypotheses (threads/instance size/lock contention) at a glance.*
- **Code hotspots** — sampling tied back to source across languages. *Proves you optimize the right code, beyond static analysis.*
- **Instruction mix comparison** — two matrix multiplications, **NEON vs SVE**, compared across runs. *Proves run-to-run comparison and platform-utilization insight.*
- **CPU microarchitecture** — Arm top-down attribution; cache layers + branch-misprediction stalls. *Proves deep hardware-level diagnosis.*
- **MCP server + LLM in Visual Studio** — summoning combined analysis (profiling + disassembly + target info + source) to get **confidence-based improvement suggestions**. *Proves the shift from passive profiling to active, AI-assisted optimization.*

## 📊 Notable Stats / Quotes
- **96-core system** used in the utilization demo; **~2/3 of cores occupied, ~1/3 idle** over a **1-second** sampling interval.
- **Performix is "available now, free to download and free to use."**
- Framing quote: *"Performance analysis can be thought of like a crime investigation. You have suspects, leads, hypotheses... It is not a straightforward linear process."*
- On AI integration: analysis goes *"from being a passive activity of sampling and profiling to a dynamic one of actively suggesting improvements and optimizations to accelerate your workload."*
- Good-science principle: *"changing one variable at a time, repeating the runs to understand consistency, and comparing results against previous baselines."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Download **Arm Performix** (free) and add one of our Cobalt instances as a target via SSH; run **system characterization** to baseline the instance, then **system utilization** on a real workload to read the core heat map.
- [ ] Things to try: Use **code hotspots** on a **.NET** workload on Cobalt to confirm managed-runtime sampling works as advertised; then run **instruction mix** to compare NEON vs SVE on any vectorizable hot path.
- [ ] Things to try: Wire up the **Performix MCP server** to an LLM in **Visual Studio** and see how actionable the confidence-based optimization suggestions actually are.
- [ ] Questions: Which Linux distros/agent requirements does the on-target Performix agent need (it auto-installs dependencies — what footprint)? Does it support Windows-on-Arm targets or Linux only?
- [ ] Questions: Is the MCP server LLM-agnostic (bring-your-own model/endpoint) and does any profiling/source data leave the machine? Which recipes are still "experimental"?
- [ ] Questions: How does Performix's Arm top-down output compare to `perf`/`topdown` tooling — is it a superset or a friendlier front-end?
- [ ] Relevant to: Cobalt migration/cost-optimization work; right-sizing Arm instance SKUs; any team profiling Java/.NET services on Azure Arm; the broader Arm-on-Azure performance story (pairs with DEMSP381 / OD828).

## 🔗 Related
- [[DEMSP381 - Scale agentic AI on Azure with Arm Cobalt VMs]] — sibling Arm partner session; scaling agentic AI workloads on the same Cobalt platform.
- [[OD828 - Latest Cobalt VMs and Azure Boost enhancements]] — the Cobalt VM family and Azure Boost context these tuning workflows run against.
- [[DEM300 - Supercharged profiling Finding performance bugs with agents]] — complementary Microsoft profiling story (Visual Studio Profiler + agents); same "AI-assisted performance" theme.
- [[OD827 - Build deploy and run Linux workloads on Azure]] — running/operating the Linux workloads you'd profile with Performix on Cobalt.
- [[DEM311 - Scale cloud-native workloads with Azure Linux]] — Azure Linux as the OS layer for cloud-native (incl. Arm) workloads under analysis.
- Source list: [[2026 Build Session List]]
