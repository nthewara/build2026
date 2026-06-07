---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/developer-workflow
  - topic/ai
  - topic/devtools
  - topic/productivity
  - topic/startups
source: https://www.youtube.com/watch?v=JFA6LiVTmuw
session_code: ODSP908
event: Microsoft Build 2026
speakers: Will (Founder, Clovo)
duration_min: 8
aliases:
  - Streamline your end-to-end developer workflow with AI
---

# ODSP908 — Streamline your end-to-end developer workflow with AI

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Will — Founder of Clovo (AI agent for on-brand asset generation; backed by the Founders Inc accelerator, Fort Mason, San Francisco; ~18k-subscriber YouTube build-in-public channel)  
> **Duration:** ~8 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=JFA6LiVTmuw)

## 🎯 TL;DR
A fast, practical lightning talk by Will, a solo/early-stage founder, walking through the **four phases of shipping a product end-to-end with AI**: (1) coming up with startup ideas, (2) building with GitHub Copilot in VS Code, (3) communicating with your team, and (4) going to market to get real users. The throughline is **leverage**: AI lets you build, document, and communicate so much faster that the optimal strategy shifts from *debating which idea is best* to *shipping many ideas and letting the market decide*. A recurring tactical theme is removing friction and context-switching by binding tested, reusable AI prompts to **programmable Logitech MX hardware** (keypad/keyboard keys + mouse action ring), so prompts, notes, and outreach messages are one keypress away. His closing thesis: **building is still the core skill — AI just gives you the leverage to take far more shots** (including previously-unjustifiable personalized software).

## 🔑 Key Takeaways
- **Ship in four phases:** Ideate → Build (Copilot/VS Code) → Communicate (team) → Go-to-market (real users). The talk is structured around this lifecycle.
- **Build for a problem you have yourself.** You already understand it deeply *and* you become your own user, enabling rapid iteration loops.
- **Be a domain expert in the space you're solving for** — it deepens problem understanding and gives you an existing network of early adopters.
- **Catch ideas the instant they appear** — they vanish fast. Will binds a Logitech MX Master 4 mouse **action ring** to open a notepad, and uses a screenshot key to capture article snippets into his notes for reference.
- **Run user interviews on deterministic questions** ("What do you spend the most time on?", "What's your day-to-day like?", "What does your org have budget for?") because describing reality is low-bias vs. asking opinions.
- **Three main AI build use cases:** writing code (GitHub Copilot), writing documentation, and writing tests. Docs and tests benefit from heavily-iterated, reusable prompts.
- **Bind tested prompts to hardware keys** (Logitech MX Creative keypad / MX Keys keyboard). In VS Code each key pastes a different proven prompt — no context-switching to hunt for or rewrite prompts.
- **Start a fresh AI session per feature** to keep the context window clean, then **write a detailed AI handoff doc** (for yourself *and* the next AI session) inside that feature's folder so context carries forward.
- **Stop debating, start shipping.** Because shipping is so fast now, try multiple features in parallel and push to production — let the market show where the pull is.
- **Use AI-generated visual docs to align your team.** Have AI produce a nicely-formatted HTML doc and present it live; teams stay aligned and digest info better with something visual to follow, and keep the doc for reference afterward.
- **Microsoft Teams auto-transcribes calls** and AI generates a summary doc + action items for the team to follow.
- **Go where your users gather.** For developers: Twitter/X, Product Hunt, and open-source projects (GitHub stars = visibility, contributors become invested). For Will's Clover audience: Instagram + LinkedIn.
- **Build in public** (Will uses YouTube) — people get invested in the journey and end up trying your software.
- **Reach users with reusable, lightly-personalized outreach** — Will stores message templates on his Logitech keys, swaps the first name, and sends fast; the goal is getting on feedback calls.
- **AI lowers the cost of personalized software** — ideas that were never worth the time/energy before are now viable.

## 📚 Detailed Notes

### Who's speaking & framing
Will introduces himself as the **founder of Clovo** (he later refers to the product as "Clover") — an **AI agent that lets brands and businesses quickly generate on-brand assets and iterate on them**. The company is **backed by the Founders Inc accelerator** in San Francisco (Fort Mason). On the side he runs a **YouTube channel (~18,000 subscribers)** documenting his startup journey — the ups and downs of building, and how he builds software. This "build in public" identity is relevant because it later becomes one of his go-to-market channels.

He frames the whole talk around **four phases of shipping a product end-to-end**:
1. Coming up with startup ideas
2. Building with Copilot in VS Code
3. Communicating effectively with the team (to move fast while keeping quality)
4. Going to market to get real-life users

### Phase 1 — Coming up with ideas
Will's idea-generation playbook has four parts:

**1. Build for a problem you have yourself.** Two reasons:
- If you already hit the problem, you likely **understand it on a very deep level**.
- You'll **use your own software** to solve it, so you can run **rapid iteration loops** as your own first user.

**2. Be a domain expert in the field you're solving for.** This also deepens problem understanding, and crucially you **already know other people in the industry**, so you can **find early adopters quickly through your network**.

**3. Don't force ideation — capture ideas when they arrive unprompted.** Will's experience is that ideas rarely come from sitting down to "think of good ideas." They surface during other activity — e.g. browsing the internet. The key risk is that **ideas disappear fast**, so you must capture them the moment they appear. His concrete tactics:
- A **Logitech MX Master 4** mouse with an **action ring**, which he configured to **open a new notepad** so he can instantly jot ideas into a running documentation file.
- A frequently-used **screenshot feature** to grab parts of articles he's reading and **save them into his notes** for later reference.
- More personally: **playing/pausing his music** to shift into a different mental mode for ideation (and while coding).

**4. Run user interviews about their day-to-day.** He deliberately focuses on **deterministic, low-bias questions**:
- "What do you spend the most time on?"
- "What is your day-to-day like?"
- "What does your organization have budget for?"

The logic: these ask people to **describe what is actually happening** rather than offer opinions, so the answers carry less bias.

### Phase 2 — Building with Copilot in VS Code
Will identifies **three major AI use cases** in his build workflow:
1. **Writing code** — primarily with **GitHub Copilot**.
2. **Writing documentation** — much more than before.
3. **Writing tests** — much more than before.

**Reusable, hardware-bound prompts (the central productivity hack).** For docs and tests he has already **tested and iterated many prompts** to consistently get the results he wants. Rather than re-finding or rewriting them in the GitHub Copilot chat, he **configured the keys on his Logitech MX Creative keypad** so that **each key pastes a different proven prompt** while he's in VS Code. This lets him execute these tasks **without context-switching** to hunt for where prompts are stored or rewrite them from scratch.

**Fresh AI session per feature + handoff docs.** For each feature he ships, he **starts a new AI session** — because of the **context window**, he doesn't want an unrelated previous feature polluting the context for the next one. To carry context forward despite the reset, after shipping a feature / ending a session he **writes a very detailed "AI doc"** — both for himself to read and for the **next AI session to catch up on** — stored **within that feature's folder**.

**Team behavior shift: ship instead of debate.** A new dynamic on his team: previously they'd **debate a lot about which feature to ship or which experiments to run**. Now, because they can **ship software so much faster**, instead of debating they simply **try multiple features and push them to production** — the philosophy is to **let the market decide** and see where the pull comes from.

### Phase 3 — Communicating with the team
AI has changed how teams communicate while shipping:

**Before:** Will would get on a call and verbally explain what he thinks is important, the milestones they're targeting, or the software issues they're hitting.

**Now:** Because AI can produce **much more documentation, quickly**, he has the **AI write a very detailed, nicely-formatted HTML doc** and **presents that to the team live on the call**. Benefits he's noticed:
- The team **stays more aligned**.
- They **digest information better** because there's **something visual to follow**.
- He **shares the doc afterward** so they have it for reference.

**Microsoft Teams for calls.** He uses **Microsoft Teams**, which **takes a transcript** of the call; AI then writes a **good summary doc and action items** for the team to follow up on.

He reiterates that **detailed documentation has always been valuable** — for the codebase *and* the business side — but historically it **took too long**. The unlock is that with a **tested, reusable prompt** you get **consistent behavior from the AI**. He keeps that prompt **saved on his Logitech MX Keys keyboard** and triggers it to generate these docs quickly.

### Phase 4 — Go-to-market: finding users
Core principle: **go where your users gather** — and that location differs by product.

For the **developer community** (his Build audience):
- **Twitter/X** — primary channel for devs.
- **Product Hunt** — lots of people there browsing for new products to try.
- **Open-source projects** — if you build something cool, people contribute and become **very invested**; via **GitHub and GitHub stars** you gain a lot of **visibility**.

For his **own product (Clover)**, whose users gather elsewhere:
- **Instagram** (where many of his users are) and **LinkedIn**.

**Build in public.** This has helped Will and others he's seen ship software. He does it via **YouTube** — documenting how he builds — so **people get invested in your journey** and end up **trying your software**.

**Closing the loop with users.** Once you have users, **reach out** (email or whatever platform) to **get on calls with them for feedback** — to build a relationship and learn how to **improve and iterate**. These outreach messages are **fairly consistent**, so he keeps **pre-written messages saved on his Logitech MX Creative keyboard**, **changes just the first name**, and sends them very quickly.

### Closing thesis — leverage, not replacement
Will's wrap-up makes the core argument explicit:
- **Building is still the skill.** AI doesn't replace it.
- **The leverage is that AI lets you build so much faster**, so you can **take more shots and test far more ideas**.
- After you ship, you **read the market signal** to decide whether an idea is worth continuing.
- A notable side effect: **much more personalized software is coming to life**. Previously it was **hard to justify the time/energy** to build niche/personal tools; **now AI brings those ideas to life much faster**, which he finds exciting.

He ends by inviting the audience to share what they ship next.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — Will's primary AI tool for writing code (and, via reusable prompts, docs and tests) inside VS Code.
- **Visual Studio Code (VS Code)** — the editor where his hardware-bound prompts paste into the Copilot chat.
- **Microsoft Teams** — used for team calls; **auto-transcribes** calls, with AI generating summary docs + action items.
- **Logitech MX Master 4 (mouse)** — its **action ring** is configured to open a new notepad for instant idea capture.
- **Logitech MX Creative keypad** — programmable keys, **each bound to a different tested prompt** (docs/tests) usable in VS Code; also stores outreach message templates.
- **Logitech MX Keys (keyboard)** — stores a tested **documentation-generation prompt** for one-press access.
- **Clovo / Clover** — Will's own product: an **AI agent that generates and iterates on-brand assets** for brands and businesses.
- **Founders Inc** — San Francisco accelerator (Fort Mason) backing Clovo.
- **Twitter/X** — recommended go-to-market channel for the developer community.
- **Product Hunt** — recommended launch/discovery platform for new products.
- **GitHub / GitHub stars** — open-source visibility and contributor engagement channel.
- **Instagram & LinkedIn** — Will's go-to-market channels for Clover's (non-developer) audience.
- **YouTube** — Will's build-in-public channel (~18k subscribers) used as a marketing/journey channel.
- **AI-generated HTML docs** — nicely-formatted documents AI produces for him to present live to his team.

## 🚀 Announcements / What's New
None explicitly announced. This is a partner/community lightning talk focused on **workflow tactics and methodology** for solo founders/small teams, not a product-launch session. The only "new" elements are **behavioral shifts** Will describes in his own practice (e.g. ship-don't-debate, AI handoff docs per feature, hardware-bound prompts).

## 💡 Demos
No formal live software demo. Will does, however, **show his physical setup as a walkthrough** — pointing to his **Logitech MX Master 4 mouse** (action ring → opens notepad), **MX Creative keypad** (keys → tested prompts in VS Code / outreach templates), and **MX Keys keyboard** (key → documentation-generation prompt). The point proven: **binding tested, reusable prompts/messages to hardware keys removes context-switching and friction**, letting him capture ideas, generate docs/tests, and send user outreach with a single keypress.

## 📊 Notable Stats / Quotes
- **~18,000 YouTube subscribers** on Will's build-in-public channel.
- **Four phases** of shipping a product end-to-end (the talk's structure).
- **Three main AI use cases** in building: code, documentation, tests.
- Deterministic user-interview questions: *"What do you spend the most time on? What is your day-to-day like? And what does your organization have budget for?"*
- > "Building is still the skill. But the leverage now is that AI lets us build so much faster. So you can put up more shots and test out way more ideas."
- On personalized software: *"In the past it's hard to justify the time and energy to build those personalized software… but now with AI you're able to bring those ideas to life so much quicker."*
- On idea capture: *"You always want to catch the ideas the moment they come up because they can very quickly go away."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Bind my most-used, **tested** GitHub Copilot prompts (generate tests, generate docs, refactor, write commit msg) to programmable keys / a Stream Deck so they paste into VS Code without context-switching.
  - Adopt the **"fresh AI session per feature + write a handoff `AI.md` in the feature folder"** pattern to manage context-window limits.
  - Switch team updates to **AI-generated, nicely-formatted docs presented live** instead of purely verbal call updates; lean on **Teams transcription + AI action items**.
  - Keep a lightly-personalized **user-outreach template** one keypress away (swap first name → send).
- [ ] Questions:
  - For solo/small teams, how much of the "ship multiple features, let the market decide" approach scales before the lack of upfront design debate creates real tech-debt or product incoherence?
  - What's a sane guardrail set so "more shots with AI" doesn't become shipping unvalidated/low-quality features to prod?
- [ ] Relevant to:
  - Personal side projects / building-in-public; prompt-library tooling; developer-productivity setup; go-to-market for indie/dev-focused products.

## 🔗 Related
- [[BRK203 - From CLI to PR]] — GitHub Copilot across the developer workflow (CLI → pull request).
- [[BRK202 - Azure DevOps meets GitHub AI powered SDLC]] — AI across the broader software-development lifecycle.
- [[BRK229 - From Skeptic to Superpower]] — adopting AI into a real dev workflow / mindset shift.
- [[DEM303 - Late to agentic coding Dont panic build]] — practical "just start building with AI agents" angle.
- [[DEM305 - GitHub Copilot Anywhere Remote CLIs to Cloud Sandboxes]] — Copilot beyond the editor.
- Source list: [[2026 Build Session List]]
