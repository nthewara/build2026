---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-models
  - topic/foundation-models
  - topic/microsoft-ai
  - topic/ai
source: https://www.youtube.com/watch?v=5vz1pUSpRAE
session_code: DEM323
event: Microsoft Build 2026
speakers: Dave Citron (CVP of Product, Microsoft AI)
duration_min: 18
aliases:
  - Under the hood of Microsoft AI models
---

# DEM323 — Under the hood of Microsoft AI models

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Dave Citron — CVP of Product, Microsoft AI  
> **Duration:** ~18 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=5vz1pUSpRAE)

## 🎯 TL;DR

Microsoft AI shipped **seven first-party foundation models** across image, transcription, voice, coding, and reasoning — all **hill-climbed from scratch with no distillation and no teacher model**. The crown jewel is **MAI Thinking 1**, Microsoft's first frontier reasoning model: a mixture-of-experts architecture with 35B active / ~1T total parameters and a 256K context window, trained on 30T+ tokens of in-house, commercially licensed data, then climbed via reinforcement learning (GRPO) from near-zero to **97% on AIME**. The session is a technical deep dive into the lab's "humanist superintelligence" philosophy, the data and RL pipeline behind Thinking 1, and **Microsoft Frontier Tuning** — a way for any developer or organization to run their own hill-climbing loop on these models inside their secure tenant, demonstrated by a Land O'Lakes case study that beat all frontier models at 10x lower cost.

## 🔑 Key Takeaways

- **Seven models announced** across five modalities: Image 2.5, Voice 2, Transcribe 1.5, Code 1 Flash, and Thinking 1 (plus Flash variants of several).
- **"We don't distill."** Every capability was earned through Microsoft AI's own training loop — no third-party weights, no black-box inheritance — giving full transparency, debuggability, and clean commercially licensed data lineage for enterprise.
- **MAI Thinking 1** is a Mixture-of-Experts model: **35B active parameters, ~1T total, 256K context window**, hill-climbed from scratch with no teacher.
- **Reasoning is learned via reinforcement learning** using **GRPO** with binary, verifiable rewards for math/code, plus **five custom innovations** to keep the RL climb stable across thousands of steps (AIME climbed near-zero → 97% in a steady log-linear line).
- **Three specialist models** (STEM, agentic, helpfulness & safety) were trained separately and then **merged** into one model with three areas of mastery.
- **Safety is an entire dedicated RL climb**, not a bolted-on filter — baked into the reward math so you "cannot trade safety for helpfulness," validated by 15 rounds of red teaming and 2,100+ adversarial scenarios.
- **Benchmark leadership punching above weight class:** AIME 25 @ 97, AIME 26 @ 94.5, LiveCodeBench @ 87.7, SweetBench Pro @ 52.8 (competitive with Opus 4.6), GPQA Diamond @ 84.2 — all from a 35B *active* parameter model.
- **Image 2.5** is #2 on the image-editing leaderboard, surpassing Nano Banana; already live in PowerPoint, rolling out to OneDrive, and on Foundry.
- **Transcribe 1.5** is positioned as the world's most accurate transcription model across **43 languages**, up to **5x faster** than rivals, beating Gemini and OpenAI flagship transcription models.
- **Code 1 Flash** ships as the default in GitHub Copilot inside VS Code today — strong agentic coding from just a 5B active-parameter model.
- **Microsoft Frontier Tuning** lets every org build its own "hill-climbing machine": private (data never moves), cost-efficient, context-aware, and lock-in-free; usage feeds back into the next training cycle so the model compounds over time.
- **Land O'Lakes proof point:** frontier-tuned **MAI Thinking 1 Flash** hit a **89.3% quality score** (higher than all frontier models) at **10x lower cost** on a real business workflow.

## 📚 Detailed Notes

### Session framing & structure
Dave Citron, CVP of Product at Microsoft AI, opens with the explicit goal of explaining *how* the headline numbers from Mustafa Suleyman's keynote earlier that morning were actually achieved — "if you were watching the keynote and thinking 'cool numbers, but how did they actually do that?' then this is the talk for you." The session is structured as: (1) the philosophy behind the models and how the lab builds; (2) a walkthrough of all seven models being shipped; (3) a deep dive into **MAI Thinking 1** — architecture, training recipe, and the reinforcement-learning system; and (4) **Frontier Tuning**, so customers can run their own hill-climbing loop on top of what Microsoft built.

### The philosophy: Humanist Superintelligence
Before going model by model, Citron stresses that philosophy drives real technical decisions at the lab. Microsoft AI calls its approach **humanist superintelligence** — state-of-the-art AI explicitly designed to **serve people and organizations, not replace them**. "Humanist" is described as non-decorative and means three concrete things:
- **Human first** — the model always prioritizes human well-being.
- **Serve, not replace** — AI that augments what people can do.
- **Platform commitment** — keep developers at the frontier.

### Why "we don't distill" — the core technical decision
The philosophy has three concrete implications for how they build, the most important being: **they do not distill.** Distillation transfers a stronger model's behavior into a smaller one and can produce fast gains (many labs do it), but it makes the **teacher's capability the practical ceiling** for the student. It also fails to test whether the lab's own training pipeline can climb from weak initial performance or make progress in domains where no good teacher exists. So Microsoft AI **hill climbs from scratch** — every capability is earned through their own training loop, not borrowed. The payoff is **full transparency and control**: they know exactly what went in (clean, commercially licensed data), with no third-party weights and no black-box inheritance, so every component can be debugged, audited, and improved. This is repeatedly framed as the foundation that enterprise customers need.

### Model 1 — Image 2.5 (image generation & editing)
Microsoft's image generation and editing model, now **#2 on the EleutherAI image-to-image leaderboard**, surpassing **Nano Banana** — described as a real step change over prior iterations. Its differentiator is **precision**: it executes edit instructions with fidelity and consistency that other models struggle with. It cleanly handles complex compositional edits — changing lighting, adding objects that match the environment, and editing one region while leaving everything else intact. The flagship **2.5** model is optimized for maximum quality (professional-grade output for creative and enterprise workflows) and is **already live in PowerPoint, rolling out to OneDrive, and available on Foundry now**. The **Flash variant** keeps the same architecture but is optimized for high-volume production — more throughput, minimal quality trade-off, significantly lower cost per token (Citron noted the Flash variant delivers quality at production scale at roughly **a third of the cost**). Users are encouraged to try it on the **MAI playground** website, even from a phone.

### Model 2 — Voice 2 (speech generation)
Microsoft's latest speech generation model, differentiated by **naturalness**. The team went deep on **prosody** — the rhythm, stress, and intonation that make speech sound like a person rather than a text-to-speech engine. The headline new capability is **fine-grained emotional control**: you can tune not just what the voice says but how it *feels* — warm, urgent, conversational, joyful. Available **today in 15 languages**, with many more coming. It also does high-fidelity **voice cloning** from just a tiny amount of source audio. A **Flash variant** is coming, designed for **voice agents** with incredibly low latency. (Citron also cited an under-150ms figure and a 72% blind-listening-test preference for Voice 2 in the model overview.) A live "joy" emotion demo was attempted on stage but suffered audio issues before partially playing.

### Model 3 — Transcribe 1.5 (transcription)
Positioned bluntly as "simply the best transcription model in the world. Not close. The best." Accuracy spans **43 languages**, beating **Gemini and OpenAI's flagship transcription models** on head-to-head accuracy benchmarks. Critically, it's optimized for **real-world use** — noisy environments, accents, domain-specific terminology, and multiple speakers — not just benchmark accuracy. On **Artificial Analysis** speed benchmarks it is "in a league of its own," up to **5x faster** than rivals while also being more accurate ("no one else comes close in both dimensions at once"). It is being integrated across the Microsoft stack — **Copilot, Teams, GitHub, Dynamics 365** — and is on **Foundry now**. Summed up as the fastest, most accurate, and most cost-effective transcription model available; "if you're building anything involving speech-to-text, this is your model."

### Model 4 — Code 1 Flash (coding)
A dedicated coding model **built from the ground up for agentic coding tasks at speed**. Benchmarks: **71.6 on SweetBench Verified** and **51.2 on SweetBench Pro** (one of the hardest real-world coding benchmarks). It's optimized to be cost-effective for high-throughput workloads and is a **5B active-parameter** coding model delivering "amazing coding performance." It is **already shipping as the default in GitHub Copilot inside VS Code** — Citron repeatedly urges developers to try it there today and send feedback.

### Model 5 (deep dive) — MAI Thinking 1 (reasoning)
**Microsoft's first reasoning model**, and the focus of the session.

**Architecture:** Mixture of Experts (MoE), **~35 billion active parameters, ~1 trillion total**, with a **256K context window**. It "punches well above its weight class" and was **hill-climbed entirely from scratch — no distillation, no teacher model**, with clean, commercially licensed data lineage suitable for shipping to enterprise customers. A **100+ page tech report** detailing exactly how it was built was released the same morning on the lab's website.

**Three guiding principles** governed every decision:
1. Capabilities should be **learned, not inherited**.
2. **Simplicity is sustainable**.
3. **Scientific rigor over shortcuts**.

**The data story (what they *didn't* use):** No open-source training sets and no synthetic data. They actively **hunted down AI-generated content on the web and removed it** from the training set (a task getting harder every month), and the **benchmarks are decontaminated** so the numbers are real.

**The data story (what they *did* use):**
- **Pre-training:** **30 trillion tokens** sourced and processed entirely in-house — web, code, books, papers, multilingual text, and domain-specific materials, with every pipeline owned end-to-end.
- **Mid-training:** an additional **3.55 trillion tokens** of curated STEM, math, and coding data with **verifiable answers** and code that either runs or doesn't. This phase **extends context to 256K** and sets up the RL climb.

**The RL climb (where the model learns to think):** The base algorithm is **GRPO** — generate a group of rollouts for a problem, score them against a verifiable ground truth, and reinforce the better ones. For math and code the **reward is binary** (did you get the right answer?). Running RL for thousands of steps on a model this size "doesn't just work," so the team built **five innovations** that together keep the climb stable across thousands of steps. The AIME score rising from **near-zero to 97% in a steady log-linear line** is offered as evidence those techniques compound correctly.

**Specialist merge:** They trained **three specialist models — STEM, agentic, and helpfulness & safety — and merged them** into a single model with three areas of mastery.

**The safety climb:** Safety is **not a filter bolted on at the end** — it's an **entire dedicated RL climb** with a reward model trained on **human preference**. By design, "you cannot trade safety for helpfulness — it's baked into the math." This was hardened with **15 rounds of red teaming** across early, mid, and late training — Microsoft's AI red team **plus independent external vendors**, covering **over 2,100 adversarial scenarios**. The result: on the safety/helpfulness scatter plot, **MAI sits above and to the right of Claude Sonnet 4.6 on about five of eight categories** — i.e., more helpful *and* safer at the same time.

**Results that the pipeline produced (with anti-contamination notes):**
- **AIME 25: 97** and **AIME 26: 94.5** — AIME 26 problems were released *after* the training cutoff; the model has never seen them.
- **LiveCodeBench: 87.7** — continuously adds new problems to prevent contamination.
- **SweetBench Pro: 52.8** — real GitHub issues on real codebases; competitive with **Opus 4.6**.
- **GPQA Diamond: 84.2** — graduate-level biology, chemistry, and physics questions answered **without using any search tools**.

The recurring thesis: this is only a **35B active-parameter** model — not the largest — yet fully competitive "because the capabilities were learned, not inherited." Citron summarizes Thinking 1 as "a clean foundation, well-designed climb, scientific rigor."

### Microsoft Frontier Tuning
The closing topic and the bridge from "our models" to "your models." The premise: most AI products today ask you to **rent a generic model and hope it works** for your business — "we don't think that's good enough." **Frontier Tuning** lets every developer and org build its **own hill-climbing machine** — a model that knows your work, your language, and your data, trained **entirely inside your environment**.

**Four things that matter for Frontier Tuning:**
- **Private** — your data never moves.
- **Cost-efficient** — you don't burn dollars on tokens you don't need.
- **Smarter on your actual context** — it improves on your real workflows.
- **You control the model** — no big-model lock-in, no dependency on anyone's roadmap but your own.

**The process:**
1. **Define your task** and what "good" looks like for your business.
2. **Bring your data** — M365 context, Azure Fabric context, workflows, domain expertise.
3. **Train inside your secure tenant**.
4. **Deploy** through either **Foundry or Copilot**.
5. **It doesn't stop** — real usage feeds back into the next training cycle, so the model gets better the more your org uses it. That feedback loop is what "hill-climbing machine" really means: it **compounds over time against your objectives, not a generic benchmark**.

### Real-world example — Land O'Lakes
**Land O'Lakes** needed to generate **product quality reports from tasting-panel discussions**. Microsoft **frontier-tuned MAI Thinking 1 Flash** on that specific task. The result: **89.3% quality score — higher than all frontier models — and 10x more cost-efficient.** Citron stresses this is "not a small model beating a big one on a toy task" but a **tuned model beating the best generalists on a real business workflow at a fraction of the cost.**

### Availability & wrap-up
- **Image 2.5, Voice 2, Transcribe 1.5** — live in **Foundry today**, and playable on the **MAI playground** website (works on mobile).
- **Thinking 1** — live on **Foundry** for a couple of **private-preview** customers, expanding soon; interested testers should **sign up on the Foundry website**.
- **Code 1 Flash** — available **right now in VS Code** with GitHub Copilot.
- All models will also be available across **Base Ten, OpenRouter, and Fireworks**.
- Learn more at the **Foundry website** or **microsoft.ai** — model cards, API documentation, and pricing.
- Citron closes by noting the team is on-site all week with more sessions and a demo booth, inviting feedback via social channels: "We're just getting started as a lab, and we have much more to come."

## 🛠️ Products / Features / Technologies Mentioned

- **MAI Image 2.5** (flagship + Flash) — image generation & editing
- **MAI Voice 2** (+ Flash) — speech generation with emotional control & voice cloning
- **MAI Transcribe 1.5** — multilingual transcription (43 languages)
- **MAI Code 1 Flash** — agentic coding model (5B active params)
- **MAI Thinking 1** (+ Thinking 1 Flash) — frontier reasoning MoE model
- **Microsoft Frontier Tuning** — in-tenant model tuning / hill-climbing loop
- **MAI Playground** (website, mobile-friendly) — try the models
- **Azure AI Foundry** — deployment & API surface for the models
- **GitHub Copilot in VS Code** — ships Code 1 Flash as default
- **Microsoft 365 / PowerPoint / OneDrive / Teams / Dynamics 365 / Copilot** — integration surfaces
- **Azure Fabric** & **M365 context** — data sources for Frontier Tuning
- **GRPO** (Group Relative Policy Optimization) — base RL algorithm
- **Mixture of Experts (MoE)** — Thinking 1 architecture
- Third-party distribution: **Base Ten, OpenRouter, Fireworks**
- **microsoft.ai** — model cards, API docs, pricing

## 🚀 Announcements / What's New

- **Seven new Microsoft AI first-party models** announced (image, transcription, voice, coding, reasoning) — all built from scratch with no distillation.
- **MAI Thinking 1** — Microsoft's **first frontier reasoning model** (MoE, 35B active / ~1T total, 256K context), with a **100+ page technical report** published the same morning.
- **Microsoft Frontier Tuning** — new capability to tune these models privately inside a customer's own secure tenant, deployable via Foundry or Copilot.
- **Image 2.5** now **#2 on the image-editing leaderboard**, surpassing Nano Banana; **live in PowerPoint**, rolling out to **OneDrive**, available on **Foundry**.
- **Code 1 Flash** is now the **default coding model in GitHub Copilot inside VS Code**.
- **Voice 2** adds **fine-grained emotional control** and **voice cloning**, in **15 languages**.
- **Flash variants** announced/forthcoming for Image, Voice, and Thinking, targeting production scale, voice agents, and tunable workloads respectively.
- Models rolling out to third-party platforms: **Base Ten, OpenRouter, Fireworks**.

## 💡 Demos

- **Voice 2 "joy" emotion demo (live, on-stage):** Citron attempted to play a sample of the Voice 2 model speaking with a joyful emotion ("I just got the best news ever. I cannot stop smiling... This is the happiest I have ever been"). The demo hit **audio playback issues** ("I'm not getting any audio... Can you hear that?") before partially playing through; Citron acknowledged it was "a little hard to hear" in the noisy room and pointed the audience to the website for clearer examples of the full emotional range and voices.

## 📊 Notable Stats / Quotes

**MAI Thinking 1 architecture & training:**
- **35B active parameters / ~1T total / 256K context window** (MoE)
- **30T tokens** pre-training (in-house) + **3.55T tokens** mid-training (curated STEM/math/code)
- **15 rounds** of red teaming; **2,100+** adversarial scenarios
- Sits **above & right of Claude Sonnet 4.6 on ~5 of 8** safety/helpfulness categories

**MAI Thinking 1 benchmarks:**
- **AIME 25: 97** · **AIME 26: 94.5**
- **LiveCodeBench: 87.7**
- **SweetBench Pro: 52.8** (competitive with Opus 4.6)
- **GPQA Diamond: 84.2** (no search tools)

**Other models:**
- **Image 2.5:** #2 on EleutherAI image-to-image leaderboard; Flash ≈ **1/3 the cost**
- **Transcribe 1.5:** **43 languages**, up to **5x faster** than rivals, beats Gemini/OpenAI flagships
- **Voice 2:** preferred on **72%** of blind listening tests; Flash **under 150 ms** latency; **15 languages**
- **Code 1 Flash:** **71.6** SweetBench Verified, **51.2** SweetBench Pro; **5B** active params
- **Land O'Lakes (frontier-tuned Thinking 1 Flash):** **89.3% quality score**, **10x** more cost-efficient than all frontier models

**Quotes:**
- "We call our approach **humanist superintelligence**... designed to serve people and organizations, not replace them."
- "**We don't distill.**... So we hill climb from scratch. Every capability in these models was earned through our own training loop, not borrowed."
- "**Capabilities should be learned, not inherited. Simplicity is sustainable. Scientific rigor over shortcuts.**"
- "**You cannot trade safety for helpfulness. It's baked into the math** with this design."
- On Transcribe 1.5: "Simply the best transcription model in the world. **Not close. The best.**"
- "We're just getting started as a lab, and we have much more to come."

## 🧠 My Notes / Follow-ups

- [ ] Things to try:
  - Test **Code 1 Flash** as the default in **GitHub Copilot / VS Code** on a real agentic coding task and compare to current default.
  - Try **Image 2.5** editing in **PowerPoint** and on the **MAI playground** (mobile) — test compositional edits (lighting changes, object insertion, region-locked edits).
  - Experiment with **Voice 2** emotional control and voice cloning on the MAI playground / Foundry.
  - Run **Transcribe 1.5** on a noisy, multi-speaker recording with domain jargon to validate the real-world accuracy claims.
  - Sign up on the **Foundry website** for **Thinking 1** private preview access.
- [ ] Questions:
  - What are the **five RL stability innovations** named in the 100+ page tech report? (Worth reading the report directly.)
  - How exactly is the **three-specialist model merge** (STEM / agentic / safety) performed — weight averaging, routing, or something else?
  - What does **Frontier Tuning** cost and what minimum data volume is needed for a meaningful quality lift?
  - How is "AI-generated content removal" from the web corpus done at 30T-token scale, and how is it validated?
  - Where does **Thinking 1** land vs **GPT-5 / Gemini 3 / Claude Opus 4.6** on a head-to-head reasoning suite beyond the cherry-picked benchmarks?
- [ ] Relevant to:
  - Enterprise teams needing **commercially licensed, auditable** model lineage (clean-data requirement for regulated industries).
  - Anyone building **voice agents** (Voice 2 Flash, sub-150ms) or **speech-to-text** pipelines (Transcribe 1.5).
  - Platform/agent teams evaluating **GitHub Copilot** model defaults (Code 1 Flash).
  - Solutions architects scoping **domain-specific fine-tuning** in-tenant via Frontier Tuning (M365 + Azure Fabric context).
  - Cost-optimization conversations — Flash variants + Frontier Tuning as the "smaller, tuned, cheaper, better" play vs renting generalist frontier models.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[Microsoft AI (MAI) models]]
- [[MAI Thinking 1]]
- [[Microsoft Frontier Tuning]]
- [[Azure AI Foundry]]
- [[GitHub Copilot]]
- [[Reinforcement Learning - GRPO]]
- [[Mixture of Experts (MoE)]]
- [[Humanist Superintelligence]]
- Keynote: Mustafa Suleyman — Microsoft AI at Build 2026