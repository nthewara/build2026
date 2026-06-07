---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/terraform
  - topic/hashicorp
  - topic/iac
  - topic/azure
  - topic/governance
  - topic/policy-as-code
source: https://www.youtube.com/watch?v=w9CXxGHi2HA
session_code: ODSP901
event: Microsoft Build 2026
speakers: Karim Satili (Senior Developer Advocate, HashiCorp)
duration_min: 18
aliases:
  - Discover, govern, and scale Azure resources with HashiCorp Terraform
---

# ODSP901 — Discover, govern, and scale Azure resources with HashiCorp Terraform

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Karim Satili — Senior Developer Advocate, HashiCorp (focus: infrastructure & orchestration tooling)  
> **Duration:** ~18 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=w9CXxGHi2HA)

## 🎯 TL;DR
Every Azure team believes they manage "everything with Terraform" — but when you actually diff Terraform state against what's running, real coverage is usually **40–60%**, not the 80–90% people claim. This HashiCorp partner session is about closing that **unmanaged-resource gap** quickly. The headline is **`terraform query` (Terraform search)** — a new CLI capability (Terraform **1.14**, released **November 2025**) that *inverts* the import workflow: instead of you knowing the resource ID up front and hand-writing an `import` block, Terraform **discovers** unmanaged resources via a search query, **generates the config + import blocks for you** into a `.tf` file, and lets you plan/apply the import. The session then layers **HashiCorp Sentinel** policy-as-code on top to govern the newly imported resources (tags, naming conventions, instance types) and eliminate drift. The pitch: turn "three weeks of inventory work" into "three commands."

## 🔑 Key Takeaways
- **The coverage gap is real and unmeasured.** Teams self-report 80–90% Terraform coverage; actual is typically **40–60%**. The problem isn't dishonesty — *nobody is measuring* the delta between state and reality.
- **Resources escape IaC for human reasons, not engineering failures.** Four recurring patterns: (1) "I'll codify it later" (later never comes), (2) the **2 a.m. incident fix** done by hand, (3) **acquisitions** where you inherit an unknown subscription, (4) the **PoC that became production** because it worked and nobody rebuilt it.
- **The goal isn't prevention — it's a fast path back.** You can't stop these situations from happening; you need a quick route from *unmanaged → managed*.
- **The gap is worse for AI/GPU workloads.** Untagged GPU resources break **cost attribution** (which team/experiment/project?), ungoverned subnets collapse **network isolation** between training and inference, and undefined managed-identity scopes destroy your **audit story** (identity sprawl, acute for agent-based architectures).
- **Import has evolved in three stages:** (1) old `terraform import` CLI — one resource/one address at a time, slow; (2) **import blocks** (since Terraform **1.5**) — plan-first, PR-reviewable, but *you still write the block and must already know the resource ID*; (3) **`terraform query` / search** (since **1.14**) — Terraform discovers the resources *and* generates the config.
- **`terraform query` is a 3-step workflow:** define a search query → run `terraform query` (authenticates to Azure like a normal plan, queries the remote API for unmanaged resources) → **generate code** into a `.tf` file.
- **No credentials in the query file.** Terraform search **inherits auth from your existing provider config** — if a normal `terraform plan` succeeds, `terraform query` succeeds.
- **Generated config includes `import` blocks.** Each discovered resource comes with an `import` block, so bringing it into state is a single `plan` + `apply` cycle — and because it uses import blocks, it works with **HCP Terraform**.
- **Import retains existing configuration.** Terraform does **not** change the imported resource's config unless you tell it to — so right after import, resources still carry their old (possibly non-compliant) settings.
- **Govern with Sentinel after importing.** **HashiCorp Sentinel** is a policy framework that *blocks* Terraform operations that violate policy. Use it to enforce tags, naming conventions, instance types, etc., on the newly imported resources.
- **Start in soft-fail, move to hard-fail.** The demo runs Sentinel in **soft-fail** (advisory only) — move to **hard-fail** as soon as possible so non-compliant changes are actually blocked.
- **Don't reinvent policies.** The **Terraform Registry** (`registry.terraform.io`) has ready-made **policy packs for Azure** to get you started.
- **It can be made agentic.** HashiCorp **Terraform agent skills** let you set much of this up programmatically / through agentic loops.

## 📚 Detailed Notes

### The problem: the gap between state and reality
The session frames a problem "every Azure team has but very few have a clean answer for": the gap between **what's in your Terraform state** and **what's actually running** in your subscriptions and tenants.

When the speaker asks practitioners for a coverage number, he hears 80%, 90%, sometimes higher. But when they sit down and actually compare Terraform state against what's running, the **real number is 40–60%**. A few teams genuinely hit 80%. Regardless of the number, everyone believes the same thing: *"we do everything with Terraform."*

The gap "isn't dishonesty, it's that nobody's measuring." Resources accumulate outside IaC for entirely human reasons, and historically the path back from unmanaged → managed required either **a heroic engineering effort** or **a freeze you couldn't afford**. The session promises a workflow that closes that gap **"in a quarter rather than a quarter-year."**

### Sidebar: what IaC / Terraform actually is
For anyone unsure what IaC or Terraform is: the *traditional* way to provision in Azure is to open the **Azure portal**, find the service, and manually click together your infrastructure. It seems fast but is **error-prone** — to reproduce the same result you must click the exact same buttons again with no mistakes.

**Infrastructure as Code** instead lets you describe infrastructure in **human-readable text files** that you can **version control** and **review with colleagues**. Because it's code, tools like **Terraform** can parse it and turn your prose into provisioned infrastructure.

### Why resources end up un-codified — the four patterns
None of these are failures of engineering discipline:

1. **"I'll codify it later."** (Most common.) Someone well-intentioned clicks something in the portal during exploration, fully meaning to bring it under management later — but later never arrives.
2. **The 2 a.m. incident fix.** Writing Terraform while production is down is a hard sell, especially for teams that don't already codify everything.
3. **The acquisition.** You inherit an environment you've never seen. All you know is there's a new subscription in your account full of stuff that doesn't look like it belongs.
4. **The PoC that became production.** It worked, it was already live serving customers, and nobody had time to rebuild it properly.

The point of the list is **not to prevent these** — you can't, and they'll keep happening — but to have a **fast path back**.

### Why the gap is worse for AI workloads
This isn't about agentic loops generating code — it's about **actual GPU resources** for AI, LLM, and ML infrastructure. The governance failures bite harder here:

- **Cost attribution breaks.** Missing tags mean the organization struggles to figure out which experiment, team, and project a given (expensive GPU) resource belongs to.
- **Network isolation collapses.** Training and inference environments have very different security postures; **one ungoverned subnet** can collapse that boundary.
- **Identity sprawl (specific to agent-based architectures).** Every agent has a managed identity; every managed identity has scopes. If those scopes **aren't defined in code**, your audit story falls apart the moment someone asks.
- **Data blast radius.** E.g. a storage account left **publicly accessible** is a leak waiting to happen.

### The evolution of importing in Terraform
Terraform has understood this problem for a long time. The import story has three generations:

1. **`terraform import` (the old CLI command).** Has existed for years and still works. But it's **one resource, one address at a time** — therefore time-consuming.
2. **Import blocks (since Terraform 1.5).** A real improvement: you get a **plan-first model**, you can review the generated config in a **pull request**, and apply when happy. *But* — **discovery is still on you**. You're still writing the import block yourself, which means **you already need to know the resource ID** inside Azure and that the resource actually exists. (Even with tooling that infers it, the discovery burden remains.)
3. **Terraform search / `terraform query` (since Terraform 1.14, Nov 2025).** This is the leap the session is built around — it removes the discovery burden.

### `terraform query` (Terraform search) — the core feature
Available in the **Terraform CLI since 1.14** (released **November 2025**). It upgrades imports by **inverting the import question**:

- **Old framing:** *"I know what I want — now help me write the config."*
- **New framing:** *"Show me what's there, generate the config from it, then let me plan the import."*

**Three steps:**
1. **Define a search query** — e.g. *"Give me all unmanaged MSSQL servers in my subscription that are in the MS Build resource group."*
2. **Run `terraform query`** on the CLI. It **authenticates to Azure the way you normally do** and queries the remote API for all the unmanaged resources. Takes a minute or two depending on data volume / number of resources.
3. **Generate code.** No more hand-coding, no copy-paste errors or forgotten attributes — Terraform **generates the code for you, stored in a `.tf` file** so you can inspect it, peer-review it, and align resources to your org's requirements.

The tagline: **"three commands instead of three weeks of inventory work."**

**Key authentication note:** you do **not** specify Azure credentials in the query file. Terraform search **inherits them from your overall provider config**. So as long as a normal `terraform plan` run can succeed, `terraform query` will also succeed.

**Scoping:** you can make queries more prescriptive by constraining to a **specific resource group** (e.g. only list unmanaged resources in the `Microsoft Build 2026 unmanaged` resource group). ⚠️ **Caveat:** if your constraints cause the API to return nothing, Terraform won't find anything either. **Don't hard-code variable values or resource names** — use variables and make sure the constraints actually match real resources.

### The generated `unmanaged.tf` file
Running `terraform query` again **with a path argument** exports the config to a file. In the demo, four discovered resources produced **~300 lines** of import statements and resource definitions. Notable details:
- Terraform leaves a **comment at the top** marking it a **generated file**, plus a **warning to inspect and verify everything** (not shown on screen but present in the file).
- Below **each** discovered + generated resource there's an **`import` block** to easily bring that currently-unmanaged resource into Terraform state.
- Importing is just **one `terraform plan` + `apply` cycle**.
- Because it uses import blocks, you can **use HCP Terraform** for this.

### "Are we done?" — no, govern next
After import you *could* stop — you've gone from unmanaged to managed in an almost programmatic way (and could automate further with the **HashiCorp Terraform agent skills** / agentic loops). But importing **retains all the old configuration** — Terraform made **no changes** to it. So the resources are managed but **not yet compliant**.

The next level is to **apply organizational policies** to the newly imported resources to **eliminate drift** and make them "feel and behave like other resources" — right tags, right naming conventions, appropriate instance types, correct SKUs, and anything else you can express as a policy.

### Governance with HashiCorp Sentinel (policy-as-code)
**Sentinel** is HashiCorp's **policy framework** that **blocks Terraform from carrying out operations that are not in line with your policy definitions.** The demo policy is built up as:

1. **Define the resource types to match** against — the set of public IPs, the NAT gateway, the security group.
2. **Collect all planned resources that are taggable** whenever a plan runs.
3. **Loop over those resources and collect their tags.**
4. **Evaluate a conditional** for violations — e.g. a **missing owner tag** or an **owner tag in the wrong format**. (Demo is deliberately simple; real orgs would have many more policies.)

Apply the policy **through Sentinel**, just like running Terraform. The result (as expected) shows the imported resources are **not aligned with the org's naming policy** — because they were knowingly imported in a non-compliant state. **Terraform happily imports them; Sentinel then prevents further changes until the drift is eliminated.**

**Soft-fail vs hard-fail:** the demo uses Sentinel in **soft-fail mode** — you get an **advisory** and can still continue. The guidance: **move to hard-fail as soon as possible** so your infrastructure is properly governed and non-compliant changes are actually blocked. (Actually *fixing* all the violations is "a task for another time.")

**Getting started with policies:** check the **Terraform Registry** (`registry.terraform.io`) for **policy packs specifically for Azure** use cases.

### Conclusion
End state: infrastructure that is **Terraform-managed** *and* **governed by appropriate Sentinel policies**. The two-line takeaway the speaker leaves you with:
- Use **`terraform query`** to bring unmanaged resources under management.
- Use **Sentinel** to enforce policies that make sense for your organization.

Three closing links were recommended: the **CLI command documentation**, a **blog post** on the why/how of `terraform query`, and a **Sentinel playground** to see the full policy in action.

## 🛠️ Products / Features / Technologies Mentioned
- **HashiCorp Terraform** — IaC tool that parses human-readable config and provisions infrastructure; the backbone of the whole session.
- **Terraform state** — the record of what Terraform manages; the gap vs. running reality is the central problem.
- **`terraform import` (CLI command)** — legacy import, one resource/one address at a time; slow but still supported.
- **Import blocks** — plan-first, PR-reviewable import mechanism introduced in **Terraform 1.5**; still requires you to know the resource ID.
- **Terraform search / `terraform query`** — new CLI capability (**Terraform 1.14**) that discovers unmanaged resources and generates config + import blocks for you.
- **HCP Terraform** (Terraform Cloud) — referenced as a place to run the import-block workflow.
- **HashiCorp Sentinel** — policy-as-code framework that blocks Terraform operations violating defined policy; used for tag/naming/instance-type governance. Supports **soft-fail** (advisory) and **hard-fail** (blocking) modes.
- **Terraform Registry** (`registry.terraform.io`) — source of ready-made **Azure policy packs**.
- **HashiCorp Terraform agent skills** — let you set up discovery/import programmatically and via agentic loops.
- **Azure portal** — the "click-ops" provisioning path that IaC replaces; used in the demo to show the messy unmanaged environment.
- **Azure resources demoed** — NAT gateway, network security groups, public IP addresses, storage account, function app, private DNS, networking foundations (~30 resources in one resource group), plus MSSQL servers (used in the example query).

## 🚀 Announcements / What's New
- **`terraform query` / Terraform search** is the standout new capability — available in the **Terraform CLI since version 1.14, released November 2025**. It enables **discovery of unmanaged resources + automatic config and import-block generation**, removing the manual "you must already know the resource ID" step of import blocks. (Presented as available/released, not a preview.)
- No private/public-preview or GA-gating language was used for the other features; **import blocks (Terraform 1.5)** and **Sentinel** were referenced as established, existing capabilities.

## 💡 Demos
A single connected end-to-end demo (Discover → Import → Govern):
- **Survey the mess (Azure portal).** Opens the subscription showing **~30 unmanaged resources** scattered across one resource group (networking, security groups, NAT gateway, storage account, function app, private DNS, public IPs). Inconsistent/partial tagging; framed as "three teams clicked this together over a year" — different conventions, no central inventory, unclear dependencies. *Point: this is the realistic unmanaged starting state.*
- **Write the search query.** Highlights three target resources to discover — the **NAT gateway**, the **security groups**, and the **two public IP addresses** — and constrains the NAT gateway query to the `Microsoft Build 2026 unmanaged` resource group. Notes **no Azure credentials in the file** (inherited from provider config). *Point: discovery is declarative and scoped; auth is automatic.*
- **Run `terraform query`.** After a few seconds, discovered resources appear (shows the first two for brevity). *Point: Terraform finds the resources for you — no manual inventory.*
- **Export & inspect `unmanaged.tf`.** Re-runs `terraform query` with a path to save config; the four resources generate **~300 lines** including a **generated-file comment**, an **inspect/verify warning**, and an **`import` block per resource**. *Point: review-ready, peer-reviewable generated config + one-cycle import.*
- **Author & apply a Sentinel policy.** Builds a policy matching the resource types, collecting taggable planned resources and their tags, and checking for a **missing/mis-formatted owner tag**. Applies via Sentinel in **soft-fail**; result correctly flags the imported resources as **non-compliant with naming policy**. *Point: import alone isn't governance — Sentinel catches and (in hard-fail) blocks drift.*

## 📊 Notable Stats / Quotes
- **40–60%** — the *actual* Terraform coverage most teams have when state is diffed against running resources.
- **80–90%+** — what teams *self-report* (the perception gap).
- **"The gap here isn't dishonesty, it's that nobody's measuring."**
- **Terraform 1.5** — introduced import blocks.
- **Terraform 1.14 (November 2025)** — introduced `terraform query` / search.
- **~30 resources** — in the single demo resource group.
- **~300 lines** — of generated config + import statements for just **four** discovered resources.
- **"Three commands instead of three weeks of inventory work."**
- On `terraform query` inverting import: from *"I know what I want, now help me write the config"* → *"show me what's there, generate the config from it, then let me plan the import."*
- **"Terraform happily imports those. Sentinel then prevents you from making further changes until you've eliminated this drift."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run `terraform query` against a real Azure subscription/resource group to measure the *actual* vs *assumed* coverage gap.
  - Try the discover → generate → import → `plan`/`apply` loop on a few known-unmanaged demo resources (NAT gateway / NSG / public IP) end-to-end.
  - Pull an **Azure policy pack** from `registry.terraform.io` and run it in Sentinel **soft-fail**, then promote to **hard-fail**.
  - Wire the generated import blocks through **HCP Terraform** rather than local CLI.
  - Explore the **HashiCorp Terraform agent skills** for automating discovery/import in an agentic loop.
- [ ] Questions:
  - Which Azure resource types are actually queryable via `terraform query` 1.14 today (full provider coverage vs gaps)?
  - How does `terraform query` handle dependencies between discovered resources (ordering of imports)?
  - Performance/scale: how does query time grow with subscription size / number of resources?
  - Best practices for de-duplicating against resources *already* in state when running broad queries.
- [ ] Relevant to:
  - Azure landing-zone / governance work and IaC drift remediation.
  - Cost attribution + tagging strategy for GPU/AI workloads.
  - Lab cleanup — discovering click-ops resources accumulated in test subscriptions.

## 🔗 Related
- [[Terraform]] — the IaC tool whose import/query workflow this session uses to close the coverage gap on Azure.
- [[Terraform import and terraform query]] — the discover→query→generate evolution (import blocks → `terraform query`/search) headlined here.
- [[HashiCorp Sentinel]] — the policy-as-code engine demoed for governing Azure resources (soft-fail vs hard-fail).
- [[OD827 - Build deploy and run Linux workloads on Azure]] — adjacent Azure infrastructure/operations session.
- [[Azure governance and policy-as-code]] — broader governance context (Azure Policy packs, naming standards) this talk plugs into.
- Source list: [[2026 Build Session List]]
