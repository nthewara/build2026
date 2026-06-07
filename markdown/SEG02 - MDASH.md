---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/security
source: https://www.youtube.com/watch?v=8QBDaRbur70
session_code: SEG02
event: Microsoft Build 2026
speakers: Microsoft (keynote security demo segment)
duration_min: 4
aliases:
  - MDASH
  - M-Dash
  - M-code scan
---

# SEG02 — MDASH

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Microsoft presenter (keynote security demo segment, following Satya Nadella on stage)  
> **Duration:** ~4 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=8QBDaRbur70)

## 🎯 TL;DR
**MDASH (rendered "M-Dash", and spoken as "M-code scan" in the demo) is Microsoft's new multi-agent AI security harness for finding and fixing code vulnerabilities.** Under the hood, **over 100 specialized agents work together to discover, debate, and *prove* exploitable vulnerabilities end-to-end** — not just flag suspicious patterns. The demo runs MDASH against a real code base from inside GitHub Copilot on a local dev machine, surfacing both traditional issues (coding errors, hard-coded secrets) and **AI-specific vulnerabilities**, then remediating them with a `Defender fix` command while keeping a human-in-the-loop diff review. The headline proof point: MDASH independently found a real, multi-file Wasmtime memory-safety bug that fooled normal scanners and single AI models. It's positioned as helping developers "create secure code from the start" and is **coming soon to the CLI and the Microsoft Defender portal**.

> [!note] Name uncertainty
> The on-screen product name is shown as **"M-Dash" / MDASH**, but the presenter verbally refers to running an **"M-code scan."** These appear to be the same offering (caption ambiguity around the "M-…" branding). Treat "M-Dash," "MDASH," and "M-code scan" as the same tool until a clearer official name is confirmed.

## 🔑 Key Takeaways
- **MDASH = a multi-agent code-security harness**, not a single scanner — **100+ specialized agents** collaborate to *discover, debate, and prove* exploitable bugs end-to-end.
- It runs as a **standalone CLI** but was demoed **inside GitHub Copilot on a local dev machine**.
- Findings are **broken down by vulnerability domain and severity**, covering both **traditional flaws** (coding errors, hard-coded secrets) and **AI-specific vulnerabilities**.
- It produces **enterprise-ready output**: a **SARIF log** + an **HTML report** suitable to hand to management.
- A **`Defender detailed`** command drills into each vulnerability (what it is, where it is, severity); a **`Defender fix`** command **auto-remediates directly in the local dev environment** with a **diff for human review** (human-in-the-loop preserved).
- It plugs into existing workflows: **create a PR**, push to the repo, and **upload SARIF to GitHub Advanced Security** to manage alongside other app-sec findings.
- **Proof of capability:** MDASH found a real **Wasmtime** out-of-bounds/host-crash bug whose flaw was **spread across three parts of the code base** — invisible to per-file scanning — and even saw past a developer comment confidently asserting the code was fine.
- **Status:** **Coming soon to your CLI and the Microsoft Defender portal.**

## 📚 Detailed Notes

### What MDASH is and where it runs
The presenter notes that security scans take a while, so they show the **results of a scan already run** rather than running one live. MDASH operates as a **standalone CLI**, but in the demo it's used from **within the GitHub Copilot app on a local dev machine** — i.e. it meets developers where they already work rather than forcing a separate tool.

### How the scan results are structured
The scan output is **broken down by vulnerability domains and severity**. Critically, it surfaces two classes of issues side by side:
- **Traditional issues** — coding errors and hard-coded secrets.
- **AI-specific vulnerabilities** in the code base — the kinds of weaknesses introduced or relevant in AI-assisted/AI-powered code.

### Under the hood: 100+ agents that prove exploitability
The differentiator is the architecture. **Over 100 specialized agents work together to discover, debate, and prove exploitable vulnerabilities end-to-end.** This is framed as **"joined-up reasoning"** — moving beyond pattern-matching to actually demonstrating that a flaw is reachable and exploitable, work that *"previously required significant manual security research effort."*

### Outputs: SARIF + HTML report
When the scan finishes it generates **both a SARIF log and an HTML report**. The HTML report is explicitly positioned as something *"I can give to my management"* — i.e. a human-readable executive artifact — while **SARIF** is the machine-readable format for tooling integration.

### Triage and remediation (the Defender commands)
- **`Defender detailed`** — lets the developer **dig into each vulnerability**: *what* it is, *where* it sits in the code, and its **severity**, to help prioritize.
- **`Defender fix`** — the system **remediates suggested fixes directly in the local dev environment**. Afterward the developer **checks the diff**, giving **full transparency about what the harness did** and preserving a **human-in-the-loop check**. (Nothing lands silently.)

### Fitting into existing workflows
Although everything shown ran **locally**, MDASH integrates upstream:
- **Create a PR** to plug into existing workflows and **push up to the repo**.
- Take the **SARIF output** and **upload it to tools like GitHub Advanced Security**, managing MDASH findings **alongside other application security findings**.

### The real-world proof: the Wasmtime bug
To show this isn't just a demo on tidy code, the presenter highlights a vulnerability that **security research teams identified using MDASH in an open-source code base — one you can go look up yourself.**

The bug (TL;DR per the segment): **Wasmtime reads an out-of-date map of an object, runs off the end, and crashes the host.** What makes it the *exact* kind of bug MDASH was built for:
- The flaw is **spread across three different parts of the code base**, so **no single file looks wrong on its own** — each looks "absolutely fine."
- There's even a **confident developer statement claiming everything is fine** — the presenter's "favorite part" — precisely the kind of reassurance that **fools normal scanners and single AI models**.

**MDASH wasn't fooled.** The multi-team agent dynamic cracked it:
1. **One team of agents spotted the suspicious gap.**
2. **Another team argued it apart** (the "debate" step).
3. **A third team built a working example that actually triggered the crash** (the "prove" step).

This three-stage discover → debate → prove pattern is the core of how MDASH establishes a vulnerability is genuinely exploitable.

### Positioning
The segment closes by framing MDASH as **"helping developers create secure code from the start,"** and confirms it is **coming soon to your CLI and the Microsoft Defender portal**, before handing back to Satya.

## 🛠️ Products / Features / Technologies Mentioned
- **MDASH / M-Dash ("M-code scan")** — Microsoft's multi-agent code-security harness; 100+ agents that discover, debate, and prove exploitable vulnerabilities end-to-end.
- **`Defender detailed` command** — drills into a finding (what / where / severity) for prioritization.
- **`Defender fix` command** — auto-remediates fixes in the local dev environment with a reviewable diff.
- **GitHub Copilot (app, local dev machine)** — the surface MDASH was demoed inside.
- **Microsoft Defender portal** — a forthcoming home for MDASH (alongside the CLI).
- **SARIF (log/output)** — machine-readable findings format; uploadable to other security tooling.
- **HTML report** — human-readable report intended for management.
- **GitHub Advanced Security** — destination for uploaded SARIF, to manage MDASH findings with other app-sec results.
- **Pull Requests (PRs)** — integration point to push local findings/fixes into existing workflows.
- **Wasmtime** — the open-source WebAssembly runtime where the demonstrated real-world multi-file memory-safety bug was found.

## 🚀 Announcements / What's New
- **MDASH ("M-Dash" / "M-code scan")** — multi-agent security harness for discovering, debating, and proving exploitable vulnerabilities, including **AI-specific** ones. **Status: Coming soon to the CLI and the Microsoft Defender portal.**
- **`Defender detailed` / `Defender fix` commands** — triage and in-place remediation with human-in-the-loop diff review. *(Demoed; ships as part of MDASH "coming soon.")*
- **SARIF + HTML report generation** and **GitHub Advanced Security / PR integration** — shown as part of the MDASH workflow.

## 💡 Demos
- **Pre-run MDASH scan inside GitHub Copilot (local dev machine):** showed findings grouped by domain/severity, mixing traditional issues (coding errors, hard-coded secrets) with AI-specific vulnerabilities. **Point proved:** MDASH integrates into the developer's existing local environment and covers both classic and AI-era risks.
- **`Defender detailed` → `Defender fix` flow:** drilled into a vulnerability, then auto-remediated it locally and reviewed the diff. **Point proved:** end-to-end detect-and-fix with full transparency and a human-in-the-loop gate.
- **Wasmtime real-world bug walkthrough:** a genuine, exploitable, **three-file** memory-safety/host-crash bug in an open-source code base — including a misleading "everything is fine" developer comment. **Point proved:** MDASH's discover/debate/prove agent teams catch joined-up vulnerabilities that fool single scanners and single AI models, replacing significant manual security-research effort.

## 📊 Notable Stats / Quotes
- **"Over 100 specialized agents are working together to discover, debate, and prove exploitable vulnerabilities end-to-end."**
- **Wasmtime bug TL;DR:** *"Wasmtime reads an out-of-date map of an object, runs off the end, and then it crashes the host."*
- Flaw **spread across three different parts of the code base** — *"no single file looks wrong on its own."*
- On the misleading code comment: *"a very confident statement from the developers claiming everything is fine … exactly the sort of reassurance that fools normal scanners and single AI models. But M-Dash wasn't fooled."*
- Agent teamwork: *"One team of agents spotted the suspicious gap, another team argued it apart, and a third team built a working example that actually triggered the crash."*
- *"This is the kind of joined-up reasoning that previously required significant manual security research effort."*
- Tagline: **"M-Dash helping developers create secure code from the start, coming soon to your CLI and the Microsoft Defender portal."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Run MDASH (once available) as a CLI scan against a personal repo; confirm the SARIF → GitHub Advanced Security upload path and check the HTML report format.
- [ ] Things to try: Test the `Defender fix` diff-review loop end-to-end and verify the human-in-the-loop gate behaves as shown.
- [ ] Questions: What's the official product name — is "M-Dash"/MDASH the brand and "M-code scan" just a verbal slip, or are they distinct? Confirm against the Defender portal listing.
- [ ] Questions: Which "AI-specific vulnerability" categories does MDASH detect (prompt injection, insecure tool use, secret leakage in agent code, etc.)?
- [ ] Questions: Where can I find the published Wasmtime bug write-up referenced ("you can go and look up yourself")? Get the CVE/advisory link.
- [ ] Questions: Pricing/licensing — is MDASH part of Defender for Cloud / GitHub Advanced Security entitlements, or standalone?
- [ ] Relevant to: AppSec / secure SDLC, AI-assisted coding security, Microsoft Defender, GitHub Advanced Security adoption.

## 🔗 Related
- [[2026 Build Session List]]
