---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/tooling
  - topic/devtools
  - topic/dotnetup
source: https://www.youtube.com/watch?v=ZMnyohA5yrw
session_code: OD804
event: Microsoft Build 2026
speakers: Chet Husk (.NET SDK team, Microsoft — GitHub @baronfel)
duration_min: 48
aliases:
  - Simplifying NET Installs with dotnetup
---

# OD804 — Simplifying .NET Installs with dotnetup

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Chet Husk — Software Engineer on the .NET SDK team, Microsoft (GitHub @baronfel)  
> **Duration:** ~48 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ZMnyohA5yrw)

## 🎯 TL;DR
Microsoft is building **`dotnet-up`** (a.k.a. ".NET up") — a single, cross-platform, native-AOT CLI that installs and manages the .NET SDK and runtimes consistently on every OS, without requiring admin/root elevation. It targets the "everyone who isn't using Visual Studio on Windows" crowd, who today face a fragmented mess of IDE installers, package managers, install scripts, and community version managers (DNVM, mise, asdf). `dotnet-up` reads `global.json` to install the exact SDK a repo needs, can install **runtimes independently of SDKs** (so you can multi-target tests without downloading multiple full SDKs), and keeps a signed, auditable manifest of everything installed so a single `dotnet-up update` keeps you patched and prunes stale versions. Everything shown is **internal-preview / "under construction"**; the roadmap runs internal preview → public preview (before end of summer) → GA, with a long-term vision of componentizing the SDK (rust-up style) and powering CI/CD actions. It's a **developer-time tool only** — production deployments should still use package managers or self-contained bundles.

## 🔑 Key Takeaways
- **The core problem: .NET installation is wildly heterogeneous.** You're either on Visual Studio/Windows (tool chain managed for you) or you're "everyone else," juggling IDE installers, package managers (winget, Homebrew, distro repos), install scripts, and community version managers — each with different trade-offs.
- **`dotnet-up` is one tool that behaves identically on every platform** (Windows, macOS, Linux), built with **native AOT** so it's fast and lightweight and "gets out of your way."
- **"Global" means *user*-global, not *system*-global.** Installs land in your user/home directory and never require elevation — no sudo, no admin.
- **It reads `global.json`** to determine which SDK version a repo wants (including roll-forward policies like `latestFeature` / `latestPatch`) and installs exactly that — `dotnet-up install` or `dotnet-up sdk install` is the one command you need after cloning.
- **Runtimes can be installed independently of SDKs.** `dotnet-up runtime install 8.0 9.0 10.0` grabs just the runtimes you need to *run* multi-targeted tests, instead of installing several hundred-MB full SDKs in parallel (the common CI/CD workaround).
- **Component-at-version syntax** is emerging: `dotnet-up runtime install ASP.NET Core@8.0`, also `.NET Runtime`, `Windows Desktop` (Windows only), etc.
- **It keeps a signed manifest / "lock file" of desired state** in a user data directory — `dotnet-up list` shows what's installed *and why* (which channel or which `global.json` requested it).
- **`dotnet-up update` keeps everything current** across tracked channels, and — uniquely for SDK management — **uninstalls/prunes** versions no longer needed by your declared requirements. Manual uninstall is also supported.
- **Provenance & supply-chain safety are first-class:** the team is working with the .NET Releases teams to **sign all binaries and manifests** so you can trust the bits are what Microsoft intended.
- **Designed for two consumers: humans *and* agents** (LLM/AI agents *and* CI/CD systems, which are "agents" too). Agents work best without admin rights in sandboxes, so the no-elevation/user-directory model fits naturally and provides guardrails against agents "unzipping a zip" the wrong way.
- **Telemetry** is collected like the .NET CLI, and the **same telemetry opt-out flags** from the .NET CLI apply.
- **Acquisition is a one-liner:** `aka.ms` links provide a shell script (curl → sh) or PowerShell (`Invoke-WebRequest` → `Invoke-Expression`); first run walks you through an **`init`** configuration wizard (pick channel, choose "terminal mode," it edits your shell profile and adds itself + `dotnet` to PATH).
- **Roadmap:** internal preview (manage stable + daily/nightly SDKs, one-shot A/B execution) → public preview before end of summer (self-update, update notifications, full signature verification, published agent skills) → GA (fit & finish, official docs, `global.json`-managed runtimes).
- **It ships "out of band"** — not tied to the quarterly .NET SDK release cadence — so gates are driven by feature-readiness *and* user feedback.
- **Explicitly NOT for production.** Use package managers (for system-wide security updates) or self-contained bundles in prod; `dotnet-up` is a developer-time convenience tool.
- **Try it & give feedback now:** docs at `aka.ms/dotnet-up/docs`, feedback at `aka.ms/dotnet-up/feedback` (a dedicated discussion category on the .NET SDK repo), and a samples repo at `github.com/baronfel/dotnet-up-repo-patterns-demo`.

## 📚 Detailed Notes

### Why this exists — the installation problem
Chet frames the problem by splitting all .NET users into two buckets:
1. **Visual Studio on Windows users** — Visual Studio manages the tool chain, updates on a frequent cadence, and delivers all the feature-band and servicing/bug-fix updates automatically.
2. **Everyone else** — and *this* is the group the team wants to help.

Installing .NET off the VS-on-Windows happy path is, in his words, a "very heterogeneous situation." He categorizes the existing mechanisms into three buckets:

- **IDE-based distribution** — Visual Studio (Windows); Visual Studio Code (cross-platform), where his team owns the **C#/.NET VS Code extension** whose job is to fetch the SDK versions a project and its tools need.
- **Package-manager-based distribution** — `winget`, **Homebrew** (macOS/Linux), and Linux distro package managers. These use the system's native package capabilities to acquire .NET. Big upside: **centralized management** (one place to update everything, including across system-wide security updates).
- **Manual distribution** — the .NET website (**get.dot.net**, "one of my favorite things to say"), the official **install scripts** (PowerShell + POSIX shells) for managing CLI/SDK installs, and a whole ecosystem of **version managers**: the community **DNVM** (".NET Version Manager"), plus pluggable/extensible managers like **mise (mise-en-place)** and **asdf**.

A crucial caveat: **many of these mechanisms are community-owned, not Microsoft-operated** (he flags them with asterisks on his slide). Some use OS packages under the hood, some use plain zips/tarballs, and some — like Homebrew — can use either depending on your preference.

### Linux makes it even messier
Linux adds the same three categories *plus* a long, tangled history: sometimes **Microsoft** provided packages for your package manager, sometimes your **distro** did, sometimes **both** existed simultaneously. That produces a decision tree just to install .NET, forcing you to weigh:
- **Feature bands:** the .NET SDK ships **four times a year**, and each quarterly shipment contains net-new features and enhancements. Distro package managers often give you centralized updates but may **restrict which feature bands** you can get.
- **Per-repo version needs:** if different repos need different SDK versions, package managers may not fit at all.

As soon as you look at the real needs of individual repos or developers, the package-manager "happy path" breaks down, and people fall back to local management (install scripts, DNVM, mise, etc.). Those tools work, but they have gaps:
- **No central management** — you can't easily see what SDKs/tool chains are installed *where* on your system.
- **No easy update** — no simple way to update one install, or all installs at once.
- **Clashes** — local installs frequently conflict with global/system-level installs. (And this is true on every platform, not just Linux.)

There's also **pain on Microsoft's side**: when users hit bugs or gaps, it's hard for the team to categorize *how* the install happened and even to **validate the install is correct** in the first place. So both ends suffer.

### The plan — "make another one" (the xkcd joke)
Chet leans into the famous **xkcd #927 "Standards"** comic by Randall Munroe ("there are 14 competing standards… let's make one universal one… now there are 15"). He's "only half joking": the plan is a brand-new install mechanism, but one designed deliberately to subsume the others. Design principles:

- **Identical behavior on every platform.**
- **Lean into user-global installs that require no elevation.** Scoped to your user/home directory (or a location you control), never impacting other users.
- **Fast & lightweight via native AOT** so it executes quickly and stays out of the way.
- **Leverage existing description mechanisms** — today that's **`global.json`**. Long term, they hope a shared way of interacting with SDK installs could let them **evolve `global.json`'s format/purpose** into something more ergonomic.
- **Close the feature gaps** that system-level installs enjoy but user-level installs lack — chiefly **central management and auditability**, which package managers and VS-style installers bake in but current user-level installs don't.
- **Provenance/signing:** working with the .NET Releases teams to **sign all binaries and all manifests**, end to end, so you know the bits are exactly what Microsoft intended to deliver.
- **A library, not just a CLI.** They're building `dotnet-up` *and* a library around it so other tools that need to install/interact with .NET installs can do it "correctly and safely." The long-term hope: the manifests and bookkeeping become a **shared resource for a constellation of tools** — think **Dependabot** and **Renovate** and the broader auditability/automated-compliance infrastructure developers already use for package references and Dockerfile references. `dotnet-up` wants to fit into and plug into that world.

He's emphatic that **everything from here is internal-preview level** — a "big giant under construction label," joking about the early-2000s blinking marquee "under construction" GIF. The point of showing it now is to convey the vision and **gather early feedback** (earlier feedback → better end product).

### Demo overview
Three things to demo:
1. **Acquisition & initialization** of `dotnet-up` on a system.
2. Using it to **get started in different repo shapes** quickly.
3. Using it to tackle **one of the more annoying tool-chain problems** (multi-runtime testing).

He works from a **scenarios repo** containing three example repository patterns:
- a **cross-platform web app**,
- a **multi-runtime testing application**, and
- an app with **up-to-date vs outdated SDK installs**.

### Demo 1 — Acquisition & `init`
- **Get it via `aka.ms` links** → a shell or PowerShell script (docs will have examples for both). Running the script **detects your platform** and downloads the correct **AOT, platform-specific** `dotnet-up` build, **verifies** it, and installs it into your **home directory by default** (you have 100% control over the location).
- PATH isn't auto-configured by the sourced script (hard to do reliably when you `source` a script on Linux), so the first invocation is manual.
- **`dotnet-up init`** runs a **configuration walk-through** the first time (or whenever you run `init`):
  - **Telemetry notice:** like the .NET CLI, `dotnet-up` collects usage telemetry; the **same opt-out flags** from the .NET CLI control it.
  - **Channel prompt:** which channel(s) to track. Chet, "a bleeding-edge person," chooses **`latest`** → installs the latest stable release today and **stays up to date over time**.
  - **Usage-mode prompt:** how you'd like to use it. The option closest to DNVM/mise expectations is **terminal mode**, which configures `dotnet-up` to **add itself to PATH** and add the **managed .NET install location** to PATH.
  - It **detected pre-existing global installs and offered to port them over** to the new managed world (he skipped that step).
- It then **downloaded the latest SDK**, installed it into its managed location, showed nice download/install **UI/UX**, and **edited the shell profile** (it detected **zsh**) so future shells get the needed env vars + PATH entries to run `dotnet-up` and `dotnet`.
- After a new shell session: **`dotnet-up info`** shows the `dotnet-up` version; **`dotnet --info`** (first run does some "crunching") confirms the install: **SDK 10.0.300**, on **macOS**, installed to the `dotnet-up`-managed location, including the **ASP.NET Core** and **.NET Core** runtimes — "exactly what anyone coming to .NET would need," achieved with just `dotnet-up init`.

### Demo 2 — `global.json`-driven SDK install (cross-platform web app)
- The web app is simple: a **library** + a **web app** that consumes it, plus a **`global.json`**.
- That `global.json` pins **SDK 10.0.100** (different from the 10.0.300 just installed) but allows **rolling forward to the latest feature band**. ("Why? I don't know — that's what the developer chose.")
- `dotnet-up sdk install` **understands `global.json`** and **rolled forward to the latest feature band** as the policy requested.
- He then edits `global.json` to **`latestPatch`** instead, reruns install, and `dotnet-up` now installs a **`1xx`-feature-band** SDK (the 100 band) — and **tells you *why*** (because the project's `global.json` specifies that version). The download/install of the new SDK is shown.
- Building/running the web app now "just works" — it uses the SDK you told it to. **One command** (`dotnet-up install` / `dotnet-up sdk install`) and you're good. He proves the **108 SDK** is the one in use.
- **Core value proposition:** clone any repo → `dotnet-up install` → get a `dotnet` SDK that works for that repo. Today, while CI helpers like **GitHub Actions `actions/setup-dotnet`** honor `global.json`, **nothing supported existed for *local* developer machines or for an *agent* acting on your behalf.** `dotnet-up` fills that gap in a supported way.

### `dotnet-up list` — tracking decisions and *why*
- `dotnet-up list` shows it's **tracking the decisions you made and the reasons**:
  - **2 SDK versions** installed.
  - Tracking the **`latest` channel** (because he explicitly chose it at startup).
  - Tracking the **`1xx` channel** (because the web app's `global.json` told it to).
- Because it tracks channels, **future releases are handled automatically**: when **10.0.109** ships in June, **10.0.110** in July, etc. (he notes 108 was May), a single **`dotnet-up update`** applies them.
- The real beauty: it's **not just installation** — it understands **what you need, what you have, and what's available**, and keeps them aligned. This directly solves the "clone a repo, run a normal `dotnet build`, and the SDK you have doesn't match the repo" problem — "solved definitively."

### Demo 3 — Installing runtimes independently (multi-runtime testing)
This is the demo Chet thinks best shows the future direction.

- **Setup:** a workspace with a **source library** (a "truncation string helper" + a helper that checks whether a string is **alphanumeric ASCII only**) and a **test project** that consumes it, with a set of test cases.
- **Multi-targeting motivation:** library authors often specialize per target framework. Example: on **.NET 10** there may be a new **span-based `IndexOf(string)` overload** you want to use that isn't available on **.NET 8**, so you add an `#if` to take a different code path on 10 vs 8 — while still building for 8 so 8 users can consume the library. This is **multi-targeting**.
- His **library targets `.NET Standard 2.0`** (no per-runtime specialization needed), but to ensure consumers on the latest/greatest .NET work, you write **tests that target multiple in-support runtimes** — here **.NET 8, 9, and 10**.
- **The pain point:** he wants to use the **latest *SDK*** (10) because that's where all the tooling features come from, regardless of which *runtime* he's building for. So he ends up with **one SDK but needing multiple runtimes** to actually run the tests.
- **`dotnet --list-runtimes`** shows only the **10** runtime installed. Running `dotnet test` against the 8/9/10-targeted tests finishes instantly but **fails to run** on 8 and 9: **"no tests ran"** because there was **no .NET Core runtime for 8** and **none for 9**; only **.NET 10 tests ran and passed**.
- **The common (wasteful) fix:** in CI/CD, people install **entirely parallel full SDKs** — an 8 SDK, a 9 SDK, and one or more 10 SDKs. Chet argues that's unnecessary because **new SDKs include new tooling and fully support building older runtimes**. You only need the *runtimes* to run the app.
- **`dotnet-up`'s answer — install runtimes directly.** He shows a **fake/hypothetical `global.json` extension** declaring needed runtimes (".NET runtime, versions 8, 9, 10") — **syntax is *not* final**, just a glimpse. In a future world `dotnet-up install` would read that and install both SDKs and runtimes for you. **Not available today.**
- **What works today:** `dotnet-up runtime install 8.0 9.0 10.0` installs **all three at once**, finding the **latest of each band**, downloading and installing them. You can also pin **specific versions** if needed.
- After installing the runtimes, **the tests run and pass** — **without installing multiple hundred-MB SDKs**. "The best of both worlds": latest tooling + the ability to do what you need. It brings **CI/CD-style convenience to local development.**
- **Other runtime components** use the **`component@version`** pattern: e.g. `dotnet-up runtime install ASP.NET Core@8.0`; also `Windows Desktop` (on Windows). This `component name @ version` pattern has been "fleshed out over a few SDK releases."
- After installing ASP.NET Core, `dotnet --list-runtimes` shows **.NET Core runtimes for 8, 9, 10** and **ASP.NET Core runtimes for 8 and 10**.

### Maintenance, updates & uninstall — "the long tail"
- Getting tooling is "only half the battle"; there's a **long tail of maintenance and upgrades** responsible teams must follow.
- **`dotnet-up list`** also tracks the **explicit runtimes** you requested — you can see what's **installed** and what was **requested**.
- When new runtime versions release, **`dotnet-up update`** covers them too. (His were already current since he'd just installed them; otherwise update would install them right there.)
- Under the covers, `dotnet-up` keeps a **manifest / installation tracker** in a **data directory in your user directory** — think of it as a **lock file for the *declared/desired state* of your system**. It's **not** intended to be shared across repos/developers (use `global.json` for shared dev requirements); the manifest is what powers the update intelligence.
- **`dotnet-up print-init-script`** is a helper that ensures your shell is configured to natively use `dotnet-up` (it's what `init` uses). Currently supported for **bash, zsh, and other POSIX shells**; **PowerShell support is in PR** and expected to land "within a week or two" of the video.
- **Uninstallation** — long missing from SDK management. After updates, old SDKs/runtimes may no longer be needed; **`update` removes out-of-date installs** no longer required by your declared requirements. You can also **manually uninstall** SDKs/runtimes.
- **Command architecture:** there are **top-level** `install` / `update` / `uninstall` commands **and component-level** ones (`dotnet-up sdk install`, `dotnet-up sdk update`, `dotnet-up runtime install`, …). This reflects a vision of **thinking about the entire .NET tool chain as *components*.**

### The component vision (rust-up parallel)
- Today the clean component lines are **SDKs** and **runtimes**, but **features/functionality within the SDK** might make sense as **discrete components**.
- For those familiar with **`rust-up`**, this is where it's heading: a world where **pieces of the SDK release at different cadences**, and instead of drowning in many update notifications and being unable to control the rate of change, a developer uses **one tool (`dotnet-up`) and one command** to manage all updates and components.

### Who it's for — humans *and* agents
Two primary consumers:
- **Humans (developers specifically).** Expectations from other ecosystems should carry over. Goal: **no new concepts to learn** — clone a repo, `dotnet-up install`, done, on **any OS**.
- **Agents — both AI/LLM agents *and* CI/CD systems** (which are "agents" in their own right; really "humans + automated use cases").

For agents specifically:
- Their expectations come from **training data + the skills/context they're given**, so the tool should **look/feel like other tools** but adapt to .NET's specifics.
- Agents can easily **"get half the story" from docs and unzip a zip the wrong way**, harming your dev experience. `dotnet-up` provides **guardrails** that ad-hoc download/execution can't.
- Agents work best **without admin rights, in sandboxes with guardrails** — which is exactly why a **no-elevation, user-directory** tool fits naturally.
- Both categories need to **stay current** (security fixes, tooling enhancements) and **express constraints semantically**: "give me the latest stable," or "keep me on the latest 10 series." `dotnet-up` lets you express those constraints and **respect them locally**, the same way CI/CD tooling respects them today.

### Explicitly a developer-time tool (NOT production)
- For **production**, keep using your **package manager** (to get framework-dependent runtimes *and* system-wide security updates as soon as available) or **bundle self-contained** if that's your deployment model. (Self-contained means you must be "on the ball every month" for security releases.)
- `dotnet-up` is about **developer-time use cases for humans (and agents)** — *not* production.

### The roadmap (milestone by milestone)

**Internal preview** (aiming for the next couple of weeks) — *try the bleeding edge & give fast feedback*:
- **Manage stable SDKs** (shown today) plus **daily/nightly SDKs** (a PR is in the pipeline). Context: monthly previews of the next major version are treated as "stable" from a release-management perspective (e.g. **.NET 11 Preview 5** is in progress; Preview 4 was just out). *Separately*, **every build in the .NET unified build system produces a usable SDK**, which can carry bug fixes or new functionality the team wants fast feedback on. Internal preview will let you say (in `global.json` or on the CLI) "give me the 11 nightlies / the hot 11 builds" and try them easily.
- **One-shot execution** for **A/B comparison**: a planned command `dotnet-up dotnet` that runs a given command against a *specific* .NET version without touching your global install. Example: validate that `dotnet build` behaves the same on **10.0.300** as on **11 Preview 5** — useful for spotting MSBuild **terminal-logger** UX changes, SDK targets behavioral changes, or trying a CLI bug fix. Lets you do ad-hoc fixes and give even faster feedback.

**Public preview** (ideally **before the end of summer**) — *helping you stay compliant*:
- **`dotnet-up` self-update** — once installed, it takes control of its own updating (with appropriate signing/validation). Compared to the **Aspire CLI**'s self-update, which has proven useful in practice.
- **Update checks & notifications** — like **Oh My Posh / Oh My Zsh**, which check once a day/week for new versions on terminal startup. `dotnet-up` would do this for **itself *and* your installed SDKs**, so you hear about security/feature updates and can hop on quickly.
- **Full signature verification** of all stable releases — of the **.NET SDK and runtime tooling** *and* `dotnet-up` itself — for the provenance/supply-chain confidence mentioned earlier.
- **Agent skills published to the `dotnet/skills` repo**, so people using LLMs for automated updates or A/B testing get good, ready-made ways to use `dotnet-up` without authoring their own skills.

**GA** — *fit & finish*:
- Polish of the tool itself, **official docs on the .NET website**, and `dotnet-up` listed/supported as an **official install method** on the .NET website.
- **Expanding `global.json` to manage runtimes** (the hypothetical syntax shown in Demo 3 becomes real).

**Far future / vision:**
- `dotnet-up` as a **vehicle to radically change how the SDK ships** and enable **faster updates of all tooling**. With AI/LLMs exploding, there's pressure to **release earlier, more often, more incrementally**; you manage risk via **broad testing + fast rollout** so you can react quickly to problems. The team wants that for the **entire .NET tool chain**, and `dotnet-up` can help **accelerate delivery** and **factor the SDK into components** that update more rapidly.
- **CI/CD integration:** today **`actions/setup-dotnet`** (GitHub Actions) and **`UseDotNet@2`** (Azure DevOps) are great but their features **subtly differ** and they may not invest equally in **caching/performance**. The hope is to use `dotnet-up` as the **implementation** of those tools to bring **consistency of experience** and a **single place** to improve performance across environments.

**Cadence note:** `dotnet-up` is **not locked to the .NET SDK ship cycle** — it ships **"out of band."** So milestone gates depend on both **feature/functionality readiness** and **user feedback** about quality/usefulness. The more feedback (even on internal nightly bits), the better.

### Call to action
- **Get `dotnet-up`** via the `aka.ms` links; start at the **docs** link, which gives the exact copy-paste snippet (shell: `curl … | sh`; PowerShell: `Invoke-WebRequest … | Invoke-Expression`).
- **Read the design spec** (created several months ago, iterated on as features are added).
- **Give feedback** at the feedback link → a dedicated `dotnet-up` category on the **.NET SDK repo discussion board**, monitored by Chet and the team.
- **Clone the samples repo** (`github.com/baronfel/dotnet-up-repo-patterns-demo`) — it has everything from the demo plus **GitHub Actions** that auto-wire `dotnet-up`. Try it on the samples and on your own repos; let them know if it flows well, performs well, and has the features you want.

## 🛠️ Products / Features / Technologies Mentioned
- **`dotnet-up` / ".NET up"** — the new cross-platform, native-AOT CLI (and accompanying library) for installing/managing the .NET SDK and runtimes at the *user* level without elevation. The whole subject of the talk.
- **.NET SDK** — the developer tool chain; ships **4×/year** in quarterly feature bands; where all tooling features come from. New SDKs support building older runtimes.
- **.NET runtimes** — **.NET Core**, **ASP.NET Core**, **Windows Desktop** (Windows-only) — installable independently of the SDK via `dotnet-up`.
- **`global.json`** — the existing file `dotnet-up` reads to determine required SDK version + roll-forward policy (`latestFeature`, `latestPatch`, etc.); future plans may extend it to declare runtimes.
- **Visual Studio** — Windows IDE that manages the .NET tool chain for you (the "bucket 1" experience).
- **Visual Studio Code + the C#/.NET extension** — cross-platform; the speaker's team owns the extension that fetches SDK versions projects/tools need.
- **Package managers:** **winget**, **Homebrew** (macOS/Linux), **Linux distro package managers** — centralized but with feature-band/per-repo limitations; recommended for **production**.
- **Install scripts** — official PowerShell + POSIX shell scripts for CLI/SDK installs (from get.dot.net).
- **DNVM (.NET Version Manager)** — community version manager.
- **mise (mise-en-place)** & **asdf** — pluggable/extensible multi-tool version managers.
- **get.dot.net** — the .NET download website.
- **Native AOT** — used to compile `dotnet-up` into a fast, platform-specific binary.
- **`rust-up`** — the Rust toolchain manager; the conceptual model for `dotnet-up`'s component/cadence vision.
- **Dependabot & Renovate** — dependency-update/compliance tools the team hopes `dotnet-up`'s signed manifests can plug into.
- **GitHub Actions `actions/setup-dotnet`** — CI action that honors `global.json` (the inspiration for the missing *local* equivalent).
- **Azure DevOps `UseDotNet@2`** (`use-dotnet`) — the Azure DevOps equivalent install task.
- **Aspire CLI** — cited as a good example of a self-updating CLI.
- **Oh My Posh / Oh My Zsh** — terminal-prompt tools cited as the model for periodic update-check notifications.
- **`dotnet/skills` repo** — where `dotnet-up` agent skills will be published.
- **MSBuild terminal logger** — example of a UX surface that one-shot A/B execution helps you compare across versions.
- **xkcd #927 "Standards"** (Randall Munroe) — the comic used to self-deprecatingly justify building "another" install mechanism.

#### Key `dotnet-up` commands seen
- `dotnet-up init` — first-run config wizard (channel, mode, PATH/profile setup, optional port of existing global installs).
- `dotnet-up info` / `dotnet --info` / `dotnet --list-runtimes` — inspect `dotnet-up` and installed SDKs/runtimes.
- `dotnet-up install` / `dotnet-up sdk install` — install the SDK a repo's `global.json` requires.
- `dotnet-up runtime install 8.0 9.0 10.0` — install runtimes directly (parallel); supports `Component@Version`, e.g. `ASP.NET Core@8.0`.
- `dotnet-up list` — show installed SDKs/runtimes, tracked channels, and the *reason* each is tracked.
- `dotnet-up update` — update tracked channels/components and prune stale versions.
- `dotnet-up uninstall` — manual removal; also component-level `dotnet-up sdk install|update`, etc.
- `dotnet-up print-init-script` — emit the shell-config snippet (bash/zsh/POSIX today; PowerShell in PR).
- `dotnet-up dotnet <cmd> <version>` — *planned* one-shot execution for A/B testing without touching the global install.

## 🚀 Announcements / What's New
- **`dotnet-up` (".NET up") unveiled** as a new, supported, cross-platform, no-elevation install/management tool for the .NET SDK + runtimes — currently **internal-preview / "under construction."** This is the headline of the session.
- **Roadmap with timelines stated:** **internal preview in the next couple of weeks**; **public preview ideally before the end of summer**; **GA** later (no firm date).
- **PowerShell support for the init/print-init-script flow** is **in PR**, expected to land **within ~1–2 weeks** of the video — at which point viewers can grab `dotnet-up` and try it.
- **Daily/nightly SDK management** via `dotnet-up` is **in PR** (internal-preview target).
- Planned-but-not-yet-shipped: **`global.json`-declared runtimes**, **one-shot A/B execution (`dotnet-up dotnet`)**, **`dotnet-up` self-update**, **update notifications**, **full signature verification of stable releases**, **published agent skills (`dotnet/skills`)**, and **using `dotnet-up` to back `actions/setup-dotnet` / `UseDotNet@2`**.
- Status framing: stable-SDK management was **demoed working**; runtime install **works today**; the `global.json` runtime-declaration syntax is **explicitly not final / hypothetical**.

## 💡 Demos
- **Demo 1 — Acquisition + `dotnet-up init` on macOS.** Showed the script downloading the correct AOT build, the init wizard (telemetry notice, channel = `latest`, terminal mode, offer to port existing global installs), shell-profile editing for zsh, and verification via `dotnet-up info` + `dotnet --info` → **SDK 10.0.300** with ASP.NET Core + .NET Core runtimes. *Proved:* getting a working .NET from scratch is one `init` away on any platform, no elevation.
- **Demo 2 — `global.json`-driven SDK install (cross-platform web app).** `global.json` pinned 10.0.100 with roll-forward; `dotnet-up sdk install` rolled forward to the latest feature band, then (after editing to `latestPatch`) installed the `1xx`/100-band SDK and **explained why** (the project's `global.json`). Built the app on the **108 SDK**. *Proved:* one command makes any cloned repo build with the exact SDK it declares — and it's transparent about the reasoning. `dotnet-up list` then showed both SDKs and the tracked `latest` + `1xx` channels with reasons.
- **Demo 3 — Independent runtime installs for multi-runtime testing.** A `.NET Standard 2.0` library + a test project multi-targeting **.NET 8/9/10**. With only the 10 runtime present, `dotnet test` reported **"no tests ran"** on 8 and 9 (missing runtimes) and passed only on 10. After `dotnet-up runtime install 8.0 9.0 10.0` (and `ASP.NET Core@8.0`), `dotnet --list-runtimes` showed Core 8/9/10 + ASP.NET Core 8/10, and **all tests passed** — **without** installing multiple full SDKs. *Proved:* you can stay on the latest SDK yet run older-runtime tests cheaply, bringing CI/CD-style convenience to local dev. Also showed a **hypothetical `global.json` runtime-declaration** syntax (explicitly not final).

## 📊 Notable Stats / Quotes
- **"You are either using Visual Studio on Windows… or you're everyone else. And that's exactly the problem that we'd like to solve."** — the framing of the whole talk.
- **"There's all these different installation mechanisms and we discovered we would make another one… and I'm only half joking here."** — the xkcd #927 self-deprecating premise.
- **The .NET SDK ships 4× a year**, each quarterly shipment containing net-new features/enhancements.
- **Release cadence example:** 10.0.**108** in May, **109** in June, **110** in July — handled automatically by `dotnet-up update`.
- **SDKs are "hundreds of megabytes a piece"** — the cost the runtime-only approach avoids.
- **"That problem we can say is solved definitively."** — on SDK/version mismatch after cloning a repo.
- **"This to me is the best of both worlds. You're on the latest tooling, but you're able to do the things that you need to do in ways that you couldn't before easily."** — on independent runtime installs.
- **"When we say global, we don't mean system global. We mean user global."** — the no-elevation design principle.
- **"Production is not what we're talking about with this tool — we're talking about developer-time use cases."**
- **.NET 11 Preview 5** in progress at the time of recording (Preview 4 just released).
- **Timelines:** internal preview "in the next couple weeks"; public preview "before the end of the summer ideally."
- **Key links:** `aka.ms/dotnet-up/docs`, `aka.ms/dotnet-up/feedback`, `github.com/baronfel/dotnet-up-repo-patterns-demo`.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Grab `dotnet-up` from `aka.ms/dotnet-up/docs` once PowerShell support lands; run `dotnet-up init` on a dev box.
  - Clone `github.com/baronfel/dotnet-up-repo-patterns-demo` and walk the three scenarios (web app, multi-runtime tests, outdated installs).
  - Replace per-repo `global.json` SDK juggling with `dotnet-up install` on a real project.
  - Try `dotnet-up runtime install 8.0 9.0 10.0` to multi-target tests *without* installing extra full SDKs (potential CI cost/time savings).
  - Test `dotnet-up update` + auto-prune behavior; inspect the manifest/lock file in the user data dir.
- [ ] Questions:
  - Where exactly does the manifest/data dir live per-OS, and what's its format (sharable for compliance tooling)?
  - How does PATH precedence interact with an existing system/Homebrew `dotnet`? Conflict handling when porting existing global installs?
  - Will the eventual `global.json` runtime syntax be standardized so `actions/setup-dotnet` / `UseDotNet@2` honor it too?
  - What's the signature-verification UX/failure mode if a manifest or binary fails validation?
  - Telemetry: which exact `.NET CLI` opt-out env vars/flags apply (e.g. `DOTNET_CLI_TELEMETRY_OPTOUT`)?
- [ ] Relevant to:
  - Cross-platform .NET dev environments (macOS/Linux) and onboarding scripts.
  - CI/CD pipeline simplification & caching strategy (GitHub Actions / Azure DevOps).
  - AI/agent-driven dev workflows needing safe, no-elevation toolchain setup.
  - Dependabot/Renovate-style supply-chain & compliance automation for .NET tooling.

## 🔗 Related
- [[2026 Build Session List]]
- 