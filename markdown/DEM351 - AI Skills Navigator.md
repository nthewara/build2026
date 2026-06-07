---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/skilling
  - topic/m365-copilot
  - topic/learning
source: https://www.youtube.com/watch?v=HTSQzsXzXz4
session_code: DEM351
event: Microsoft Build 2026
speakers: Matt Ernie, Shri (Shinidi)
duration_min: 23
aliases:
  - AI Skills Navigator
---

# DEM351 — AI Skills Navigator: Accelerate tech skills with personalized learning

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Matt Ernie (Senior Technical Program Manager, Global Skilling @ Microsoft) & Shri / "Shinidi" (Engineering Manager who helped build the AI Skills Navigator)  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=HTSQzsXzXz4)

## 🎯 TL;DR
Microsoft's **AI Skills Navigator (ASN)** is the official Microsoft content repository for tech skilling, unifying Microsoft Learn paths/modules, applied skills, credentials, skilling sessions, LinkedIn Learning, and curated YouTube videos into one personalized experience. The session frames the shift from last year's *workforce transformation* ("build confidence with AI") to this year's *work transformation* ("redesign how work gets done so AI creates real impact for builders"). Through a fictional enterprise ("Zava") standing up an AI platform team, the presenters demo personalized recommendations, an AI-assisted **playlist authoring tool** that builds sprint-aligned curricula, AI-narrated podcast summaries, interactive **skilling sessions** with an AI virtual trainer and coach, team progress tracking, and the newly **GA learning agent in M365 Copilot** that surfaces learning directly in the flow of work. The core message: the gap isn't *knowing AI exists* — it's *knowing how to apply it to the job in front of you*, and ASN is designed to close that gap.

## 🔑 Key Takeaways
- The skilling conversation has evolved from **workforce transformation** (build AI confidence) → **work transformation** (redesign how work gets done so AI delivers real impact for builders).
- The real gap is **application**: not knowing AI is available, but knowing how to apply it to the specific job in front of you.
- **AI Skills Navigator (ASN)** is Microsoft's official, single-place content repository: Microsoft Learn paths & modules, applied skills, certifications/credentials, skilling sessions, LinkedIn Learning content, and curated official YouTube videos.
- Content is **segregated by level across different roles** (e.g., Developer), with tracks like AI-assisted coding, build & orchestrate agents, and agentic DevOps — visible even before sign-in.
- **Lightweight onboarding**: pick your *roles of interest* (e.g., AI Engineer, Data Scientist) and *learning preferences* (visual / reading / hands-on / interactive); these drive personalization on a **"For You"** page.
- **Team Skilling** lets a lead chat with an agent and, based on objectives, goals, and time constraints, auto-generate a curated **playlist** — the authoring tool is **catalog-aware** and builds a **sprint-aligned curriculum** tied to a deliverable.
- Playlists can be **assigned to team members** (delivered via Teams), who accept an invitation to join the same playlist.
- **AI-generated podcasts**: Learn modules can be turned into a conversational ~5-min podcast with **two distinct voices** (not text-to-speech), grounded in the actual module — ideal for learning on the go.
- **Skilling Sessions** are a hybrid digital/classroom experience featuring an **AI virtual trainer** plus a **skilling session coach** (grounded in the course + Microsoft Learn content) that runs knowledge checks, answers context-aware questions, and nudges learners based on their progress.
- The **learning agent in M365 Copilot** is **generally available as of the session date** to all M365 Copilot users; it surfaces learning in the flow of work using **Work IQ** + your learning profile, with diverse starter prompts and task recommendations.
- Organizations can deploy the learning agent to unlock richer capabilities: **enterprise content sources, admin upskilling, and agent reporting**.
- **Credentials** close the loop — they validate and showcase growth to leadership/teams; ASN hosts the full Microsoft catalog of credentials with direct paths to Microsoft Learn (prep, practice exams, exam sign-up).
- **Team progress tracking ("view shared progress")** lets a lead see how a playlist is *landing* (not just consumed/checked), spot where members are stuck, and intervene; playlists map to **sprints** (e.g., 4-week sprint or two 2-week sprints) tracked week-over-week against the deliverable.
- **ASN content within the learning agent is "coming soon"**, and the **learning agent is coming to Copilot Chat in the near future**.
- Call to action: **sign into ASN, create/modify your profile** for personalized recommendations, and **register for Skills Fest (June 8–12)**.

## 📚 Detailed Notes

### Framing: From Workforce Transformation to Work Transformation
Matt Ernie (Senior TPM, Global Skilling @ Microsoft) opens by contrasting last year vs. this year:
- **Last year:** the upskilling conversation centered on **workforce transformation** — helping people *build confidence* with AI.
- **This year:** that has expanded into **work transformation** — *redesigning the way work gets done* so AI can create real impact for builders.

The central thesis: **"It's not just knowing that AI is available. It's knowing how to apply it to the job in front of you. That is the gap this experience is designed to close."** ASN brings LinkedIn Learning and trusted YouTube videos all in one place, and—via the **learning agent in M365 Copilot**—learning can show up **in the flow of work**, moving people from their work task to relevant upskilling based on their **role, goals, and context**.

### Scenario Setup: Zava + Two Personas
To ground the demo, the presenters use **Zava**, a fictional global enterprise standing up an **AI platform team**:
- **Shri (Shinidi)** — in real life an engineering manager who helped build ASN — plays an **engineering lead** at Zava who needs to ramp his team to **ship a production-grade agent**. His team also builds internal agents connecting to **SharePoint** and various connectors within their ecosystem.
- **Matt** — plays one of **Shri's developers** on that team.

### Homepage (Signed-Out Experience)
Shri starts on the ASN **homepage without signing in** and already sees:
- Content **segregated by levels across different roles**.
- The **Developer** role is his focus; scrolling reveals rich content tracks: **AI-assisted coding**, **build and orchestrate agents**, and **agentic DevOps**.

### Signed-In Experience & Onboarding
After onboarding (described as "pretty light"), Shri walks through two lightweight profile controls:
1. **Roles of interest** — he chose **AI Engineer** and **Data Scientist** (many other roles available).
2. **Learning preferences** — choose to be more **visual**, **reading**, **hands-on**, or **interactive**.

These preferences **determine the personalization** of content. Because he selected AI Engineer, the **personalization / "For You" page** surfaces relevant content such as: generating tests with AI, evaluating generative AI applications, creating machine learning models, etc.

> Note: The presenters candidly flagged some live **UI rendering glitches** ("there are some problems with the way it is showing up… this looks okay, but this doesn't") during the signed-in walkthrough.

### Explore Content
Beyond personalized recommendations, the **Explore Content** section offers the broader catalog:
- **Curations by level** (mirroring the homepage segmentation).
- **Expert Voices** — industry-trusted folks featured within ASN.
- A **filter by modality** at the bottom, covering the full ecosystem: **MS Learn learning paths & modules**, **credentials**, **LinkedIn Learning content**, **skilling sessions**, and **videos**.

### Team Skilling & AI-Assisted Playlist Authoring
As a lead, Shri's job is to use **Team Skilling**, a feature where you **chat / interact with an agent** and, based on your team's **objectives, goals, and time constraints**, curate a **playlist**.

He had pre-created one with these inputs (the prompt/parameters):
- **Goal:** upskill the team to **ship a production agent on Microsoft 365 Copilot**.
- **Requirements:** leverage **Microsoft Graph** and **SharePoint connectors**; **evaluate the agent in Microsoft Foundry (Azure)**; **instrument telemetry with Power BI**.
- **Assumptions:** **mid-level developers**, **4 weeks** total, **8 hours per week**.

He then walked through the agent's **reasoning / how it built the plan**:
1. **Identified the objective** and the **skill plan goal** from the prompt.
2. **Identified the different skilling topics** based on that objective.
3. **Searched all content within the catalog** to **stitch together the playlist** (catalog-aware authoring).

The **generated playlist** had four sections:
1. **Copilot agent studio — agent design and lifecycle**
2. **Grounding with Microsoft Graph and SharePoint connectors**
3. **Evaluation**
4. **Telemetry and monitoring**

He then **assigned the playlist to Matt** (one of his developers).

### Assigning & Accepting a Playlist (Teams Handoff)
- Shri **sends/assigns** the playlist; it appears in **Matt's Teams**.
- Matt sees that "**Shri has invited me to accept this playlist**," **accepts the invitation**, and is welcomed into the **same playlist** Shri created.

### Developer Experience — Consuming the Playlist
Matt, as a busy developer, doesn't plan to spend all day in the playlist but wants to **get oriented** and find some beginner content.

**a) Learn module → AI-generated Podcast**
- He opens a **Learn module on building agents in Copilot Studio**. Learn modules can be text-heavy.
- He chooses to turn it into a **podcast** to listen to while walking to a meeting.
- Key point: it's generated with **two different voices** — a **conversational podcast, not text-to-speech** — **grounded in the actual module**, giving an **~5-minute summary** of the full module so he can grab key takeaways while multitasking. (Live audio didn't play, but the capability was explained.)

**b) Curated YouTube Video**
- Back in the playlist, there's a **YouTube video on Copilot Studio fundamentals**. All videos are **curated from Microsoft official YouTube channels** — supporting people who prefer learning from video, backed by a deep catalog.

**c) Skilling Session — AI Virtual Trainer + Coach**
- Matt opens **"Introduction to Agentic AI business solution architecture,"** a **skilling session**.
- It's **not just a video** — it's a **hybrid between a digital learning experience and the structure/support of a classroom**, delivered virtually.
- Components:
  - An **AI virtual trainer** hosts the session.
  - A **skilling session coach** (right-hand side) is **grounded in the content of the course** *and* **Microsoft Learn content**, and is an expert in both.
- The coach is **progress-aware**: it knows where you are and how far you've progressed, so it can answer **context-specific questions**, **nudge** you (e.g., offer a "quick recap"), and run **knowledge checks** when you reach certain points in a section — reinforcing what was learned. (A couple of coach responses were slow/garbled live, but it eventually answered.)

### Learning Agent in M365 Copilot (GA Announcement)
Shri tips Matt off to a **new** capability: the **learning agent in M365 Copilot**. Rationale: **not everything is a structured path like a playlist** — there are situations where you need to **learn something in the middle of your work** and don't know where to look.

- Matt **opens the learning agent directly in M365 Copilot**, where he already generates/summarizes/drafts design documents — it's **right in the agent rail**.
- **Status:** the agent is **generally available as of the session date**, available to **all M365 Copilot users**.
- **Org deployment** lights up richer capabilities: **enterprise content sources**, **admin upskilling**, and **agent reporting**.
- **Roadmap:** ASN content within the agent is **"coming soon,"** and the learning agent is **coming to Copilot Chat in the near future**.

**Agent home & Work IQ–driven personalization:**
- The agent home shows **diverse starter prompts** generated via **Work IQ**, based on the **skills in his learning profile**.
- His **recent activity** is shown, plus **task recommendations** grounded in what he's doing at work (via Work IQ + selected skills).
- Other options surfaced: **getting credentials** and **practicing with AI**.

**Example flows:**
- "**Watch videos about AI prompting**" → the agent looks **across its full source set** (ASN **plus** LinkedIn Learning and enterprise sources) and returns recommendations.
- "**Deepen your learning with applied skills**" → the agent searches **all available options** and recommends **applied skills**. Matt picks **"create an AI agent,"** which jumps straight into ASN. An **applied skill** is described as an **immersive, hands-on, lab-based assessment** that proves you know something *because you can actually do it* — hence high value.

### Credentials — Turning Learning into Proof
Matt emphasizes that **learning should lead somewhere**, which is where **credentials** come in:
- Credentials **validate and showcase growth** to leadership and team — "I can prove that I know something by getting a credential."
- ASN has the **full Microsoft catalog of credentials**, many recognizable from **MS Learn**.
- Searching for "agent" surfaces relevant, **newly updated** credentials, e.g.:
  - **Copilot and agent administration fundamentals**
  - **Create agents in Microsoft Copilot Studio**
  - **AI Agent Builder Associate** *(name approximate from captions)*
  - **Azure AI apps and agents developer associate** *(name approximate from captions)*
- Opening a credential shows **targeted roles**, **included skills**, and a path to **Microsoft Learn** for **preparation, practice exams, and exam sign-up** — all from within ASN.
- Developer framing: *"this is how skilling turns into something I can point to — not 'I just took the training' but 'here's the credential that says I can do it, I can ship it.'"*

### Team Progress Tracking (Lead View)
For the final segment, Shri shifts back to the **lead perspective** to see **how the playlist is landing** — not just whether content was consumed/checked:
- **"View shared progress"** shows progress **across a specific playlist**.
- He can see **where the team is stuck** (and where he is, from his own pre-curation pass), and the **same view applies to Matt** — e.g., Matt has started with **fundamentals**; if Matt needs support, **this is where the lead would intervene**.
- **Sprint mapping:** playlists can be **dropped into a sprint** — e.g., a **4-week sprint**, or **two 2-week sprints spread across four weeks** — tracked **week over week** against the **deliverable** (here: a **production-ready agent**).

### Recap & Next Steps
Quick recap of what was shown:
- **AI Skills Navigator** = official Microsoft content repository for skilling, containing **Microsoft learning paths, modules, applied skills, certifications, skilling sessions, and LinkedIn content**.
- An **AI-assisted playlist authoring tool** that is **catalog-aware** and builds a **sprint-aligned curriculum** for a deliverable.
- The **learning agent in Microsoft 365 Copilot**.

**Calls to action:**
1. **Sign into AI Skills Navigator**, **register**, and **create / modify your profile** to get personalized recommendations.
2. **Register for Skills Fest** — an upcoming event running **June 8–12**, registrations open — to keep the momentum going.

## 🛠️ Products / Features / Technologies Mentioned
- **AI Skills Navigator (ASN)** — Microsoft's official single-place content repository for tech skilling (Learn paths/modules, applied skills, credentials, skilling sessions, LinkedIn Learning, curated YouTube).
- **Learning agent in M365 Copilot** — agent in the Copilot rail that surfaces learning in the flow of work; GA as of session date.
- **Work IQ** — powers personalized starter prompts and task recommendations in the learning agent, based on work activity + learning profile.
- **Team Skilling** — chat-with-agent feature for leads to curate playlists from objectives/goals/time constraints.
- **AI-assisted playlist authoring tool** — catalog-aware tool that reasons over a prompt and stitches a sprint-aligned playlist from the catalog.
- **"For You" / personalization page** — role- and preference-driven content recommendations.
- **Explore Content** — broader catalog browsing with curations by level, Expert Voices, and modality filters.
- **Expert Voices** — industry-trusted contributors featured in ASN.
- **Skilling Sessions** — hybrid digital/classroom learning with an AI virtual trainer.
- **AI virtual trainer** — hosts skilling sessions virtually.
- **Skilling session coach** — progress-aware AI coach grounded in the course content + Microsoft Learn; runs knowledge checks and answers questions.
- **AI-generated podcasts** — two-voice conversational ~5-min summaries grounded in a Learn module (not TTS).
- **Applied skills** — immersive, hands-on, lab-based assessments.
- **Credentials / Certifications** — full Microsoft catalog hosted in ASN, with paths to prep, practice exams, and exam sign-up.
- **View shared progress** — lead-facing team progress tracking across a playlist.
- **Microsoft Learn** — source of learning paths, modules, and credential prep/exam details.
- **LinkedIn Learning** — content source integrated into ASN and the learning agent.
- **Curated Microsoft official YouTube channels** — video content source.
- **Microsoft Teams** — channel through which assigned playlists are delivered/accepted.
- **Microsoft 365 Copilot** — host environment for the learning agent and the team's production agent target platform.
- **Copilot Studio** — agent-building platform referenced in modules and credentials.
- **Microsoft Graph** — grounding/connector target for the team's agent.
- **SharePoint connectors** — grounding/connector target for internal agents.
- **Microsoft Foundry (Azure)** — referenced for evaluating the agent. *(Caption said "foundry azure Microsoft foundry"; interpreted as Azure AI Foundry.)*
- **Power BI** — used to instrument/visualize telemetry.

## 🚀 Announcements / What's New
- **Learning agent in M365 Copilot — Generally Available (GA) as of the session date** to all M365 Copilot users. Org-deployable to unlock enterprise content sources, admin upskilling, and agent reporting.
- **AI Skills Navigator content inside the learning agent — "Coming soon."**
- **Learning agent in Copilot Chat — coming in the near future.**
- **Skills Fest event — June 8–12**, registrations open (call to action to register).
- Several **credentials are "newly updated" / newly available** (e.g., Copilot & agent administration fundamentals, Create agents in Copilot Studio, AI Agent Builder Associate, Azure AI apps and agents developer associate).

## 💡 Demos
- **Signed-out homepage** — showed role/level content segmentation (Developer track: AI-assisted coding, build & orchestrate agents, agentic DevOps). *Proves:* value is visible before any sign-in/onboarding.
- **Onboarding & personalization** — set roles of interest (AI Engineer, Data Scientist) + learning preference; "For You" page populated accordingly. *Proves:* lightweight profile inputs drive meaningful personalization.
- **Explore Content** — curations by level, Expert Voices, modality filter. *Proves:* breadth of catalog beyond personalized picks.
- **Team Skilling playlist authoring** — entered objective/requirements/constraints; agent reasoned (objective → topics → catalog search) and produced a 4-section playlist. *Proves:* AI can build a sprint-aligned, catalog-aware curriculum tied to a real deliverable.
- **Assign → accept playlist via Teams** — Shri assigned to Matt; Matt accepted the invite in Teams. *Proves:* lead-to-IC handoff is built in.
- **Learn module → podcast** — two-voice ~5-min grounded summary (audio failed live but explained). *Proves:* flexible modality for learners who prefer audio/on-the-go.
- **Curated YouTube video** — Copilot Studio fundamentals from official channels. *Proves:* video learners are supported with vetted content.
- **Skilling session** — AI virtual trainer + progress-aware coach with knowledge checks and Q&A. *Proves:* classroom-grade, interactive, context-aware guided learning at scale.
- **Learning agent in M365 Copilot** — Work IQ starter prompts, task recommendations, "watch videos about AI prompting," "deepen learning with applied skills" → jump into ASN applied skill "create an AI agent." *Proves:* just-in-time learning in the flow of work, sourcing across ASN + LinkedIn + enterprise.
- **Credentials search** — searched "agent," opened a credential, viewed roles/skills, path to Microsoft Learn for prep/exam. *Proves:* learning converts into provable, shippable credentials.
- **Lead progress view ("view shared progress")** — team/individual progress against a sprint-mapped playlist, intervene where stuck. *Proves:* managers get outcome-oriented visibility, not just completion checkmarks.

## 📊 Notable Stats / Quotes
- **Playlist parameters:** mid-level developers, **4 weeks**, **8 hours/week**.
- **Playlist structure:** **4 sections** (agent design & lifecycle → grounding with Graph/SharePoint → evaluation → telemetry & monitoring).
- **Podcast:** generated with **2 distinct voices**, **~5-minute** module summary.
- **Sprint mapping:** e.g., a **4-week sprint** or **two 2-week sprints across four weeks**.
- **Skills Fest:** **June 8–12**.
- > "It's not just knowing that AI is available. It's knowing how to apply it to the job in front of you. That is the gap this experience is designed to close." — Matt Ernie
- > "Last year the upskilling conversation centered on workforce transformation… Today that conversation has expanded into work transformation." — Matt Ernie
- > "This is how skilling turns into something I can point to — not 'I just took the training' but 'here's the credential that says I can do it, I can ship it.'" — Matt (paraphrased)
- > An applied skill is "an immersive hands-on lab-based assessment that shows you you know something because you can do it."

## 🧠 My Notes / Follow-ups
- [ ] **Things to try:**
  - [ ] Sign into **AI Skills Navigator**, create a profile, set roles of interest + learning preference, and check the "For You" page.
  - [ ] Enable the **learning agent in M365 Copilot** (GA) and explore Work IQ–driven starter prompts/task recommendations.
  - [ ] Build a **Team Skilling playlist** via the AI authoring tool for a real deliverable (objective + constraints) and inspect the agent's reasoning.
  - [ ] Generate a **module podcast** and test the two-voice summary on a commute.
  - [ ] Run a **skilling session** end-to-end to experience the AI virtual trainer + coach + knowledge checks.
  - [ ] Search **credentials** in ASN for agent/Copilot certs and map a path to an exam.
  - [ ] **Register for Skills Fest (June 8–12).**
- [ ] **Questions:**
  - [ ] What are the exact admin/deployment requirements to light up enterprise content sources, admin upskilling, and agent reporting for the learning agent?
  - [ ] When exactly does ASN content land *inside* the learning agent, and when does the agent reach Copilot Chat?
  - [ ] Which licenses/SKUs are required for the learning agent vs. ASN itself?
  - [ ] Confirm exact credential names (captions garbled "AI Agent Builder Associate" / "Azure AI apps and agents developer associate").
  - [ ] Is the playlist authoring agent available to all leads, or gated by tenant/role?
  - [ ] Does "Microsoft Foundry" = Azure AI Foundry for the evaluation step?
- [ ] **Relevant to:**
  - [ ] Team upskilling / ramp plans for AI platform & agent-building teams.
  - [ ] Anyone shipping production agents on M365 Copilot (Graph + SharePoint grounding, Foundry eval, Power BI telemetry).
  - [ ] Managers needing outcome-based progress tracking across sprints.

## 🔗 Related
- [[Microsoft 365 Copilot]]
- [[Copilot Studio]]
- [[Microsoft Learn]]
- [[Azure AI Foundry]]
- [[Microsoft Graph]]
- [[Work IQ]]
- Skills Fest (June 8–12) — registration event
- AI Skills Navigator (ASN) — Microsoft official skilling repository
