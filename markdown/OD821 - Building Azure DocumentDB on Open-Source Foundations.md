---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/documentdb
  - topic/nosql
  - topic/open-source
  - topic/databases
  - topic/postgres
  - topic/ai
source: https://www.youtube.com/watch?v=nvwl9Qp1x3I
session_code: OD821
event: Microsoft Build 2026
speakers: Abinav Romesh (Product Manager, Azure DocumentDB)
duration_min: 42
aliases:
  - Building Azure DocumentDB on Open-Source Foundations
---

# OD821 — Building Azure DocumentDB on Open-Source Foundations

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Abinav Romesh — Product Manager, Azure DocumentDB team  
> **Duration:** ~42 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=nvwl9Qp1x3I)

## 🎯 TL;DR
This session tells the "long winding story" of how Microsoft built **Azure DocumentDB** — a fully **MongoDB-compatible, PostgreSQL-backed NoSQL document database** — by starting with a managed service, going *back* to build an open-source engine from it, then funnelling all the open-source learnings *back* into the managed product. PM Abinav Romesh walks through the ~1.5-year open-source journey (MIT license, the Linux Foundation, and the crucial distinction between the open-source **project** and the commercial **product**), explains *why Postgres* was the foundation (extensibility via Citus, PG vector, etc.), and then details the three pillars of the managed service: **cheaper** (decoupled storage/compute, up to 32 TB disks, no charges for backups/networking/support/metrics), **faster** (SSD v2 driving 12× IOPS gains and **1 million writes/sec on a single node**), and **better** (multicloud + hybrid-cloud replication with zero data loss). Two live demos show globally distributed failover across Azure/AWS/GCP and on-prem↔Azure hybrid sync.

## 🔑 Key Takeaways
- **Azure DocumentDB = a fully MongoDB-compatible, Postgres-backed, open-source NoSQL document database**, offered as a fully managed Azure service built on top of the open-source engine.
- **Unusual build order:** managed service first → open-sourced the engine → fed open-source learnings back into the managed product. The open-source project is the foundation under the commercial product.
- **The single biggest learning was separating "project" vs "product"** — two distinct cohorts with two completely different success metrics (community-health metrics vs business metrics) that must coexist.
- **MIT license** was chosen deliberately for maximum permissiveness and zero friction: three paragraphs, no restrictions, ~10 seconds to read. "No regrets, clearly the right decision."
- **Joining the Linux Foundation** was about *credibility and trust*: it reassures developers Microsoft can't "pull the rug" — even if everyone left, the foundation keeps the project alive (directly addresses the "elephant" and "bus" factors).
- **Three open-source health metrics introduced:** **elephant factor** (how many orgs supply ≥50% of contributions — want it *high*), **bus factor** (how many key contributors must vanish before the project stalls — want it *low*), **heartbeat factor** (commits / PRs / releases over time = momentum).
- **Why Postgres:** in the AI era there's "no luxury of time to start from scratch." Postgres is extensible — replication/HA (Citus), graph, and **vector search (PG vector)** are all extensions, so DocumentDB didn't reinvent indexing, query performance, throughput, or HA.
- **DocumentDB's own contribution** is the **query protocol/translation layer** on top of Postgres that funnels NoSQL/MongoDB-style operations into the Postgres engine.
- **Three product pillars: cheaper, better, faster** — and improvements on each must not cost the user more.
- **Cheaper via decoupled storage & compute:** disks scale to **32 TB today** (vs competitors capping at ~4 TB), heading to 64 TB and eventually 256 TB. A 200 TB customer dropped from **~100 compute nodes to ~13** because storage increments are far cheaper than compute increments.
- **"Two knobs only" pricing:** no charge for product support, no managed-service license/subscription lock-in (tear down the cluster = pay nothing), **no backup charges, no networking/egress charges (~20% of a competitor's bill), no metrics/observability charges.**
- **Real TCO wins:** a DB2-on-prem → DocumentDB migration (262 TB) saved **~$9 million/year**; an HBase migration **cut the bill by more than half**, with the bigger win being *fewer decisions* (just machine size + disk size).
- **Faster via Azure SSD v2 (premium managed disks):** IOPS cap went from 20,000 → **80,000 (≈12× performance)**, decoupled from disk size, at **no extra cost** — pricing dropped from $2,880–$4,500/mo down to a flat **$280/mo** for the same performance.
- **Milestone:** **1,000,000 writes/sec on a single 32-core node** with only a 2 TB disk — **~200,000 transactions/dollar, nearly 2× a competitor's transactions-per-dollar** (with headroom to spare).
- **Better via open-source foundation:** **multicloud replication** (Azure primary → AWS + GCP) and **hybrid-cloud sync** (on-prem/Kubernetes ↔ Azure) with **global strong consistency and zero data loss**, managed via a **Kubernetes operator** and a **VS Code extension**.
- **`documentdb.io`** is a fully independent, community-driven site (own repo you can contribute to) with an **AI-built samples gallery and a `skills.md`** so samples can be "vibe coded."

## 📚 Detailed Notes

### Who they are: the product in one breath
Azure DocumentDB is positioned as an **open-source, fully MongoDB-compatible NoSQL document database** that is **Postgres-backed** — and that Postgres backing is where the open-source fundamentals come from. Because it's fully open source, it supports **multicloud**, which means two things: (1) running across multiple cloud providers, and (2) **hybrid cloud** — "one foot on-prem and one foot on Azure." On top of that foundation Microsoft built a **managed service**, so Azure DocumentDB gives you "all the managed bells and whistles, the knobs and levers" of the engine, but fully managed in Azure.

The overarching theme of the talk: they **started with a managed service, went back to build an open-source engine from it, and then funnelled all the open-source learnings back into the managed service.**

### The journey to open source (a ~1.5-year+ timeline)
- **Before January 2024:** the product already existed and went **GA** as a managed service (under a previous name, before it was called DocumentDB). Interestingly, **the name "DocumentDB" appeared in the open-source project *before* the team started calling themselves that** — "a whole different story," and the broader conversation started "a little over two years ago."
- **January 2024:** the team began seriously thinking about what open source would mean. The logic: *we're already built on an open-source database (Postgres), so why not open-source the product itself* and let the developer community see what's being built and participate.
- **Early advice (a key inflection):** being part of Microsoft, they leaned on internal teams with open-source pedigree. Because of their **Postgres background** and **Citus** (acquired **2019**, which had built a scale-out Postgres database), they got strong guidance on the right *mindset* — most importantly, to **clearly define what the project should look like vs what the product should look like**. This was a huge, ongoing learning.
- **Licensing:** long conversations about the right license. Landed on the **MIT license** for maximum simplicity and zero friction — three paragraphs, no restrictions on users or contributors, "build around it, on top of it, next to it." Multiple licenses can apply depending on project nature, but MIT was the call. "No regrets, clearly the right decision."
- **September (legal):** discussions about the **separation of project and product** — a project sitting independently of Microsoft but still run by Microsoft. Most lessons here were about **dos and don'ts**, not the technical nature of building open source.
- **End of December → January 2025:** "scrambled to the finish line" and made the big announcement — **DocumentDB went open source**. Very well received: lots of media/press, strong adoption, and the classic open-source signals (**GitHub stars, forks, clones**) all rose sharply.
- **A few months later:** real external interest — **up to 10 organizations publicly voiced support**, willing both to *use* the project and *build on top of it*.
- **Final step — the Linux Foundation:** to earn true credibility in the open-source community, they joined an open-source foundation (the **Linux Foundation**). This ties directly back to the product (more below).

### Project vs Product — two cohorts, one hard problem
The first big decision: if you build *around* an open-source project, what's the separation between **project** and **product**? They're completely different cohorts.

- **The open-source project** targets **developers in the open / on GitHub** who either have their own projects needing a database, or are building projects and need a platform. Within this, two buckets:
  - **Users (the largest cohort, as expected):** people who want to *consume* a database for their app, not build one of their own. "Anything and everything needs data… housed somewhere." They predominantly wanted a **NoSQL database**, and many were **Postgres enthusiasts**. Being fully permissive gave them a free, no-restrictions, compatible open-source project.
  - **Contributors (the much smaller cohort):** people looking to **build a database/managed service of their own** and wanting a *platform* to do it on — exactly what Microsoft itself did *on top of Postgres*. (By building DocumentDB on Postgres, Microsoft is itself a contributor in the Postgres space.) They initially assumed a **~1-in-50 split (≈98/2 users-to-contributors)**, but reality skewed even further toward users per contributor.
- **The product** targets **companies building a product of their own that needs a database** — and they want far more than contributions. They want **full management**: elasticity, storage/compute, high availability, disaster recovery, security guardrails — "a full-blown product, not just a database." This is the **revenue-driving** side.

Beyond Citus, the team drew on other in-house open-source experts and mentors: **open-source Postgres contributors on the team**, the **TypeScript** team (an in-house open-source project now among the most popular languages, alongside Python and Node), and **Visual Studio / VS Code** (one of the most popular developer platforms — exactly the cohort they want to serve).

### Measuring success differently: product metrics vs project metrics
A core insight: **the project and product need completely different success measures, yet must coexist.**
- **Product (business) metrics:** number of customers, number of clusters, core counts, storage under management, revenue, profit — the usual business KPIs.
- **Project (community-health) metrics** — all new to the team:
  - **Elephant factor** — how many organizations account for **at least 50%** of contributions. **Higher is better** (more diverse community). A low number means contributions are still concentrated in one org (fine, but low diversity).
  - **Bus factor** — "as ridiculous as it sounds": how many vital contributors could be "hit by a bus" before the project **stalls**. **Lower is better** — it means lots of people can pick up the slack if someone leaves. It measures **resilience to members leaving**.
  - **Heartbeat factor** — general project health: how many **commits, pull requests, and releases** (minor and major) — i.e., **momentum**. Growing over time signals a project the community genuinely cares about.

In short: the **product is about business metrics; the project is about community engagement/involvement metrics** — very different worlds.

### documentdb.io — a genuinely independent community entity
To prove the project and product are independent, the project has its own website, **`documentdb.io`**, which lives completely outside the managed product. It's **community-driven** — you can contribute to the **website's own repository** yourself. It already hosts things like a **samples gallery** (the samples are **AI-built**) and the project ships its own **`skills.md`** that you can use to build samples on top of DocumentDB — these can be **"vibe coded."** The point: make the developer's life very simple, while keeping the project a standalone entity.

### Why join the Linux Foundation? Trust and protection
People kept asking what the *angle* was in joining a foundation. The answer is **developer trust**:
- In the early days the **elephant factor** was low — contributions were still heavily driven by Microsoft. The team didn't want the community to fear that Microsoft could **"pull the rug"** — e.g., say "sorry, go use the Azure managed service, we're dropping the open-source project." That would strip independence and power from developers.
- Joining a foundation — especially one as **credible as the Linux Foundation** — protects against that. Tying back to the **bus factor**: even if *everyone left tomorrow* and nobody was watching the project, **the foundation ensures the project doesn't disappear.** Worst case it just sits there, but it won't go away; the community can keep using and building on it, and **all permissive components continue to exist.**

### Why Postgres? Extensibility in the AI era
When building something as fundamental as a database, "we don't have the luxury of time to go back and start from scratch." Postgres has been around a long time and **already solved a lot of problems**. Popularity cited (and called a likely *underestimate*):
- **1,000,000+ developers worldwide**, **100,000+ contributors** (several on the DocumentDB team), **~45,000+ commits in the last year**, **50K+ GitHub stars**, **300M+ downloads** — the **fastest-growing open-source database of the last decade.**

The key property they leverage is **extensibility**. Rather than always modifying the core engine, you add **extensions** on top of Postgres:
- **Citus** — a Postgres extension for **scale-out / replication / high availability**.
- **Graph** capabilities — available as an extension.
- **PG vector** — an extension enabling **vector search** for semantically meaningful results, which is exactly what AI/**RAG** workloads need ("AI in a database is all about RAG and vector search").

Because of this, when building a NoSQL database on Postgres they **did not have to reinvent indexing, query performance, throughput, or high availability** — those already existed as solutions/extensions. **What they focused on building was the query protocol** on top of Postgres that **funnels** operations into Postgres so they can leverage "all the goodness Postgres brings to the table."

### The managed service: three pillars — Cheaper, Better, Faster
For Azure DocumentDB (the managed service built around open-source DocumentDB), three primary pillars were targeted — and each improvement must **not cost the user more**:
1. **Cheaper** — the lowest entry point in the NoSQL / document-database / API-compatible space. **TCO** is "one of our biggest claims to fame."
2. **Better** — not just cheaper; quality must not be compromised. Better than prior versions of themselves *and* than competing products, giving developers (and, today, **agents**) the best compatible NoSQL experience on open-source foundations.
3. **Faster** — continually faster than prior selves and competitors; **lower latency and higher throughput.**

### Pillar 1 — Cheaper: decoupling storage from compute
The earliest design decision: **separate the *cost* of storage and compute** so they aren't dependent on each other. With many competitors, a bigger machine forces a bigger disk, or a capped disk size forces you to **add another machine just to get more storage** — a major pain point.

**Real customer example — 200 TB migration from a competing database:**
- Competitors cap disks at **~4,000 GB / 4 TB**. To hold 200 TB (plus headroom for compaction), you'd need **~100 compute nodes** — "insane," massively over-provisioned.
- DocumentDB offers **32 TB disks today**. Same 200 TB now needs only **~13 nodes**.
- Counterintuitive math: yes, you pay for 8× the storage, but you drop to **~1/8 the compute** — and because **storage increments are far cheaper than compute increments**, the net is a big saving (compute is far more expensive than storage).
- **Roadmap:** working toward **64 TB disks**, and "eventually" **256 TB disks** ("will take a while"), which shrinks node counts further — e.g., **~6 beefy machines** can do a lot; **6–13 nodes** is the realistic range vs ~100 over-provisioned.

**"Two knobs only" — costs competitors charge that DocumentDB absorbs (won't even appear on your invoice):**
- **Product support** — first-party managed service, so no separate support charge (unlike some products that bill Azure customers for support).
- **Managed-service license/subscription lock-in** — there's **no subscription-style license** for the managed service; **tear down your cluster and you pay nothing** (distinct from the open-source *project* license, which is about permissiveness). 
- **Backups** — **no backup charges**. On the 200 TB workload, zero backup cost/month is an enormous saving — the more you bring in, the more you save.
- **Networking / data egress** — typically your app runs in one V-Net and the database in another, and **egress from the DB's V-Net to the app's V-Net is billed**. DocumentDB, as a first-party Azure product, **does not charge for this — "at least 20% of an invoice" from a competitor wiped away.**
- **Metrics / observability** — **no charge for metrics.** "You shouldn't have to pay for observability for something you need to use," and the database sits at the bottom of the stack where telemetry/health/mitigation matter most.

**TCO customer stories:**
- **DB2 on-prem → Azure DocumentDB, 262 TB:** the **32 TB disks** were the biggest selling point. Compared against DB2's on-prem cost plus backups, data-transfer, data-center, and compute costs, they saved **~$9 million/year** — and that beat even competing NoSQL-compatible products. "An absolute no-brainer."
- **HBase → Azure DocumentDB:** compute and storage were reasonably close (DocumentDB a bit cheaper on storage), but the differentiators were a **licensing component** (DocumentDB has none) and **backups** (not even on the customer's HBase invoice — ignored in the comparison). Even so, the customer **cut their bill by more than half.** The most meaningful impact wasn't just cost — it was **fewer decisions**: only **machine size + disk size** to reason about, no licensing/backups/networking "rocket science." Predictable, and "that's the end of it."

### Pillar 2 — Faster: Azure SSD v2 (premium managed disks)
Being built in Azure lets DocumentDB leverage the Azure ecosystem — notably **Premium SSD v2 managed disks**, which became mainstream over the past year. The gains had to come at **no extra cost** (a 12× perf boost is worthless if it costs 12× more).
- The big SSD v2 advantage: **far more IOPS and bandwidth without provisioning ever-larger disks** — decoupling performance from disk size.
- **Before:** capped at **20,000 IOPS**, and you had to move to the **largest possible disk** to get there.
- **Now:** up to **80,000 IOPS** *without* the largest disk, with **the cost of those IOPS absorbed by DocumentDB** → effectively a **12× performance boost at no configuration change and no scale-up.**
- **Pricing impact:** previously **$2,880/mo up to $4,500/mo**; now you **start and stay at ~$280/mo** for the performance that previously required ~$4,500. Faster IOPS = faster reads/writes and lower query latency; since it's an internal optimization, the user isn't charged for it.

### Faster: the 1-million-writes-per-second milestone
A recent experiment with SSD v2 hit **1,000,000 writes/sec on a single node** — "a huge milestone."
- Setup: a **32-core machine** with only a **2 TB disk**. In the past you'd have needed a **32 TB disk to get just 20,000 IOPS**; here a 2 TB disk delivered **80,000 IOPS**.
- Quantified as **~200,000 transactions/dollar.** A comparable setup on a competitor reaches only ~80% of DocumentDB's throughput — but because DocumentDB is **also cheaper**, a 20–25% throughput edge becomes a **nearly 2× advantage in transactions/dollar.**
- Importantly, **there was still headroom** — they could exceed a million, but a million is where results were truly **sustained and consistent.**

### Pillar 3 — Better: multicloud & hybrid-cloud (enabled by the open-source foundation)
"Better" is unlocked precisely because DocumentDB runs on an **open-source foundation**: it can run **inside Azure, outside Azure, and as a managed service in Azure** — and crucially, **connect the Azure managed component to instances in other clouds or on-prem.** This enables **multicloud replication** and **hybrid-cloud sync** (detailed in the demos below), orchestrated with the **open-source Kubernetes operator** and a **VS Code extension** for DocumentDB, all with **global strong consistency and zero data loss.**

### Wrap-up & resources
The talk closes by reiterating the arc — *how Azure DocumentDB was built on open-source foundations and on top of an open-source project* — and points to two links: **`documentdb.io`** (the independent open-source project: events, updates, everything open-source DocumentDB) and the **Azure managed service** page (new features, performance improvements, TCO benefits, ongoing changes).

## 🛠️ Products / Features / Technologies Mentioned
- **Azure DocumentDB** — the fully managed Azure service: a MongoDB-compatible, Postgres-backed NoSQL document database with managed elasticity, HA/DR, security, and backups.
- **Open-source DocumentDB** — the independent open-source engine/project the managed service is built on; MIT-licensed, MongoDB-compatible, Postgres-backed.
- **PostgreSQL ("Postgres")** — the foundational engine; chosen for maturity and **extensibility** (1M+ devs, 100k+ contributors, 300M+ downloads).
- **Citus** — Postgres extension for **scale-out / replication / high availability**; Microsoft acquired Citus Data in 2019; the team a key mentor/inspiration.
- **PG vector** — Postgres extension enabling **vector search** for semantic/RAG (AI) workloads on the database.
- **MongoDB-compatible API** — the wire/query compatibility DocumentDB provides via its query-protocol/translation layer on top of Postgres.
- **Azure Premium SSD v2 (managed disks)** — the storage tech behind the **faster** pillar; decouples high IOPS/bandwidth from disk size.
- **Kubernetes operator (open-source)** — provisions/manages DocumentDB across clusters; used in both the multicloud and hybrid-cloud demos.
- **VS Code extension for DocumentDB** — dev tooling shown in demos; manages multiple cloud connections and a global connection string that follows failover.
- **`documentdb.io`** — the community-driven, independently hosted project website (own contributable repo) with an AI-built **samples gallery** and a **`skills.md`** for "vibe-coded" samples.
- **Prometheus & Grafana** — used in the multicloud demo to chart write throughput and visualize the failover.
- **MIT License** — the permissive (three-paragraph) license chosen for the open-source project.
- **Linux Foundation** — the open-source foundation DocumentDB joined for credibility and developer trust/protection.
- **TypeScript / VS Code / Visual Studio** — cited as in-house open-source successes and mentors/cohort references (not features of DocumentDB).
- **AKS / AWS / GCP Kubernetes** — the three clouds used in the multicloud replication demo (Azure primary).

## 🚀 Announcements / What's New
- **No formal GA/preview product launches were announced in this session** — it's a build-story/architecture talk. The closest "new" items, as described:
  - **1,000,000 writes/sec on a single node** — presented as a recent experimental milestone (32-core machine, 2 TB disk, 80,000 IOPS via SSD v2), ≈200,000 transactions/dollar, with headroom remaining.
  - **80,000 IOPS cap (up from 20,000)** and the associated **~12× performance / flat ~$280/mo pricing** via Premium SSD v2 — described as current capability at no extra cost.
  - **32 TB disks available today**, with **64 TB** in progress and **256 TB** on the longer-term roadmap.
  - **Multicloud replication** (Azure↔AWS↔GCP) and **hybrid-cloud sync** (on-prem/Kubernetes↔Azure) shown via demos — presented as working capabilities of the open-source-backed managed service (status/GA not explicitly stated).
  - Prior milestones recounted (historical, not new): managed-service **GA before Jan 2024**; **open-source release Jan 2025**; **Linux Foundation** membership.

## 💡 Demos
- **Demo 1 — Multicloud replication & managed failover (Azure · AWS · GCP).** Using the open-source engine + Kubernetes operator, DocumentDB is provisioned across **AKS, AWS, and GCP** clusters. Start state: **Azure hosts the primary** (3 instances) replicating to **GCP and AWS** (1 replica each) — globally strong consistency + local HA. The **VS Code extension** shows three per-cloud connections, while the app uses a **global connection string** that auto-repoints to the new primary on failover. Data inserted on AKS is shown replicating live to GCP and AWS; **global strong consistency** means a write only returns success once **acknowledged by the primary and at least one remote replica** — guaranteeing **zero data loss** if the primary dies. Using **Prometheus/Grafana**, writes appear on Azure (green), then **AWS is promoted to primary** via a **managed promotion** (Azure demoted, writes committed, AWS promoted) — the same flow a regional failover triggers. The Grafana chart shows only a **small blip** during failover with **no application-side intervention**. **Proves:** globally distributed DocumentDB across three clouds with quick, fully managed failover and zero data loss.
- **Demo 2 — Hybrid-cloud sync (on-prem/Kubernetes ↔ Azure).** Open-source DocumentDB runs **on-prem via the Kubernetes operator** (top-left connection in the VS Code extension) connected to **Azure DocumentDB** in the cloud; a **sync service** keeps the two in sync. Steps: (1) **insert** one document on-prem → after local persistence it **replicates to Azure** (verified by clicking the Azure connection); (2) **update** two fields on-prem → changes replicate to Azure; (3) **resilience test** — **stop the sync service**, insert **three** documents on-prem (persist locally with no errors), confirm Azure still shows only **1 document while on-prem has 4** (no replication while down); then **restart the sync service** — the **three additional documents appear in Azure**, sync **picking up exactly where it left off**. **Proves:** hybrid-cloud deployments keep running at steady state even when the replication pipe breaks, and re-sync cleanly on reconnect with no data loss.

## 📊 Notable Stats / Quotes
- **1,000,000 writes/sec** on a **single 32-core node** with a **2 TB disk** — "a huge, huge, huge milestone," with headroom to spare.
- **~200,000 transactions/dollar**, **≈2×** a competitor's transactions-per-dollar (competitor reaches ~80% of the throughput, and DocumentDB is also cheaper).
- **IOPS: 20,000 → 80,000** (≈12× performance) at **no extra cost** via SSD v2.
- **Pricing: from $2,880–$4,500/mo down to a flat ~$280/mo** for equivalent performance.
- **Disks: 4 TB (competitor cap) → 32 TB today → 64 TB (in progress) → 256 TB (roadmap).**
- **200 TB customer:** **~100 nodes → ~13 nodes** by decoupling storage/compute.
- **DB2 → DocumentDB (262 TB): ~$9M/year saved.**
- **HBase → DocumentDB:** bill **cut by more than half**; key win = **only two knobs** (machine size + disk size).
- **Networking/egress charges eliminated ≈ 20% of a competitor's invoice.**
- **Postgres popularity:** **1M+ developers**, **100k+ contributors**, **~45k+ commits/yr**, **50K+ GitHub stars**, **300M+ downloads** — fastest-growing OSS database of the last decade.
- **Assumed user:contributor split ≈ 98:2** ("at least one in every 50") — reality skewed even more toward users.
- **Open-source health metrics:** **elephant factor** (orgs supplying ≥50% of contributions — want high), **bus factor** (key contributors lost before stall — want low), **heartbeat factor** (commits/PRs/releases = momentum).
- *"The MIT license is three paragraphs… it'll take you about 10 seconds to finish reading… No regrets, clearly the right decision."*
- *"We didn't have to reinvent the wheel when it came to indexing… query performance… throughput and high availability"* — on building atop Postgres.
- Timeline markers: managed-service **GA before Jan 2024**, OSS thinking **Jan 2024**, **MIT** decision, **Sept** legal, **OSS launch Jan 2025**, then **Linux Foundation**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: spin up **open-source DocumentDB locally / on Kubernetes** via the operator; try the **`documentdb.io` samples gallery + `skills.md`** to "vibe code" a sample app; stand up a **vCore-style cluster in Azure DocumentDB** and test MongoDB-API compatibility against an existing Mongo workload; experiment with **PG vector** for a small RAG demo.
- [ ] Things to try: reproduce a scaled-down **hybrid sync** (on-prem K8s ↔ Azure) and a **multicloud replica** to feel the failover UX in the VS Code extension.
- [ ] Questions: What's the **GA/preview status** of multicloud + hybrid replication and the 64 TB/256 TB disks? Is **global strong consistency** the default or opt-in, and what's the latency cost of the "primary + 1 remote replica" ack? How does the **query protocol** handle Mongo aggregation-pipeline / index coverage edge cases? Pricing specifics of the **flat $280/mo** tier (which SKU/region)? How does this relate to **Cosmos DB for MongoDB (vCore)** branding/lineage?
- [ ] Relevant to: any team weighing **MongoDB-compatible NoSQL on Azure**, **multicloud/hybrid DR** strategies, **AI/RAG apps needing vector + document storage**, and **TCO/cost-optimization** migrations off DB2/HBase/other NoSQL.

## 🔗 Related
- [[PostgreSQL]] — the extensible open-source engine underneath DocumentDB.
- [[Citus]] — scale-out Postgres extension (acquired 2019) that mentored the project.
- [[PG vector]] — Postgres vector-search extension powering RAG/AI scenarios.
- [[MongoDB]] — the API/wire compatibility target for DocumentDB.
- [[Azure Cosmos DB for MongoDB (vCore)]] — the closely related managed Mongo-compatible Azure offering / lineage.
- [[Premium SSD v2]] — Azure managed-disk tech behind the IOPS/performance gains.
- [[Linux Foundation]] — the open-source foundation DocumentDB joined for governance/credibility.
- [[Vector search & RAG]] — the AI database pattern this engine targets.
- Source list: [[2026 Build Session List]]
