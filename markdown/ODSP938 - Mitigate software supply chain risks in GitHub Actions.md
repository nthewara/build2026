---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/supply-chain
  - topic/github-actions
  - topic/security
  - topic/devops
source: https://www.youtube.com/watch?v=FPjvL-No46E
session_code: ODSP938
event: Microsoft Build 2026
speakers: Erica Heidi (Staff DevRel Engineer, Chainguard)
duration_min: 15
aliases:
  - Mitigate software supply chain risks in GitHub Actions
---

# ODSP938 — Mitigate software supply chain risks in GitHub Actions

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Erica Heidi — Staff DevRel Engineer, Chainguard  
> **Duration:** ~15 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=FPjvL-No46E)

## 🎯 TL;DR
A short, practical theater session from Chainguard's Erica Heidi laying out **five concrete strategies to reduce software supply chain risk in GitHub Actions**: (1) inspect repos for insecure defaults — and let GitHub Copilot agent audit your workflows for you; (2) minimize your attack surface by stripping unneeded runtime/OS dependencies (e.g. using minimal container images); (3) pull dependencies from trusted sources because ~98% of malware is injected at build/distribution time, not in source; (4) pin actions and images **by digest, not by tag**, since tags can be rewritten/hijacked; and (5) **ban long-lived Personal Access Tokens (PATs)** in favor of short-lived, scoped credentials. The recurring real-world case study is the **Trivy compromise**, where an org-wide PAT plus `pull_request_target` code execution and tag rewriting gave attackers full control of an org. Chainguard tooling (minimal containers, language libraries, digestabot, Octo STS) is presented as a way to operationalize each tip.

## 🔑 Key Takeaways
- **Five-step mental model:** inspect → minimize attack surface → trust your sources → pin by digest → kill long-lived PATs.
- **`pull_request_target` + code execution is one of the most dangerous misconfigs:** PR code runs in the context of the main branch, with access to its secrets and environment variables, enabling **secret exfiltration** from forks/external contributors.
- **Tags are mutable and therefore untrustworthy:** attackers can rewrite an existing tag to point at a malicious commit, so anyone pinning by tag silently pulls poisoned code. **Always pin actions and container images by digest (immutable hash).**
- **The Trivy attack is the canonical example:** an **org-wide PAT with broad privileges** was exfiltrated via `pull_request_target`, and attackers rewrote prior tags to the same malicious commit — giving them full org control (create/delete repos, cut releases, etc.).
- **Use GitHub Copilot agent as a security auditor:** prompt it directly in your repo to "evaluate my GitHub Actions and find potential vulnerabilities." In the demo it correctly flagged `pull_request_target` code execution, write-capable tokens on PRs, secrets exposed to attacker-controlled binaries, and tag-based action pinning.
- **~98% of malware is inserted at build & distribution time**, not in the reviewed source code — so source review alone gives a false sense of security. This is the "**ghost release**" gap between verifiable source and the actual published artifact.
- **Public registries were built for distribution/collaboration, not security:** most language-ecosystem registries (npm, PyPI, etc.) lack strong anti-tampering protections, making them attractive propagation nodes.
- **Minimal images dramatically cut CVE exposure:** Chainguard's Python image reported **~4 CVEs vs ~579** for the default Docker Hub Python image — a "low-hanging fruit" win just from swapping base images.
- **Attackers are "shifting left"** — turning developer laptops and CI/CD pipelines into propagation nodes because that's where credentials and secrets live, enabling lateral movement across projects and even orgs.
- **Protect `main` and release tags by default** — these protections are **off out of the box**; enable branch protection (no direct pushes) and tag protection (no rewrites) to contain malicious-code propagation and blunt stolen-PAT injection.
- **Short-lived tokens limit blast radius:** even if a credential leaks, it expires quickly. Octo STS issues temporary, scoped credentials using the concepts behind Sigstore/Cosign.
- **Defense in depth, not removing functionality:** the goal is removing what you *don't* need (extra deps, broad scopes, mutable refs), not stripping features you actually use.

## 📚 Detailed Notes

### Framing: why GitHub Actions is a supply chain target
GitHub Actions workflows execute code with access to secrets, tokens, and environment variables, and they pull in third-party actions and dependencies — both **direct and transitive**. Any weak link in that chain can become a foothold. Even **low-privilege access** can be a starting point for privilege escalation and further exploitation. Erica frames the talk around five strategies, each illustrated with concrete misconfigurations and the real-world **Trivy** compromise.

### Tip 1 — Inspect repositories for insecure defaults and bad practices
Start by auditing what's already wrong. The bad practices to hunt for:
- **`pull_request_target` with head/PR code execution** — the headline risk (detailed below).
- **Long-lived Personal Access Tokens (PATs) with broad privileges** — over-scoped, rarely rotated.
- **Direct shell execution that can be manipulated by external actors** — untrusted input flowing into shell steps.
- **Actions pinned by tag** rather than by immutable digest.
- **Unprotected `main` branch** and **unprotected release tags** — mutable refs an attacker can overwrite.

This can feel overwhelming to audit by hand. The recommended shortcut: **use the GitHub Copilot agent directly in your repository** and ask it to evaluate your GitHub Actions and find potential vulnerabilities. Erica built an **intentionally vulnerable demo repo** (designed to demonstrate secret exfiltration) and Copilot was "very successful" at detecting the issues.

#### What Copilot flagged in the demo
- **`pull_request_target` with code execution** (running a Go setup step). **Why it's dangerous:** when someone opens a PR, the PR's code is executed — and with `pull_request_target` it runs **in the context of the actual main branch**, with access to all the **secrets and environment variables** used in real main-branch builds. Depending on how the workflow runs code, **any secret or variable can be exfiltrated**. This is the **same method used in the initial Trivy exploitation**, where attackers abused `pull_request_target` running with a broadly-privileged PAT.
- **Secrets exposed to a target/attacker-controlled binary** — rated critical.
- **A write-capable token granted permission to write pull requests** — high risk.
- **An action snippet pinned to a tag** — insecure because **tags can be rewritten**. This too featured in the Trivy attack: attackers rewrote previous tags to all point to the same malicious commit, so anyone pinning by tag would pull the new, payload-injected code.

#### Branch and tag protection
Because these protections are **off by default**, you must enable them in repo settings:
- **Protect release tags** so they cannot be rewritten → prevents malicious code from being re-released to downstream users and **contains propagation**.
- **Protect `main`** so nobody can push directly → blunts attackers who use a **stolen PAT to inject straight onto main**.

### Tip 2 — Minimize your attack surface
"Simple in theory" — fewer entry points means fewer things to exploit; a low-hanging fruit you can't ignore. Key points:
- **Account for direct *and* transitive dependencies** — the dependencies of your dependencies are also risk. Any weak link can be a foothold; even from low privilege, attackers may escalate.
- **The goal is not to remove functionality** you actually use — it's to remove what **doesn't need to be in your runtime**. There are typically many runtime-level and **base-OS-level dependencies you don't need**.
- **Use minimal container images** to shrink that surface. Erica's example: **Chainguard containers** are very minimal and **build all packages from source**, which keeps images up to date with patches applied. The payoff cited: a **Chainguard Python image with ~4 CVEs vs ~579 CVEs for the default Docker Hub Python image** — a significant reduction achieved simply by swapping the base image used to build your runtimes and GitHub Actions environments.

### Tip 3 — Pull from trusted sources
The core statistic and threat model:
- **98%+ of malware is inserted during build and distribution time**, bypassing the normal maintainer review of source code. You don't see the malicious code in the repo because it's **injected during CI/CD directly into the artifacts** produced at build time and then distributed to registries everywhere. Public repos download these **tampered artifacts**, which differ from the source code. There's generally **low visibility into what happens at build time**.
- **"Ghost release":** attackers exploit the gap between the **verifiable source code** and the **build artifacts** that consumers actually pull from public registries.
- **Public registries lack security guarantees:** they were built mostly to facilitate **distribution and collaboration**, not to protect artifacts from tampering. Most public registries across language ecosystems **don't have strong anti-tampering measures** — security wasn't the original concern at the volume/scale we now share code.
- **Attackers are "shifting left":** they focus on turning **developer laptops and CI/CD pipelines into propagation nodes**, because that's where credentials and secrets live. With those credentials they **spread laterally** to other projects and even other orgs.

#### Chainguard libraries as a trusted source
Reduce this risk by pulling language dependencies from a trusted source — **Chainguard libraries**, currently available for the **Python, Java, and JavaScript** ecosystems. How it works:
- Builds run in a **safe, temporary, reproducible ("tamper-proof") build environment**.
- Dependencies are pulled directly from Chainguard's repos.
- **Pre- and post-install scripts are not executed**, so you only get versions that are safe to install.
- Claimed result: **avoid 90%+ of the risk associated with build/distribution-time attacks.**

### Tip 4 — Pin by digest, not by tag
Even Copilot flagged that you shouldn't reference actions by tag. Instead **pin to a digest**:
- A **digest is a unique hash** pointing to a **specific build** of a container image or GitHub action. Pinning by digest means you're **never pulling unknown code** — you always pull the exact same build/code you ran before, immune to tag rewriting.
- **Trade-off:** digests **go stale** over time; you must update the digest when new versions of the image or action are released. The upside is it **gives you time to update on your terms** instead of silently pulling whatever a mutable tag now points to.

#### digestabot
To keep digests current, Chainguard created **digestabot** — a **free, open-source tool** that keeps your workflows and Dockerfiles up to date. Whenever a new version of a container or GitHub action is released, **digestabot opens a pull request with the updated digest**. You configure it via a **workflow YAML file**, and it then performs these digest updates automatically. Pinning by digest (kept fresh by digestabot) is presented as the **safest tagging practice** for containers and GitHub Actions.

### Tip 5 — Ban long-lived Personal Access Tokens
Don't use long-lived tokens — they're dangerous because:
- People **forget about tokens**, often grant **very long expiry** and **broad privileges**.
- This is exactly what enabled **Trivy**: an **org-wide PAT was exfiltrated**, giving attackers **full control over the whole org** — they could **delete and create repos, create releases, and do basically anything**.

The fix is **short-lived tokens** that grant **only limited privilege** to a workflow run **for a limited time**. Even if exfiltrated, the credential **expires quickly**, so a leak is far less catastrophic.

#### Octo STS
Chainguard offers a **free GitHub App called Octo STS** that implements this strategy using **the same concepts behind Sigstore and Cosign**. It **issues temporary credentials that expire after a short period**. Octo STS acts as the **identity that opens/authorizes requests in your repo**, and you install it from GitHub.

### Closing recap (the speaker's own TL;DR)
1. **Inspect** your repository for insecure defaults and bad practices — use **Copilot** to evaluate your GitHub Actions and find vulnerabilities.
2. **Minimize attack surface** — remove unneeded runtime software → fewer entry points and fewer vulnerabilities.
3. **Pull from trusted sources** — npm incidents are increasing; be deliberate about **where your open-source software comes from**.
4. **Pin by digest, not by tag** — tags can be hijacked; use **digestabot** to keep digests updated.
5. **Ban long-lived PATs; use short-lived tokens** — use **Octo STS** for this.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Actions** — CI/CD workflow platform; the subject of the talk and the primary attack surface discussed.
- **GitHub Copilot agent** — used in-repo as a security auditor; prompted to "evaluate my GitHub Actions and find potential vulnerabilities," and successfully detected the demo's misconfigs.
- **`pull_request_target`** — GitHub Actions trigger that runs PR code in the base/main-branch context with access to its secrets; the central dangerous misconfiguration.
- **Personal Access Tokens (PATs)** — long-lived GitHub credentials; over-scoped/org-wide PATs are the recurring root cause (Trivy).
- **Branch protection / tag protection** — GitHub repo settings (off by default) that prevent direct pushes to `main` and rewriting of tags/release tags.
- **Container image digests** — immutable content hashes for pinning images/actions instead of mutable tags.
- **Chainguard containers** — minimal container images built from source, kept patched; cited ~4 CVEs vs ~579 for default Python.
- **Chainguard libraries** — trusted-source language dependencies for **Python, Java, and JavaScript**; built in tamper-proof environments, no pre/post-install scripts executed.
- **digestabot** — free, open-source Chainguard tool that auto-opens PRs to update image/action digests in workflows and Dockerfiles.
- **Octo STS** — free Chainguard GitHub App issuing short-lived, scoped credentials (built on Sigstore/Cosign concepts) as the identity that authorizes repo requests.
- **Sigstore / Cosign** — signing/identity technologies whose concepts underpin Octo STS's temporary-credential model.
- **Docker Hub** — referenced as the source of the default (high-CVE) Python image, contrasted with Chainguard's minimal image.
- **npm / PyPI (public registries)** — language-ecosystem registries cited as lacking strong anti-tampering protections; npm incidents noted as increasing.
- **Trivy** — referenced as the real-world supply chain compromise case study (org-wide PAT exfiltration + `pull_request_target` + tag rewriting).

## 🚀 Announcements / What's New
None explicitly announced. This was a best-practices/strategy theater session; the Chainguard tools referenced (minimal containers, libraries, digestabot, Octo STS) are presented as existing, available offerings rather than new releases or previews.

## 💡 Demos
- **Intentionally vulnerable demo repository + Copilot audit:** Erica set up a repo containing many deliberately insecure configurations, built specifically to demonstrate **secret exfiltration** via a vulnerable GitHub Actions workflow. She then ran the **GitHub Copilot agent** with a prompt to evaluate the Actions and find vulnerabilities. **Point proved:** Copilot reliably surfaced the real issues — `pull_request_target` with code execution (running Go setup), secrets exposed to an attacker-controlled binary, a write-capable token allowed to write PRs, and an action pinned by tag — demonstrating that an AI agent can do a fast, effective first-pass security review of your workflows.

## 📊 Notable Stats / Quotes
- **~4 CVEs vs ~579 CVEs** — Chainguard's minimal Python image versus the default Docker Hub Python image.
- **98%+ of malware is inserted during build and distribution time** (bypassing source-code review) — the core argument for pulling from trusted sources.
- **90%+ of build/distribution-time risk avoided** — claimed benefit of using Chainguard libraries.
- **Trivy compromise:** an exfiltrated **org-wide PAT** gave attackers full org control — ability to **create/delete repos and create releases** at will.
- Paraphrased framing: *"I hope you stay safe and see you next time."* — closing sign-off.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run the **GitHub Copilot agent** against our own repos with the prompt "evaluate my GitHub Actions and find potential vulnerabilities" as a quick first-pass audit.
  - Audit workflows for **`pull_request_target` + code execution** and confirm no fork PR can reach main-branch secrets.
  - Enable **branch protection on `main`** (no direct push) and **tag/release-tag protection** (no rewrite) where missing.
  - Migrate action and base-image references from **tags → digests**; trial **digestabot** to keep them fresh.
  - Evaluate **Chainguard minimal images** (esp. language base images) to cut CVE counts in CI runners.
  - Inventory **PATs**; replace long-lived/org-wide PATs with short-lived scoped tokens; trial **Octo STS**.
- [ ] Questions:
  - How does Octo STS's trust model (Sigstore/Cosign-based OIDC) compare to GitHub's native OIDC-to-cloud federation — when would we pick one over the other?
  - What's the maintenance overhead of digest pinning at scale, and does digestabot batch updates sensibly to avoid PR noise?
  - Coverage/limits of Copilot's vulnerability detection vs dedicated tooling (e.g. GHAS code scanning, zizmor, StepSecurity Harden-Runner)?
- [ ] Relevant to:
  - Any team owning GitHub Actions pipelines; DevSecOps / platform engineering; supply chain security (SLSA), SBOM, and CI/CD hardening initiatives.

## 🔗 Related
- 
