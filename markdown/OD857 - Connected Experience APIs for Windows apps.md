---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/windows
  - topic/apis
  - topic/app-development
  - topic/cross-device
source: https://www.youtube.com/watch?v=L9U0J3LJu6w
session_code: OD857
event: Microsoft Build 2026
speakers: Sri Tejaswi, Avinash
duration_min: 14
aliases:
  - Connected Experience APIs for Windows apps
---

# OD857 — Connected Experience APIs for Windows apps

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Sri Tejaswi (Product Manager, Windows Connected Experiences) · Avinash (Engineer, Windows Connected Experiences)  
> **Duration:** ~14 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=L9U0J3LJu6w)

## 🎯 TL;DR
Windows **Connected Experiences** is a platform that lets a third-party app stop being "just an app on Windows" and instead **become part of Windows** — surfacing inside first-party Windows surfaces (taskbar, widgets board, system search, the share sheet) to earn discovery, engagement, and net-new installs. The session goes deep on two of the three shipping APIs: **Resume** (cross-device continuity that hands an in-progress activity from a phone to the PC via a taskbar nudge, and can even drive an install if the app isn't on the PC yet) and the **People API** (donate contacts so they become first-class citizens in widgets, search, and share, with deep-link actions and relevance ranking). The headline pitch is **value compounding**: the more an app donates about a user's people and activities, the more Windows routes engagement, downloads, and trust back to that app — and it's all integrate-once. Resume offers two integration paths (Continuity SDK vs WNS push) with a clear decision matrix, and the whole model is privacy-scoped: contact data is readable only by Windows system surfaces, never app-to-app, and is removed on uninstall.

## 🔑 Key Takeaways
- **Connected Experiences = "your app becomes part of Windows."** You write the integration once and Windows gives you surfaces, ranking, engagement, and installs back. The three APIs are **Share, People, and Resume**.
- **The model is already proven at scale.** The story has gone from *announcing* three APIs at a prior Build to *shipping* them with real partners and real traction.
- **People API drives ~10M+ sessions/month from a single surface** — share-sheet "people suggestions" alone — i.e. 10M monthly app-engagement opportunities.
- **Resume is a top taskbar performer** just 3 months post-release: **nearly 1 in 4 users** who see a Resume taskbar nudge interact with it.
- **Combined reach: 50M+ devices/month** across Share + People + Resume, driving **over a billion sessions** back to partner apps in the last year.
- **Resume = cross-device continuity.** Start an activity on mobile (podcast, article, message), sit at the PC, and a taskbar badge (with a phone icon) lets you resume the exact state with one click.
- **Resume can install the app, not just resume it.** If the user *doesn't* have the app on their PC, the Resume badge still appears and one click drives the install — Windows owns the whole funnel: awareness → install → engagement, all in a single click.
- **You define what "resume" means** for your app (music, chat, or document continuity) and Windows routes it.
- **Resume has two integration paths: Continuity SDK (Android, LTW/CDH signaling) or WNS push notifications (any platform, cloud-driven).** A decision matrix picks the right one; sometimes you use both.
- **Resiliency is the core pattern for the SDK path** — stop publishing while disconnected, retry when the connection is restored.
- **People API makes app contacts first-class citizens** across the people widget, system search, and share — with the app writing **zero widget UI code**; the API handles the UI, ranking, and surfacing.
- **Enrich contacts with two layers: interactions (communication URIs → message/audio/video, mapped to app-manifest protocols) and relevance (privacy-free interaction signals that drive ranking).**
- **Privacy is by design:** contacts are scoped to **system surfaces only** (`other app read access = system only`), there is **no app-to-app sharing**, signals carry **no PII**, everything is **removed on uninstall**, and users can toggle visibility in Settings.
- **Resume is a Limited Access Feature** — you must request access through Microsoft (links provided in-session).

## 📚 Detailed Notes

### What "Connected Experiences" is — and the business case
Sri Tejaswi (PM on **Windows Connected Experiences**) frames the whole talk around one idea: Connected Experiences lets your app **become part of Windows** rather than merely run on it. The promise to developers is concrete — better **discovery**, more **engagement**, more **installs**, and **seamless continuity across devices**. The mechanism is that **first-party Windows surfaces** (taskbar, widgets board, system search, share sheet) will actively drive users back into partner applications.

The narrative arc: at a previous Build, Microsoft *announced* three Connected Experiences APIs; since then they've moved to *shipping* them with real partners and measurable traction. The three APIs are **Share, People, and Resume**. This session zooms into two of them in depth — **Resume** and **People** (specifically two new People surfaces) — treating Share as the already-established baseline.

### Proof points / why a developer should care (the scale numbers)
Before any code, Sri makes the ROI case with usage data:
- **People API** — from **just one surface** (share-sheet "people suggestions"), it drives **over 10 million sessions per month**. Framed as "10 million times app-engagement opportunities."
- **Resume** — only **3 months** into release and already **one of the top performers on the taskbar**: **nearly 1 in 4 users** who see a Resume taskbar nudge interact with it (an unusually high click-through for a taskbar surface).
- **Combined** — Share + People + Resume together **reach over 50 million devices in a month**, and in the **last year** these experiences have **driven over a billion sessions back to partner applications**.

The takeaway Sri draws: *the model works.* Windows surfaces reliably drive discovery, engagement, and installs back to the app — so integrating is a growth lever, not a checkbox.

### Windows Resume — what it does
**Resume gives your app continuity across devices and can drive net-new installs.** The user scenario: a person is doing something in your app on mobile — listening to a podcast, reading an article, writing a message — then sits down at their PC. **Windows Resume** lets them continue that exact activity on the PC.

**Demo 1 — media continuity (Spotify on a Pixel 8 → PC):**
- A user listens to music on Spotify during a morning commute on a Pixel 8.
- She sits at a PC where **Spotify is integrated with the Continuity SDK**.
- When the **device is in proximity** of the Windows PC, **Spotify publishes a "resume context."**
- Spotify appears on the taskbar **with a phone badge** — that badge shows up *because* Spotify published the resume context; **Windows received it and surfaced the nudge.**
- **One click** resumes the **same album at the same timestamp**, now playing on the PC.

**The install funnel (the part that's "really interesting for you as a developer"):**
- What if the user **doesn't have Spotify on their PC**? The **Resume badge still appears.**
- One click **drives the user to install the app** — "user's phone activity just drove a PC app to install."
- The user **neither browsed nor visited the Store**; **Windows handled the entire funnel** — awareness → install → engagement — **in a single click**, and is then ready to resume on subsequent uses.

**Demo 2 — chat continuity (WhatsApp):**
- A user is texting a friend on WhatsApp about shopping items and, mid-conversation, sends a bunch of links to look at.
- They sit at the PC; **WhatsApp publishes a resume context**, Windows receives it, the badge appears.
- The **same conversation is picked up exactly where they left off**, now in the desktop app.

**Generalisation:** Resume isn't just media. "**Music continuity, chat continuity, or document continuity** — *you* define what resume means for your app, and **Windows routes it.**"

### Resume integration — two paths (Avinash)
Engineer Avinash takes over the "under the hood." Resume supports **two integration paths**, and the right choice depends on your **platform, connectivity model, and engagement scenario**:
1. **Continuity SDK**
2. **Windows Push Notifications (WNS)**

#### Path 1 — Continuity SDK (end-to-end flow)
1. The app **publishes a resumable activity** through the **Continuity SDK on Android**.
2. Windows **receives it via LTW CDH signaling** (Link to Windows / Cross-Device Host signaling).
3. It **surfaces on the taskbar** as a **Resume entry point**.
4. When the user clicks Resume, **Windows activates the desktop app using an app-provided deep link**, restoring the experience exactly where the user left off.

**Five integration steps with the SDK:**
- **Step 1 — Add a dependency** to your Gradle file. The **Continuity SDK is now published to Maven and GitHub.**
- **Step 2 — Declare in your manifest** that the app is a **resume activity provider** (the value **`4` maps to "resume activity"**).
- **Step 3 — Initialize the SDK and register event handlers.** Two callbacks come back:
  - **`onContextRequestReceived`** — indicates the **connection is established**; the app can now send resume app context to **LTW (Link to Windows)**.
  - **`onSyncServiceDisconnected`** — your **signal to stop** (device disconnected or sync channel down).
  - Then call **`appContextManager.initialize`** — from here your app is wired into the continuity platform.
- **Step 4 — Create an `AppContext` object** representing a resume intent:
  - **`contextId`** uniquely identifies this activity instance.
  - **`type = resume activity`** — *the important line* — tells Windows the payload should **participate in cross-device resume experiences.**
  - Finally **`sendUpContext`** publishes the activity into the continuity platform.
- **Step 5 — Handle callbacks:**
  - **`onContextResponseSuccess`** — the resume activity was **accepted by LTW.**
  - **`onContextResponseError`** — something failed (connectivity dropped / sync service unavailable).
  - **Key pattern = resiliency:** apps should **stop publishing while disconnected and retry once the connection is restored.**

#### Path 2 — WNS (Windows Notification Service)
This path **does NOT require Link to Windows or the Continuity SDK.** Instead, your **app's cloud backend communicates directly with Windows via the WNS channel** using push notifications. It still **surfaces on the taskbar as a Resume entry point**, and a click **activates the desktop app**, restoring state.

**Trade-off:** No Link to Windows needed, and it **works for any platform (Android or iOS)** — *but* the **app must already be installed on Windows**: **there is no Store installation flow on this path.**

**Steps for the WNS path:**
- **Register your channel URI:** the PC requests a **WNS channel URI** and sends it to the server. The **channel URI becomes the address** for communicating with Windows from your app.
- **Build the resume request and send the WNS notification** (sample code shown), including some **mandatory headers** when sending the request.

#### The decision matrix
Pick the path that fits the scenario:
- **Deep mobile→PC integration *with* an installation flow → Continuity SDK.**
- **Broad reach, cloud-driven, app *already on* Windows → WNS.**
- Both paths yield the **same end result**: a **taskbar badge + a deep link + a "pick up where you left off" experience.** Sometimes you use **both**.

#### Access model
**Resume is a Limited Access Feature.** You must **request access through Microsoft** (the session shows the links to do so).

### People in Windows — making contacts first-class citizens
Back to Sri for the second concept: **People**. App contacts can become **first-class citizens across Windows**, with the potential to show up on **widgets** and even the **search box**. The example app is again **WhatsApp**, integrated with the **People API**, having **"donated" its users' contacts** to Windows.

**Demo 3 — the People widget (widgets board):**
- The **people widget** shows contacts that all came from WhatsApp (donated via the People API; Windows renders them).
- **Ordering is not random:** WhatsApp also **donated interaction signals**, which **help ranking** — *the app feeds the signals, Windows does the math.*
- **Clicking a contact opens WhatsApp directly to that conversation** — because WhatsApp **registered a communication URI** for that contact; when clicked, **Windows fires that URI** and launches the chat.
- Crucially, **WhatsApp wrote zero lines of widget UI code** — the **People API handled everything.**

**Demo 4 — system search:**
- A user searches for **someone** in Windows system search. If the app has donated contacts with the right signals, **Windows matches** and shows that contact as a **"people result" right alongside apps, files, and web results.**
- **WhatsApp attribution** is shown on the result, plus **action buttons: message, call, and video call.**
- "**Donate contacts once and it shows up here in search with actions ready to go.**"

### People API — how to build it (code walkthrough, Avinash)
Full integration "from zero to contacts showing up in widgets, search, and share":

1. **Create a user data account.** Third-party apps must create a user data account with **`com.microsoft.peoplecontract`** — this is the **opt-in to People**, a **one-time setup per app.**
2. **Store contacts.** Create a **contact list** and **set `otherAppReadAccess = systemOnly`** — *this last line is very important*: it means **only Windows system services (widget, search, share) can read these contacts; no other app on the device can see them.** User contact data stays controlled.
3. **Create a contact object.** The **`remoteId`** is the **app's unique identifier for that contact**; then **save** it. Windows now knows about the contact, making it **eligible as share suggestions, widgets, and search experiences.**
4. **Enrich the contact** (where it gets interesting — so far the app only donated a bare contact). Enrichment adds **capabilities, deep links, and interaction semantics** via **annotations** — annotations are how you tell Windows **what action your app supports** for a contact. Two layers:
   - **Layer 1 — Interactions (communication URI annotations):** declare the **operations your app supports** for a contact — **message, audio call, video call**. For **each operation, register a corresponding protocol in your app manifest.** Windows then surfaces interaction with contacts directly through the app's communication capabilities using those protocols.
   - **Layer 2 — Relevance (donating signals):** **signals** are **lightweight interaction events** with your app's contacts, **donated without any PII.** Windows uses signals to **rank and surface the most relevant contacts** across **widget, search, and share.**

### The core thesis — value compounding + privacy by design
Sri closes on the central mental model: the value of the Connected Experiences API **isn't one-time integration — it's value compounding.** The "real moat" for apps on the platform is that **the more your app donates about users' people and activities, the more engagement Windows drives back** — which in turn yields **more downloads** and **more user trust in your desktop app.**

And **throughout, user data stays in control:**
- Contacts are **scoped to system surfaces only.**
- **No app-to-app sharing.**
- **Everything is removed on uninstall** of the app.
- Users can **toggle contact visibility anytime in Settings.**
- All of this is **built into the platform by design.**

### How to get started (the call to action)
- **For People:** integrate with the **cross-device People API**, **donate your contacts**, **add communication URIs**, and **donate activity signals** so contacts **rank higher** across widget, search, and share.
- **For Resume:** integrate with **Continuity SDK or WNS (sometimes both)** to make your app's activity work across **Android *and* iOS** apps with Windows.
- **Start at `learn.microsoft.com`** — links are presented in-session for each area.
- Closing line: "**Connected Experiences is how your app not just be an app on Windows, but actually become a part of Windows. You write the integration once, and Windows gives you surfaces, ranking, engagement, and installs.**"

## 🛠️ Products / Features / Technologies Mentioned
- **Windows Connected Experiences** — the platform that lets third-party apps surface inside first-party Windows surfaces to gain discovery, engagement, and installs. Built on three APIs: Share, People, Resume.
- **Connected Experiences APIs (Share / People / Resume)** — the three shipping APIs; this session covers Resume and People in depth.
- **Windows Resume** — cross-device continuity feature: hand an in-progress mobile activity to the PC via a taskbar badge + deep link; can also drive an install. A **Limited Access Feature** (request access via Microsoft).
- **People API (cross-device People API)** — donate app contacts so they become first-class citizens in the people widget, system search, and share, with ranking and deep-link actions.
- **Continuity SDK** — Android SDK for the Resume "deep integration" path; publishes resumable activities; **now published to Maven and GitHub.**
- **WNS (Windows Notification Service / Windows Push Notifications)** — the cloud-driven Resume path; app backend pushes resume requests to Windows via a WNS channel URI; works on any platform but requires the app already installed on Windows.
- **Link to Windows (LTW) / Cross-Device Host (CDH) signaling** — the transport by which Windows receives Continuity-SDK-published activities ("LTW CDH signaling").
- **Taskbar (Resume entry point / phone badge)** — the surface where Resume nudges appear.
- **Widgets board / People widget** — surfaces donated contacts (zero widget UI code from the app).
- **Windows system search** — surfaces donated contacts as "people results" alongside apps, files, and web, with message/call/video actions.
- **Share sheet (people suggestions)** — the People surface already driving 10M+ sessions/month.
- **`com.microsoft.peoplecontract`** — the user-data-account contract an app creates to opt into People (one-time per app).
- **Communication URIs** — registered per-contact to deep-link actions (message/audio/video) into the app via manifest-declared protocols.
- **Spotify** — partner used in the media-continuity Resume demo (Pixel 8 → PC).
- **WhatsApp** — partner used in the chat-continuity Resume demo and in both People demos (widget + search).
- **Google Pixel 8** — the Android phone used in the Spotify Resume demo.
- **learn.microsoft.com** — where the documentation/getting-started links live for each area.
- **Gradle / Maven / GitHub** — build/distribution surfaces for the Continuity SDK dependency.

## 🚀 Announcements / What's New
- **Continuity SDK is now published to Maven and GitHub** — developers can add it as a Gradle dependency (a "now available" distribution milestone called out explicitly).
- **Two new People surfaces** beyond the existing share-sheet suggestions: contacts can now appear in the **people widget (widgets board)** and in **Windows system search** as first-class people results with message/call/video actions.
- **Progression from "announced" to "shipping with real partners"** — the three Connected Experiences APIs (Share/People/Resume) have moved from a prior Build's *announcement* to shipping at scale (50M+ devices/month).
- **Resume remains a Limited Access Feature** requiring access requests through Microsoft (status/access model reiterated, not newly GA'd).
- No explicit GA-vs-preview labels were stated for the individual surfaces in this talk beyond the Continuity SDK distribution and the live partner traction; the session frames the platform as in-market and scaling rather than newly previewed.

## 💡 Demos
- **Demo 1 — Spotify media continuity + install funnel (Pixel 8 → PC).** Music playing on a Pixel 8; sitting at a PC in proximity, Spotify publishes a resume context; a taskbar badge with a phone icon appears; one click resumes the same album at the same timestamp on the PC. Variant shown: if Spotify isn't on the PC, the badge still appears and one click installs the app — **proving Windows owns the full awareness→install→engagement funnel in one click.**
- **Demo 2 — WhatsApp chat continuity.** A mobile WhatsApp conversation (shopping links sent mid-chat) is resumed on the PC desktop app exactly where it left off via the taskbar badge — **proving Resume generalises beyond media to chat continuity.**
- **Demo 3 — People widget.** WhatsApp-donated contacts render in the widgets board people widget, ordered by donated interaction signals; clicking a contact opens that exact WhatsApp conversation via a registered communication URI — **proving the People API delivers ranking + deep-link actions with zero widget UI code from the app.**
- **Demo 4 — People in system search.** Searching a person in Windows search returns the donated contact as a people result alongside apps/files/web, with WhatsApp attribution and message/call/video action buttons — **proving "donate once, surface everywhere with actions ready."**

## 📊 Notable Stats / Quotes
- **10M+ sessions/month** driven by the People API from a single surface (share-sheet people suggestions) — "10 million times app-engagement opportunities."
- **~1 in 4 (nearly 25%)** of users who see a Resume taskbar nudge interact with it — and Resume is **a top taskbar performer just 3 months post-release.**
- **50M+ devices/month** reached by Share + People + Resume combined.
- **Over a billion sessions** driven back to partner applications in the last year by these experiences.
- **"Windows handled the entire funnel — from awareness to install to engagement — all within a single click."**
- **"You define what resume means for your app, and Windows routes it."** (music / chat / document continuity)
- **"WhatsApp didn't write a single line of widget UI code here. The People API handled everything."**
- **"The key idea of Connected Experiences API isn't just one-time integration. It's value compounding."**
- **"Connected Experiences is how your app not just be an app on Windows, but actually become a part of Windows."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Pull the **Continuity SDK** from Maven/GitHub and stand up the **5-step Resume flow** on an Android test app (Gradle dep → manifest provider value `4` → init + handlers → `AppContext` with `type=resume activity` → `sendUpContext` + success/error callbacks). Verify the taskbar badge + deep-link resume.
  - Prototype the **WNS Resume path** end-to-end (register WNS channel URI → build resume request with mandatory headers → push to Windows) for an iOS or cloud-driven app where the desktop app is already installed.
  - Implement the **People API** integration: create a `com.microsoft.peoplecontract` user data account, store contacts with `otherAppReadAccess = systemOnly`, set `remoteId`, then enrich with **communication URI annotations** (message/audio/video + manifest protocols) and **PII-free signals**, and confirm contacts appear in widget + search + share with working actions.
  - Validate the **install funnel**: confirm a Resume badge appears (and triggers a Store/app install) when the desktop app is *not* present — Continuity SDK path only.
  - Test the **resiliency pattern** (stop publishing on `onSyncServiceDisconnected`, retry on reconnect) against flaky connectivity.
- [ ] Questions:
  - What exactly are the **mandatory WNS headers** for a resume request, and what's the payload schema for the deep link?
  - What's the **Limited Access Feature approval** turnaround and eligibility bar for Resume? Any cost/partner-tier gating?
  - Does the **manifest provider value `4`** have other documented values (i.e. what activity types beyond "resume activity" exist)?
  - How are **interaction signals weighted** for ranking — recency vs frequency? Any rate limits on signal donation?
  - For WNS path on iOS, how does Windows associate the pushed resume with the correct installed desktop app identity?
  - What's the user-facing **Settings toggle** path for contact visibility, and does revoking remove already-surfaced data immediately?
- [ ] Relevant to:
  - Any first-party/partner **Windows desktop app** wanting cross-device continuity or store install lift (media, messaging, docs).
  - **Phone Link / Link to Windows** integration work and cross-device strategy.
  - **Growth/engagement** initiatives looking for zero-/low-UI surfaces (taskbar, widgets, search) to drive installs and DAU.
  - Privacy/compliance review of contact donation (system-only scope, no PII signals, uninstall cleanup).

## 🔗 Related
- [[BRK261 - Build and ship faster with a developer-optimized experience on Windows]] — broader Windows developer platform / experience story this Connected Experiences work sits within.
- [[DEM345 - From prompt to app build AI powered apps on Windows]] — companion Windows app-building session; complementary surface for app developers targeting Windows.
- [[DEM346 - WSL improvements and the new Containers CLI and APIs]] — sibling Windows-platform developer session from the same event track.
- [[ODSP916 - Design systems for every user including people and LLMs]] — design-system context relevant to surfacing contacts/people consistently across Windows surfaces.
- Source list: [[2026 Build Session List]]