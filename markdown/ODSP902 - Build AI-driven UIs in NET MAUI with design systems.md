---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet-maui
  - topic/design-systems
  - topic/ai
source: https://www.youtube.com/watch?v=htZlWar7dkM
session_code: ODSP902
event: Microsoft Build 2026
speakers: Vishnu Menon (Senior Product Manager, Syncfusion)
duration_min: 10
aliases:
  - Build AI-driven UIs in .NET MAUI with design systems
---

# ODSP902 — Build AI-driven UIs in .NET MAUI with design systems

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Vishnu Menon — Senior Product Manager, Syncfusion  
> **Duration:** ~10 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=htZlWar7dkM)

## 🎯 TL;DR
This Syncfusion-led lightning session tackles a common pain: AI can scaffold a .NET MAUI UI in seconds, but the result is unpolished, inconsistent, and not production-ready because the AI has no knowledge of *your* application's design context. Vishnu Menon argues the fix is two complementary pieces — a **design system** (the source of truth for what good UI looks like: colors, typography, spacing, reusable components) and **AI skills** (structured Markdown instruction files that constrain *how* the AI makes UI decisions). By feeding the agent both a design system and control-specific skills (e.g. Syncfusion's `.NET MAUI` control skills plus a custom `design-system` skill), the same prompt that previously produced a sloppy dashboard instead generates a consistent, design-system-compliant employee dashboard. The thesis: *"We are not asking AI to design UI. We are teaching it how we design UI."*

## 🔑 Key Takeaways
- AI generates UIs fast, but those UIs are typically **not polished or production-ready** — they need manual rework.
- The root cause is missing context: AI **lacks the design system and design context** of your specific application (its spacing rules, component patterns, design standards).
- AI also has **limited/imperfect knowledge of UI controls** — it mixes and matches controls and APIs that don't belong together, producing a **guess-based implementation**.
- "AI is powerful, but without the right inputs and constraints, it can only guess, not design with intention."
- The solution rests on **two key ideas: a design system + skills.**
- A **design system** keeps the UI consistent across the whole app: colors, typography, spacing, reusable components, layout patterns, and guidelines.
- In .NET MAUI, a basic design system already exists in `Resources/Styles/Styles.xaml` (per-control styles) and `Colors.xaml` (shared color tokens like a primary color) — define a button's `FontFamily` once (e.g. Open Sans Regular) and it applies everywhere across platforms.
- A design system **reduces repeated hard-coding of values** and **eliminates repeated UI decisions**, enabling faster development — especially in enterprise apps where the UX team designs new features to match the existing system.
- A **skill** is a way to guide the AI to perform a task using **structured instructions and rules**; skills aren't limited to UI/design — they're a general mechanism.
- Skills live in an **`.agent/skills/`** folder as a `skill.md` (a.k.a. `skills.md`) file describing the control, its use case, *when to use the skill*, getting-started steps, and references (e.g. a linked `troubleshooting.md`) the agent can read on demand.
- Crucially: **skills do not render UI — they constrain the decisions.** "A skill defines *how* the AI should behave; a design system defines *what* good UI looks like; design-system skills guide the AI to follow it."
- **Without skills**, the AI guesses what to generate; **with skills**, it has design tokens and layout rules, so it produces a more consistent UI.
- Syncfusion ships installable per-control skills for its .NET MAUI controls (copy a one-line command into the terminal to drop the skill files into `.agent/skills/`).
- The closing principle: **don't ask AI to design your UI — teach it how you design UI**, then let it apply that.

## 📚 Detailed Notes

### Session agenda
Vishnu Menon (Senior Product Manager, Syncfusion) frames the talk around building AI-driven UIs in .NET MAUI "not just faster, but in a more consistent and intelligent way" using a design system. The agenda he lays out:
1. Problems in UI building / why AI struggles with UI building.
2. The "golden standards" — the design system.
3. AI skills.
4. The AI-driven UI workflow.
5. A concluding demo.

### The problem — AI-generated UIs look fine but aren't production-ready
He opens in the IDE with a deliberately naïve baseline: he prompts the AI directly — *"Create a simple employee dashboard mobile application using .NET MAUI"* — with no extra guidance. The AI produces a working, colorful employee dashboard with a variety of controls. Functionally it works. But on closer inspection the cracks show:
- **Color issues on the "View Dashboard" button.**
- **Color issues in the card-like controls.**
- **Misaligned icons in the CollectionView.**

These are small but real defects that a developer would have to **manually rework**. The takeaway: AI can generate UIs very quickly, but they are **not polished, not production-ready** out of the box.

### Why this happens — no design context + shaky control knowledge
Two reinforcing reasons:
1. **No design context / design system.** The AI doesn't know your application's spacing rules, component patterns, or design standards. It has no notion of what "consistent" means *for your app*.
2. **Limited knowledge of UI controls.** The AI **mixes and matches controls** and **mixes and matches APIs** that aren't meant to go together.

The combined result is that, given only a prompt, the AI produces a **guess-based implementation** rather than an intentional design. Menon's framing of the core issue: *"AI is powerful, but without the right inputs and constraints, it can only guess, not design with intention."*

### The solution at a high level — design system + skills
Two key ideas solve it:
- **A design system** — the source of truth for what good UI looks like.
- **Skills** — the mechanism that makes the AI actually follow that source of truth.

### What a design system is
A design system is "a system that keeps your UI consistent throughout your application." It includes **colors, typography, spacing, reusable components, layout patterns, and guidelines.**

He grounds it in something every .NET MAUI developer already has. When you create a new .NET MAUI project, inside the **`Resources/Styles/` folder** there's a **`Styles.xaml`** file containing styles for the different controls — that's a basic, concrete example of a design system. For instance, a `Button` style can specify a `FontFamily` of **Open Sans Regular**; from then on, **wherever** you use a `Button` in the app, across different platforms, it picks up Open Sans Regular automatically. This is what keeps the UI looking standard across platforms and controls.

**`Colors.xaml`** serves the same purpose for color — e.g. define a **primary color** once and have it be consistent across all platforms.

Benefits he calls out:
- **Reduces repeated hard-coding** of values — define once, reuse everywhere.
- **Eliminates repeated UI decisions** — in an enterprise app with a proper design system, when you add a new feature the UI/UX team delivers designs that *match* the existing system; without one, every feature re-litigates the same UI choices.
- Net effect: **faster development.**

### What a skill is
A **skill** is "a way to guide the AI to perform a task using structured instructions and rules." Importantly, skills are **general-purpose** — this talk is about *design-system* skills, but skills can be used for many other use cases too.

He opens a sample project and shows a skill living under **`.agent/skills/`** — specifically a **"Syncfusion Mobile Button"** skill for the Syncfusion `.NET MAUI` Button control. The key file is **`skill.md`** (he refers to it as the `skills.md`/`skill.md` file), and it contains:
- **What the implementation / use case is.**
- **When to use the skill.**
- **Getting started** steps — the agent follows these when adding the control.
- **References** to additional files — e.g. a **`troubleshooting.md`** the agent can open if it hits a problem.

The mental model: the agent **reads `skill.md`** to learn how things work; if it runs into trouble while adding the control, it follows the references (e.g. into `troubleshooting.md`) for help.

### The key distinction — skills constrain decisions, they don't render UI
Menon's crisp summary of how the pieces relate:
- **Skills do NOT render UI — they constrain the decisions.**
- **A skill defines *how* the AI should behave.**
- **A design system defines *what* good UI looks like.**
- **Design-system skills guide the AI to follow the design system.**

### What skills change in practice — guessing vs. constrained generation
He contrasts the two paths explicitly:
- **Without a skill:** when you prompt, the AI **guesses** what to generate and returns a **guess-based UI**.
- **With a skill:** the AI has **design tokens, layout rules, and more understanding**, so it produces a **more consistent UI**.

### The demo — installing skills and regenerating the dashboard
For the demo, Menon uses **Syncfusion `.NET MAUI` controls** and their published skills:
1. **Install a control skill.** Syncfusion provides skills for its controls; you **copy a single line of code** (from a Syncfusion skills source/URL) into your **terminal**, and it copies all the skill files into the **`.agent/skills/`** folder. (He notes pressing a confirm key — heard as "slash Y" / `Y` — to accept the copy.) He installs skills for several controls for demo purposes, including the **Syncfusion Mobile Button** shown earlier.
2. **Add a design-system skill.** He reveals the skill folder in **Finder** and pastes in an additional **`design-system`** skill he prepared for the demo. This tells the AI **which design system to follow** for the generated UI.
3. **Run the prompt.** He pastes the prompt and lets the AI work, this time **with the skills present.**

**What the AI produced (with skills):**
- An **employee model**.
- **Design tokens** — created exactly as instructed by the **design-system skill**.
- An **employee dashboard page** (and associated page code).

When run, the result **looks very good**: the **design system is clearly followed** and **everything looks consistent** — a direct contrast to the unpolished baseline from the start of the talk.

### Conclusion — teach the AI how you design
Menon closes on the central principle: *"We are not asking AI to design UI. We are teaching it how we design UI."* Given the right design system and skills, the AI can design the UI for you to a consistent, production-quality standard. He points to a **QR code containing the GitHub link** for the demo sample and signs off with "Happy coding with AI."

## 🛠️ Products / Features / Technologies Mentioned
- **.NET MAUI** — Microsoft's cross-platform .NET framework for building native mobile/desktop UIs; the target platform for the whole talk.
- **Syncfusion .NET MAUI controls** — Syncfusion's commercial UI component library for .NET MAUI; used to build the polished demo dashboard (e.g. the Syncfusion Mobile Button).
- **AI skills (`.agent/skills/` + `skill.md`)** — structured Markdown instruction files (with use case, "when to use," getting-started, and references like `troubleshooting.md`) that an AI agent reads to constrain how it implements a task/control.
- **Syncfusion control skills** — installable, per-control skill packs Syncfusion ships for its .NET MAUI controls; dropped into `.agent/skills/` via a one-line terminal command.
- **Custom `design-system` skill** — an author-prepared skill that tells the agent which design system (tokens, rules) to follow when generating UI.
- **.NET MAUI design system files** — `Resources/Styles/Styles.xaml` (per-control styles, e.g. Button `FontFamily` = Open Sans Regular) and `Colors.xaml` (shared color tokens, e.g. a primary color) — the built-in, basic example of a design system.
- **Design tokens** — named, reusable style values (colors, spacing, typography) the AI generated as directed by the design-system skill.
- **CollectionView / card controls / Button** — .NET MAUI UI controls referenced where the naïve AI output showed alignment and color defects.
- **AI coding agent + IDE terminal** — the agentic dev tooling driving generation; skills are installed and prompts are run from here.
- **GitHub** — hosts the demo sample (shared via a QR code at the end).

## 🚀 Announcements / What's New
None explicitly announced. This is an educational/best-practices session demonstrating an existing pattern (design systems + AI skills with Syncfusion .NET MAUI controls), not a product-launch talk. No previews, GA dates, or roadmap items were stated.

## 💡 Demos
- **Baseline (no skills) demo.** Prompt: *"Create a simple employee dashboard mobile application using .NET MAUI."* Result: a functional, colorful dashboard that on inspection has color issues on the "View Dashboard" button and card controls, plus misaligned icons in the CollectionView. **Point proved:** AI generates UI fast but unpolished/not production-ready because it lacks design context.
- **Installing Syncfusion control skills.** Copies a single Syncfusion-provided line into the terminal, which drops the control skill files into `.agent/skills/`. **Point proved:** skills are easy to add and give the agent real control knowledge.
- **Adding a `design-system` skill via Finder.** Pastes a prepared `design-system` skill alongside the control skills. **Point proved:** you can hand the agent an explicit design system to follow.
- **Regenerating the dashboard (with skills).** Re-runs the prompt; the AI produces an employee model, **design tokens (per the design-system skill)**, and a consistent employee dashboard page. When run, it looks good and the design system is clearly followed. **Point proved:** with a design system + skills, the *same* task yields a consistent, polished, production-grade UI.

## 📊 Notable Stats / Quotes
- *"AI is powerful, but without the right inputs and constraints, it can only guess, not design with intention."*
- *"Skills do not render UI. They constrain the decisions."*
- *"A skill defines how the AI should behave. A design system defines what good UI looks like, and design-system skills guide the AI to follow it."*
- *"We are not asking AI to design UI. We are teaching it how we design UI."*
- *"Happy coding with AI."*
- (No numeric benchmarks or stats were presented — this was a short, qualitative session.)

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Stand up a small .NET MAUI app, define a real design system in `Styles.xaml`/`Colors.xaml`, then add a `.agent/skills/design-system/skill.md` + Syncfusion control skills and compare "no-skill" vs "with-skill" generations on the same prompt.
- [ ] Things to try: Write a reusable `design-system` skill (design tokens + layout rules + "when to use") that any agent in the repo can read; test whether it survives across different prompts/agents.
- [ ] Things to try: Locate the Syncfusion demo GitHub repo (QR/link in the talk) and inspect their `skill.md` + `troubleshooting.md` structure as a template.
- [ ] Questions: What exactly does the one-line Syncfusion skill installer copy, and where does it pull from (a Syncfusion skills feed/URL)? Is it free/open or licence-gated?
- [ ] Questions: How do `.agent/skills/` skills here relate to OpenClaw/Anthropic-style skills and to the broader Agent Skills format — is `.agent/skills/skill.md` a Syncfusion convention or a shared standard?
- [ ] Questions: How well does this generalise beyond Syncfusion (e.g. to plain .NET MAUI controls, Telerik, or Toolkit controls)?
- [ ] Relevant to: building consistent AI-assisted UIs, design-system governance, agentic coding workflows, and our own skill-authoring practices.

## 🔗 Related
- [[.NET MAUI]]
- [[Design systems]]
- [[AI skills]]
- [[Syncfusion]]
- [[Design tokens]]
- [[Agentic coding workflows]]
- [[AI-assisted UI development]]
- Source list: [[2026 Build Session List]]
