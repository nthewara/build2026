---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
source: https://www.youtube.com/watch?v=uHtva5r9itY
session_code: SEG03
event: Microsoft Build 2026
speakers: Microsoft Discovery & Quantum team (product segment)
duration_min: 6
aliases:
  - Microsoft Discovery
---

# SEG03 — Microsoft Discovery

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Presenter from the Microsoft Discovery & Quantum team (product segment) — name not stated on-screen  
> **Duration:** ~6 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=uHtva5r9itY)

## 🎯 TL;DR
**Microsoft Discovery** is an agentic platform for scientific R&D that treats discovery like agentic software engineering. The app is built on VS Code, and its core insight is that science maps onto a developer's workflow: **planning → coding → testing/deploying** becomes **write a paper → run the discovery → test in a real lab**. It runs a "discovery engine" — a team of specialized agents that continuously follow the scientific method in the background, exploring hypotheses and running long-running simulations (hours or days). The demo, built with **Cambridge Consultants (part of Capgemini)**, used Discovery to find new proteins that can decompose PET plastic so it can be truly recycled instead of downcycled — all the way through to submitting jobs to a real automated lab.

## 🔑 Key Takeaways
- **Agentic discovery ≈ agentic software engineering.** Discovery is deliberately built on VS Code because the parallels are strong; developers will recognise the plan/code/test/deploy loop.
- **Three scientist tasks mirror the dev lifecycle:** (1) write a scientific paper / explore a line of research = *planning*; (2) perform the actual discovery to find new proteins = *coding*; (3) create a lab protocol & test in a real lab = *testing + deploying to production*.
- **The discovery engine is a background team of agents** always running, following the scientific method — **not sequential**; it explores hypotheses and runs simulations dynamically, sometimes for hours or days.
- **Open agent ecosystem:** Discovery includes a community of agents, models, and tools across many domains. You can use open source, third parties, or build your own.
- **It creates agents on the fly.** If no out-of-the-box agent exists for a task, Discovery generates one (with its YAML definition and supporting code).
- **Knowledge graph for full traceability:** Discovery internally builds a knowledge graph combining public scientific literature with internal knowledge — giving complete visibility into the reasoning so scientists stay in full control.
- **HPC-integrated:** Agents tap high-performance computing for compute-heavy simulations (e.g. generating protein candidates millions of times in parallel).
- **Closes the loop to the physical world:** Discovery can integrate directly with an automated lab, sending instructions to lab equipment — unifying the digital agents and the physical world in one discovery loop.

## 📚 Detailed Notes

### The problem: PET plastic is downcycled, not recycled
Today, recycling a PET plastic bottle means shredding and melting it. The result is **degraded** material — you can't make the same bottle again. This is **downcycling**. **Cambridge Consultants (part of Capgemini)** is using Microsoft Discovery to advance research toward a better approach: instead of melting the plastic, use **proteins to decompose it**, so it can be recycled again and again.

### What Microsoft Discovery is
- The **Microsoft Discovery app** is based on **VS Code**, because *agentic discovery has many parallels with agentic software engineering*.
- The presenter frames the scientist's goals as three tasks that look just like a developer's workflow:
  1. **Write a scientific paper** about the topic / explore an existing line of research → like **planning**.
  2. **Perform the actual discovery** to find new proteins → like **coding**.
  3. **Create a lab protocol** to test results in a real lab → like **testing & deploying to production**, but for science.

### The discovery engine (the background agent team)
- Launching kicks off the **discovery engine**: think of it as a **team of specialized agents always running in the background, following the scientific method**.
- You can **see the agents** in the app and **add more**.
- Discovery ships with a **community of agents, models, and tools across many domains** — use **open source, third parties, or create your own**.
- Crucially, the engine is **not sequential**. Like science itself, it **explores hypotheses and performs long-running simulations dynamically**, and can keep running for **hours or even days**.

### Step 1 — The research paper (knowledge graph + traceability)
- Opening a completed run shows the **files it created**, including the **research paper** the scientist asked for.
- To produce it, Discovery uses an **internal knowledge graph** that brings together **public scientific literature and internal knowledge**.
- This is described as a **critical asset**: it provides **complete visibility of the reasoning**, so **scientists can be in full control**.

### Step 2 — The discovery itself (finding new proteins)
The approach Discovery took to come up with new plastic-decomposing proteins:
1. **An AI model** to predict how good a protein is for the task.
2. **A way to generate new proteins.**
3. **A way to identify the most promising ones.**

**The model:**
- Discovery **trained multiple models and picked the best**.
- There was **no out-of-the-box agent** for this — so Discovery **created one on the fly** ("pretty cool").
- It generated all the files, including the **agent's YAML** definition and the **Python code to train the models**.

**Generating candidates (HPC):**
- Generating new protein candidates **requires a lot of compute**, and Discovery is **integrated with HPC** for complex simulations.
- The process: it started with a **seed protein**, then created **variations by replacing small segments**, then **applied the trained model** to judge whether each variation helped — **learning in the process**.
- This was done **millions of times, in multiple parallel jobs**, exploring a **huge tree of proteins**.
- **Result: 80 proteins** ready to be sent to the lab for testing — the equivalent of "deploying software."

### Step 3 — From digital proteins to the physical lab
- Making a real protein is more complicated. The **most common method is inserting DNA into bacteria** so the bacteria produce the protein.
- Discovery generated another file containing **all the DNA sequences** to create each protein. This could be sent to a lab to create and test the proteins manually.
- **Or go one step further:** with an **automated lab**, integrate it directly with the agents. In the session, the presenter simply runs **"submit job to lab."**
- This uses a **custom agent that sends instructions to the lab equipment** — and it's **very real**: **Cambridge Consultants has an automated lab**, shown live.
- The lab application has a **Copilot interface** so scientists can interact with the lab to **design experiments** — "it feels like being **Iron Man, but for chemistry**."
- Discovery submits the job; since the **bacteria need to grow**, it takes time. A previous run shows **all the steps the agents performed — most completely automated, with human supervision**.

### The big picture
This is **bringing together the physical world and the digital agents in a unified discovery loop**. The plastic-recycling protein hunt was **just one example** — **customers across industries are using Microsoft Discovery today** to embrace "a new era of scientific discovery."

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Discovery** — Agentic platform for scientific R&D; the central product of the segment.
- **Microsoft Discovery app** — The application itself, **built on VS Code**, reflecting the parallels between agentic discovery and agentic software engineering.
- **Discovery engine** — Background "team" of specialized agents continuously following the scientific method; non-sequential, runs hypotheses & simulations for hours/days.
- **Community of agents, models & tools** — Open ecosystem spanning many domains; supports open source, third-party, and custom-built agents.
- **On-the-fly agent creation** — When no agent exists for a task, Discovery generates one (incl. its YAML definition and supporting code).
- **Knowledge graph** — Internal graph combining public scientific literature + internal knowledge; provides full reasoning visibility / traceability.
- **HPC integration** — Agents use high-performance computing for compute-heavy simulations (e.g. massively parallel protein generation).
- **Automated lab integration / custom lab agent** — Sends instructions to physical lab equipment, closing the digital-to-physical loop.
- **Copilot interface (in the lab app)** — Lets scientists interact with the automated lab to design experiments.
- **VS Code** — The base/IDE the Discovery app is built on.

## 🚀 Announcements / What's New
- No explicit GA dates, version numbers, or formal roadmap milestones were stated in this segment.
- Framed as **available and in use today**: *"Customers across industries are using it today."*
- Notable *capabilities highlighted* (presented as current, not "coming soon"): the VS Code–based app, the always-on agentic discovery engine, on-the-fly agent creation, the knowledge graph, HPC integration, and direct automated-lab integration.

## 💡 Demos
- **End-to-end PET-recycling protein discovery (with Cambridge Consultants / Capgemini).** A single live walkthrough proving Discovery can take a scientist from *research paper → model training → protein candidate generation → DNA sequences → submitting a job to a real automated lab*, all driven by background agents with human supervision.
  - **Point proved:** Agentic discovery can run the full scientific lifecycle (plan/code/test/deploy analog) and **connect digital agents to the physical world** via a real automated lab — not just a simulation.

## 📊 Notable Stats / Quotes
- **80 proteins** generated and "ready to be sent to the lab for testing."
- Protein variations evaluated **"millions of times, in multiple jobs in parallel,"** exploring "a huge tree of proteins."
- Discovery runs can continue **"for a while, even hours or days."**
- > "It feels like being **Iron Man, but for chemistry**." — on the lab's Copilot interface.
- > "This is bringing together the **physical world and the digital agents in a unified discovery loop**."
- > "Customers across industries are **using it today** to embrace a new era of scientific discovery."
- On recycling today: shredding + melting PET yields a **degraded** result you "cannot use to make this bottle again" — i.e. **downcycling**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Explore the Microsoft Discovery docs — how the agent **community/marketplace** works, and how "create an agent on the fly" is exposed to users.
- [ ] Things to try: Look at how the **knowledge graph** ingests "internal knowledge" — connectors, data residency, IP controls.
- [ ] Questions: Which **HPC** backend does Discovery integrate with (Azure HPC? specific SKUs?), and what's the cost/quota model for "millions of jobs in parallel"?
- [ ] Questions: What's required to integrate a **custom automated lab** (the lab agent + equipment instructions interface) — is there an SDK/protocol?
- [ ] Questions: Is Microsoft Discovery GA, in preview, or access-gated? Availability/pricing not stated here.
- [ ] Relevant to: Anyone framing **agentic AI for R&D / scientific computing**; the "science = software lifecycle" analogy is a strong mental model for dev audiences.

## 🔗 Related
- [[2026 Build Session List]]
