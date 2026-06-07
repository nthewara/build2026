---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/quantum
  - topic/hardware
  - topic/research
source: https://www.youtube.com/watch?v=rjgsMQ-CO7o
session_code: DEM314
event: Microsoft Build 2026
speakers: Microsoft Quantum hardware physicist (15-year program veteran; name not stated in captions)
duration_min: 15
aliases:
  - Majorana 2 Topological Quantum Computing
---

# DEM314 — Majorana 2: The Topological Leap Toward Quantum Computing at Scale

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** A senior Microsoft Quantum hardware physicist (self-described 15-year veteran of the topological quantum program; specific name not captured in the auto-captions)  
> **Duration:** ~15 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=rjgsMQ-CO7o)

## 🎯 TL;DR
Microsoft is pursuing quantum computing via a distinctive **topological qubit** approach that encodes information in **Majorana modes** — exotic quantum states that are inherently protected from errors and decoherence. This talk presents "Majorana 2," the latest generation of the topological processing unit, built on a brand-new material stack that swaps aluminium for a **lead (Pb) superconductor**, yielding a claimed **~1,000× improvement in qubit performance** and a qubit **lifetime extended from ~10 milliseconds up to a full minute**. Because the qubits are tiny (~micron-scale) and fast (microsecond operations), a million-qubit chip could fit on something the size of a credit card. AI- and simulation-driven design compressed a decade's worth of progress into a single year, letting Microsoft **pull its roadmap to a commercially viable quantum machine forward from 2033 to 2029**.

## 🔑 Key Takeaways
- Microsoft's quantum bet is justified by industry-disrupting potential: **drug discovery** (shorter therapy-development cycles), and **energy/climate** (better catalysts for carbon capture and nitrogen fixation).
- Strategy is a **unified AI + Quantum + HPC** approach: AI for design/optimization, quantum for fast computation and high-quality data generation, HPC to glue the hybrid workflows together. End goal: **CPU + GPU + QPU working seamlessly** in Microsoft's cloud.
- The program was conceived as a **full-stack quantum machine** from day one — not a qubit count race — spanning physical hardware → QPU → quantum error correction + classical compute → applications.
- Target qubit properties: **small (~micron), fast (~microsecond operations), and reliable.** Topological qubits uniquely satisfy all three.
- The reliability comes from a **new phase of matter** — a **topological superconductor ("topoconductor")** — engineered by combining a conventional superconductor + semiconductor under a magnetic field to host **Majorana modes**.
- New **Majorana 2 material stack uses a lead (Pb) superconductor instead of aluminium**; lead's **parent gap is ~4× larger**, which translates to a **~1,000× improvement in qubit performance.**
- It was **not a drop-in swap** — the entire semiconductor stack was re-engineered (new substrate, optimized quantum well and interfaces) to work with lead. All within **one year.**
- Qubits use **H-shaped superconducting structures** patterned on semiconductor, with separate **tuning, control, and readout** gate layers; a 2×2 array occupies only tens of microns². A **million-qubit chip ≈ credit-card-sized.**
- Qubits are **digitally controlled** and co-integrated with **cryo-CMOS on the same chip at millikelvin temperature** to solve the input/output (wiring/control) bottleneck.
- **Readout is fast RF capacitance sensing**: tiny capacitance changes over time map to qubit states (Z-basis measurement).
- **Qubit lifetime jumped from ~10 ms (aluminium devices) to up to ~1 minute** — about a 1,000× gain — described as "enormous on the scale of qubits."
- AI-enabled design tools (from a partner "discovery" team) optimized **100+ parameters**, letting the team **design the complex chip in under a month.**
- Headline roadmap acceleration: **commercially viable quantum machine moved from 2033 → 2029.**
- The supporting paper is posted on **Azure Quantum's website and on arXiv.**

## 📚 Detailed Notes

### Why quantum — the industry-disruption thesis
The talk opens with the motivation: quantum computing can potentially transform entire industries.
- **Healthcare:** enabling certain drug discoveries via quantum computation could **shorten the cycle for therapy development.**
- **Energy & climate:** discovering/simulating certain catalysts could enable **faster carbon capture** and solve the **nitrogen fixation** problem.

These are classic quantum-advantage candidates because they hinge on simulating quantum chemistry/materials that are intractable for classical machines.

### The unified AI + Quantum + HPC strategy
Microsoft frames itself as uniquely positioned because it develops all three components in-house:
- **AI** → design and optimization.
- **Quantum** → faster computation *and* generation of **high-quality data** that AI then consumes.
- **HPC** → the connective tissue supporting these **hybrid workflows**, making the overall approach practically useful.

The end-state vision: **CPU, GPU, and QPU all working seamlessly together** within Microsoft's cloud offerings to solve commercially valuable problems.

### Full-stack philosophy (not a qubit-count race)
From the program's inception, the goal was a **full-stack quantum machine**, explicitly *not* about individual qubits or raw qubit counts. The stack spans:
1. **Physical hardware** and the **quantum processing units (QPUs).**
2. **Quantum error correction** plus the **classical compute** required to run it.
3. The **top application layer** — making the machine actually useful to a consumer.

### Bottom-up qubit requirements
Working bottom-up from extensive studies, the team concluded the qubits must be:
- **Small** — roughly micron-sized.
- **Fast** — operations at the **microsecond** scale.
- **Reliable** — most importantly.

Satisfying *all three simultaneously* is very hard, which is why a fundamentally different approach was needed.

### Why topological — information immune to errors
The **topological approach** is where reliability "shines." The core idea: encode information in **Majorana modes** — exotic quantum degrees of freedom. Information stored this way is **inherently protected from / immune to errors and decoherence**, the very problem that plagues all other qubit platforms. (Decoherence — loss of quantum information to the environment — is the central enemy of every competing modality.)

To get these degrees of freedom, the team had to **invent a new material stack and a new phase of matter** that supports them.

### The new phase of matter — the "topoconductor"
Beyond the familiar phases (solid, liquid, gas), Microsoft engineered a **topological superconductor**, shortened to **"topoconductor."**
- It emerges by **combining a conventional superconductor with a conventional semiconductor** in the right proportions, **under a magnetic field.**
- **Superconductor:** conducts electricity with **zero resistance.**
- **Semiconductor:** has controllable **electron density.**
- Combined correctly, they generate a **unique state hosting the Majorana modes** used to encode information.
- The engineering challenge was creating the **right interface** between superconductor and semiconductor so the layered material behaves as a **single, unified phase of matter.**

### Fabrication — devices built atom by atom
Quantum devices "live or die" on material quality and whether stringent constraints are met. New **fabrication recipes** were required.
- Last year's results already showed a **tremendously improved interface** between the lower semiconductor and the superconductor versus where they started.
- Key technique: fabricating devices **atom by atom** (illustrated in a short movie during the talk). This was "the key recipe for success."

### Majorana 2 — the lead (Pb) superconductor breakthrough
This year's headline improvement is a **new material stack** that replaces the **aluminium** superconductor with a **lead (Pb) superconductor.**
- **Lead's parent gap is ~4× larger than aluminium's.**
- That larger parent gap **directly translates into a ~1,000× improvement in qubit performance** (as reported in the accompanying paper).
- Crucially it was **not a simple "drop and replace"** — the **entire semiconductor stack** had to change to accommodate lead:
  - **Switched the substrate.**
  - **Optimized the quantum well.**
  - **Optimized all the interfaces** in the stack.
- All of this was achieved **within one year.**

> The speaker, a 15-year program veteran, notes the AI-and-simulation-enabled progress of this single year **equals the progress made in the entire first decade** of their tenure — i.e. the development cycle is dramatically accelerating.

The paper is available on the **Azure (Azure Quantum) website** and on **arXiv.**

### The qubit array — H-structures and gate layers
With the material recipe in hand, the team builds qubits from it.
- Qubits are based on **H-shaped structures** — superconducting layers patterned on top of semiconductor.
- Demonstrated as a **2×2 array.**
- The array is wired by distinct **gate layers** corresponding to **tuning, control, and readout.**
- To perform **single-qubit or two-qubit measurements**, the team **activates the right quantum dots / layers** for that operation.

### Scale — million qubits on a credit card
Scale is a recurring emphasis (note the **micron** scale bar):
- **Four qubits occupy only tens of microns².**
- Therefore a **million-qubit chip could fit on a chip the size of a credit card.**
- Small, **densely packed** qubits enable a **modular structure** capable of solving very large, commercially viable problems.

### Digital control + cryo-CMOS (solving the I/O problem)
The qubits operate at **millikelvin temperatures.** A major engineering hurdle is the **input/output problem** — getting control/readout signals in and out of an ultra-cold, ultra-dense chip.
- Qubits are **digitally controlled.**
- They are **coupled with cryo-CMOS on the same chip**, placed at the **same millikelvin stage** as the topological qubits, so the control electronics sit right next to the qubits and tame the I/O bottleneck.
- (In the chip photo: a quantum chip powered by the **topological core** on the left, with the cryo-CMOS co-integrated.)

### Measurement — fast RF capacitance readout
A real fabricated device was shown (false-color H-structures with the tuning/control/readout gates visible).
- The **lower qubit was tuned up** and subjected to a **fundamental measurement** by connecting a **loop** at the top and measuring the qubit state in the **Z basis (Z configuration).**
- Readout is done via a **fast RF readout scheme** that measures **capacitance as a function of time.**
- **Small changes in capacitance correspond to different qubit states (0 and 1).**

### The lifetime result — milliseconds to a minute
The pivotal data point:
- **Qubit lifetime increased up to ~1 minute** — "enormous on the scale of qubits."
- The **previous aluminium-based device maxed out at ~10 milliseconds.**
- That's roughly a **1,000× improvement in lifetime.**
- Attributed to "thinking about everything all together" — **materials → design**, all **enabled by AI and simulations**, optimizing the entire qubit array.

### Velocity → roadmap pulled forward
Being able to **iterate a new material stack, new design, and new system and measure the devices all within one year** gave the team confidence in the approach and in their development velocity.
- This confidence let Microsoft **accelerate the roadmap to a commercially viable quantum machine from 2033 to 2029.**

### AI-accelerated design
The design itself was heavily accelerated by AI, via collaboration with a partner **discovery team.**
- They fed in **all the design rules and requirements** and **optimized over 100+ parameters.**
- Using the partners' **AI-enabled tools**, they **designed this complex chip in less than a month.**

### Closing thesis
The punchline: Microsoft **turned a hard physics problem into a roadmap for a scalable quantum computer.** The secret to meeting the stringent requirements of quantum computing at scale is **better materials, better interfaces, better fabrication, better algorithms, and better designs — pushing on all cylinders simultaneously.** The talk closes to take questions.

## 🛠️ Products / Features / Technologies Mentioned
- **Majorana 2 (topological QPU)** — Microsoft's latest topological quantum processing unit built on the new lead-based material stack; the subject of the talk.
- **Topological qubit / Majorana modes** — qubits that encode information in exotic Majorana quantum states, inherently protected from errors/decoherence.
- **Topological superconductor ("topoconductor")** — the engineered new phase of matter (superconductor + semiconductor + magnetic field) that hosts the Majorana modes.
- **Lead (Pb) superconductor** — new superconducting material replacing aluminium; ~4× larger parent gap → ~1,000× qubit performance gain.
- **Cryo-CMOS** — control electronics co-integrated on-chip at millikelvin temperature to digitally control qubits and solve the I/O problem.
- **H-structure qubit array** — superconducting H-shaped structures on semiconductor, organized into tuning/control/readout gate layers (shown as a 2×2 array).
- **RF capacitance readout scheme** — fast radio-frequency readout measuring capacitance-vs-time to distinguish qubit states.
- **Topological core** — the core powering the demonstrated quantum chip.
- **Unified AI + Quantum + HPC stack** — Microsoft's overarching strategy combining AI (design/optimization), quantum (computation/data), and HPC (hybrid workflow support), targeting CPU+GPU+QPU in the cloud.
- **Azure Quantum (Azure website)** — where the supporting research paper is posted (also on arXiv).
- **AI-enabled design tools (partner "discovery" team)** — used to optimize 100+ parameters and design the chip in under a month.

## 🚀 Announcements / What's New
- **New Majorana 2 material stack** announced: a **lead (Pb) superconductor** replacing aluminium, claimed to deliver a **~1,000× improvement in qubit performance** (driven by lead's ~4× larger parent gap).
- **New quantum processing unit (QPU)** built with this material stack, with **cryo-CMOS co-integrated on the same chip.**
- **Qubit lifetime improvement** to **up to ~1 minute** (from ~10 ms in the prior aluminium device).
- **Roadmap acceleration:** commercially viable quantum machine target **moved from 2033 → 2029.**
- **Supporting research paper** published on the **Azure Quantum website** and on **arXiv** (status: published/available; specific GA/preview labels not applicable — this is research hardware, not a shipping product).

> Note: This is a research/hardware milestone talk. No commercial product GA or public preview availability dates were stated beyond the 2029 commercial-machine roadmap target.

## 💡 Demos
- **Chip photograph walkthrough** — the speaker showcased the actual quantum chip: a topological-core-powered quantum chip with **cryo-CMOS co-integrated on the same chip**, illustrating the digital-control / millikelvin co-location design that addresses the I/O problem.
- **"Atom by atom" fabrication movie** — a short film showing devices being fabricated atom by atom, used to prove the fabrication-quality recipe behind the improved superconductor/semiconductor interface.
- **Real fabricated device + live measurement data** — false-color image of the H-structure device with visible tuning/control/readout gates, accompanied by an actual **Z-basis measurement of the lower qubit**: a **capacitance-vs-time trace** whose small steps correspond to qubit states 0/1 — demonstrating working tune-up and fast RF readout, and underpinning the **~1-minute lifetime** result.

## 📊 Notable Stats / Quotes
- **~1,000× improvement in qubit performance** from the lead superconductor's larger parent gap.
- **Lead parent gap ≈ 4× larger** than aluminium.
- **Qubit lifetime: up to ~1 minute** (vs **~10 ms** maximum for the previous aluminium device) — roughly **1,000× longer.**
- **Four qubits in tens of microns²**; **a million-qubit chip could fit on a credit-card-sized chip.**
- **100+ parameters optimized** by AI tools; **chip designed in under a month.**
- **Roadmap pulled forward from 2033 to 2029** for a commercially viable quantum machine.
- Qubit targets: **micron-sized, microsecond operations, highly reliable.**
- *"We turned the hard physics problem into a roadmap for a scalable quantum computer."*
- *"The level of improvement ... that happened over the last year is equivalent to the level of progress that we've made in the first decade of my ... tenure"* (speaker has been with the program **15 years**).
- Qubits operate at **millikelvin temperatures.**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Find and read the cited paper on the **Azure Quantum site / arXiv** for the lead-superconductor topoconductor and the ~1-minute lifetime claim; verify the parent-gap → performance scaling argument.
- [ ] Questions: Is the ~1-minute "lifetime" a **coherence (T₂)**, relaxation (T₁), or parity/Majorana lifetime? How many of the "qubits" demonstrated are full **topological qubits** vs. enabling sub-components? What error rates / gate fidelities accompany the lifetime number? What does "commercially viable" mean concretely for the 2029 target (qubit count, logical qubits)?
- [ ] Relevant to: Quantum-advantage use cases in **chemistry/materials simulation** (catalysts, nitrogen fixation, carbon capture) and **drug discovery**; the broader **CPU+GPU+QPU hybrid cloud** architecture story; Microsoft's prior **Majorana 1** announcement for comparison.

## 🔗 Related
- [[Microsoft Build 2026]]
- 
