---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/observability
  - topic/genai
  - topic/monitoring
  - topic/ai
source: https://www.youtube.com/watch?v=NtLuXXNKbJw
session_code: ODSP907
event: Microsoft Build 2026
speakers: Datadog (LLM Observability team)
duration_min: 13
aliases:
  - Monitor GenAI applications beyond golden signals
---

# ODSP907 — Monitor GenAI applications beyond golden signals

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Datadog (LLM Observability team — partner/sponsor session)  
> **Duration:** ~13 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=NtLuXXNKbJw)

## 🎯 TL;DR
A focused Datadog partner talk arguing that the classic "golden signals" (latency, errors, traffic, saturation — LETS) are still the bedrock of monitoring but leave you **blind to what matters most in GenAI apps**. GenAI is fundamentally different because of non-deterministic behavior, a variable/unpredictable cost structure, new attack vectors, and subjective quality. The session walks each golden signal and shows how to extend it for GenAI (e.g. multi-stage latency, model-level error categories, per-feature/per-model traffic, GPU + rate-limit saturation), then adds **three new monitoring dimensions** — **cost**, **safety/security**, and **quality**. It closes by mapping all of this onto Datadog **LLM Observability**, which captures the standard signals plus token/cost tracking, prompt/response eval, PII masking, and prompt-injection detection in one place. The recurring thesis: *a perfect "200 OK" means nothing if your model is hallucinating, leaking PII, or burning your budget one token at a time.*

## 🔑 Key Takeaways
- **Golden signals (LETS) aren't going away** — latency, errors, traffic, saturation remain the foundation; GenAI just demands you instrument them more granularly.
- **GenAI differs on four axes:** non-deterministic behavior, variable cost structure, new attack vectors, and subjective quality — so traditional approaches fall short.
- **Latency must be tracked per pipeline stage**, not just end-to-end: RAG retrieval time, the LLM call itself, external API calls, and total request time (still watch median + P95/P99).
- **Errors need a new category beyond HTTP 4xx/5xx:** LLM model errors such as context-length exceeded, safety-filter triggered, and model overloaded — segment by endpoint, model, and user segment.
- **Traffic should be segmented by feature, user type, and model**, not just measured as raw RPS — this drives capacity, per-model rate-limit management, and cost control.
- **Saturation bottlenecks have shifted to GPU utilization and API rate limits / model-serving capacity** — the discipline is old, the bottlenecks are new.
- **Cost is dynamic and unpredictable** and can spiral silently via three mechanisms: **token creep**, **model drift**, and **uncached calls**.
- **Cost control = tag everything:** feature-level, user-level, model-level, and endpoint-level tagging give the attribution needed for chargeback, abuse detection, and optimization.
- **Safety/security threats are tiered:** critical = PII leakage + data exfiltration; high = prompt injection + jailbreaking; medium = denial-of-wallet + model extraction.
- **Security metrics that "don't look like errors":** prompt injection rate, PII detection rate, content moderation score, and jailbreak attempts.
- **Quality is the dimension that ultimately matters** but is subjective, context-dependent, and hard to quantify — there's no ground truth, context matters, hallucinations are a major challenge, and satisfaction is a spectrum not a binary.
- **Track six quality metrics:** hallucination rate, relevance score, user satisfaction, answer completeness, retrieval (RAG) quality, and response coherence.
- **Complete GenAI observability = LETS + cost + safety + quality** — together they cover health, financial spend, security posture, and output quality.
- **Datadog LLM Observability** is positioned as the single tool that unifies all four dimensions (auto-captured metrics, cost tracking, eval tooling, PII masking, prompt-injection detection).

## 📚 Detailed Notes

### Why GenAI breaks traditional monitoring — the four shifts
The talk opens by asking what makes GenAI applications *fundamentally different* from the software we've monitored for decades, and answers with four key shifts:
1. **Non-deterministic behavior** — the same input can produce different outputs, so assertions and binary pass/fail checks no longer hold.
2. **Variable cost structure** — spend is tied to token consumption and model choice, making it dynamic and hard to predict rather than a fixed infra line item.
3. **New attack vectors** — prompts become an attack surface (injection, jailbreaking, exfiltration) that classic web security wasn't designed for.
4. **Subjective quality** — "good" output is contextual and judged on a spectrum, not a deterministic correct/incorrect result.

These four shifts frame the rest of the talk: keep the golden signals, but layer new dimensions on top.

### The golden signals (LETS) — still the bedrock
The session uses **LETS** = **L**atency, **E**rrors, **T**raffic, **S**aturation as "the fundamental building block of all monitoring." The core message for each is that the *signal* stays the same but GenAI requires **more granular instrumentation and segmentation**.

#### 1. Latency — "how long does each request take?"
- Traditional practice: watch **median latency** (the average user experience, e.g. ~850 ms) plus **P95 / P99** to catch slow requests, outliers, and bottlenecks.
- For GenAI, total click-to-response time is not enough — you must **instrument latency at multiple stages within the GenAI pipeline**:
  - **RAG retrieval time** — how long it takes to find relevant documents.
  - **LLM call time** — the model invocation itself.
  - **External API call time.**
  - **Total request time.**
- Understanding the **latency breakdown** is critical for optimization and for pinpointing exactly where users experience delays.

#### 2. Errors — "what's the error rate and what types?"
- Traditional monitoring covers HTTP status codes (e.g. 400 client errors, 500 server errors).
- GenAI adds a **new category: LLM model errors** returned directly from the model provider, including:
  - **Context length exceeded.**
  - **Model safety filter triggered.**
  - **Model overloaded.**
- Best practice: **track error rates by endpoint, by model, and by user segment** to spot patterns quickly and stop small issues from becoming major outages.

#### 3. Traffic — "how much demand is the system handling?"
- Typically tracked as **requests per second (RPS)** over time to understand usage patterns and ensure capacity.
- For GenAI, the raw count of API calls isn't enough — **segment traffic** by:
  - **Feature** — e.g. internal chatbot vs external-facing summarization tool.
  - **User type** — e.g. premium vs new users driving the most traffic.
  - **Model** — which specific model (large vs small, expensive vs cheap) handles the majority of volume.
- Benefit: segmentation lets you optimize capacity, manage **model-specific rate limits** effectively, and control costs.

#### 4. Saturation — "how constrained are your resources?"
- Generally measured via utilization of critical infrastructure.
- For GenAI the **bottlenecks have shifted** to two new areas:
  - **GPU utilization.**
  - **API rate limits** (and model-serving capacity).
- The discipline is nothing new, but these are **new critical bottlenecks** to watch so the system can handle increased traffic.

### New Dimension 1 — Cost monitoring
Traditional LETS metrics "completely miss the financial implications" of GenAI. Because spend is dynamic and unpredictable, **without visibility your costs can and often will spiral out of control.**

#### The three ways cost escalates without warning
- **Token creep** — engineers or product managers quietly increase the context window to improve quality. Since cost is directly tied to token count, spend can jump **overnight** without any financial review.
- **Model drift** — a team swaps a faster/cheaper model for a slower/more expensive one under the premise of "better quality." Even with identical usage volume, this escalates spend.
- **Uncached calls** — the same query repeatedly hits the API when there's no effective caching layer, so you pay for the **exact same expensive model completion over and over** (redundant spend).

Without granular visibility into these three, costs escalate rapidly.

#### Cost attribution strategy — "tag everything"
A robust cost-attribution strategy comes down to **mandatory tagging** at four levels:
- **Feature-level tagging** (e.g. `summarization`, `text-to-speech`) → tells you which feature costs the most.
- **User-level tagging** (e.g. `user_id`, organization) → essential for **chargeback**, accurate billing, and spotting **abusive usage** before it drains the budget.
- **Model-level tagging** (e.g. `model`, `provider`) → immediate visibility into high-leverage optimization areas; lets you **benchmark the true expense** of one model vs another.
- **Endpoint-level tagging** (region, environment, provider) → aids infra planning; shows how regional distribution or staging-vs-prod impacts total spend.

Making tagging mandatory gives the visibility to understand where money goes and how to control it.

### New Dimension 2 — Safety & security
The GenAI threat landscape is categorized by risk level:
- **Critical risk:** **PII leakage** and **data exfiltration**.
- **High risk:** **prompt injection** (described as probably the most common attack) and the related **jailbreaking**.
- **Medium risk:** **denial-of-wallet** (an attack against your budget) and **model extraction** (sustained, systematic probing with queries to reverse-engineer the model).

The key insight: you must **monitor for security breaches that don't look like errors.** Four key security metrics:
- **Prompt injection rate.**
- **PII detection rate.**
- **Content moderation score.**
- **Jailbreak attempts.**

### New Dimension 3 — Quality monitoring
Described as "arguably the most crucial" new dimension: LETS tells you the service is *up*, cost + safety tell you it's *budget-compliant and secure*, but for a GenAI app **the only thing that truly matters is whether the output is good.**

#### Why quality is hard to measure
Quality in GenAI is inherently subjective, context-dependent, and hard to quantify with traditional metrics, for four reasons:
- **No ground truth** — there's often no single correct answer to compare against.
- **Context matters** — the same response can be good or bad depending on the situation.
- **Hallucinations are a major challenge.**
- **Subjective satisfaction** — we've moved from a binary "works/doesn't work" world to a **spectrum**, where users judge responses on how helpful, accurate, and complete they are.

#### The six quality metrics to implement
To move beyond "it works" status codes and truly measure output:
- **Hallucination rate.**
- **Relevance score.**
- **User satisfaction.**
- **Answer completeness.**
- **Retrieval (RAG) quality** — you must measure how good the retrieval feeding generation is.
- **Response coherence.**

Together these give a **complete, multi-dimensional view** of quality needed to optimize the app.

### Bringing it all together — the complete monitoring stack
Comprehensive GenAI observability means going **"beyond beyond" the traditional golden signals** — a complete stack that combines:
- **LETS metrics** → tell you *if* the system is running.
- **Three new dimensions** → tell you *how* it's running:
  - **Cost** — how much are we spending?
  - **Safety / security** — is it secure?
  - **Quality** — is the output good?

Uniting LETS with cost, safety, and quality yields visibility into the application's **health, financial spend, security posture, and output quality** simultaneously.

### Vendor positioning — Datadog LLM Observability
The talk closes with Datadog's own product, **Datadog LLM Observability**, positioned as covering all of the above in one central application:
- **Standard metrics** — automatically captures and visualizes latency, errors, **tokens per second**, and **API rate-limit usage** directly from your LLM calls.
- **Quality & cost** — tracks and analyzes costs across different models, and evaluates prompt/response quality via **integrated eval tools** plus **tracing of tool usage**.
- **Safety & security** — monitors security risks, including **identifying and masking PII** in prompts/responses and **detecting prompt injections** or unsafe content.

### Closing thesis
The recap: golden signals (latency, errors, traffic, saturation) are the **bedrock of monitoring and aren't going anywhere** — but for GenAI apps, **LETS alone leaves you blind to the things that matter most.** The memorable closing line frames the whole talk: *"A perfect 200 OK means nothing if your model is hallucinating, leaking PII, or burning through your budget one token at a time."*

## 🛠️ Products / Features / Technologies Mentioned
- **Datadog LLM Observability** — Datadog's product for monitoring GenAI/LLM apps; auto-captures golden-signal metrics (latency, errors, tokens/sec, rate-limit usage) and adds cost tracking, prompt/response quality evals, tool-usage tracing, PII masking, and prompt-injection/unsafe-content detection in one platform.
- **Golden signals / LETS** — the monitoring framework of Latency, Errors, Traffic, Saturation used as the foundation throughout.
- **RAG (Retrieval-Augmented Generation)** — referenced as a GenAI pipeline stage to instrument for latency and as a quality input ("retrieval quality" must be measured).
- **LLM model-provider error types** — context-length-exceeded, safety-filter-triggered, model-overloaded; the new error category beyond HTTP status codes.
- **GPU utilization & API rate limits** — the new saturation bottlenecks for GenAI workloads.
- **Eval tooling / tracing** — Datadog's integrated capabilities for scoring prompt/response quality and tracing tool calls.

## 🚀 Announcements / What's New
None explicitly announced. The session is an educational/partner overview of GenAI monitoring practices plus a positioning of Datadog LLM Observability; no new releases, previews, or GA milestones were stated.

## 💡 Demos
No live demos were shown. The session was a conceptual/slide-driven walkthrough (golden signals → cost/safety/quality dimensions → Datadog product overview) rather than a hands-on demonstration.

## 📊 Notable Stats / Quotes
- **"A perfect 200 OK means nothing if your model is hallucinating, leaking PII, or burning through your budget one token at a time."** — closing thesis of the talk.
- **"LETS alone leaves you blind to the things that matter most."** — on why golden signals are necessary but insufficient for GenAI.
- Example latency figure cited for median user experience: **~850 ms** (illustrative).
- **6 quality metrics**, **4 security metrics**, **4 cost-tagging levels**, **3 cost-escalation mechanisms**, **3 new dimensions**, **4 golden-signal categories** — the talk's quantified structure.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Evaluate **Datadog LLM Observability** against Azure-native options (Azure AI Foundry observability / tracing, Application Insights, Azure Monitor) for a GenAI app; prototype **per-stage latency instrumentation** (RAG retrieval vs LLM call vs total) and add **feature/user/model/endpoint cost tags** end-to-end.
- [ ] Questions: How do these six quality metrics (hallucination, relevance, satisfaction, completeness, retrieval quality, coherence) get computed in practice — LLM-as-judge, embeddings, human feedback? What's the overhead/cost of running quality evals continuously vs sampled? How does Datadog's PII masking and prompt-injection detection compare to Azure AI Content Safety / Prompt Shields?
- [ ] Relevant to: GenAI/agent platform observability strategy; FinOps for AI (token-cost governance, denial-of-wallet); AI security posture (PII leakage, prompt injection, jailbreaking); RAG pipeline reliability and eval frameworks.

## 🔗 Related
- [[ODSP933 - Agentic infrastructure needs agentic observability]] (sibling Build 2026 observability session — extends these ideas to agentic systems)
- [[Golden signals (LETS) — Latency, Errors, Traffic, Saturation]] (the foundational monitoring framework this talk builds on)
- [[GenAI observability — cost, safety, quality dimensions]] (the three new dimensions introduced beyond LETS)
- [[Datadog LLM Observability]] (the vendor product positioned at the end of the session)
- [[RAG retrieval quality & evaluation metrics]] (quality dimension: hallucination rate, relevance, coherence, retrieval quality)
- [[AI security — PII leakage, prompt injection, jailbreaking, denial-of-wallet]] (the GenAI threat landscape covered in the safety dimension)
- [[FinOps for GenAI — token creep, model drift, uncached calls]] (cost-control practices and tagging strategy from this session)
- Source list: [[2026 Build Session List]]
