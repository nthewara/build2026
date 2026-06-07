---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/edge-ai
  - topic/iot
  - topic/robotics
  - topic/ai
source: https://www.youtube.com/watch?v=5RTUT3U96bc
session_code: OD837
event: Microsoft Build 2026
speakers: Cosmos Darwin (Product Manager, Microsoft Azure)
duration_min: 22
aliases:
  - Build and deploy AI at the edge for real-world impact
---

# OD837 — Build and deploy AI at the edge for real-world impact

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Cosmos Darwin — Product Manager, Microsoft Azure  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=5RTUT3U96bc)

## 🎯 TL;DR
"Physical AI" — combining language models and generative AI with robots and physical systems — is poised to extend AI's benefits to domains (inspections, construction, logistics, retail stocking, food prep) that information-worker AI has largely skipped. Cosmos Darwin and his team built a **basic agentic robot** that picks and places objects in response to messy, natural, fluid spoken instructions. The entire intelligence stack runs **locally** on a small industrial computer (Lenovo ThinkEdge SE100 with an NVIDIA RTX 2000 GPU) wired over USB to an RGB camera, an omnidirectional microphone, and a 6-DoF tabletop robot arm. The software stack uses Microsoft's **adaptive cloud** technologies: **Azure Linux** + **K3s**, **Foundry Local** (now packaged as a Linux container image, enabled by Azure Arc) hosting the models, **small form factor infrastructure** (cloud provisioning/management of edge devices, in preview), and **Azure IoT Operations** for telemetry back to the cloud. The models: **NeMoTron Speech** (NVIDIA speech-to-text), open-vocabulary vision detectors, and **Qwen-3 1.7B** for reasoning + tool calling (pick / place / pick-and-place / stop). The novel part is the agentic interpretation of messy inputs; the motion planning/execution is conventional robotics. All components are available off-the-shelf in preview today.

## 🔑 Key Takeaways
- **Physical AI is the next frontier:** AI's productivity gains have been unevenly distributed — concentrated on documents/spreadsheets/information workers — while physical-world work (inspection, repair, construction, warehousing, retail stocking, food prep) has barely changed in 1-2 decades.
- **Why robots struggled here:** Robots excel in controlled, repetitive environments (e.g., factories) but historically fail where interacting with people and a changing "open world" environment is core to the job.
- **Agentic robotics changes the equation:** Recent advances in AI models — especially the ability to run language models locally — enable a shift from rigid conventional robotics to an *agentic* approach that can reason about messy inputs and adapt to a changing environment.
- **Natural, fluid interaction:** The demo robot accepts rambly, conversational commands with no strict syntax and no start/stop ceremony — it reasons about intent even when the instruction is messy.
- **Continuous perception & adaptation:** Because it's continuously listening and looking, the robot adapts mid-task when objects are moved or instructions change midstream (e.g., "Wait, I changed my mind…").
- **Everything runs locally on the edge:** All intelligence runs on a single small industrial computer co-located with the robot, connected over plain USB — no cloud calls at runtime.
- **Approachable, off-the-shelf hardware:** Deliberately budget, off-the-shelf peripherals (a webcam-like UVC RGB camera, a UAC omnidirectional mic, a 6-DoF arm with gripper) — nothing fancy, no depth camera — so anyone can replicate it at home.
- **Foundry Local on Linux:** Foundry Local — previously on Windows then Windows+Android — is now packaged as a **container image for Linux**, hosting all AI models locally with an **OpenAI-compatible REST API** (a drop-in replacement for cloud inference calls).
- **Model trio behind the demo:** NeMoTron Speech (STT, free in the Foundry Local catalog, very low error rate), open-vocabulary vision detectors (returning object coordinates + axis of rotation), and **Qwen-3 1.7B** (reasoning + tool calling) — all free in the catalog and running on-device.
- **Tool calling is the brain:** The small language model simply chooses among four tools — **pick, place, pick-and-place, stop** — based on what it sees and hears; the rest (motion planning + arm execution) is conventional robotics.
- **Local inference = predictable low latency + GPU acceleration:** Foundry Local auto-detects hardware accelerators (the SE100's NVIDIA RTX 2000) and lights up the full top-to-bottom stack (driver → device plugin → user-mode libs) for you — sped up Qwen reasoning **by many times** without the app code touching the GPU.
- **Cloud control plane for edge fleets:** Small form factor infrastructure brings cloud provisioning/management (previously Azure Local on big servers) to small industrial devices — provision via ownership voucher, pick the OS from the portal (no keyboard/monitor), get an ARM resource, and grant access via Microsoft Entra ID instead of post-it passwords or shared SSH keys.
- **Azure IoT Operations for fleet telemetry:** Streams real-time operational data (e.g., requested pick/place coordinates) up to the cloud (Microsoft Fabric) with built-in connectors (OPC UA, HTTP, ONVIF), an industrial-grade MQTT broker, and in-flight data transformation — critical for diagnosing fleets across many locations.
- **All available in preview today:** Small form factor infrastructure, Foundry Local as a Linux container image (enabled by Azure Arc), and Azure IoT Operations are all available off-the-shelf to try right now.

## 📚 Detailed Notes

### Framing: The Opportunity & Challenge of Physical AI
The session reframes the usual AI narrative. When we talk about AI — including at Build — it's usually a chatbot on a computer screen. The speaker argues there is far more potential in bringing AI **out into the physical world**.

The benefits of AI advances have **not been evenly distributed**. The common examples are documents and spreadsheets — essentially *information workers* benefiting. Several categories of work have *not* seen the same change:
- **Inspections, maintenance, and repairs** out in the physical world.
- **Construction / job sites** — much building happens outside factories; look around any job site and you won't see many robots, just people.
- **Logistics, distribution, and warehousing** — looks much the same as a decade or two ago; productivity gains haven't materialized.
- **Brick-and-mortar retail and quick-serve restaurants** — stocking shelves, food prep — largely untouched by recent AI gains.

**The common theme:** in all of these, *interacting with other people* and *interacting with a changing, open-world environment* is a core part of the work. This is exactly what robots have historically struggled with. Robots excel in **controlled environments doing the same task repeatedly** (a factory is the canonical example), but struggle to make inroads where the environment is dynamic — so this work looks much as it has for decades.

**What's changing:** With recent advances in AI models — and the ability to **run them locally** — it's now possible to move from conventional *robotics* to a more *agentic* approach to robots that may handle these dynamic tasks better.

### The Demo: A Basic Agentic Robot
Expectations were set explicitly: *"it's not going to take anyone's job,"* but it demonstrates the potential of combining AI — especially language models — with physical systems.

In the demo, the presenter interacts with a small tabletop robot arm using natural speech:
- "Hey robot, can you pick up the red cube? … and put it in the bowl. Wait — I changed my mind, can you give it to me?" → robot hands it over.
- "Now, pick up the green brick. … Now, put it in this green bowl." → robot complies.

**Why the interaction is notable:**
- **No strict command syntax** and no need to start/stop the robot — the human interacts naturally and fluidly, simply saying what they want, even in rambly sentences ("please would you mind maybe picking up that thing there?").
- Because it's an **agentic robot**, it **reasons about what it heard** and figures out intent even when the input from the person is messy.
- It **responds as the environment changes** — continuously listening and looking — so when objects are moved or the instruction changes midstream, it adapts and keeps going.

The presenter extrapolates: imagine a different **embodiment** with more sophisticated hardware and a broader repertoire of skills acting as a **helpful collaborator** in spaces where people historically couldn't benefit from a robot collaborator due to the challenges above.

### How It Works — Hardware Setup
All the intelligence to make the robot work runs on **one small industrial computer**, physically on the table co-located with the robot (visible in the video background):
- **Compute:** **Lenovo ThinkEdge SE100** — chosen because it's industrial-grade with an **optional NVIDIA discrete GPU**. Many other devices would also work; this was just their choice.
- **Connection:** plain **USB**, nothing fancy, to three peripherals.
- **Peripheral 1 — Camera:** a **UVC-compliant RGB camera**, positioned over the workspace looking down at the table. (Not a depth camera — essentially a classic webcam.)
- **Peripheral 2 — Microphone:** a **UAC-compliant omnidirectional microphone** to capture speech.
- **Peripheral 3 — Robot arm:** a small tabletop arm with **6 degrees of freedom** (a 7th if you count the gripper attachment).

All peripherals are deliberately **approachable, off-the-shelf, budget options** — there's very little stopping you from trying this at home.

### How It Works — Software Stack
On the small industrial computer:
- **OS:** **Azure Linux**.
- **Model host:** **Foundry Local**, originally on Windows, then Windows + Android, and **now newly packaged as a container image you can run on Linux** — a great fit for this scenario. Foundry Local hosts all the AI models used.

### How It Works — Runtime Pipeline
At runtime, the system comes together as three pipelines feeding a reasoning model:

**1. Speech pipeline (audio → text)**
- Audio from the microphone is **split into utterances**, then fed into **NeMoTron Speech streaming**.
- **NeMoTron** is a **speech-to-text model developed by NVIDIA**, available **free in the Foundry Local catalog**, and one of the best models for performance and very low error rate.
- It reliably transcribed everything said even though the presenter was **facing away from the mic, not speaking clearly, with ambient noise**. Output: text of what the user said.

**2. Vision pipeline (frames → coordinates + rotation)**
- Frames from the overhead camera are **continuously captured** and fed into a variety of vision models, including an **open-vocabulary detector model**, to recognize everything on the surface.
- Recognizes color blocks and the bowls/containers, a human hand, and — though not shown in the demo — **everyday objects** like sunglasses or a wedding ring.
- For each detection it returns the **coordinates within the frame** of where the object was seen, and where applicable the **orientation / major axis of rotation** (critical for the arm to grasp the object correctly).

**3. Reasoning (the most important part)**
- The text (from speech) and coordinates (from vision) are fed into a **small language model running locally** on the industrial computer.
- For the demo they chose **Qwen-3** — free in the Foundry Local catalog and supporting **reasoning and tool calling**. They used the **1.7 billion parameter** version (a small language model); with more compute you could run a larger version and possibly handle more complex instructions.
- Given the inputs, the language model **chooses among a set of available tool calls**. The demo exposed **four tools**:
  - **pick** — pick up an item at a location.
  - **place** — put an item somewhere at another location.
  - **pick-and-place** — both as one movement.
  - **stop** — e.g., when the user says "Wait," the model interprets it as a **stop** tool call.
- In the running example, it's a **pick-and-place** call where the **pick target = the red cube** and the **place target = the hand (the presenter)**.

**4. Execution (conventional robotics)**
- Once interpreted, the chosen tool call is **converted into a sequence of movements** that are **planned out**, and the **robot arm executes** them.
- This part is **no different from the past** — it's conventional robotics. The novel value is the **flexibility / "humanness"** of interpreting very messy inputs, figuring out intent, and completing the task if it's within the available toolset.

### Adaptive Cloud Tech #1 — Small Form Factor Infrastructure
- The "industrial computer" used to run the whole demo.
- Microsoft Azure has offered cloud capabilities for years (e.g., **provisioning and managing machines from the cloud**) that were previously **limited to Azure Local on big servers**.
- **What's new:** those capabilities are now **available in preview for smaller industrial form factors**.
- **Demo flow in the Azure portal:**
  - Go to provision a machine; input the **ownership voucher** for the Lenovo SE100; the portal picks it up.
  - **Choose the software stack to install** straight from the cloud portal — **no keyboard or monitor needed**. (They chose Azure Linux.)
  - After provisioning, you get a **resource representation in Azure Resource Manager** — a **"provisioned machine" resource type** that looks and works much like a cloud VM, with visibility and management functions.
  - Example: **grant a colleague access** to the machine directly from the portal using **Microsoft Entra ID** — no password on a post-it, no emailed SSH key.
- **Why it matters:** essential when scaling to **hundreds or thousands** of devices distributed across many locations — managing everything through the **cloud control plane** is extremely helpful.

### Adaptive Cloud Tech #2 — Foundry Local (Linux container)
- Used the **Linux container image** flavor of Foundry Local.
- Stack on the device: **Azure Linux** + a **K3s** (small single-node Kubernetes) to keep things straight. Their application code (just **Python**, nothing fancy) is packaged as a **container**, and **Foundry Local is deployed alongside it as a container**.
- Foundry Local exposes an **OpenAI-compatible REST API** for inferencing requests — so you **don't host the AI models in your own code** (which is clunky and runs into size/agility issues).
- **Specific advantages highlighted:**
  - **Trusted, authoritative model access:** name the model (e.g., **Qwen-3 1.7B**) in a config file; Foundry Local retrieves a **trusted copy from the Foundry Local online catalog**, downloads it, and runs it **entirely locally** — **no calls to the cloud after that**.
  - The catalog has **many options**, including **NeMoTron Speech**.
  - **Drop-in cloud replacement:** access the running model via an endpoint just like in the cloud — except it's running **locally next to your code**, giving **super predictable latency** (vital for real-time physical-world interaction).
  - **Automatic hardware acceleration:** Foundry Local **detects available hardware accelerators** and lights them up. On the SE100 (which has an **NVIDIA RTX 2000**), the **whole top-to-bottom stack lines up** — **kernel-mode driver → device plugin → user-mode libraries inside the container** — so your **app code doesn't touch the GPU** yet still benefits from **GPU-accelerated inference**.
  - **Result:** sped up Qwen reasoning **by a factor of many times** (they tried both ways — a huge boost).
  - In the Azure portal you can **see GPU usage** — each time Qwen interprets instructions, there's a **small spike** in GPU usage (shown via a pre-release tool / screenshot that may change before release).

### Adaptive Cloud Tech #3 — Azure IoT Operations
- A **suite of platform services** to **connect to devices and protocols** in your local environment, route their **data up to the cloud**, and potentially **route commands back** (e.g., mission plans for a robot).
- Includes **built-in connectors** for **OPC UA, HTTP, ONVIF**, and an **industrial-grade MQTT broker**. As data flows into the broker, you **configure how it's transformed and sent to the cloud** — e.g., for analysis in **Microsoft Fabric**.
- **The monitoring problem in the demo:** the robot's **span/reach** is small (maybe ~half a meter), but the **camera's field of view is larger**. So the camera can see an object the robot is asked to grab, but the **arm physically can't reach it**. For a single tabletop robot this is easy to diagnose by eye — but **across many field locations**, real-time telemetry is everything.
- **Deployment:** On the **K3s** instance, IoT Operations was deployed using the **extension approach** — **both IoT Operations and Foundry are available as extensions** (a couple of clicks or a single YAML file).
- **Operations experience:** approachable enough for an **operations persona** (not just IT) who knows about millimeter offsets, etc. You **configure how data flows** from a discovered asset (here, the robot arm) up into a **cloud workspace**, and can **transform the data in flight** — e.g., unit conversions, adding/removing properties. In their case they **removed the Z coordinate** (irrelevant for reach checks), so data arrives in **Microsoft Fabric already cleaned and formatted** for the data team.
- **What they configured:** stream **all the coordinate requests** — every time the robot is asked to grab something at a location, it **streams back the requested coordinates** so they can **analyze whether each was safe or unsafe to reach**, all in **real time**.

### Closing Thesis
Advances in AI together with **Azure's adaptive cloud approach** are making it easier than ever to **build and operate intelligent physical systems**. This year and in the years ahead, we'll have to **update our notion of what tasks AI can be extended to** with an **agentic approach to robotics**. Everything shown is **available off-the-shelf to try now**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft adaptive cloud approach** — the umbrella strategy spanning the technologies below.
- **Foundry Local** — local model host; previously Windows, then Windows + Android, **now a Linux container image** (enabled by Azure Arc); OpenAI-compatible REST API; trusted model catalog; automatic hardware accelerator detection.
- **Azure Local** — referenced as where cloud provisioning/management capabilities previously lived (on big servers).
- **Small form factor infrastructure** — cloud provisioning/management for small industrial edge devices (preview); ownership voucher provisioning; "provisioned machine" ARM resource type.
- **Azure IoT Operations** — platform services suite; connectors (OPC UA, HTTP, ONVIF); industrial-grade MQTT broker; in-flight data transformation; deployed as a K3s extension.
- **Azure Arc** — enables Foundry Local as a Linux container image.
- **Azure Linux** — OS running on the edge device.
- **K3s** — small single-node Kubernetes on the device; hosts app + Foundry Local + IoT Operations as containers/extensions.
- **Microsoft Entra ID** — identity-based access grant to the edge device from the cloud portal.
- **Azure Resource Manager (ARM)** — provides the cloud resource representation of the provisioned edge machine.
- **Microsoft Fabric** — cloud destination for streamed/analyzed telemetry data.
- **Azure portal** — used for provisioning, access management, and viewing GPU usage.
- **Models:**
  - **NeMoTron Speech** (NVIDIA) — streaming speech-to-text; free in the Foundry Local catalog; very low error rate.
  - **Open-vocabulary vision detector model(s)** — object recognition returning coordinates + axis of rotation.
  - **Qwen-3 (1.7B)** — small language model; reasoning + tool calling; free in the Foundry Local catalog.
- **Hardware:**
  - **Lenovo ThinkEdge SE100** — industrial edge computer with optional NVIDIA discrete GPU.
  - **NVIDIA RTX 2000** (RTX 2000E shown on-device) — the GPU used.
  - **UVC-compliant RGB camera** (overhead, webcam-class, not depth).
  - **UAC-compliant omnidirectional microphone**.
  - **6-DoF tabletop robot arm** (+ gripper as 7th DoF).

## 🚀 Announcements / What's New
- **Small form factor infrastructure** — cloud provisioning and management capabilities (previously limited to **Azure Local on big servers**) are **now available in preview for smaller industrial form factors**.
- **Foundry Local as a Linux container image** — newly packaged to run on **Linux** (previously Windows, then Windows + Android), **enabled by Azure Arc**, **available as a preview**.
- **Azure IoT Operations** — highlighted as available for you to try (deployable as a K3s extension alongside Foundry).
- All three are positioned as **off-the-shelf, available in preview right now**.

## 💡 Demos
- **Agentic robot pick-and-place (live demo video):** A 6-DoF tabletop arm responds to natural, conversational speech — picks up a red cube, then mid-instruction the user says "Wait, I changed my mind, give it to me" and the robot hands it over; then picks up a green brick and places it in a green bowl. Demonstrates natural/fluid interaction, no strict syntax, continuous listening/looking, and mid-task adaptation.
- **Cloud provisioning of the edge device (Azure portal):** Inputting the **ownership voucher** for the Lenovo SE100, choosing **Azure Linux** as the software stack from the portal (no keyboard/monitor), and getting a **provisioned machine ARM resource**; then **granting a colleague access via Microsoft Entra ID**.
- **GPU usage visualization:** A screenshot/portal view of the **NVIDIA RTX 2000E** in the device showing **GPU usage spikes** each time Qwen interprets instructions (via a pre-release tool that may change before release).
- **Azure IoT Operations configuration:** Configuring data flow from the **discovered robot arm asset** up to a cloud workspace, **transforming data in flight** (e.g., removing the Z coordinate), and **streaming all requested pick/place coordinates** in real time to analyze safe vs. unsafe reach — landing cleaned data in **Microsoft Fabric**.

## 📊 Notable Stats / Quotes
- **6 degrees of freedom** on the robot arm (7th if counting the gripper).
- **Qwen-3 1.7 billion parameters** — the small language model used for reasoning + tool calling.
- **4 tools** exposed to the model: pick, place, pick-and-place, stop.
- **GPU acceleration sped up Qwen reasoning by "a factor of many times"** (a "huge boost" vs. CPU-only).
- **Robot reach ~half a meter**, smaller than the camera's field of view — the source of the "can see but can't reach" telemetry scenario.
- **No cloud calls at runtime** — after the model is downloaded from the Foundry Local catalog, everything runs locally inside the Foundry Local container.
- > *"It's not going to take anyone's job, but it does serve to sort of show the potential of combining AI, especially language models, with physical systems."*
- > *"Robots excel when you're in a controlled environment, you're doing the exact same task over and over… but all of those examples are domains where robots have struggled to make inroads."*
- > *"The benefits from those advancements have not been evenly distributed."*
- > *"We are going to have to update our notion of what types of tasks it is possible to extend AI to with an agentic approach to robotics."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Replicate the setup at home — off-the-shelf 6-DoF arm, UVC webcam, UAC omnidirectional mic, and a small edge box; the presenter explicitly says there's little stopping you.
  - Stand up **Foundry Local as a Linux container** on a K3s single-node cluster; pull **Qwen-3 1.7B** and **NeMoTron Speech** from the catalog and hit the OpenAI-compatible REST endpoint.
  - Test the **GPU auto-acceleration** path on an NVIDIA-equipped edge device (e.g., RTX 2000) and benchmark reasoning latency with vs. without GPU.
  - Try **small form factor infrastructure** preview: provision an edge device from the Azure portal via ownership voucher and manage access through Microsoft Entra ID.
  - Wire up **Azure IoT Operations** as a K3s extension to stream coordinate telemetry into Microsoft Fabric, with in-flight transforms (e.g., drop Z).
- [ ] Questions:
  - Which specific **open-vocabulary detector model(s)** were used for the vision pipeline (the talk doesn't name them)?
  - What's the end-to-end **latency budget** (speech → vision → reasoning → motion) for it to feel "real time"?
  - How does the agentic interpretation degrade with a **larger Qwen** vs. 1.7B on more complex, multi-step instructions?
  - What are the **safety/guardrail** patterns for tool calling when the model misinterprets a messy instruction near people?
  - Pricing/licensing and preview availability boundaries for **small form factor infrastructure** and **Foundry Local on Linux**.
- [ ] Relevant to:
  - Edge AI / physical AI / agentic robotics POCs.
  - Manufacturing, logistics/warehousing, retail stocking, food prep, field inspection/maintenance scenarios.
  - Anyone running **local LLM inference at the edge** with Foundry Local + Azure Arc.
  - Fleet management of distributed edge devices via Azure control plane + IoT Operations.

## 🔗 Related
- [[Foundry Local]]
- [[Azure IoT Operations]]
- [[Azure Arc]]
- [[Azure Local]]
- [[Adaptive Cloud]]
- [[Edge AI]]
- [[Agentic Robotics / Physical AI]]
- [[Microsoft Build 2026]]
