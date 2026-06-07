---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/github-copilot
  - topic/cli
  - topic/cloud-sandboxes
  - topic/ai
source: https://www.youtube.com/watch?v=JJmmunwXcu8
session_code: DEM305
event: Microsoft Build 2026
speakers: Ali (Ellie), Denson (Dennis)
duration_min: 23
aliases:
  - GitHub Copilot Anywhere Remote CLIs to Cloud Sandboxes
---

# DEM305 — GitHub Copilot Anywhere: From Remote Control CLIs to Cloud Sandboxes

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ali ("Ellie") & Denson ("Dennis") — GitHub Copilot product/engineering presenters  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=JJmmunwXcu8)

## 🎯 TL;DR
GitHub Copilot is breaking free of the single desktop session. This session demos two complementary ways to use Copilot **anywhere**: **Remote Control sessions**, which let you take a *locally-running* Copilot session (CLI, the new Copilot desktop app, VS Code, or JetBrains) with you on the go — steering and monitoring it in real time from github.com or the GitHub mobile app via a link/QR code; and **Cloud Sandboxes** (now in **public preview**), which give every Copilot session its own *isolated cloud environment* so the host machine becomes optional — Copilot keeps running even if your laptop disconnects, shuts down, or "goes off the balcony." The talk closes with **Chronicle**, a feature that indexes all your Copilot sessions across every client so you can query your history for tips, stand-up reports, custom-instruction improvements, and cost/token reduction guidance. The unifying theme: developer choice over **how, where, and when** you work.

## 🔑 Key Takeaways
- **Remote Control** lets you take a local Copilot session on the go and steer/monitor it in real time from a phone or browser — your local machine stays the host.
- It works across **most Microsoft/GitHub Copilot clients**: the CLI, the new Copilot desktop app (launched the day before this talk), VS Code, and JetBrains.
- It works with **any project structure** — GitHub repos, Azure DevOps (ADO) repos, or even a CLI session with **no repository** at all.
- You activate it with **`remote on`** in the CLI; **`remote off`** stops it, **`remote show`** reports whether the active session is remotable. **Ctrl+E** surfaces a **QR code** alongside the link.
- Remote sessions appear on **github.com** and in the **GitHub mobile app**, but are **private to you by default** — the permission structure is unchanged; you can optionally share with others who have repo access.
- Tip: set **`remote sessions true`** in `settings.json` to make *all* local sessions remotable by default; use **`keep alive on`** so the session doesn't sleep while your machine must stay online.
- Enterprise/org licenses require an admin to enable the **remote control** policy and set it to **view and control**.
- **Cloud Sandboxes (public preview)** give each Copilot session its **own isolated cloud environment** — sandboxed at the tools, file system, and network level for safer, more confident coding.
- With a sandbox, the **host machine becomes optional**: Copilot runs in the cloud and keeps working even after the laptop disconnects or shuts down (vs. Remote, where closing the host kills the session).
- Launch a sandbox session with the **`--cloud`** flag (e.g. `copilot --cloud`); it provisions a sandbox in seconds and wraps it in a remote-control session.
- **Cloud agent policies** govern sandboxes — the *same* firewall rules, recommended allow-list, and custom allow-list used by Copilot Cloud Agent (under Settings → Copilot → Cloud Agent) apply when scoped to a repository.
- **Billing/persistence model:** while Copilot works, the sandbox runs; when it finishes, an **implicit snapshot** of process + disk is taken, the sandbox enters a **stopped** state, and **compute scales to zero** (no idle cost). A follow-up message **resumes** from the snapshot with the same files and processes.
- Cloud Sandboxes also enable **agent fan-out** — run many agents (e.g. ~30) on cloud resources instead of overloading your local machine.
- **Chronicle** indexes *all* your Copilot sessions across every client (CLI, desktop app, VS Code, JetBrains, github.com, Cloud Agent, code review) and lets you query that history via **`/chronicle`** for tips, search, stand-up reports, custom-instruction improvements, and cost tips.

## 📚 Detailed Notes

### Framing: Developer Choice — How, Where, and When You Work
The presenters open with a (self-deprecating) Copilot-generated title slide and a serious point: **the pace of innovation has never been faster**, expanding what's possible day-to-day. They argue your best ideas don't only arrive while sitting at the computer — they come at the airport, on the train, in the living room. The session is therefore about **developer choice**: not just *how* you work, but also *where* and *when*. Two capabilities deliver this — **Remote Control sessions** (Ali/Ellie) and **Cloud Sandboxes** (Denson/Dennis) — bookended by **Chronicle**.

### Remote Control Sessions — What They Are
Remote Control "lets you take your local work on the go." You take a Copilot session **running on your own machine** and continue to **monitor and steer it in real time** from another device. Key properties:
- **Clients supported:** demoed via the **CLI**, but the same applies to the **new Copilot app** (launched the day before), **Copilot in VS Code**, and **Copilot in JetBrains** — "most of the local clients" in the Microsoft/GitHub ecosystem.
- **Surfaces to control from:** **github.com** (web) and the **GitHub mobile app**.
- **Project-structure agnostic:** works with a **GitHub repo** (demoed), an **ADO repo**, or even a **CLI session with no repository**.
- **Same session everywhere:** the exact CLI session is mirrored to phone and web — "same exact experience."

### Remote Control — How to Use It (Commands & Flow)
The core workflow, all from the CLI:
- **`remote on`** — turns the active session into a remotable session; produces a **shareable link**.
- **Ctrl+E** — displays a **QR code** in addition to the link (scan it to open the session in the GitHub mobile app).
- **`remote off`** — stops a started remote session.
- **`remote show`** — reports whether your active session is currently remotable.

In the live flow, Ali turns remote on, scans the QR with a phone, opens the session in the **GitHub app**, and types an instruction ("add Mexico to the header") from the phone. The change is reflected **back in the CLI in real time**, demonstrating true bidirectional steering. **Permission requests** raised by Copilot surface on the mobile/internet-connected device for approval. Alternatively, without the mobile app, you simply open **github.com** and view/steer the same session there.

### Remote Control — Permissions & Privacy
By default, remote sessions are **viewable only to you** — they appear in your github.com and GitHub mobile app, but the **permission structure is unchanged**. If you *want* to share a session with someone who also has access to that repo, that's an option, but **nothing is shared by default**.

### Remote Control — Tips & Tricks
- **Make all sessions remotable by default:** edit `settings.json` and set **`remote sessions true`**, so every local session is steerable on the go without per-session opt-in.
- **Keep the host awake:** because Remote Control requires your **local machine to be online**, use **`keep alive on`** (in the CLI or whichever client — desktop app, VS Code, JetBrains) so the session doesn't go to sleep.
- **Enterprise/org policy:** if your Copilot license comes through an **enterprise or organization**, work with your **enterprise admin** to enable the relevant policy. The policy to turn on is **remote control**, set to **view and control**.
- **Known limitation (the bridge to Cloud):** Remote requires the host to stay online — which is exactly the constraint Cloud Sandboxes remove.

### The Motivating Question: "Can Copilot Have Its Own Machine?"
Denson reframes: Remote Control is powerful (he says he uses it "almost every day"), but the natural next question is **what if Copilot had its own isolated environment** — its own machine to work in, decoupled from your laptop? That question motivates **Cloud Sandboxing**.

### Cloud Sandboxes — What They Are (Public Preview)
Announced **now in public preview**. At the core: **every Copilot session that uses a cloud sandbox gets its own isolated environment in the cloud.** Three headline benefits:
1. **Confidence / true isolation:** the session is "truly sandboxed literally to the tools you want to give it" — scoped at the **tools**, **file system**, and **network** level. You can code with more confidence because Copilot operates in a contained ecosystem.
2. **Host-optional, work-from-anywhere (literally):** the Copilot instance runs in the cloud, so you can connect even if your laptop disconnects from the internet, shuts down, or "if I throw my laptop out the balcony — it will still work." (Contrast: with Remote, closing the host **kills** the session.)
3. **Scale beyond local resources:** for "ultra agent maxers" who want ~30 agents running simultaneously on heavy apps, sandboxes **allocate cloud resources** instead of overloading your local machine.

### Cloud Sandboxes — How to Launch (Demo Walkthrough)
Using the same World Cup demo app, Denson contrasts the two modes:
- He first shows that Ali's **Remote** CLI session is steerable from github.com — then **mocks a laptop shutdown** by closing the host session/tab. Result: on github.com the session is **no longer interactable** ("it's been shut down") — the defining limit of Remote.
- He then launches Copilot with the **`--cloud`** flag (`copilot --cloud`). The flow:
  1. **Provision a cloud sandbox** within the first few seconds of initiating.
  2. **Create a remote-control session** for that sandbox.
  - "The only thing that's actually changing here is **where does this session run**" — in this case, the cloud.
- The in-sandbox experience is **identical to local CLI**: plan mode, **autopilot**, "enable all" permissions, etc. He asks it to **create a PR for a live broadcasting experience** for the World Cup final.
- **Proof of host independence:** the session shows up in github.com tabs as a "create PR" session; he then **closes the cloud working tab and refreshes** — the Copilot session is **still working** because it's hosted in the cloud.

### Cloud Sandboxes — Policies & Governance
To prevent a cloud session from going "off the rails," **cloud agent policies** apply to sandboxes. Under **Settings → Copilot → Cloud Agent**, the **same policies** used by Copilot's Cloud Agent govern the sandbox used by the CLI:
- **Firewall rules**
- **Recommended allow-list**
- **Custom allow-list**

These apply to sandboxes created when you're **scoped to a specific repository**.

### Cloud Sandboxes — Persistence, Billing & the Snapshot Model
The "magic" of cloud sandboxing is its lifecycle and cost model:
- **While Copilot is active/working → the sandbox runs** (compute is on).
- **When Copilot finishes its job →** the system takes an **implicit snapshot** of the **process and disk** of the sandbox; the sandbox moves to a **stopped** state; **compute scales down to zero** (no active compute, no idle cost).
- **When you send a follow-up →** the system **resumes the Copilot instance from that snapshot**, restoring the **same sandbox, same files, and same processes** that were active before.

This means sessions are durable and resumable without paying for idle compute between turns.

### Remote vs. Cloud — Summary Comparison
| Aspect | Remote Control | Cloud Sandbox |
|---|---|---|
| Where it runs | Your local machine | Isolated cloud environment |
| Resources used | Local | Cloud |
| Host required? | **Yes** (must stay online) | **No** (host optional) |
| Best for | Local iteration on your active machine | Persistent cloud workspace; isolation; many agents |
| Steerable from | github.com, GitHub mobile app | github.com (remote-control session over the sandbox) |
| Survives laptop shutdown? | No | Yes |

### Chronicle — Turning Session History into Guidance
Denson hands back to Ali to close with **Chronicle**. Core idea: **every Copilot session you run builds a history you can query**, and from that history you can take **actionable steps** to improve how you work with Copilot.
- **Where it runs / what it indexes:** Chronicle runs in the **desktop app, CLI, VS Code, JetBrains, and github.com**, and it **indexes all of your sessions specific to you** across all of those surfaces — including **Copilot Cloud Agent** and **Copilot code review**.
- **How to access:** in any session, regardless of client, run **`/chronicle`** to see the available options.
- **Capabilities (the options shown):**
  - **Tips** based on your **usage patterns** (`chronicle tips`).
  - **Search across all of your sessions**.
  - **Stand-up report** (if your team does stand-ups).
  - **Custom-instruction improvements** — suggestions to update your custom instructions.
  - **Cost tips** — guidance on reducing **token usage and cost**.
- **Works with both modes:** Chronicle covers **all** your Copilot sessions whether they used a **cloud sandbox** or **`--remote`**.
- **Goal:** "turn your session history into a practical source of guidance" for working with Copilot.

### Closing Theme
The presenters return to the opening idea: it's never been a more dynamic time to be building, and these features are about improving not just **how** you work, but **where** and **when** you choose to work.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — across CLI, desktop app, VS Code, and JetBrains clients.
- **Copilot CLI** — primary demo client; commands `remote on/off/show`, `keep alive on`, `copilot --cloud`, `/chronicle`.
- **New Copilot desktop app** — "launched yesterday" (relative to the talk); recommended by both presenters.
- **Copilot in VS Code** and **Copilot in JetBrains** — supported clients for Remote, keep-alive, and Chronicle.
- **GitHub mobile app** — surface for steering/monitoring remote sessions and approving permission requests.
- **github.com** — web surface for viewing/steering remote and cloud-sandbox sessions.
- **Remote Control sessions** — take a local session on the go (link + Ctrl+E QR code).
- **Cloud Sandboxes** — isolated per-session cloud environments (public preview).
- **Cloud Agent policies** — firewall rules, recommended allow-list, custom allow-list (Settings → Copilot → Cloud Agent).
- **Copilot Cloud Agent** and **Copilot code review** — among the session sources Chronicle indexes.
- **Chronicle** — session-history indexing and guidance (tips, search, stand-up, custom-instruction improvements, cost tips).
- **Autopilot / plan mode** — Copilot CLI working modes shown in the cloud demo.
- **`settings.json`** — config file where `remote sessions true` enables remote-by-default.
- **Azure DevOps (ADO) repos** — supported alongside GitHub repos.

## 🚀 Announcements / What's New
- **Cloud Sandboxing for GitHub Copilot — now in public preview.** Each Copilot session gets its own isolated cloud environment (tools/file system/network scoped), with a host-optional, snapshot-and-resume, scale-to-zero billing model and cloud agent policy governance.
- **New Copilot desktop app** — referenced as having **launched the day before** the session ("we launched yesterday").
- **Remote Control sessions** and **Chronicle** are presented as available capabilities across the Copilot client family (CLI, desktop app, VS Code, JetBrains, github.com).

## 💡 Demos
- **Remote Control (Ali/Ellie):** A purpose-built **World Cup app** is improved via Copilot (UI theming PR). Spotting a missing host country (**Mexico** alongside USA & Canada) in the header, Ali runs **`remote on`**, hits **Ctrl+E** for a QR code, scans it live on stage into the **GitHub mobile app**, and instructs Copilot from the phone to add Mexico — the edit reflects **live in the CLI**. She also shows the identical session on **github.com**.
- **Cloud Sandbox (Denson/Dennis):** Demonstrates Remote's limitation by **closing the host tab** (session becomes non-interactable on github.com). Then launches **`copilot --cloud`**, which **provisions a sandbox in seconds** and creates a remote session; asks Copilot to build a **live, minute-by-minute broadcasting experience for the World Cup final** as a PR. **Closes the cloud tab and refreshes** to prove the session keeps running host-free. Previews the resulting PR and runs a **live simulation** (group stage → round of 32 → final) culminating in a **"live" final** broadcast.

## 📊 Notable Stats / Quotes
- **"If I throw my laptop out the balcony, it will still work. Copilot still gets to go."** — on cloud sandbox host-independence.
- **"The only thing that's actually changing here is where does this session run."** — Remote vs. Cloud distinction.
- **"~30 of our agents working at the same time"** — the "ultra agent maxer" scenario motivating cloud resource allocation.
- **Compute scales to zero** between turns via an **implicit snapshot** of process + disk — resumed on the next follow-up message.
- Audience poll: only a handful (~"four people") had previously tried Remote Control — i.e. a new/early-adoption feature.
- Demo flourish: simulated **Turkey winning the World Cup final 3–0** (goal "from Kenan Yıldız, 30th minute") to validate the new live broadcast feature ("This is live. This is real, not coded in.").

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run **`remote on`** + **Ctrl+E** on a CLI session and steer it from the GitHub mobile app.
  - Set **`remote sessions true`** in `settings.json` and test **`keep alive on`**.
  - Launch **`copilot --cloud`** and verify the host-optional behavior (close tab → refresh → still running).
  - Configure **Cloud Agent policies** (firewall + allow-lists) scoped to a repo and confirm they apply to sandboxes.
  - Run **`/chronicle`** → try `tips`, search, stand-up report, custom-instruction improvements, and **cost tips**.
- [ ] Questions:
  - What are the **exact pricing/compute units** for cloud sandboxes (snapshot storage vs. active compute)?
  - Which **enterprise policies** gate Cloud Sandboxes vs. just Remote Control's "view and control"?
  - Sandbox limits: max **concurrent agents**, region availability, and runtime/timeout ceilings?
  - How long are **snapshots retained**, and is there a separate storage cost?
- [ ] Relevant to:
  - Mobile/on-the-go developer workflows; long-running agent tasks; teams wanting isolation/governance for AI coding; cost-conscious agent fan-out.

## 🔗 Related
- 
