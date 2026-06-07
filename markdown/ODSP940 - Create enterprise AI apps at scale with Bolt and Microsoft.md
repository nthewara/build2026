---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/bolt
  - topic/low-code
  - topic/ai
  - topic/enterprise
  - topic/azure
source: https://www.youtube.com/watch?v=w8vAY4vK3HQ
session_code: ODSP940
event: Microsoft Build 2026
speakers: Will (Bolt), Joe (Bolt)
duration_min: 15
aliases:
  - Create enterprise AI apps at scale with Bolt and Microsoft
---

# ODSP940 — Create enterprise AI apps at scale with Bolt and Microsoft

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Will (Bolt) & Joe (Bolt) — both from Bolt / StackBlitz  
> **Duration:** ~15 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=w8vAY4vK3HQ)

## 🎯 TL;DR
Bolt (from StackBlitz) and Microsoft show how prompt-driven app building can move from quick prototypes to **governed, production-ready enterprise applications**. The core argument: most AI app builders assume a blank canvas, but enterprises already have existing apps, governed cloud environments, design standards, and security requirements — so the real question is "can AI-generated work fit into what we already have?" Bolt's collaboration with Microsoft Azure and Microsoft 365 answers this by letting teams start from existing conversation/context (in Microsoft Copilot), build with approved **design systems**, drive automation via the **Bolt CLI**, and produce reviewable front-end code that deploys into Azure via GitHub/Azure DevOps workflows and Microsoft identity/security tooling. The session demos three pillars — design systems, the Bolt CLI, and the Bolt interface — culminating in a full travel app with auth, a database, and an OpenAI-backed server function built in just a couple of prompts.

## 🔑 Key Takeaways
- **Speed alone isn't enough for enterprises.** Prompt-driven development shortens the gap between idea and working software, but developers and IT need governance, control, and a clear deployment path for what happens *after* generation.
- **The blank-canvas assumption is the problem.** Most AI app builders start from scratch; enterprises instead need to *increment existing applications*, add features safely, and get code developers can review, govern, and deploy without rewriting everything.
- **Bolt = a controlled path from idea to application**, not just a faster generator. Developers define standards and approved foundations *up front*, so creators (PMs, designers, operators) can move fast while output still fits the org's technical foundation.
- **Developers don't have to be the first to prompt.** They pre-approve foundations, environments, and the deployment path; the broader team then builds within those guardrails.
- **Three pillars** drive the workflow: (1) **Design systems** — a shared, approved foundation so every project starts with the right components/patterns/brand instead of a blank canvas; (2) **Bolt CLI** — programmatic interaction to bundle assets, connect repos/workflows, and publish standards; (3) **Bolt interface** — an intuitive build surface for the whole team.
- **Microsoft Copilot is the planning layer.** A conversation/requirements doc becomes a clean project brief (design goals, layout, UI ideas, audience, constraints, success criteria), then Copilot tags the **Bolt agent** and hands a structured prompt directly to Bolt — no lost requirements.
- **Copilot ↔ Bolt is a direct integration.** You can "Build" straight from Copilot, and even tag the Bolt agent inside direct-message conversations to apply discussed changes to the project.
- **Bolt CLI bundles a local component library into a Bolt design system.** It makes sense of your code + design artifacts/docs, generates a **Storybook** instance to browse components, and removes some of the agents' non-deterministic behavior — giving developers control over exactly what code gets produced.
- **Component libraries flow from VS Code → Copilot → Bolt.** A bundled tarball (or a private NPM registry) feeds the design system, so generated apps reuse pre-built, approved code via `package.json`.
- **Real-time collaboration is built in.** Share a project URL to co-access the agent chat live, see who's prompting and when, comment on parts of the project, and queue fixes for the Bolt agent.
- **Full app capabilities ship from prompts:** email/Google authentication, a database with user management, file storage, secrets, analytics, domains & hosting — plus **server functions** that call external APIs (e.g. OpenAI GPT-5) with securely stored secrets.
- **Plan mode** lets you preview the agent's intended implementation (and answer clarifying questions) before it builds — saving time and tokens.
- **Built-in database security scan** runs before publishing; with no issues found, the site publishes to a live URL ready for customers.

## 📚 Detailed Notes

### The enterprise problem with prompt-driven development
Prompt-driven development has already transformed what individual creators can do: a product manager, designer, or developer can describe an idea and quickly get a working prototype, internal tool, or new feature on screen. That speed is powerful because it shortens the distance between an idea and something people can actually use.

But for enterprise teams, **speed on its own is not enough** — especially for the developers and IT teams responsible for what happens *after* something is generated. The fundamental flaw: most AI app-building tools assume you're starting from a **blank canvas**. That's fine for prototypes and some internal tools, but it's not how most enterprise software works. Large organizations already have:
- Existing applications
- Governed cloud environments
- Developer workflows
- Design standards
- Security requirements

So the developer problem is reframed. It's not "*can* AI generate an app?" — it's **"can this fit into what we already have?"** Can teams increment existing applications, add features safely, and give developers code they can review, govern, and deploy **without rewriting everything from scratch**?

The real question for a Microsoft Build audience: *How do you make AI-powered app creation faster while keeping developers in control of the code, approved foundations, environments, and deployment path?*

### How the Bolt × Microsoft collaboration answers it
With **Bolt on Microsoft Azure and Microsoft 365**, teams start from the **conversation and context they already have**, then move toward applications that fit inside infrastructure they already trust. Concretely:
- **Bolt-generated front-end code** can be reviewed, extended, and deployed into **Azure**.
- Teams connect that work into their **GitHub and Azure DevOps** workflows, **Microsoft identity and security** tooling, and the **governance patterns** enterprise developers already use.
- Developers don't have to be the first person prompting in Bolt to benefit — they **define the standards** and **approve foundations, environments, and the deployment path**, so creators move faster while output still fits the org's technical foundation.

The summary positioning: **Bolt is not just a faster way to generate an app — it's a controlled path from idea to application.**

### The three pillars covered in the demo
1. **Design systems** — gives every team a shared foundation. An organization makes its approved design system available in Bolt, so every project starts with the right components, patterns, and brand standards instead of a blank canvas.
2. **Bolt command line interface (CLI)** — gives developers a programmatic way to interact with Bolt. They can bring in approved assets, connect existing repos and workflows, and make the organization's technical standards available to the broader team.
3. **Bolt interface** — gives everyone on the team an intuitive, capable place to build. PMs, designers, operators, and developers can prompt, iterate, and create features while still working within the foundations developers have approved.

**The goal (stated explicitly):** accelerate app creation for the whole organization *while preserving governance, security, and developer standards*.

### Part 1 — Starting in Microsoft Copilot (Will's demo: the planning layer)
The work starts **before anyone opens Bolt**, in **Microsoft Copilot**. A team turns a conversation, set of requirements, or early product idea into a clean **project brief**.

- **Initial prompt (example):** "We run a travel website. For our blog post, we want to create a new template that highlights the photos related to the travel destinations rather than the blog heading text. Can you suggest a starter template page we can move to from what we have now?"
- Copilot immediately returns **design goals, a layout structure, UI ideas, and more**. This is the **planning layer** — Copilot captures the goal, audience, user needs, constraints, success criteria, and any technical or brand requirements that should shape the application.
- **Refinement prompt:** "Optimize this for SEO." → Copilot adds a hero section, an SEO intro, a structured snapshot, and more.
- **Handoff to Bolt:** tag the Bolt agent → "Summarize this conversation in a prompt for Bolt." It outlines the plan. Tag Bolt again and ask it to **build with these specifications**. Because **Copilot connects directly with Bolt**, you select **Build** and the prompt is sent over to Bolt, where the project starts building.

**In Bolt:** the project is created with a **full hero carousel** focusing on images, as requested. The **agent history** shows it executed the plan and put a focus on SEO. In full-screen preview you can scroll and inspect the built page — it has **hover animations** and finishing touches like chapters and zoom-on-hover, a "complete guide to Kyoto," a **bento grid** of place photos, and an elegant preview of related destinations.

**Iterating from a teammate conversation:** to give destinations more focus on the image, you can have a discussion with a colleague, then **tag the Bolt agent directly in that conversation** to read it and make the changes in the project. The Bolt agent highlights destination images more (image over text). After Build + preview, the related-destinations section changes from a **three-column grid to a single column**, putting much more focus on each destination's background image.

**Why this matters:** creating the brief by going back and forth with Copilot gives the team a **shared source of truth before building**. Copilot structures the project's intent using **organizational context**, and the direct Bolt integration means **no lost requirements, decisions, or constraints**. You can also tag the Bolt agent directly in DMs.

### Part 2 — The developer's perspective with the Bolt CLI (Joe's demo)
Joe frames a common developer reality: PMs request the ability to work with **code and components the dev team has already built**, and in the modern era of design tools, AI tools, and many systems, you need to work across many contexts. The demo: take a **component library from a local environment**, send it to Bolt, and have the Bolt agent use it to build new internal applications, examples, or prototypes with that specific code.

- **Setup:** open a **VS Code** instance containing a small **component library** (a set of components) plus a demo website — a small travel application with destinations. The *content* of the site isn't the point; the point is the **process of sharing pre-built code** so other team members can prototype with it.
- **Tool:** the **Bolt CLI**. Out of the gate it can, among other things, **bundle and create a design system** — it goes through your code and any design artifacts/documentation you give it to make sense of how to work with your components, so it can build new applications on top of that existing material.
- **Core value proposition:** start to **remove the non-deterministic qualities of the agents** and give developers **control over what's produced and what code is used** as part of the system.
- **Workflow:** Joe uses a small **skill that wraps the Bolt CLI** to provide context about the tools, then prompts (in Copilot's chat): *"Let's go ahead and use the Bolt CLI to create a design system and publish it within Bolt."* The agent (in Copilot) completes and creates a **design system inside Bolt**.
- **Viewing it in Bolt:** go to **bolt.new** → personal profile → **Settings → Design system**. Bolt has an **agent that gets trained on and understands the specifics of your component library/design system**. (Joe pre-ran this so there's no waiting.) Opening it shows a generated **Storybook instance** to traverse and navigate the components — viewable in context, and usable as a **catalyst to build new internal apps/prototypes** from the team's existing code.

**Building with the design system:**
- In the prompt area, **select "design system"** and choose the component library (a "Poet"/component library).
- Prompt: *"Let's build a travel destinations landing page."* The Bolt agent **invokes the design system abilities** and builds a travel app based on the packaged content/component library.
- **Inspecting generated code:** look at `package.json` — Joe **bundled a tarball** of the local component library (from VS Code) and dropped it into Bolt. Alternatively you can pull from a **private NPM registry** (configurable in Bolt under packages & private registries). Bundling lets you provision and **share the library across many applications/circumstances quickly**.
- **Recap of the flow:** straight from the **VS Code instance → Copilot → Bolt**, using all the seeded local code/components. The result is an app the **PMs can pick up and build with**, handed back to Will.

### Part 3 — Building the full app in the Bolt interface (back to Will)
**Collaboration:** sharing the **project URL** lets multiple people access the project and the **agent chat in real time** — seeing who's prompting and when. Teams can **collaboratively comment** on parts of the project and **queue fixes** for the Bolt agent.

**Adding authentication:**
- Prompt: *"Please add user auth with email so a user can log in and save travel plans to their account. By clicking the plan-a-trip feature, it should open a modal asking them for their desired destinations."*
- Model selected: **Claude Opus 4.7** ("Oakus 4.7" in captions). Run in **plan mode** + build.
- **Plan mode** shows what the agent intends *before* it acts — often saving time and tokens. The generated plan: set up a **database with authentication**, the **plan-a-trip model**, and more. No clarifying questions → implement.
- **Result:** create an account and sign in. The **database** is viewable via an icon — user authentication with **email sign-in** enabled (and **Google sign-in** can also be enabled), **user management** showing all created accounts, plus **file storage, secrets, analytics, domains, and hosting**. Testing **plan a trip** opens a modal — using the **same design system** as the rest of the site — asking for travel destinations.

**Adding a server function (OpenAI integration):**
- Prompt: *"Please create a server function which uses the OpenAI GPT-5 model. I will provide my OpenAI API key. After I enter my desired destinations, travel dates, and notes and click save trip, it should send this info to OpenAI and create an itinerary for me. While generating, I should see a spinner inside the save-trip button, and the modal should refresh with this itinerary once generated."*
- Plan mode → it **asks clarifying questions** (answered) → turn off plan mode → build.
- After building, the agent **asks for the OpenAI API key**. Add it under **Secrets** → paste → **Create secret** → securely saved.
- **Test:** plan a trip — *Patagonia, 1st–4th December, two travelers, "I love hiking."* → **Save trip** → "generating itinerary" (spinner) → the **server function calls the OpenAI API** and generates a **4-day Patagonia itinerary**. Built in essentially **two prompts**.

**Publishing:** the project can be collaborated/shared or **published directly**. A built-in **database security scan** reports **no issues**, so it publishes to a **live site** ready to be viewed by customers.

### Closing
The demo covered building with your **enterprise design system**, **programmatically interacting with Bolt via the CLI**, and using the **Bolt interface**. For more, see Bolt's YouTube channel and **bolt.new**. The Microsoft × Bolt partnership lets you bring your **organization's context via Microsoft 365**, the **scalability and reliability of Microsoft Azure**, plus the **speed of Bolt**.

## 🛠️ Products / Features / Technologies Mentioned
- **Bolt** (from StackBlitz) — AI app-building platform; the controlled path from idea to governed, production-ready application.
- **Bolt interface (bolt.new)** — the build surface where the whole team prompts, iterates, previews, and ships apps.
- **Bolt agent** — the AI agent inside Bolt that builds/edits projects; can be tagged from Copilot and from conversations/DMs.
- **Bolt CLI** — programmatic interface to Bolt; bundles/creates and publishes design systems, brings in approved assets, connects repos/workflows.
- **Bolt Design systems** — approved, reusable component/pattern/brand foundation made available in Bolt (managed under personal profile → Settings → Design system).
- **Microsoft Copilot** — the planning layer; turns conversations/requirements into a structured project brief and hands a prompt directly to Bolt.
- **Microsoft Azure** — target cloud for deploying Bolt-generated code; provides scalability and reliability.
- **Microsoft 365** — brings organizational context into the workflow.
- **GitHub & Azure DevOps** — developer workflows Bolt work can connect into.
- **Microsoft identity & security tooling** — governance/security integration for enterprise deployment.
- **Storybook** — component explorer instance generated by Bolt from the design system to browse components in context.
- **VS Code** — local environment hosting the component library/demo site before sharing into Bolt.
- **Private NPM registry / tarball bundling** — two ways to feed a component library into Bolt (via `package.json`).
- **Claude Opus 4.7** — model selected in Bolt for the auth build (captioned "Oakus 4.7").
- **OpenAI GPT-5** — model called by the generated server function to produce a travel itinerary.
- **Bolt platform capabilities shown:** authentication (email + Google sign-in), database, user management, file storage, secrets, analytics, domains & hosting, server functions, plan mode, real-time collaboration/comments, built-in database security scan, one-click publish to a live site.

## 🚀 Announcements / What's New
- **Bolt × Microsoft partnership / "Bolt on Microsoft Azure and Microsoft 365"** is positioned as the headline collaboration — enabling enterprise app creation that brings in M365 context, deploys to Azure, and connects to GitHub/Azure DevOps and Microsoft identity/security tooling. (Presented as an available/collaborative capability rather than with explicit preview/GA dates.)
- No specific preview/GA status, dates, or version numbers were stated for individual features. Beyond the partnership framing, **no other product launches were explicitly announced** — the session is a capability/workflow walkthrough.

## 💡 Demos
- **Demo 1 — Copilot → Bolt planning handoff (Will):** Built a travel-blog template from a Copilot conversation. Refined for SEO, summarized the conversation into a Bolt prompt, tagged the Bolt agent, and clicked Build → Bolt produced a hero-carousel, image-focused page with hover animations, a Kyoto guide, and a bento photo grid. *Proves:* org context/requirements flow losslessly from Copilot into a built Bolt project, and the Bolt agent can be tagged inside conversations to apply changes.
- **Demo 2 — Bolt CLI + design system from local code (Joe):** Took a local component library in VS Code, used the Bolt CLI (via a Copilot-driven skill) to bundle and publish a design system into Bolt, viewed it as a generated Storybook, then prompted Bolt to build a travel landing page that consumed the bundled library (tarball in `package.json`; private NPM registry as an alternative). *Proves:* developers can seed approved, pre-built code into Bolt so the team builds on a controlled, deterministic foundation.
- **Demo 3 — Full app build in the Bolt interface (Will):** Added email/Google auth + a database with user management via plan mode; then added a server function calling OpenAI GPT-5 to generate a Patagonia itinerary, storing the API key in Secrets; ran a database security scan (no issues) and published to a live site. *Proves:* production-grade features (auth, DB, secrets, external API server functions) plus governance (plan mode, security scan) ship in ~two prompts with built-in collaboration.

## 📊 Notable Stats / Quotes
- "**Bolt is not just a faster way to generate an app, but it's a controlled path from idea to application.**"
- "**The goal is simple: accelerate app creation for the whole organization while preserving governance, security, and developer standards.**"
- "Most AI app-building tools assume you are starting from a **blank canvas**… but it's not how most enterprise software works."
- "The developer problem is not just *can AI generate an app?* It is, **can this fit into what we already have?**"
- The core value of the design-system/CLI path: "we're starting to take some of the overall **non-deterministic qualities of the agents**, remove some of that, and give you back the **control** of actually what's produced."
- Full app (auth + database + OpenAI-backed server function generating a 4-day Patagonia itinerary) built in essentially **two prompts**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Bundle a local component library into a Bolt design system via the **Bolt CLI** (tarball vs private NPM registry) and build a sample app on top of it; test the **Copilot → Bolt "Build"** handoff; try **plan mode** to compare token usage vs straight build; wire a **server function** calling OpenAI with a key stored in Bolt **Secrets**; deploy Bolt front-end output into **Azure** via GitHub/Azure DevOps.
- [ ] Questions: What exactly does "deploy into Azure" cover — App Service / Static Web Apps / Container Apps? How deep is the GitHub/Azure DevOps + Microsoft identity integration (SSO/Entra ID)? Is the Bolt database first-party or a partner backend, and where does it run relative to Azure governance? Pricing/licensing of "Bolt on Azure + M365"? Availability/GA status of the partnership? Does the design-system training keep components in sync as the source library evolves?
- [ ] Relevant to: Enterprise/low-code app teams wanting governed AI app generation; platform/dev-tooling teams standardizing on approved design systems; Microsoft customers consolidating on Copilot + M365 + Azure who want faster front-end delivery without losing governance, security, or code review.

## 🔗 Related
- 
