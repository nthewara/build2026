---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/security
  - topic/devsecops
  - topic/runtime
  - topic/defender
  - topic/github-advanced-security
  - topic/ai-security
source: https://www.youtube.com/watch?v=FcymSA7jZL8
session_code: OD841
event: Microsoft Build 2026
speakers: James Brotsos
duration_min: 18
aliases:
  - Ship fast stay secure from code to runtime
---

# OD841 — Ship fast, stay secure: from code to runtime

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** James Brotsos (Product Manager, securing code and applications — Microsoft)  
> **Duration:** ~18 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=FcymSA7jZL8)

## 🎯 TL;DR
Microsoft is collapsing the long-standing trade-off between shipping fast and staying secure by embedding AI-powered security directly where developers already work — the terminal, the IDE, and the pull request. The centerpiece is a **multi-model agentic scanning harness** (code name **M-**) delivered through the **Defender CLI**, which orchestrates 100+ specialized AI agents across an ensemble of frontier and distilled models through a five-stage pipeline to find vulnerabilities that traditional pattern-matching scanners miss. Critically, it doesn't just flag issues — it explains them, suggests fixes (via Copilot), and in most cases opens the pull request. **Microsoft Defender for Cloud** and **GitHub Advanced Security** then work together to trace a single vulnerability from a line of code all the way to runtime risk in the cloud (and back), correlating exploitability, internet exposure, and sensitive-data paths to prioritize what actually matters. The session walks the full lifecycle — code → build → ship → run — including AI model supply-chain security (catching malicious pickle-serialized PyTorch models). The Defender CLI is **available today**.

## 🔑 Key Takeaways
- **"Ship fast vs. stay secure" is a false trade-off.** The whole thesis: you no longer have to pick one. Security gets embedded into existing developer surfaces (terminal, PR, IDE) rather than bolted on as extra process, tools, or dashboards.
- **AppSec is a team sport, but the workflow is broken.** Today security teams typically drop findings on developers' desks ~2 weeks after code ships, or developers ignore scan results because they lack context to act. The intent is good; the collaboration is broken.
- **The product is the system, not the model.** The Defender CLI is powered by a multi-model agentic harness (code name **M-**) — "The model is one input. The system around it is the product."
- **100+ specialized agents, 5-stage pipeline.** M- orchestrates over a hundred AI agents across frontier + distilled models through: (1) prepare attack surface, (2) scan candidate code paths, (3) validate findings (agents debate reachability/exploitability), (4) deduplicate, (5) prove the vulnerability by constructing triggering inputs.
- **Semantic reasoning beats string matching.** M- doesn't look for known-bad strings; it reasons about what the code actually does "the way an attacker would," catching vulns traditional static analysis gives a clean bill of health.
- **Scan → Find → Fix, all in the terminal (true shift-left).** The developer loop runs locally before code even touches the repo. Copilot generates fixes; no context switching, no ticket filing, no copy-pasting.
- **Code-to-runtime correlation in both directions.** Defender for Cloud + GitHub Advanced Security let a code vulnerability be traced to runtime cloud risk — and a cloud risk mapped back to the exact line of code and developer who can fix it.
- **Risk is contextual, not absolute.** The same XPath injection scores very differently if the code runs in an internet-exposed container with a path to sensitive data versus an internal dev tool. Internet exposure + path to value + known vuln = the highest priority risk when combined.
- **Single pane of glass for security managers.** The **AI Code Security Initiative** rolls up every finding (CLI, pipeline, agentless code scanning) into a curated, prioritized view — score, recommendations, repos with findings, trends — instead of an alert list to hunt through.
- **Attack paths answer "what puts me at risk right now?"** Defender maps vulnerabilities to the live cloud environment, modeling whether an attacker can reach the asset and what they'd gain, across code → build → ship → run phases.
- **One fix can close multiple CVEs, auto-assigned to Copilot.** From an attack path, a GitHub issue can be created directly, assigned to Copilot; fixing one package can resolve additional transitive CVEs (demo: bumping a package fixed the critical + 2-3 more).
- **AI models are an unguarded supply chain.** Models flow in daily from Hugging Face, internal training pipelines, and shared registries — mostly uninspected. Malicious pickle serializations can embed arbitrary-code payloads inside seemingly normal PyTorch models. Defender discovers all models across workspaces/registries, flags malicious/vulnerable content, and the same CLI can scan model artifacts in the pipeline before deployment.

## 📚 Detailed Notes

### The core problem: a broken collaboration workflow
James Brotsos frames application security as a "team sport" with developers on one side and security managers on the other, theoretically collaborating in the middle. In reality, that collaboration breaks down: security teams drop findings on developers' desks roughly **two weeks after the code shipped**, or a developer ignores a scan result because they lacked enough context to act on it. The intent is good but the workflow is broken. The proposed fix is **not** more process, more tools, or more dashboards — it's embedding security directly into the surfaces developers already use: the terminal, the pull request, and the IDE.

### The two worlds and the intersection
- **Developer's world (left):** code, dependencies, infrastructure as code, pull requests, security alerts, issue tracking.
- **Security team's world (right):** security posture, running workloads, attack paths, exploitability, business criticality, recommendations.
- **The intersection (the bet):** **Microsoft Defender for Cloud** and **GitHub Advanced Security** working together so a vulnerability found in code can be traced all the way to runtime risk in the cloud — and in reverse, a cloud risk can be mapped back to the exact line of code and the developer who can fix it.

With AI agents in the loop, Microsoft isn't just connecting these dots — it's **explaining** the findings, **suggesting** the fix, and in most cases **opening the pull request**.

### The engine: the M- multi-model agentic scanning harness
The Defender CLI is powered by a harness with the code name **M-**. What makes it different from prior scanners:
- It does **not** rely on a single model doing pattern matching.
- It **orchestrates over a hundred specialized AI agents** across an ensemble of **frontier and distilled models**.
- It runs them through a **five-stage pipeline**:
  1. **Prepare the attack surface.**
  2. **Scan candidate code paths.**
  3. **Validate findings** — agents actually *debate* whether a bug is reachable and exploitable.
  4. **Deduplicate** findings.
  5. **Prove the vulnerability** by constructing triggering inputs.
- Guiding philosophy: *"The model is one input. The system around it is the product."*

Because it reasons about semantic/logic flow rather than known-bad strings, M- catches vulnerabilities that traditional pattern-matching static analysis would clear. It reasons about what the code actually does "the way an attacker would."

### The developer loop — Scan, Find, Fix (in the terminal)
Demonstrated in a repository called **benchmark-python**, an open-source project with real vulnerabilities buried in code that traditional scanners would pass clean.
1. **Scan:** Run the Defender CLI (powered by M-) directly in the terminal. The scan catches vulnerabilities traditional pattern matching completely misses — all locally, with no waiting on a pipeline. This is shift-left happening *before the code even touches the repository*.
2. **Fix:** Issue the `fix` command against the standardized output file (a **SARIF** result file). Copilot analyzes the vulnerability, understands the code context, and makes the actual change — no context switching, no ticket, no copy-pasting. The AI understands what's broken and rewrites the code.
3. **Review:** Switch to VS Code to review changes rather than blindly accepting them. Copilot reads through the files, applies its logic, edits the files, and writes the fixed files. The developer sees the vulnerable code on the left and the fixed code side-by-side on the right — not a black box. Each change can be reviewed, understood, and accepted/rejected like a normal code review. Then re-run tests and commit.

This is "developer-first security": the scanner found it, AI suggested a fix, and review happens in the same editor used every day — no context switching, no separate security tool, no ticket sitting in the backlog for two sprints.

### Carrying findings into the pull request
The same finding the CLI caught locally (and the pipeline enforced) surfaces directly in the PR. Crucially, it's not just a red flag saying "XPath injection found." Defender explains exactly what's wrong: *the header value is injected directly into the XPath query, letting an attacker alter the predicate and disclose data they shouldn't see.* Directly below the finding, Copilot suggests the fix: **parameterize the XPath query and pass the input as a bound variable** — and it even tells you to verify the fix works.

The developer security loop in action: **the CLI catches it, the pipeline gates it, and the PR annotates it** with enough context to fix in minutes, not days.

### Switching hats: the security manager view (AI Code Security Initiative)
Now the question becomes: *Across all my repos, all my pipelines, all my teams, where is my application's security posture?* The **AI Code Security Initiative** is the team's single pane of glass for everything shown on the developer side. Every finding from every scan — the CLI, the pipeline, and agentless code scanning — rolls up here:
- Overall **score**, number of **recommendations**, which **repositories** have findings, and how they're **trending**.
- Not a list of alerts to hunt for — a **curated, prioritized** view of application security risk.

The most powerful part: these aren't isolated code findings. Defender **correlates them with the cloud environment**. The XPath injection found in the CLI, if running in an **internet-exposed container with a path to sensitive data**, surfaces with a **completely different risk score** than the same finding in an internal dev tool. Each recommendation traces back to the source, the repository, and the line of code — the security team sees the risk; the developer sees where to fix it. Same data, different lens.

### Attack paths — "which findings actually put me at risk right now?"
A list of findings isn't enough; the real question is which findings actually create risk *right now*. That's what the **attack path** answers. Defender maps vulnerabilities to the live cloud environment and asks: *Can an attacker actually reach this? What can they get if they exploit it?*
- Filter on **risk factors** such as **internet exposure** and **path to sensitive data** to prioritize the riskiest applications running in real time.
- Any one factor alone (internet exposure, a path to something valuable, a known vulnerability) might be low priority — but **combined, that's your biggest risk.**

In an example attack path hosted in **Azure** (viewed in the Azure portal), the path shows internet exposure and high-severity vulnerabilities. The recommendation view lists all known vulnerabilities for the container, including a package "in the news relatively recently."

### Code-to-runtime phases (the killer view)
A single view shows the full lifecycle for a running container:
- **Code** — the repository where the source lives.
- **Build** — the pipeline that built it.
- **Ship** — the registry that contains the container.
- **Runtime** — the actual cluster running the container.

From here you can see the exact source that built it and the source vulnerabilities identified, and prioritize **even higher** because you know that container is internet-exposed and accessing sensitive data (e.g., code injections become critical-asset priorities).

### Closing the loop: GitHub issue → Copilot fix
One of the biggest pain points for security teams is tracing back to **exactly where/who** needs to fix a vulnerability — issues land on a tracking board, get lost in the backlog, and finding the right developer takes a long time. With the **GitHub Advanced Security integration**, you can **create a GitHub issue directly from the attack path view** and it does more than create an issue — it **assigns it to Copilot**. The demo shows that fixing one package would also resolve **three additional CVEs** (the one critical plus two more). Copilot identifies the exact place and code to fix immediately. In this case it was simply updating a package from `0.1` to `1.13`, but the fix could be buried in base images or other packages with a more **transitive** property. This is where security teams "meet developers exactly where they work."

### A blind spot: AI model supply-chain security
Pivoting to the cloud inventory, Brotsos raises something most security teams "aren't even thinking about yet": **AI models flowing into your environment every single day** — from **Hugging Face**, internal training pipelines, and shared registries — mostly **uninspected**.

This isn't hypothetical. **Early this year, attackers on Hugging Face were weaponizing model artifacts using pickle serializations** to embed malicious payloads inside what looks like a normal PyTorch model. You download it, load it, and the moment **pickle deserializes** the file, it **executes arbitrary code**. Even though the industry is pushing toward safer formats like **TensorFlow** and **safetensors**, a massive amount of **PyTorch** remains in production.

**What Defender provides — discoverability first:** customers are generally surprised they don't know how many models are running across their workspaces and registries (there's no central location by default — models live across multiple **Azure ML workspaces** and registries). Defender finds all of them and tells you exactly what you have. Models flagged with a **yellow bar** mean Defender found something; recommendations are populated specifically on models containing **malicious or vulnerable content**. Drilling into a model's asset page → threats and vulnerabilities shows the scanner found that a specific **pickle file contains a malicious serialization payload** — the exact attack described, now sitting in production, potentially connected to a live endpoint.

**Remediation (treat models like immutable artifacts):** disable or unpublish the affected model version in the registry/workspace, archive it, disconnect it from the endpoint, and deploy a clean version. Same principle as a container image — **replace, don't patch.**

### Catching it before deployment
Better still: catch it before it's ever deployed. The **same CLI scanner can scan model artifacts too.** In a separate repo containing ML training scripts, model artifacts, and a deployment pipeline, the pipeline scan (using the Defender CLI) catches **low-severity vulnerabilities** — and because it's a model artifact, even a low-severity finding "should be considered very risky." The pipeline catches it **before it finishes**, gating the bad model from reaching production.

### Bringing it all together — the complete lifecycle
The session demonstrated a complete security lifecycle from the first line of code to a running cloud workload:
- A developer **scanned locally with the CLI**, got **AI-powered fixes**, and reviewed them in **VS Code**.
- The **same engine ran in a GitHub Actions pipeline** as a **gate**.
- The **PR was annotated** with findings and **Copilot-suggested fixes**.
- The **security team saw everything roll up to an Initiative view**, discovered an **attack path** connecting code vulnerabilities to real runtime risk, and traced a running container all the way back to the **commit** that introduced the problem.
- A **GitHub issue was created, Copilot wrote the fix, and the loop was closed.**
- Then it went further into **AI model security**, catching a **malicious pickle file in the pipeline** and imagining AI security posture across an entire model inventory.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Defender for Cloud** — core cloud security posture platform; correlates code findings with runtime cloud risk, attack paths, and model inventory.
- **Defender CLI** — terminal-native scanner powered by the M- harness; runs locally (shift-left) and in CI pipelines; can scan code **and** AI model artifacts. **Available today.**
- **M-** (code name) — the multi-model agentic scanning harness behind the CLI; 100+ specialized AI agents, ensemble of frontier + distilled models, five-stage pipeline.
- **GitHub Advanced Security** — integration that surfaces findings in PRs, enables issue creation from attack paths, and assigns fixes to Copilot.
- **GitHub Copilot** — generates and applies code fixes; gets auto-assigned GitHub issues; writes fixes that can close multiple CVEs.
- **GitHub Actions** — CI pipeline where the same scanning engine runs as a gate.
- **GitHub Issues** — created directly from the security/attack-path view; auto-assigned to Copilot.
- **VS Code** — IDE used for side-by-side review/accept/reject of Copilot fixes.
- **AI Code Security Initiative** — security manager's single pane of glass aggregating findings (CLI, pipeline, agentless code scanning) with score, recommendations, repos, and trends.
- **Agentless code scanning** — one of the finding sources rolling up to the Initiative view.
- **Attack path analysis** — maps vulnerabilities to live cloud environment; filters on internet exposure, sensitive-data path, severity.
- **Azure portal / Azure ML workspaces / registries** — environment where attack paths and AI models are inspected; models discovered across multiple workspaces/registries.
- **SARIF** — standardized scan output format consumed by the `fix` command.
- **Hugging Face** — external source of (potentially weaponized) model artifacts.
- **PyTorch / pickle serialization** — vulnerable model format; pickle deserialization can execute arbitrary code.
- **TensorFlow / safetensors** — safer model serialization formats the industry is moving toward.
- **Demo repos:** `benchmark-python` (code vulns), plus a separate ML repo (training scripts + model artifacts + deployment pipeline).

## 🚀 Announcements / What's New
- **Defender CLI is available today** — the terminal-native, agentic multi-model scanner (powered by M-) for code and AI model artifacts is generally available now.
- **Multi-model agentic scanning harness (code name M-)** revealed — 100+ specialized AI agents across frontier + distilled models, running a five-stage validate-and-prove pipeline, positioned as a step-change beyond single-model pattern-matching scanners.
- **AI Code Security Initiative** — unified security-posture rollup across CLI, pipeline, and agentless code scanning, with code-to-cloud correlation.
- **AI model security in Defender** — discovery of models across Azure ML workspaces/registries plus scanning for malicious/vulnerable content (e.g., malicious pickle serialization), in production *and* in-pipeline before deployment.
- **GitHub Advanced Security ↔ Defender for Cloud integration** enabling code-to-runtime tracing in both directions, PR annotations, and issue-creation-with-Copilot-assignment from attack paths.

## 💡 Demos
1. **Local CLI scan (`benchmark-python`):** Ran the Defender CLI in the terminal; caught vulnerabilities traditional pattern matching misses by reasoning about semantic logic flow — entirely local, pre-repository (shift-left).
2. **Terminal `fix` command:** Issued `fix` against the SARIF result file; Copilot analyzed the vuln, understood context, and rewrote the code in place — no ticket, no copy-paste, no context switch.
3. **VS Code side-by-side review:** Reviewed Copilot's changes (vulnerable code left, fixed code right); read files, applied logic, edited and wrote fixed files; reviewer can accept/reject each change, re-run tests, and commit.
4. **Pull request annotation (XPath injection):** Showed the finding in the PR with a plain-language explanation (header value injected into XPath query → predicate tampering / data disclosure) plus Copilot's suggested fix (parameterize the query / bound variable) and a verify-the-fix prompt.
5. **AI Code Security Initiative view:** Security-manager rollup of all findings with overall score, recommendations, repos with findings, and trends; demonstrated code-to-cloud risk-score differences (internet-exposed container w/ sensitive data vs. internal dev tool).
6. **Attack path in Azure portal:** Filtered on risk factors (internet exposure, sensitive-data path, high severity); explored a container's known vulnerabilities (incl. a recently-in-the-news package).
7. **Code → Build → Ship → Run lineage view:** Traced a running container back through registry, pipeline, and source repository/commit; prioritized code injections as critical-asset risks.
8. **GitHub issue + Copilot auto-fix:** Created/viewed a GitHub issue from the attack path, auto-assigned to Copilot; fixing one package (bump `0.1` → `1.13`) would also resolve 2-3 additional CVEs.
9. **AI model inventory + malicious pickle detection:** Discovered models across Azure ML workspaces/registries; yellow-bar flags; drilled into asset page → threats/vulnerabilities to see a pickle file flagged with a malicious serialization payload; reviewed remediation (unpublish/archive/replace).
10. **In-pipeline model artifact scan:** A separate ML repo's pipeline ran the Defender CLI and caught low-severity (but high-risk) model vulnerabilities *before the pipeline finished* — gating a bad model before deployment.

## 📊 Notable Stats / Quotes
- **"The model is one input. The system around it is the product."** — core design philosophy of the M- harness.
- **100+ specialized AI agents** orchestrated across an ensemble of frontier and distilled models.
- **5-stage pipeline:** prepare attack surface → scan candidate code paths → validate (agents debate reachability/exploitability) → deduplicate → prove (construct triggering inputs).
- **~2 weeks** — typical lag between code shipping and security findings landing on a developer's desk (the broken-workflow status quo).
- **1 fix → 3 additional CVEs** — fixing a single package in the demo resolved the critical finding plus three more CVEs (a package bump from `0.1` to `1.13`).
- *"Minutes, not days"* — time-to-fix once the CLI catches it, the pipeline gates it, and the PR annotates it with context.
- *"Replace, don't patch."* — remediation principle for both malicious model artifacts and container images (immutable artifacts).
- **"Early this year, attackers on Hugging Face were weaponizing model artifacts using pickle serializations"** — real-world threat motivating AI model security; loading the model triggers arbitrary code execution on pickle deserialization.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install and run the **Defender CLI** (available today) against a sample repo (e.g., the `benchmark-python` style project) to see what it catches vs. our current static analysis.
  - Test the terminal `fix` command + Copilot flow end-to-end (scan → SARIF → fix → review in VS Code → commit).
  - Wire the same engine into a **GitHub Actions** pipeline as a gate and confirm PR annotations with Copilot-suggested fixes show up.
  - Point the CLI at **model artifacts** (a PyTorch/pickle model) to verify malicious-serialization detection before deployment.
  - Explore the **AI Code Security Initiative** rollup and an **attack path** in the Azure portal to see code→build→ship→run lineage.
- [ ] Questions:
  - What is **M-** officially called (is the code name being replaced at GA), and what models actually make up the frontier + distilled ensemble?
  - Licensing/cost: is the Defender CLI free, bundled with Defender for Cloud, or gated behind GitHub Advanced Security?
  - How does it handle **transitive** vulnerabilities buried in base images — does it auto-trace and fix those too?
  - What are the false-positive/false-negative rates of the agent "debate" validation stage vs. traditional SAST?
  - Which CI systems beyond GitHub Actions are supported (Azure DevOps, GitLab, Jenkins)?
  - For AI model scanning — does it cover formats beyond pickle/PyTorch (ONNX, GGUF, safetensors edge cases)?
- [ ] Relevant to:
  - DevSecOps / shift-left security strategy and tooling consolidation.
  - Azure / Defender for Cloud posture management and attack-path prioritization.
  - GitHub Advanced Security + Copilot adoption for automated remediation.
  - AI/ML supply-chain security and model governance (Azure ML workspaces/registries).
  - Any team shipping containerized, internet-exposed workloads handling sensitive data.

## 🔗 Related
- 