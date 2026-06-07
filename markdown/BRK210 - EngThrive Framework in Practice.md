---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/developer-productivity
  - topic/engineering-culture
  - topic/ai
  - topic/metrics
source: https://www.youtube.com/watch?v=wDqipcHkaEM
session_code: BRK210
event: Microsoft Build 2026
speakers: Microsoft engineering leader (EngThrive program lead; works with Satya + SLT; prev. Google, Netflix)
duration_min: 48
aliases:
  - EngThrive Framework in Practice
---

# BRK210 — Future of Developer Productivity: Microsoft's EngThrive Framework in Practice

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Senior Microsoft engineering leader who owns the **EngThrive** function (drives developer-productivity transformation with Satya & the SLT; references J. Patrick's **Core AI** org; previously ran platform/infrastructure at Netflix and productivity work at Google) — name not stated on the recording  
> **Duration:** ~48 min (~28 min talk + ~20 min Q&A)  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=wDqipcHkaEM)

## 🎯 TL;DR
This talk is about using AI to change **how we work, not what we build** — i.e. transforming engineering productivity rather than shipping AI features. The speaker argues that simplistic activity metrics (lines of code, PR counts, tokens consumed) are not just useless but *actively harmful*, and introduces **EngThrive**, Microsoft's framework for making it "fast and easy to build great work," measured across three categories: **speed, ease, and quality**. The single most important idea is **outcomes over activity** ("progress over motion") — measure systems, not individuals, and target durable outcome metrics like *idea-to-customer time*, *innovation-time ratio*, and *time-to-first-PR*. Two real ~8-week case studies (recovering focus time; cutting time-to-first-PR) show small focused teams (5 and 8 people) driving company-wide impact by building a business rhythm (ROBs) around one outcome metric and applying AI to break old bottlenecks.

## 🔑 Key Takeaways
- **Two AI value propositions:** (1) AI to make *products* better, (2) AI to make *ourselves* better. This talk is entirely about #2 — transforming how engineers work.
- **Reductive productivity metrics are harmful.** "Lines of code" and "PR counts" were debunked as performance metrics 10–15 years ago, yet the AI news cycle made the industry forget it. Don't.
- **Where engineering time actually goes (industry P50):** ~40% innovation, ~45% keeping-the-lights-on, ~15% org responsibilities. Actual *active coding* is only **~10–15% of a developer's week**.
- **The objective is simple to say, hard to do:** *create more value, faster.*
- **The SDLC is shifting.** For teams in the "third wave," time/energy is moving heavily toward **plan** and **validate**; **create** (coding) is trending asymptotically toward zero; deploy/operate lag but also shrink. **Code is becoming an *output* of the system, not an input.**
- **Model capability is uneven across the stack:** code generation is near-elite; system design/architecture, verification, operations are progressively weaker; **taste** is something models won't reach — it stays a human contribution.
- **AI doesn't change the *definition* of productivity.** Productivity = ability to create outcomes; that's durable regardless of tools.
- **EngThrive mission:** "make it **fast and easy** to build **great work**." *Fast + easy* = the engineering experience/system; *great work* = what you make. All three (speed, ease, quality) must move together — no teeter-totter.
- **Measure systems, not individuals.** "Idea to production" or "build completion time" describe the *system* you operate in, not personal performance. Individual performance is a separate, more nuanced conversation.
- **The three flagship outcome metrics:** **Idea-to-customer** (calendar time idea → in customer hands), **Innovation-time ratio** (drive from ~39% toward 80–90%), and **Quality** (defect-escape / incidents-per-PR, mean-time-to-mitigate, customer-love).
- **Activity metrics are useful for understanding behaviour change — but never *target* them.** Targeting an activity metric destroys its fidelity (e.g. "token maxing").
- **Gaming an *outcome* metric is fine — you create the success you sought.** A no-op first PR still proves your machine/infra/deploy/review loop all work. "Game an outcome metric → you get promoted."
- **Operating principles:** create space to find/fix bottlenecks; **leadership accountability at the highest level** (started with Satya + SLT 3 yrs ago); **continuous improvement, not hitting a fixed benchmark.**
- **Consistent company-wide metrics matter enormously** — fragmented metrics prevent system optimization.
- **It's always the right time to start** — early wins are low-hanging fruit; AI now lets small teams break decades-old bottlenecks fast.

## 📚 Detailed Notes

### Framing: two ways AI creates value
There are two AI value propositions: using AI to make our **products** better (integrate into experiences, change customer experiences) and using AI to make **ourselves** better (change *how* we work, not *what* we build). The entire talk is about the second — transforming the way we work. The speaker keeps a large chunk (~20 min) for open Q&A.

### "Productivity in the AI era" — the question everyone asked
Everyone has heard some version of *"are engineers more productive with AI?"* It was asked for the right reasons: software engineering is fundamentally changing, and when the way you develop changes, you need insight or it's scary. That fear makes **overly simplified, reductive metrics attractive — but they're not helpful, and they go from not-helpful to *actively harmful*** when you're trying to drive transformation. The industry already learned (10–15 years ago) that "lines of code per engineer" or "PR counts" are meaningless as performance metrics — yet pop culture and the news cycle caused a collective amnesia in the last few months.

### Where developer time actually goes (longitudinal studies)
Microsoft runs longitudinal studies across the industry and internally and publishes papers (one at the start of this year). The foundational model splits developer time into **three buckets**:
- **Innovation** — ~40% (P50; sometimes cited as ~39%)
- **Running the business / keeping the lights on** — ~45%
- **Organizational responsibilities** (meetings, trainings, "citizen of the business" work) — ~15%

Drilling in: time actually *interacting with code/technical systems* is only about a quarter of that, and **active coding is somewhere between 10–15% of an engineer's week** in functioning, mature businesses. Everyone wishes for more, but that's the common pattern — which is exactly why reducing "productivity" to "how much code / how fast" is wrong. The real goal: **create more value, faster.**

### How work is changing — the three "waves" of AI interaction
A frame Microsoft uses internally and externally for how AI has changed work:
1. **Wave 1 — Transactional / direct interaction** (ChatGPT era, ~3.5 years ago): ask the model a question, get a back-and-forth answer.
2. **Wave 2 — Asynchronous agents** (became real ~Aug / mid-last-year): give an agent a task, it works asynchronously and can use tools.
3. **Wave 3 — Agents on complex goals** (emerging now): agents have **tools, memory, entitlements** and pursue rich, complex goal-seeking. Still "frothy" — open questions about responsibilities and how to empower agents — but maturing day by day.

### The SDLC is being reshaped (the "identity crisis")
Classic SDLC: **plan → create → validate → deploy → operate.** Historically (industry averages):
- **Operate** ≈ 75–80% of time
- **Create** (active coding) ≈ 10–15%
- **Plan / validate / deploy** ≈ the remainder

For teams moving into the third wave, this is **fundamentally different**: time/energy concentrates on **plan** and **validate**, while **create** "rapidly, asymptotically moves toward zero." Deploy and operate also shrink but lag behind coding's collapse. The profound shift: **code is becoming an *output* of the system rather than an *input*.** Code is still (today) the source of truth, but *how* and the *nuance* by which it's written is changing shape.

### Model capability is *not* uniform across the stack
The transition from input→output isn't happening evenly:
- **Code generation:** frontier/foundational LLMs can write a single line of code "as good as any of us."
- **System design / architecture / sustainability understanding:** not there yet; improving, but slower than raw code quality.
- **Verification:** some recent gains (things possible now that weren't 6 months ago) but **sublinear**.
- **Operations:** improving much more slowly.
- **Taste:** models "are not there at all," and the speaker doesn't expect that to change — **taste is what great engineers bring and will keep bringing.**

The reason for showing this: the nature of the highest-performing teams, *where the bottlenecks are*, and how to enable teams to do more are all continuously changing.

### Productivity itself is durable
AI changes much about how we work, **but it does not change the fundamental concept of productivity or how you measure it.** Productivity = the ability to create outcomes; the way you think about, measure, and understand outcomes is the same regardless of tools. (AI does help us *understand* outcomes in new, powerful ways — a Q&A thread.)

### EngThrive — the mission and the triad
**EngThrive** is Microsoft's name for understanding, shaping, and building programs around using AI to help engineers be more successful. Mission: **"make it fast and easy to build great work."**
- **Fast + easy** describe *how* we work — the engineering experience, the system, the whole SDLC life cycle.
- **Great work** describes *what* we make.

This **triad is non-negotiable** — you can't have just one or two. There's **no teeter-totter**: improving speed must not sacrifice ease or quality; you can't crank a "quality dial" while dialing down speed/ease. All metrics are organized into **three categories: speed, ease, and quality.**

### Activity vs Outcome — the single most important idea
> *"Progress over motion. Activity describes motion. Outcomes describe progress."*

If you take away one thing: **measure and target changes in *outcome*, not *activity*.** "How much more code did our engineers produce?" is an activity metric.
- **Activity metrics** come in two flavours: metrics describing *how we work* (AI adoption/usage, tokens consumed, agent-based PR counts) and metrics describing *what we did* (PR counts). These are **interesting and genuinely useful** for understanding how behaviours are changing — **but they are not metrics you target.**
- **Outcome metrics** describe *what you achieve*.

**Side effect of targeting activity — "token maxing":** people grind tokens for no real value because they've heard they're "expected" to be AI-active. The speaker's vivid illustration: any of us could become the company's largest token consumer / code producer overnight — spin up a junk repo, open a bunch of terminals, have them spew non-functional Python in 150–300-line chunks, commit and push endlessly ("burn burn burn"). Lots of energy, **zero value.** That's the inevitable failure mode of activity targets. Target outcomes instead and you create outcomes that matter.

### "Accelerate" — measure systems, not individuals
A fundamental principle (referred to as **"accelerate"**): it is **not focused on measuring individuals — it measures systems.** "How fast can I go from idea to production?" or "how long does my build take?" are **system** measures (the life cycle you operate in), not individual performance metrics. Distilling productivity into an individual metric is non-functional. **Employee performance is a separate, much more nuanced conversation.** Productivity is measured at the **system level** and by how that system impacts individuals.

### The three flagship outcome metrics
1. **Speed → "Idea to customer."** Calendar days/hours from an idea's origination (a PRD taking shape, a ticket with an idea but no design doc, maybe no engineer yet involved) all the way to value in the customer's hands (through experimentation/treatments/canaries). Powerful because you can drill in to find bottlenecks across the life cycle.
2. **Ease → "Innovation time" (innovation-time ratio).** The ~39% innovation slice from the time-allocation donut. **Drive it as high as possible — 80–90% is a great target.** Be highly attentive to what's *sucking up* engineering time and minimize it; AI is now breaking decades-old bottlenecks here.
3. **Quality.** Fairly well understood industry-wide: **defect-escape rate** (a.k.a. **incidents per PR**), **mean-time-to-mitigate** (responsiveness), plus a **customer-experience / product-love** measure. Also framed as measures of *defect escape, resilience, and experience*.

There's also a dense **"eye chart"** of the full metric set — shown for reference only — representing Microsoft's state-of-the-art, driven to be **as consistent as possible across the entire business**. The importance of **company-wide consistent metrics can't be overstated**: you need a common frame to optimize systems. Microsoft worked backwards toward this maturity over several years; starting from such a complete position is uncommon.

### From metrics to action — "good old-fashioned program management"
Once you have good outcome metrics, the next step is just disciplined program management driven by directional metrics. **Key operational principles of EngThrive:**
1. **Create space to identify, understand, and execute on bottlenecks** in the SDLC (use the measures to find them).
2. **Leadership accountability for developer experience at the absolute highest level** — started with **Satya and the SLT ~3 years ago**, when metrics were far less mature (began with a couple, then iterated and grew).
3. **Focus on continuous improvement, not hitting a particular benchmark.** This was the #1 question/fear leaders raised: *"a reorg happened, another team merged in, my benchmark will move and I'll be punished."* That's explicitly **not** the point — the goal is constantly asking *what can we do to improve developer experience / make it faster & easier to build great products.*

**Things to work backwards toward (practical North Star):**
- **Consistent company-wide metrics** — avoid fragmentation at all costs.
- **Leverage existing tooling:** e.g. **focus time** (a component of innovation time) comes **straight out of Viva Insights** out of the box.
- **Real-time dashboards** so people can self-serve and take action.
- **Business processes that drive accountability** — run **ROBs** (rhythm-of-business reviews).
- **Gather and share reusable patterns** — especially now that AI plays such a big role in transformation.

**Encouragement:** it's always the right time to start, because early on the **big wins are low-hanging fruit.**

### Case Study 1 — Recovering Focus Time (~8 weeks, ~5-person driving team)
**What focus time is:** uninterrupted hours per work week not broken up by meetings (and other interrupters). It's the **key to getting into flow.** Microsoft has extensive longitudinal/internal research showing **profoundly better outcomes on nearly every dimension** for developers with more focus time. (Done within **Core AI**, J. Patrick's organization.)

**How they started the flywheel (process, not heavy tech):**
1. **At senior-leadership level, picked ONE metric** to focus on — rather than telling the whole org to go find the "optimal" metric. They used **developer surveys** to find top pain points; "**feeling fragmented / not enough time to focus**" rose to the top.
2. **Defined roles with clear accountability** — every engineering leader at the highest level was responsible for moving the metric, with clear intention/focus.
3. **Bi-weekly reviews** — every 2 weeks leaders convened; each got ~5 minutes within an hour to present: current data, what they're digging into, the changes they're making, and report-back in 2 weeks (decide to double-down, pivot, or evolve). **Every conversation grounded in the data.**
4. **Data source:** Viva Insights focus time, enriched with additional developer instrumentation/telemetry.

**Outcomes (in 8 weeks):**
- **+2.1 hours of focus time recovered per engineer per week (P50).**
- **+13% PR velocity** — noted as an *activity* change (a behavioral indicator that developers got back into flow), not the outcome target.
- **−25% in "bad developer day" telemetry** (a recently published EngThrive paper dives deeper into "bad developer days").
- Decrease in several **wasteful meeting patterns** across the org.
- Net **≈ 55,000 hours of engineering time recovered** through "good hygiene and cleanup."

**Why this example matters:** done **fast**, and **mostly *not* built on AI directly** — it used information *derived from* AI. Manifesting this data is only possible now because AI can analyze it into a great outcome metric you can act on. Part of the fragmentation came from **operational toil (keeping the lights on)** — which is exactly where AI was then applied. **This was the origin of the SRE agent**: it handles many SRE/operational/system-health tasks "no one wants to do," freeing SREs to do richer, deeper SRE work (building deeper understanding of system shapes). Lesson: huge progress comes fast when you **build a business rhythm around one piece of outcome data.**

### Case Study 2 — Time to First PR (~8 weeks, ~8-person driving team; AI-centric)
**The metric (speed):** **time to first PR** — how long for a new hire (or someone changing teams) to submit their first PR on that team. **Target: < 1 week.** At the start, company-wide it was **more than a week** (a decent amount more), affecting tens of thousands of technical staff.

**Why it matters:** getting into the real development experience fast **changes multi-year trajectories** — strong empirical correlations with long-term engineer success, not just intuition.

**Four major interventions (over 8 weeks):**
1. **Built "First Mate" agent** — present on **day zero**; the moment a person is online they're attached to it. It has info about their team/destination and helps them begin engineering work, land their **first PR**, then progress toward their **10th PR**. (They track **time-to-first-PR, time-to-10th-PR, and time-to-30th-PR.**)
2. **Improved pull-request-workflow documentation** — surprisingly, far more valuable **for consumption by the First Mate agent** than by humans, creating a flywheel of fast agent self-improvement.
3. **Created video exercises** — visual walkthroughs of creating a PR. Sounds trivial, but Microsoft's **internal first-party systems differ** from external Azure tooling, so visuals were **astonishingly effective.** They hadn't done this before simply because there was **no impetus** — the outcome-metric focus created the impetus to do the previously deprioritized thing.
4. **Communicated to managers org-wide** (via a company all-hands leadership forum) to **raise expectations** for how fast new/transferring engineers onboard.

**The "isn't this gameable?" objection:** Yes — and **it doesn't matter.** Even a **no-op first commit to production** proves your machine works, you're attached to the infra, you understand the deployment cycle, code presence, and the code-review loop. **"When you game an outcome metric, you create the success you sought to create."** → *"Game an outcome metric → you get promoted. Game an activity metric → welcome to the game (anybody can do that)."*

**Outcomes & downstream effects:** hit the **<1-week target.** Time-to-first-PR is a powerful leading indicator: **by a person's 10th PR they can predict with high precision** that person's future coding activity and innovation time. Compressing/accelerating these produced **massive positive changes in developer behaviour**, correlating to faster **idea-to-production** and **more time creating new value / less toil.** AI made it possible to tackle a previously unreasonable problem (endless reading and maintaining of always-out-of-date documentation).

### Closing takeaway
Of everything: **outcomes over activity is the most important thing right now**, and it stays **durable** as AI keeps changing the tools in our hands. *Outcomes are everything; activities are constantly changing.*

### Q&A highlights
- **Q: Daily stand-ups and Teams messages — don't those kill focus time?**
  - **Teams messages are NOT counted** as focus-breakers — for remote teams they're the equivalent of work conversation. (Caveat: some message classes *are* distracting; teams share best practices on notification setup to minimize distraction.)
  - **Stand-ups / certain meeting classes are excluded.** Viva can detect meeting type (attendee count, rhythm, titles) to identify genuine working meetings. They also **compressed meetings into blocks** — guidance that ICs shouldn't be booked into meetings after ~1pm / in the afternoon.
  - **Every meeting must have an agenda, purpose, and clear outcome.** The org set the **expectation to decline/cancel** meetings lacking these — not just permission, an expectation.
- **Q: How did you measure "outcome" — just number/size of PRs? And is there a minimum focus-time block?**
  - **Flow block:** industry converges on **60 / 90 / 120 minutes**; Microsoft subscribes to **120 minutes** of contiguous uninterrupted time. (Speaker personally was in the 60–90 camp from Google/Netflix days but moved to 120 after seeing objective outcomes.)
  - **Outcomes are *not* PR volume.** PRs feature in some metrics (idea-to-customer relates to PRs; time-to-nth-PR uses a PR as a point in time) but **throughput/volume/flow is deliberately *not* a metric.** Reiterated: activity metrics show how behaviours change, but **the moment you set an incentive around an activity metric it loses all fidelity and becomes meaningless.**
- **Q: How do you understand "more" / change over time?**
  - They categorize change as **features, bugs/fixes, enhancements, reductions in operational burden, migrations, security/dependency work** (tied to the **Secure Future Initiative**). For heavy-coding teams they separate **new features vs. work needed just to keep systems alive**, so idea-to-customer can be understood as **throughput/volume** as well as calendar time.
- **Q: How do you get executive buy-in to care about outcome metrics?**
  - No easy answer — the answer is **speak up.** *"We have way more power than we think."* ICs and first/second-line managers can say *"it is impossible / too hard for me to do the right thing — here's an idea to improve our speed/ease/quality."* It doesn't mean stop all work. **AI now lets small, focused, ambitious teams (5 and 8 people, <2 months) drive company-wide change** by tackling classic bottlenecks fast. And the **common language of outcomes-over-activity is itself one of the most effective change levers** — even execs rooted in decades-old ways need that understanding built. The fruit is **incredibly low-hanging.**

## 🛠️ Products / Features / Technologies Mentioned
- **EngThrive** — Microsoft's framework/function for using AI to make engineers more successful; mission "make it fast and easy to build great work," measured via speed/ease/quality.
- **"Accelerate"** — the underlying measurement philosophy/approach: measure *systems*, not individuals.
- **First Mate (agent)** — onboarding agent attached to new/transferring engineers on day zero; helps them land their first PR and progress to their 10th; central to the time-to-first-PR case study.
- **SRE agent** — Microsoft agent that handles SRE/operational/system-health tasks no one wants to do; originated from the focus-time case study, freeing SREs for deeper SRE work.
- **Viva Insights** — Microsoft 365 analytics tool that provides **focus time** out of the box; the primary data source (enriched with extra telemetry) for the focus-time case study, and can classify meeting types.
- **Microsoft Teams** — messaging/collaboration; deliberately *not* counted as a focus-time interrupter.
- **"Bad developer day" telemetry** — an EngThrive signal/metric (decreased 25% in case study 1); covered further in a recently published EngThrive paper.
- **ROBs (Rhythm of Business reviews)** — the recurring business-process cadence used to drive accountability and change.
- **Secure Future Initiative (SFI)** — Microsoft's security program; used as an example of separable work categories (security updates, dependency management, migrations) when analyzing throughput.
- **Developer surveys** — qualitative data source used to pick which metric to target (surfaced "feeling fragmented").
- **Frontier / foundational LLMs** — referenced for their strong single-line code generation vs. weaker design/verification/operations capability.
- **Real-time dashboards** — recommended tooling so teams self-serve and act on the metrics.

## 🚀 Announcements / What's New
None explicitly announced as product releases/previews/GA — this is a framework/practices talk. Items referenced as existing or recently published:
- A **recently published EngThrive paper** (within the last couple of weeks) covering **"bad developer days"** in more depth.
- An earlier **longitudinal developer-time study/paper** published at the start of the year.
- **First Mate** and the **SRE agent** are described as in-use internal Microsoft agents (not framed as new Build announcements).

## 💡 Demos
No live software demos. The talk was delivered via slides and **two real internal case studies** (focus time; time-to-first-PR), described above rather than demonstrated live.

## 📊 Notable Stats / Quotes
**Stats:**
- Industry P50 time split: **~40% innovation / ~45% keeping-the-lights-on / ~15% org responsibilities**; innovation slice cited as **~39%**.
- **Active coding ≈ 10–15% of an engineer's week.**
- Historical SDLC time: **operate ≈ 75–80%**, create ≈ 10–15%.
- Innovation-time target: **drive toward 80–90%.**
- ChatGPT era began **~3.5 years ago**; Wave-2 agents became real **~August / mid-last-year.**
- Flow blocks debated at **60 / 90 / 120 min** — Microsoft uses **120 min.**
- **Case study 1 (8 weeks):** +**2.1 hrs** focus time / engineer / week (P50); +**13%** PR velocity; −**25%** bad-developer-day telemetry; **≈55,000 hours** of engineering time recovered.
- **Case study 2 (8 weeks):** time-to-first-PR cut from **>1 week** to the **<1 week** target.
- Case-study driving teams were **5 people** and **8 people**; both done in **<2 months.**
- The two flagship case studies ran in **8–12-week** windows.

**Quotes:**
- *"Progress over motion. Activity describes motion. Outcomes describe progress."*
- *"Code is rapidly becoming output of a system rather than input of the system."*
- *"Taste is definitely one of the aspects that we bring to the table … and will continue bringing to the table."*
- *"When you game an outcome metric, you create the success that you sought to create."*
- *"If you can game an outcome metric, you get promoted. If you can game an activity metric — welcome to the game."*
- *"We have way more power than we think."* (on IC/manager agency to push for change)
- *"It's always the right time to get started because … the big wins are low-hanging fruit."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Adopt **outcomes-over-activity** language in your own team; pick **one** outcome metric (e.g. idea-to-customer or focus time) and run **bi-weekly data-grounded reviews**. Pull **focus time from Viva Insights** if available. Consider a lightweight onboarding agent / better PR-workflow docs + short videos to cut time-to-first-PR.
- [ ] Questions: Which **"bad developer day"** signals does the new EngThrive paper define, and can they be reproduced outside Microsoft? How is **idea-to-customer** instrumented end-to-end (ticket → canary)? How do you keep **company-wide metric consistency** without it becoming bureaucratic?
- [ ] Relevant to: Engineering leadership / DevEx programs; DORA / SPACE / "Accelerate" metric discussions; AI-transformation strategy; onboarding & SRE-agent automation.

## 🔗 Related
- [[2026 Build Session List]]
- DORA / "Accelerate" (Forsgren et al.) metrics; SPACE framework for developer productivity
- Microsoft EngThrive / "bad developer days" research paper (2026)
- 