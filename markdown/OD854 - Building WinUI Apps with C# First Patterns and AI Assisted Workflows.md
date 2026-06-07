---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/winui
  - topic/dotnet
  - topic/csharp
  - topic/windows-app-sdk
  - topic/ai
source: https://www.youtube.com/watch?v=tPO3vwRVB-M
session_code: OD854
event: Microsoft Build 2026
speakers: Chris Anderson (Engineer, Windows UI team)
duration_min: 27
aliases:
  - Building WinUI Apps with C# First Patterns and AI Assisted Workflows
---

# OD854 — Building WinUI Apps with C# First Patterns and AI Assisted Workflows

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Chris Anderson — Engineer, Windows UI team (working on new experimental framework features)  
> **Duration:** ~27 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=tPO3vwRVB-M)

## 🎯 TL;DR
Chris Anderson from the Windows UI team makes the case that WinUI is here to stay — the team is dropping the version number (it's now just "WinUI", not "WinUI 3"), there is **no new framework coming**, and Microsoft is putting real muscle behind closing the platform's known gaps. The first half is a state-of-the-union on the fundamentals developers keep asking for: performance (memory wins + a new system compositor), quality/bug fixes, new controls (DataGrid, charting), completing the open-source journey (moving the team to work primarily in the public repo), and credible migration/interop stories for WinForms and WPF. The second half pivots to where development is heading — AI-assisted coding and **code-first / C#-first** workflows — and introduces a brand-new experimental open-source project, **Microsoft UI Reactor**, a React/SwiftUI/Compose-style functional reactive projection of WinUI controls into C#. The bulk of the talk is a live demo building a reactive WinUI app entirely in C# with hot reload, state, collections, async data, a diffing reconciler with dev-tools visualization, and an experimental pie-chart control. Reactor is explicitly a high-churn playground for ideas that, once proven, get pushed down into production WinUI.

## 🔑 Key Takeaways
- **WinUI is not being replaced.** The team has "no intention of building a new framework" — they're dropping the "3" and calling it just **WinUI**, signaling commitment and no massive breaking shift.
- **Performance fundamentals first.** Heavy investment in **memory usage** improvements and a switch to a **system compositor** for better performance; these changes have already hit the public Git repo and will land in experimental/preview Windows App SDK builds shortly.
- **New controls coming:** **DataGrid** and **charting** are up next, shipping in the core WinUI bits to unlock data-oriented scenarios.
- **Open source is nearly complete.** Phase 3 (run tests in public) is done; **Phase 4** moves the team off internal source repos to work **almost exclusively in the public repo**, landing all PRs publicly so the community can see and contribute in real time.
- **First-party adoption is accelerating** — WinUI is being integrated into the Windows **shell** faster, so more Microsoft features will be built on it.
- **Feature-gap backlog is being worked through** — long-standing gaps (e.g. system tray, limited windowing) that today force devs to lean on open-source libraries.
- **Migration/interop is a priority:** make **WinForms ↔ WinUI** interop "bulletproof" in both directions, and bring **WPF ↔ WinUI** mix-and-match to parity ("no problems").
- **AI has changed how code is written** — Chris says he "rarely types semicolons anymore," using AI for most code, plus code reviews, tests, and specs. The platform is being shaped around this shift.
- **Code-first is the new default.** CLI coding tools (Claude Code, GitHub Copilot) + VS Code + a terminal make code the de-facto way to build; WinUI wants **C# elevated from "code-behind" to a first-class way to write an entire app**.
- **C#-first parity goal:** controls, templates, and features currently locked behind **XAML** should be fully reachable from a C#-first experience.
- **New experimental framework announced: Microsoft UI Reactor** — an open-source functional/reactive C# projection of WinUI controls, inspired by SwiftUI, Jetpack Compose, and React.
- **Reactor ≠ how things will ship.** It's a deliberate **high-churn experimental playground**; even controls written in Reactor's syntax (e.g. DataGrid) will likely ship in core WinUI written in C++ on the same WinRT frameworks.
- **Good ideas graduate.** As Reactor experiments "bake," they get pushed down into production WinUI so they become consistent across the stack.
- **Community participation is the point** — Reactor already has external contributors and PRs; the explicit ask is clone it, build something, file feedback, send PRs.
- **The reactive model demoed end-to-end:** components + `render`, `useState`/`useReducer`, keyed list virtualization, a diffing **reconciler** with opt-in **dev tools** that highlight per-frame changes, and first-class **async resources** with loading/error/data states and dependency-triggered refetch.
- **Primary call to action:** keep using and building on WinUI (it's the supported path forward) **and** go try Reactor to influence the future direction.

## 📚 Detailed Notes

### Framing: earn the right to build the shiny things first
Chris opens by deliberately *not* leading with the new and shiny. Before talking about attractive future "baubles," he wants to cover the foundational work the team needs to do to "earn the right" to build them. These are the core features people have repeatedly asked for and genuinely need to be productive on WinUI. The throughline of the whole first half: credibility and fundamentals before novelty.

### Performance fundamentals & quality
The first priority is **performance and quality** — fixing a lot of bugs and investing heavily in:
- **Memory usage** improvements.
- Switching over to a **system compositor**, which should yield even better performance improvements.

Crucially, this work has **already hit the public Git repo** and is available to play with today. **Windows App SDK (WinAppSDK)** versions incorporating these changes will be available shortly through the **experimental and preview branches**. The message: this isn't a roadmap promise — the code is public now.

### New controls: DataGrid and charting
The team is adding a lot of new controls. Specifically called out:
- **DataGrid**
- **Charting**

Both are "up and coming" and should be out relatively shortly, showing up in the **core WinUI bits**. The goal is to let developers go after far more **data-oriented scenarios** that the platform couldn't serve well before.

### Completing the open-source journey
Open-sourcing WinUI has been a long, phased path that Chris is personally excited to finish:
- **Phase 3 (recently hit):** tests can now run **in public**. Anyone can grab the bits, **compile WinUI**, and run the test suite to confirm they have something fully functional. If they make changes, they can run the tests to confirm they haven't broken anything — an essential property of a real open-source library.
- **Phase 4 (the big next step):** move the team from **internal source repos** to working **primarily and almost exclusively in the public repos**. The team will start landing **all of their pull requests** on the public side.

The point of Phase 4 is to reach a place where Microsoft can **accept changes from the community**, **engage** with the community, and let the community **see the work instantly** as it happens — not on a delayed mirror.

### The themes the team keeps hearing (and the answers)
Chris explicitly addresses the recurring community feedback:

**1. "Are you actually serious this time? Will you stick with this framework?"**
WinUI 3 is ~4 years old, and people fear each year might bring yet another brand-new framework announcement. The answer is emphatic: **no new framework.** In fact, the team is **dropping the number** — referring to it as just **WinUI** — because there is no intention of a massive breaking shift. They want to **stretch WinUI to be accessible for any use case**, are integrating it into the **shell** at a faster rate, and expect **first-party Microsoft features** to be built on WinUI. They acknowledge enterprise adoption of a new UI framework takes a long time, and frame *now* as the moment to show they're committed and putting their "muscle" behind it.

**2. "There are too many feature gaps beyond DataGrid and charting."**
Developers point to missing capabilities like proper **system tray** support and **limited windowing**, which force many to rely on **open-source libraries** to patch the platform. Chris acknowledges a **large backlog** and commits to working through it to address the called-out feature gaps — framed as one of the biggest issues holding the platform back.

**3. "How do we migrate? Is it all-or-nothing?"**
People worry about moving off their current frameworks: can they **incrementally adopt** WinUI, or must they rewrite everything? Today there's a *reasonable* **WinForms interop** story — "not great, but reasonable," and it works pretty well. The team wants to make it **bulletproof**: WinForms ↔ WinUI interop should be **super easy in either direction**. They also want **WPF migration to be equally good** — you should be able to **mix and match WPF and WinUI with no problems**. This is acknowledged as a big chunk of future work.

### The two industry shifts shaping the platform's future
Chris pivots from "fix the fundamentals" to "where is software development going," naming two big trends:

**Shift 1 — AI assistance has transformed how code is written.** It changed the way *he* writes software: he "rarely types semicolons anymore" and is "almost always using AI to drive most of the code." He uses AI for **writing code, code reviews, writing tests, and help with specs**. This AI shift has "really transformed the way you write all the code," and the platform direction has to account for it.

**Shift 2 — more dynamic UI, expressed as code-first.** Two sub-trends:
- **Dynamic UI has accelerated.** He cites **SwiftUI, Jetpack Compose, and React** as the industry's current best practices for building dynamic UI — making it "super straightforward" to build things that are incredibly **flexible and responsive** to what the user does.
- **Code as the primary way to build.** The move to **CLI-based coding tools** (he names **Claude Code** and **GitHub Copilot**) has made **VS Code + a terminal window** "one of the most productive places to be." This pushes toward a world where **code-first becomes the de-facto standard.**

### The C#-first goal for WinUI
The concrete ambition: elevate **C#** to be a **primary way to target WinUI**. Today C# is largely a way to write **code-behind**; the team wants it to be a way to **write an entire application**. You should be able to build on the **existing WinUI framework** — using its **controls, templates, and all its features** — from a **C#-first experience**. The problem: several of those capabilities are currently **locked behind needing XAML**, and the goal is to **bring C# up to parity** so you don't need XAML to reach them.

### Announcing Microsoft UI Reactor (experimental)
The headline new thing: **Microsoft UI Reactor** — a **new experimental, open-source framework** for the team to experiment with new styles of programming, new controls, and new app models for WinUI's future. How to think about it:
- It's a **place to experiment with ideas the team doesn't yet have full conviction behind**, developed **out in the open** as an open project from day one.
- It is **very early** and **high-churn** — lots of code changes daily. "We are likely to change every line of code in this project."
- It's explicitly **open for a ton of feedback, guidance, and participation** from the community. Community PRs are **already landing**, and the team wants more.
- **Graduation model:** as good ideas are found and "baked," they get **pushed down into the production WinUI bits**, becoming consistent and standard across the WinUI stack so they don't stand out. So if something in the Reactor layer looks "foreign," don't panic — it's a trial that may or may not get promoted.

The two-part call to action: **keep building on WinUI** (the supported, invested-in path forward) **and** **clone Reactor, try it, and give feedback** (file issues, send PRs).

### What's inside the Reactor repo
Reactor is a new open-source project showing the **future direction** the team is thinking of for WinUI. It contains two distinct things:
1. **A set of experimental new controls / experiences** the team thinks will be delivered as part of **core WinUI** — using the **XAML you know, data binding, and the MVVM architecture**. (These controls are not tied to the Reactor syntax; e.g. charting would just be a general WinUI feature.)
2. **A new domain-specific language / projection of WinUI controls into C#** — enabling **C# as your primary programming experience** for people who prefer a **functional, reactive style** over a XAML-based approach.

Almost **everything in the open-source project is written using this new C# style** — mostly so the team could experiment with the style as they built the controls and "see where the edges were." Important caveat: they **don't expect this to be the right way to build most controls.** Many controls will be **integrated directly into WinUI**, written in **C++ using the same WinRT frameworks** developers already know. Seeing a DataGrid written in Reactor syntax does **not** mean that's how the DataGrid will ultimately ship — it's an **experimental playground**.

Chris reiterates the meaning of "experimental" here: likely to **change every line**, **change the syntax**, etc. The current syntax uses a **fluent functional-style expression**, but that may completely change — they're working **with the C# team** on the right way to express these construction patterns so it "feels very natural in the language." External contributors have already added features, filed issues, and issued PRs.

### Demo — the basic app: window, component, render
The live demo builds a reactive WinUI app entirely in C#:
- A **`reactor app run`** call starts the project and **creates a window**.
- A **`dev tools` flag** is passed (something you'd normally only put in a **debug build**) — revisited later.
- The core unit of composition is a **component**. You **override `render`**, create a **title bar heading**, a **text block**, and put them in a **flex column**.
- First tweak: the text is hard to see, so he bumps the **font size** and saves.
- He adds a **flex column** with a **margin of 24** to indent the header/"hello" text, then makes it occupy all available space with **`grow: 1`** and **`basis: 0`**.
- Below, a standard **`dotnet watch`** command drives **hot reload**; the app updates live. (He warns **hot reload isn't always stable** and the app "might crash" — a recurring honest caveat.)
- Both **imperative construction** and **expression-based construction** styles are supported — "whatever you like to do."

### Demo — adding state (useState)
To make it interactive, he introduces **state**:
- Creates a **`count`** state initialized to **0** and a **`name`** state.
- Updates the text to interpolate the **name** and **count**, showing you can run **any C# function** inside `render`.
- Adds a **name field** (a text input bound to get/set the name) and a **row of buttons** (a flex row): a **minus** button (`set count to count - 1`) and a **plus** button (`set count to count + 1`).
- Adds spacing with a **column gap of 4**, drops the name field and buttons into the header.
- Result: typing in the name field updates the text; clicking **plus** increments the **count** live. A minor layout glitch is noted to be fixed shortly.

### Demo — collections and the re-render problem (useReducer)
He moves to a richer, collection-valued case:
- Builds a list: a numeric **range to 100**, mapping each index to a string like **`item #<i>`** plus **8 characters of a new GUID** (`Guid.NewGuid().ToString()` truncated), materialized into a **list**.
- Visualizes it with a **ListView**, providing a **key selector** (the unique item strings make good keys) and a **view builder** that creates a **text block** per item with a **margin of 8**.
- Puts the ListView in the flex grid as the **largest piece** (consuming remaining space), which also fixes the earlier layout glitch. Items now render, scroll in a list box, and **plus still works**.
- **Key teaching moment:** clicking plus regenerates **all** the GUIDs — because `render` is **called every frame / on every change**. The framework **recomputes the display and diffs** the two trees, updating only what actually changed. But here the GUID strings are recomputed each run, so they all churn. **`useState` values persist** across renders; the inline `range`/GUID computation does not.
- **Fix:** switch from recomputing inline to a **`useReducer`** (the collection-valued primitive) returning **`items`** and **`updateItems`**. Saving **immediately fixes the bug** — increment/decrement and text edits work, and the items **no longer recompute every frame**.
- He then wires an **add** method/button using `updateItems` (a function taking the incoming list and returning a new list): prepends a **new `item #<list.count + 1>` + GUID** to the front, keeping the rest. Clicking **add** inserts new items at the top, everything still functions.

### Demo — the reconciler and built-in dev tools
To make the **diffing / incremental update** visible, he returns to the **dev tools** idea:
- The hypothesis: there's a case for **developer-friendly features built into the framework**. The **dev tools menu** appears **conditionally** — only when you've **set the `dev tools` property** to opt in **and** specified on the **command line** that you want that instance run with them on. This lets you **turn on developer features in your product** and write **conditional debug code trivially**.
- Built-in feature: **"highlight reconciler changes."** With it on, clicking **plus** shows the framework is **only updating the string** (it's one big string), and clicking into the text shows the **text box** updating too — a live visualization of **what changes each frame**.
- Demonstrating granularity: inside the list item he replaces the single text block with a **flex row** containing a **second text block** showing **`count: <count>`** (same margin of 8). Initially everything flashes red (re-rendered completely / new elements created), but subsequent **plus** clicks only re-render **that count portion** — while the top "hello" line, being **one atomic text block with a big interpolated string**, must update the **whole string**. The separate count element gets **incremental updates**. He then turns off the "flashy blinky" highlighting.

### Demo — building new components (function vs class)
Two ways to factor out a component:
- **Extract a method** — e.g. pull the flex row into a **`listItemView`** function. That's *all* that's needed: a new function **is** a new component, no extra ceremony. Changing a label (e.g. to "countish") just works (with the occasional `dotnet watch` crash, "as promised").
- **Create a full component class** — more work but gives you a **lifecycle**: you know when the component is **mounted into the tree**, and there's an **`update` method** you can override. He writes a `listItemView` class **deriving from `component`**, declares the **properties it takes** (an **item** and a **count**), with roughly the same content, plus a **helper method** so callers can just call **`listItemView(...)`** instead of doing manual construction. Adding **`using static`** for the components lets the call site bind to it; saving shows no functional change.

### Demo — an experimental pie chart control
To showcase a **new control** candidate, he swaps the ListView for a **pie chart**:
- **`pieChart`** takes the **list of data** (the items) plus a **value function** — he returns **1** for every item so each slice is a unit.
- After a compile error reminder ("I have to have code that compiles for it to work"), he limits it to the **first five** items.
- Adds a **label** via a **label view** that returns **`listItemView(item, count)`**, so labels show the counts — and they **increment when you click plus**.
- Labels are hard to see, so he sets a **`listLabelRadiusOffset` of 30** to push them out, then makes it **`15 * count`** — so the labels **move outward as the count changes**. This demonstrates how much **flexibility** the reactive system gives: you can transform the code and the **UI continuously updates to keep up**.

### Demo — asynchronous data (resources, match, loading/error/data)
Everything so far was **synchronous**; he closes by showing **async**:
- Introduces a **resource** — an **asynchronous value**. It's hard-coded to **delay 2 seconds**, then **randomly fail ~20% of the time** ("just cuz that's what the network does").
- This breaks the existing code two ways: you **can't update the item** directly (it's now async) and the result **isn't a list yet** (no `.take`). You must **get the data out of the async result**.
- Solution: **`items.match(...)`**, which returns an element and lets you specify **what UI to show per state**:
  - **Loading** → a text block saying **"loading"**.
  - **Error** → (ignoring the error detail) a **red** text block saying **"error."**
  - **Data (success)** → takes the resolved value (**`data`**) and feeds it into the existing rendering function.
- On save, it briefly shows **loading**, then drops into an **error** state (it lost the random race).
- To retry, he makes the resource depend on the **name**: "whenever name changes, pretend that's a **dependency** of this resource." Now changing the **name** re-triggers the resource — it goes to **loading**, "wins the lottery this time," and shows the value.
- Takeaway: Reactor provides **easy-to-use asynchronous functions** that handle the normal UI cases — trivially showing **loading** and **error** states for **any async value**, including **lists** that return these.

### Closing
That covers the breadth of the **core pieces of Microsoft UI Reactor**: an **experimental framework** with a **new set of controls** (e.g. **charting**, which would be **general WinUI**, not Reactor-specific — "very few things would ever be specific to the reactor syntax") plus the **C#-first** functional way of doing development to "see how it feels." Final ask, repeated: **clone the repo, build something, send feedback, file feedback items, issue a PR** — "let's go see what we can do with this… and learn together."

## 🛠️ Products / Features / Technologies Mentioned
- **WinUI** (formerly "WinUI 3") — Microsoft's native UI framework for Windows; the "3" is being dropped to signal no breaking framework reset. Core focus of the talk.
- **Windows App SDK (WinAppSDK)** — the distribution vehicle; new perf changes land via its **experimental** and **preview** branches.
- **System compositor** — what WinUI is switching to for better rendering performance.
- **DataGrid (control)** — new data-grid control coming to core WinUI for data-oriented scenarios.
- **Charting (control)** — new charting/visualization support coming to core WinUI (demoed via an experimental pie chart).
- **Microsoft UI Reactor** — newly announced experimental, open-source project: a functional/reactive **C#-first projection** of WinUI controls + an experimental controls playground. Ideas graduate into production WinUI when proven.
- **XAML** — WinUI's markup language; today some controls/templates/features are locked behind it. The C#-first goal is to reach parity without requiring XAML.
- **Data binding / MVVM** — the architecture Reactor's XAML-based controls still use; familiar WinUI patterns.
- **WinRT frameworks / C++** — how most production WinUI controls will actually be implemented (not in Reactor syntax).
- **WinForms** — legacy desktop framework; target of a "bulletproof" two-way interop story with WinUI.
- **WPF** — desktop framework; goal is mix-and-match parity with WinUI for migration.
- **Windows shell** — being integrated with WinUI at a faster rate; first-party features built on WinUI.
- **`dotnet watch`** — standard .NET CLI command driving hot reload in the demo (noted as not always stable).
- **Hot reload** — live code-update mechanism used throughout the demo.
- **VS Code + terminal** — cited as one of the most productive modern dev setups; emblem of the code-first shift.
- **Claude Code** — CLI-based AI coding tool cited as part of the code-first trend.
- **GitHub Copilot** — AI coding assistant cited as part of the code-first / CLI coding trend.
- **SwiftUI / Jetpack Compose / React** — industry best-practice dynamic-UI frameworks Reactor draws inspiration from.
- **Reactor primitives:** `component` + `render`, **`useState`**, **`useReducer`** (collection-valued), **ListView** with key selector + view builder, **flex column / flex row / flex grid** layout (`grow`, `basis`, margin, column gap), **reconciler** (diffing engine), built-in **dev tools** ("highlight reconciler changes"), **pie chart** (`pieChart`, `listLabelRadiusOffset`), and **resources** (async values) with **`.match`** over loading/error/data states + dependency-based refetch.

## 🚀 Announcements / What's New
- **WinUI drops its version number** — now officially just **"WinUI"** (not "WinUI 3"), signaling long-term commitment and no breaking framework reset.
- **Performance work is public now** — memory improvements + the **system compositor** switch have already landed in the public Git repo; **WinAppSDK** builds with these changes arrive shortly via experimental/preview branches.
- **DataGrid and charting controls** announced as coming to core WinUI "relatively shortly."
- **Open-source Phase 3 complete** (tests run in public) and **Phase 4 underway** — the team moves to work and land **all PRs almost exclusively in the public repo**.
- **WinForms ↔ WinUI** interop to be made "bulletproof" in both directions, and **WPF ↔ WinUI** mix-and-match brought to parity (future work, no dates).
- **Microsoft UI Reactor** — a **new experimental open-source framework** released/announced at this session: a C#-first functional reactive projection of WinUI plus an experimental controls playground. Explicitly early, high-churn, and feedback-driven.

## 💡 Demos
- **Reactive WinUI app in pure C# (live, hot-reloaded):** Built a window + component overriding `render`, styled a title bar/heading/text block in a flex column (font size, margin 24, `grow 1`/`basis 0`). Proved C#-first construction with `dotnet watch` hot reload. *Point: you can build real WinUI UI entirely in C# with a fast inner loop.*
- **State with `useState`:** Added `count` and `name` state, a name input, and minus/plus buttons that mutate count live. *Point: ergonomic React-like state in C#.*
- **Collections + the re-render lesson:** Generated a 100-item list of `item #i` + GUID, rendered via ListView with a key selector and view builder; showed that `render` runs every frame and **diffs**, that inline GUID computation churns every frame while `useState` persists, then fixed it with **`useReducer`** and added a prepend-`add` action. *Point: understand the render/diff model and use the right state primitive.*
- **Reconciler visualization via built-in dev tools:** Opt-in `dev tools` (property + command-line flag) enabled "highlight reconciler changes," visually proving only changed elements update — a single big interpolated string updates wholesale, while a separate `count:` text block gets incremental updates. *Point: the framework does fine-grained incremental updates, and ships debuggability.*
- **Component factoring (function vs class):** Extracted a `listItemView` function (a function *is* a component), then rebuilt it as a full `component` subclass with declared props (item, count), lifecycle/mount + `update`, and a `using static` helper call site. *Point: scale from quick functions to full lifecycle-aware components.*
- **Experimental pie chart control:** Swapped ListView for `pieChart` over the first 5 items with a value function and label views showing live counts; animated labels outward with `listLabelRadiusOffset = 15 * count`. *Point: rich new controls + reactive transforms keep the UI in sync automatically.*
- **Async data with resources:** A `resource` that delays 2s and randomly fails ~20%, surfaced via `items.match` into loading/error(red)/data states, with the resource depending on `name` so changing the name re-triggers a fetch. *Point: first-class, easy async with built-in loading/error/data handling for any async value.*

## 📊 Notable Stats / Quotes
- *"We have no intention of building a new framework… we're kind of dropping the number and we're referring to WinUI as just WinUI."* — the headline commitment.
- *"WinUI 3 is 4 years old."* — context for the "are you serious this time?" skepticism.
- *"I rarely type semicolons anymore. I'm almost always using AI to drive most of the code that I'm writing."* — on the AI shift in how he codes.
- *"This is a place where we are likely to change every line of code in this project."* — definition of "experimental" for Reactor.
- **Phase 3 → Phase 4** open-source milestones (public tests → team working almost exclusively in the public repo).
- Demo constants: **range to 100** items, **8 characters** of a GUID per item, **margin 24 / margin 8 / column gap 4**, **first 5** pie slices, async **2-second delay** with **~20% random failure**, label offset **`15 * count`**.
- *"Please pick up WinUI, go build something with it… and then the last thing is, let's go try out Reactor. Give us feedback."* — the closing two-part call to action.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the **Microsoft UI Reactor** repo, build the sample app with `dotnet watch`, and try `useState`/`useReducer`, ListView keying, the pie chart, and async `resource` + `.match`.
  - Enable the built-in **dev tools** ("highlight reconciler changes") to see the diffing reconciler in action on a real list.
  - Grab the **public WinUI Git repo**, compile it, and run the public test suite (now possible post-Phase 3); watch for **WinAppSDK** experimental/preview builds with the memory + system-compositor wins.
  - Prototype a **C#-first** WinUI screen to feel where XAML is still required vs. where C# now reaches parity.
- [ ] Questions:
  - What's the timeline/branch for the **system compositor** + memory improvements reaching a stable WinAppSDK release?
  - Will the **DataGrid/charting** controls ship XAML-first, C#-first, or both — and on what schedule?
  - How stable will the Reactor **syntax** be given the collaboration with the C# team, and what's the bar for an idea to "graduate" into core WinUI?
  - What's the concrete plan/timeline for **WPF ↔ WinUI** mix-and-match parity and bulletproof **WinForms** interop?
- [ ] Relevant to:
  - Anyone building or maintaining **Windows desktop apps** (WinUI/WPF/WinForms) and weighing migration or incremental adoption.
  - Teams interested in **functional/reactive UI** (React/SwiftUI/Compose-style) but on the Windows/.NET stack.
  - **AI-assisted / code-first** desktop development workflows with Copilot/Claude Code + VS Code.

## 🔗 Related
- [[ODSP929 - Build modern NET apps with Uno Platform AI and visual tools]] — another C#/.NET path to building cross-platform Windows UI; complementary take on modern app dev with AI + visual tools.
- [[OD803 - Taking your AI to the edge with NET MAUI]] — the other Microsoft .NET UI framework; useful contrast to WinUI's Windows-native focus.
- [[OD806 - NET 11 in depth]] — the .NET runtime/language backdrop for C#-first WinUI development.
- [[OD805 - AI Building Blocks for NET Add intelligence to your C sharp apps]] — adding AI to C# apps, pairing with the AI-assisted workflow theme here.
- [[BRK220 - Using AI tools to teach old apps new tricks]] — modernizing/migrating existing (often desktop) apps with AI, relevant to the WinForms/WPF migration story.
- [[BRK203 - From CLI to PR]] — the CLI/agentic coding workflow (Copilot/Claude Code) that underpins the "code-first" shift Chris describes.
- [[BRK207 - GitHub Copilot in Visual Studio Agents That Debug Profile Test]] — AI-assisted coding/debugging in the Microsoft toolchain, reinforcing the AI-shift framing.
- Source list: [[2026 Build Session List]]
