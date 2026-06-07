---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/csharp
  - topic/ai
  - topic/ai-sdk
  - topic/agents
  - topic/mcp
  - topic/rag
source: https://www.youtube.com/watch?v=LB64QnwhLZM
session_code: OD805
event: Microsoft Build 2026
speakers: Bruno (Developer Relations, GitHub/Microsoft)
duration_min: 44
aliases:
  - AI Building Blocks for NET Add intelligence to your C sharp apps
---

# OD805 — AI Building Blocks for .NET: Add intelligence to your C# apps

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Bruno — Developer Relations / Developer team, GitHub/Microsoft  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=LB64QnwhLZM)

## 🎯 TL;DR
.NET now has a complete, layered stack of **AI building blocks** — all shipped as plain C# libraries (no black boxes) — that let you add intelligence to apps incrementally. Bruno deconstructs a real **.NET Aspire–orchestrated support application** ("Sava") into **five layers**: (1) **Microsoft.Extensions.AI** — a provider-agnostic chat abstraction (`IChatClient`) that talks identically to cloud models (Azure AI Foundry) and local models (Ollama, Foundry Local); (2) **Embeddings + Vector Data + Data Ingestion** for RAG, with pluggable in-memory / SQLite / Chroma vector stores and a reader→chunker→enricher→writer ingestion pipeline; (3) **Tools via MCP** using the first-class C# MCP SDK; (4) **Agents** via the **Microsoft Agent Framework** (the `IAgent` wrapper over `IChatClient`, plus workflows and multi-agent orchestration); and (5) **Agent-to-Agent (A2A)** to connect heterogeneous agents (e.g. a Microsoft Agent Framework agent talking to an NVIDIA NeMo agent). The recurring themes: **same interface everywhere**, **integrated identity over API keys** (use `AzureCliCredential`/`DefaultAzureCredential` with Foundry — never keys), and **start local to learn, switch to cloud for power**. Everything maps to two canonical resources: the **AI apps for .NET developers** docs and the **Generative AI for Beginners – .NET** sample repo.

## 🔑 Key Takeaways
- **Microsoft.Extensions.AI is the foundation** — a provider-agnostic chat abstraction exposing `IChatClient`. The *same* interface connects to cloud (Foundry) or local providers; swapping models is a one-line deployment-name change.
- **The whole stack is just C# libraries.** No black boxes — chat, embeddings, vector data, ingestion, MCP, agents, image generation are all open, inspectable libraries any .NET dev can use.
- **Prefer integrated identity over API keys.** With Azure AI Foundry, use `AzureCliCredential` / `DefaultAzureCredential` (Entra ID) instead of endpoint+model+key. Bruno repeats: *"Don't use keys if you're using Foundry."*
- **Three lines start a chat:** create the Azure AI client → get an `IChatClient` → send the prompt. That's "the magic."
- **Local-first development is a first-class path.** Run the *identical* code against Ollama (`localhost:11434`) or **Foundry Local** with small models (Phi-4-mini, Qwen, Llama, NeoTron/Nemotron) — learn locally, scale to cloud later.
- **RAG decomposes into reusable building blocks:** Embeddings (text→vector of meaning), Vector Data (storage + similarity search), and Data Ingestion (read → chunk → enrich → write). Each is a swappable piece.
- **Embeddings encode *meaning*, enabling cross-language semantic query.** Tiny ONNX/MiniLM models (~50–80 MB) are great for local learning; cloud/multilingual models win for multi-language scenarios.
- **Vector search returns results *with a similarity score*** (e.g. 0–100). Score quality depends entirely on how well you build the ingestion + query pipeline; reranking and hybrid search are available.
- **MCP (Model Context Protocol) is the standard wire protocol for external tools.** .NET has a **first-class C# MCP SDK**; you can consume *any* public MCP and also **build your own MCP servers** to expose your resources/tools.
- **Function invocation must be enabled** on the chat client for it to call MCP/tools. Bruno demos the **Microsoft Learn MCP server** answering a "latest version" question the bare model couldn't.
- **Filter tools before passing them.** MCP clients can expose thousands of tools; passing them all burns context — select the ones you actually need.
- **An agent = LLM + system instructions + tools.** The **Microsoft Agent Framework** adds an `IAgent` interface that wraps `IChatClient`; the minimal agent needs only a name, description, and instructions.
- **Streaming token-by-token matters for UX.** The chat client supports both wait-for-full-response and streaming; streaming gives users the "it's working / real-time" feel.
- **Multi-agent orchestration & workflows are built in.** Compose agents (writer → editor) via sequential, round-robin, or concurrent patterns; a **workflow is itself an agent** and can be run with `RunStreamingAsync`. **Dev UI** visualizes agents/workflows, traces, and tool calls live.
- **A2A (Agent-to-Agent) connects heterogeneous agents** across URLs via a well-known agent card (`/.well-known/agent-card.json`). Originally from Google, now under the **Linux Foundation**. Azure AI Foundry can register custom A2A agents in its Tools panel.
- **Everything is observable.** The whole app is orchestrated with **.NET Aspire**; traces show generative-AI telemetry even across a non-.NET (NVIDIA NeMo) agent. Two links to remember: **Generative AI for Beginners – .NET** (samples) + **AI apps for .NET developers** (docs).

## 📚 Detailed Notes

### The end-to-end reference app: "Sava" support center (Aspire-orchestrated)
Bruno opens with the *finished* real application rather than slides: **Sava**, a content-showcase **support center app** where users analyze incidents. In the chat the user can **generate images**, **analyze specific payment errors / incidents**, get **data-analysis responses**, ask for a **deeper analysis**, and request the app to **explain why it gave a particular feedback** — tying the feedback of a payment incident to **external (grounded) information**.

Behind it, everything is coordinated with **.NET Aspire**. The Aspire graph runs **three services**:
- A **Web UI** — a **Blazor .NET** app.
- A **Microsoft Agent Framework agent** doing **image generation** and **data-grounded** work.
- A second agent which, in this scenario, is an **NVIDIA NeMo agent** (built on NVIDIA's **NeMo Agent Toolkit**) doing **data analysis**.

In Aspire **traces**, every interaction shows general details for the model calls, and — importantly — even the **NeMo agent surfaces generative-AI (GenAI) telemetry**. The point: it's all stitched together from **.NET AI building blocks**, and the rest of the talk "deconstructs the magic."

### The five layers (mental model)
Bruno splits the stack into **five layers** (group them differently if you like):
1. **Foundation — Microsoft.Extensions.AI** (chat abstraction).
2. **Data — Vector data, embeddings, data ingestion** (RAG).
3. **Tools — internal tools and **MCP**.**
4. **Agents — the Microsoft Agent Framework.**
5. **Agent-to-Agent (A2A)** — connecting two agents (and related: AG-UI, covered in other sessions).

Two canonical resources underpin everything:
- **Official docs:** *AI apps for .NET developers* — covers Microsoft.Extensions.AI, evaluation libraries, data ingestion, etc.
- **Samples:** *Generative AI for Beginners – .NET* — real, runnable code samples.

### Layer 1 — Microsoft.Extensions.AI (the chat foundation)
**Microsoft.Extensions.AI** is a **provider-agnostic chat abstraction**. Its key surface is the **`IChatClient`** interface. Because it's an abstraction, you can connect to:
- **Cloud** chat models (e.g. **Azure AI Foundry**, or other providers), and
- **Local** models (Ollama, Foundry Local) — *with the same interface.*

**Auth — integrated identity, not keys.** Depending on backend/library, instead of the standard `endpoint URL + model name + API key`, you can use **integrated security / integrated identity** and pass your **Entra ID** to authenticate. *"If you're using Foundry, this is the way to go."*

**The cloud chat sample (file-based app).** Libraries used: **Microsoft.Extensions.AI** + **Azure.AI** (Azure AI Foundry). The backend (Bruno's Foundry) hosts several models: **GPT-Image-2** (image generation), **GPT-5-mini**, a **Grok** model, and **text-embedding** models. The app uses **integrated security** (no API key); endpoint + model come from **user secrets** (default ≈ GPT-5-mini).

The "three lines that make the magic":
1. Create the **Azure AI client** (here with an **`AzureCliCredential`** — Bruno already ran `az login` so the console session is authenticated).
2. Get an **`IChatClient`** from it.
3. Send the prompt and read the response.

> Demo: asked *"What is your model name?"* → GPT-5 replied roughly *"I don't have a personal name; I'm an AI assistant based on OpenAI's GPT family."* (Models usually won't name themselves.) Bruno then changed the **deployment name** to **Kimi K2 (≈ "Kimi 2.6")** and re-ran → it answered *"I am Kimi, an AI assistant developed by Moonshot."* **Both ran in Azure** — illustrating how trivially you swap models.

**The local models path.** Same `IChatClient`, different provider. Bruno runs **Ollama** (also doable with **LM Studio** or **Foundry Local** — *"Foundry Local is very, very good"*). His Ollama instance has **Nemotron, Phi-4-mini, Qwen, Llama, and a Gemma model** installed. A small **"Llama Monitor"** taskbar app shows which models are **loaded** vs **waiting**.

> Demo: a new chat client pointed at **`localhost:11434`** using **Phi-4-mini**, asked to **analyze the sentiment** of several sentences and produce an **overall average sentiment** — *all running locally*. First run is slow (model not yet in memory; same as Foundry Local cold start); once loaded, it streams the full sentiment analysis. **Identical interface and procedure** whether local (Foundry Local/Ollama) or cloud (your provider/Foundry, with endpoint+model+key *or* endpoint+model+integrated security — the recommended path).

This is "LLM / GenAI 101": working with chat. Next step → **data**.

### Layer 2a — Embeddings (encoding meaning)
Models have constraints — they **don't have access to all your data** — so the usual next step is **RAG**. RAG breaks into named steps with their own building blocks: **reader, chunker, embeddings, vector store**.
- **Vector data** handles **storage + similarity search**.
- **Data ingestion** handles **read, chunk, enrich**.
- **Embeddings** **convert text into a vector that represents its *meaning***.

You can generate embeddings **locally** (Foundry Local) or in the **cloud** (e.g. OpenAI **text-embedding-3-small**; **Cohere** and others available in Foundry). For local experimentation, Bruno recommends an **ONNX model** — the **MiniLM** family is great; tiny models (~**50–80 MB**) run fast and produce embeddings. Because an embedding captures **meaning**, you can **query by meaning** — and even **query in another language** than the source; **multilingual** scenarios usually benefit from larger **cloud** models. The pattern: **learn locally, switch to cloud for more powerful models.**

Everything maps to lessons/docs: the *AI apps for .NET developers* homepage → Microsoft.Extensions.AI library → a **quick start** ("build an AI app using OpenAI or Azure OpenAI to chat with .NET") → the **embeddings concept** page → tutorials and more libraries.

### Layer 2b — Vector Data + a simple RAG demo (movies)
The **simple RAG** sample steps:
1. Use the libraries; read endpoints. Use a **cloud LLM** + a **cloud embedding deployment** (here **text-embedding-3-small** from OpenAI in Foundry). Auth via `az login` (CLI credential).
2. Create an **embedding generator**.
3. Create an **in-memory vector store** + a collection. (For demo, the collection is **deleted and recreated** each run.)
4. A small helper supplies ~5–10 fake **movies**; each becomes a **record** with **key**, **title**, **description**, and an **embedding** generated **from the description**.
5. Run **two queries**, each turned from a string into an **embedding**, then a **search** (out-of-the-box in the extensions). Search applies a **vector-to-vector cosine** algorithm to find the closest vectors, returning the match **plus a similarity score** (e.g. 98/100 = excellent; 40/100 = weak).

The record shape: **key** (string), **title** (string), **description** (string), **embedding** (vector). **Distance function = cosine similarity.** Starts in-memory but can **easily switch to Chroma DB** (or any vector database).

> Demo (`rag-simple`): builds the movie list, then:
> - *"Show me a family-friendly movie that includes ogres and dragons"* → **Shrek** (~**0.49 / ~50%**) and **The Lion King**. (*"We probably need to work better on the descriptions to get it closer."*)
> - *"Show me a movie about a hacker who discovered reality is a simulation"* → **The Matrix** (top), plus **Inception** (its description mentions simulations/reality → semantic relationship).
> Two results show per query because the code requests **top-2**.

Developer next steps once you grasp the building blocks: experiment — e.g. retrieve top-5 then **rerank**, or use **hybrid search** strategies. The libraries support all of it.

### Layer 2c — Data Ingestion pipeline (production-shaped RAG)
A more realistic ingestion sample (`data-ingestion-simple`):
1. Read chat model + embeddings config; create a **logger** and clients via **CLI credentials** — *"No keys. Don't use keys if you're using Foundry. Always default Azure credentials / CLI credentials."*
2. Build the steps (**read → chunk → enrich → write**) as a **pipeline**:
   - **Markdown reader** — reads `.md` documents.
   - **Semantic similarity chunker** — splits big documents into chunks so related content stays together (a **max token size** is defined).
   - **Summary enricher** — generates a short **AI summary per chunk** to improve retrieval quality.
   - **Vector store writer** — writes into a **SQLite vector store** (via a connection string; local store). Collection is `delete` + `ensure-exists` (only for demo; not needed every time in prod).
3. The pipeline ties together **reader, chunker, enricher, writer, and a logger factory**; it then **processes each document**.
4. **Search / Q&A:** user query → embedding → **search top-3**.

The arc: from the trivial "store strings that represent movies" to a much richer pipeline that ingests **markdown, PDF, or any content** through the standard steps — **reader, chunker, enrich, embeddings, vector store**.

> **Recap so far:** chat → embeddings → vector data → data ingestion. At this point you start to evolve *beyond* Microsoft.Extensions.AI toward **tools**.

### Layer 3 — Tools via MCP (Model Context Protocol)
**MCP** is a **standard wire protocol** (created by **Anthropic** a couple of years ago; *"everybody's on MCP right now"*). It's the modern way to connect **external tools** (and internal tools, since you can run MCP servers locally) to your apps. .NET has a **first-class C# SDK for MCP** that works with Microsoft.Extensions.AI and can connect to **any public MCP**.

Where to find servers: the **MCP registry on GitHub** lists tools — e.g. the very popular **Playwright MCP** (automation) and the **GitHub MCP**. Bruno demos the **Microsoft Learn MCP server** (`learn.microsoft.com/mcp`), which provides access to the **latest Microsoft Learn documentation**.

The demo asks the same question **twice** — *"What is the latest version of Microsoft Agent Framework for C#? Answer with the version number and the link to the official documentation."* — first **without** MCP, then **with** MCP.

Key code points:
- **System prompt:** *"You are a .NET documentation assistant."*
- Create the chat client with **endpoint + CLI credential + deployment name**, and crucially **enable function invocation** — this lets the chat client **invoke external tools** (here, the MCP). *(There are multiple ways to attach tools: at client creation, per-call, filtered — see the docs.)*
- **First call (no MCP):** ask the question, show the answer.
- **Second call (with MCP):**
  - Create an **HTTP client transport** (part of the MCP SDK) pointing at the server. The Microsoft Learn server needs **no auth**; servers like **GitHub** or **Hugging Face** require **OAuth/tokens** (separate Hugging Face sample exists).
  - Create an **MCP client** over that transport.
  - **List the tools** the server exposes.
  - Re-ask the question, attaching **`ChatOptions`** with the **collection of MCP tools**.

**Streaming aside:** the chat client supports **chat completion**, **responses**, etc., and on the client side you can **wait** for the full answer or **stream token-by-token** (better UX — the real-time "it's working" feel users expect from ChatGPT-style apps).

**Tool-filtering caution:** if an MCP exposes **thousands of tools**, passing them all **burns context** — filter to the tools you actually need first.

> Demo (`mcp` sample, GPT-5-mini): 
> - **Before (no MCP):** *"I don't have live access to internal documentation… I can't fetch the current latest NuGet version."* (streamed token-by-token).
> - **After (with MCP):** connects to the **Microsoft Learn MCP server**, exposing tools like **Microsoft Docs search** (and "patterns"); returns the **Microsoft Agent Framework .NET packages** (e.g. `Microsoft.Agents.AI`) and a link to the **Agent Framework overview** (which is noted as **tested and GA**). The exact version is buried in the page rather than crisply returned — *but the mechanism works*: the agent is given access to **information (data)** and **external tools (MCP)**.

> **Note:** You can also **author your own MCP servers** to expose your resources/tools — also covered in the docs.

### Layer 4 — Agents (Microsoft Agent Framework)
A quick definition: **an agent = an LLM (your choice) + a set of system instructions (defines behavior) + tools (memory, third-party services like the Learn MCP, etc.).** Agents scale from very simple to complex, and bring in adjacent topics: **workflows**, **connections to external agents (A2A)**, **durable functions / durable workflows**, and more.

**`IAgent` — the new interface.** On top of `IChatClient`, the **Microsoft Agent Framework** adds an **`IAgent`** interface. You create a chat client, then ask it to **create an agent**. The **minimal agent** needs only **name + description + instructions** — it's essentially a **wrapper over the chat client**, so it keeps the same patterns/capabilities (including streaming).

> Demo (`maf 01`, "hello world"): a **"writer"** agent (instructions: write engaging short stories) is asked to *"write a short story about a haunted house with a character named Lucia."* Runs with **integrated security** (or could run via **Foundry Local** with **Phi-4-mini** entirely local) and **streams** the story token-by-token via `RunStreamingAsync`.

**Agent + MCP tools** (`maf MCP01`): same MCP wiring as before, but now the **tools are attached to the agent at creation**. Re-asking the *"Agent Framework version for C#"* question (streamed): it connects to **doc search**, shows the **Microsoft search** tool, and this time **returns the version** plus learn/agent-config links — *"mostly because the system prompt in this one is better than the previous one."*

**Multi-agent orchestration** (`maf 01` + `maf 02`): one **chat client** provides LLM access to **two agents** — a **writer** and an **editor**. The Microsoft Agent Framework offers multiple composition styles:
- **Manual:** call an agent, process its output, feed it to the next, repeat.
- **Workflow patterns:** **sequential** (one→next), **round-robin**, **concurrent/all-at-once**, and more.

Key lines: **create a workflow**, then **add your agents/nodes**. Because a **workflow is itself an agent**, you run it with **`RunStreamingAsync`** (agent-1 → agent-2). 

**Dev UI:** a "super cool" tool to **visualize agents/workflows in real time** — test workflows and agents, and view **traces, tool calls**, etc. in a single, very nice UI.

Tie-back to Sava: that app likely uses an orchestrating agent that employs **A2A**, where one A2A endpoint is a **Microsoft Agent Framework agent** and the other is the **NVIDIA NeMo agent** — all working together from the same building blocks.

### Layer 5 — Agent-to-Agent (A2A)
**A2A** connects agents that live at **different URLs** (potentially different frameworks/vendors). The contract is the **agent card** — a **well-known** `/.well-known/agent-card.json` describing how the agent works; you can fetch it in real time to inspect an agent.

> Demo (`a2a` sample): a **writer agent** runs at a **local URL** (an **A2A server**), and a **client** consumes it via A2A. Bruno notes the Sava **NeMo** agent similarly exposes its **agent card** at its well-known URL.

**Provenance:** A2A was **initially created and open-sourced by Google** and is now part of the **Linux Foundation** — a clean way to connect agents from different versions/vendors.

**A2A in Azure AI Foundry:** In any Foundry project's **Tools** panel, under **custom** scenarios, you can **add an A2A agent** — provide a name and the input **URL** (the `/.well-known/agent-card.json`), and configure **authentication** for that agent. The same is doable via the .NET libraries.

### Image generation (bringing it all together)
The final demo (`maf image-generation`) plugs image generation into the agent model:
- Use a **text-to-image / image-generation** library targeting the **GPT-Image-2** model in the cloud (requires **endpoint + API key** here — another auth example) and create a client.
- Define a **task that generates the image** from a description — this becomes a **tool**.
- Create an **agent** (name + instructions) and **register the image-generation tool**.
- When the agent is asked to create an image, it routes to the tool and (if the model/plugin is available) **produces an image**.

This shows the same compositional pattern: an agent + a tool + a model, all from the building blocks.

### Closing — it's all just C# libraries
Wrap-up: the session covered **Microsoft.Extensions.AI, embeddings/vector data/ingestion, MCP tools, agents, A2A, and image generation** — and **all of it is C# libraries** you can read and use, **no black boxes**. There's much more: the **Microsoft Agent Framework doesn't stop at single agents** — it supports **AG-UI** (see other sessions), **durable workflows**, and many more building blocks. Go back to the docs to see what else is available.

**Two links to remember:**
- **Generative AI for Beginners – .NET** — the code samples.
- **AI apps for .NET developers** — the official documentation.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft.Extensions.AI** — provider-agnostic chat abstraction; core interface **`IChatClient`** (supports chat completion, responses, and streaming).
- **Microsoft Agent Framework** — adds the **`IAgent`** interface over `IChatClient`; agents, workflows, multi-agent orchestration; noted **GA / tested**. Packages e.g. **`Microsoft.Agents.AI`**.
- **C# MCP SDK** — first-class **Model Context Protocol** SDK (HTTP client transport, MCP client, tool listing, `ChatOptions` tool passing); consume any public MCP and author your own servers.
- **Azure AI Foundry** — cloud model host (GPT-Image-2, GPT-5-mini, Grok, text-embedding-3-small, Kimi K2, etc.); supports **integrated identity** and a **Tools** panel for **custom A2A** agents.
- **Foundry Local** — local model runtime (*"very, very good"*); local chat + embeddings.
- **Ollama** — local model provider at **`localhost:11434`**.
- **LM Studio** — alternative local model provider.
- **.NET Aspire** — orchestration + observability (service graph, traces with GenAI telemetry).
- **Blazor (.NET)** — web UI of the Sava app.
- **Dev UI** — visual tool to test/inspect agents & workflows (traces, tool calls) in real time.
- **Vector stores:** **in-memory**, **SQLite** vector store, **Chroma DB** (swappable).
- **A2A (Agent-to-Agent)** protocol — Google-origin, now **Linux Foundation**; agent card at `/.well-known/agent-card.json`.
- **NVIDIA NeMo Agent Toolkit** — used for the data-analysis agent in Sava (non-.NET agent surfacing GenAI traces).
- **MCP servers used/referenced:** **Microsoft Learn MCP** (`learn.microsoft.com/mcp`, no auth), **Playwright MCP** (automation), **GitHub MCP** (OAuth), **Hugging Face MCP** (tokens). Discover via the **MCP registry on GitHub**.
- **Models referenced:** **GPT-5-mini** (default demo model), **GPT-Image-2** (image gen), **Grok**, **OpenAI text-embedding-3-small**, **Cohere** embeddings, **Kimi K2 (Moonshot)**, **Phi-4-mini**, **Qwen**, **Llama**, **Gemma**, **Nemotron/NeoTron**, **ONNX / MiniLM** embedding models.
- **AG-UI** — mentioned as a related topic covered in other sessions.
- **Auth/SDK:** **`AzureCliCredential`** / **`DefaultAzureCredential`** (Entra ID integrated identity); **user secrets** for config.
- **Reference resources:** **Generative AI for Beginners – .NET** (samples) and **AI apps for .NET developers** (docs).

## 🚀 Announcements / What's New
This is an on-demand, content/education session rather than a launch session — **no headline product launches were explicitly announced.** The closest "what's new / current state" notes worth flagging:
- The **Microsoft Agent Framework** is presented as **GA / tested**, with an **`IAgent`** interface layered on `IChatClient`, plus built-in **workflow patterns** (sequential, round-robin, concurrent) and **multi-agent orchestration**.
- Emphasis that the **entire .NET AI stack ships as open C# libraries** (chat, embeddings, vector data, ingestion, MCP, agents, image generation) — *"no black boxes."*
- **A2A** is highlighted as now under the **Linux Foundation**, with **Azure AI Foundry** able to register **custom A2A agents** in its Tools panel.
- **Dev UI** is called out as the visual tool for testing agents/workflows with live traces and tool calls.

## 💡 Demos
1. **Sava support center app (the reference app)** — Aspire-orchestrated 3-service app (Blazor UI + Microsoft Agent Framework agent + NVIDIA NeMo agent). Showed in-chat **image generation**, **payment-incident analysis**, **deeper analysis**, and **grounded "why this feedback"** explanations; Aspire **traces** show GenAI telemetry even for the NeMo agent.
2. **Cloud chat (model-swap)** — file-based app via Microsoft.Extensions.AI + Azure AI, integrated security. Asked *"What is your model name?"*: **GPT-5** declined to self-name; switched deployment to **Kimi K2** which replied *"I am Kimi… developed by Moonshot."* — both in Azure.
3. **Local chat (sentiment)** — same `IChatClient` against **Ollama** (`localhost:11434`) with **Phi-4-mini**; analyzed sentence sentiments + overall average **fully locally** (cold-start load then streamed). Llama Monitor showed loaded/waiting models.
4. **Simple RAG (movies)** — in-memory vector store, OpenAI **text-embedding-3-small**, cosine similarity, top-2 results with scores. *"Ogres and dragons"* → **Shrek** (~50%) + **Lion King**; *"hacker discovers reality is a simulation"* → **The Matrix** + **Inception**.
5. **Data ingestion pipeline** — markdown reader → semantic-similarity chunker → AI summary enricher → **SQLite** vector store writer (with logging), then top-3 Q&A search.
6. **MCP (chat client) — Microsoft Learn** — same version question **before vs after** MCP. Before: *"no live access… can't fetch latest NuGet version."* After: connected to **Microsoft Learn MCP**, listed **Docs search** tool, returned **Agent Framework .NET packages** + overview link (noted GA).
7. **Agent hello-world** (`maf 01`) — a **writer** agent streams a haunted-house story featuring **Lucia**.
8. **Agent + MCP** (`maf MCP01`) — agent with MCP tools; fast connect to doc search; this time **returns the version** (better system prompt).
9. **Multi-agent workflow** (`maf 01`+`02`) — **writer → editor** via a workflow (sequential/round-robin/concurrent options); workflow run as an agent with `RunStreamingAsync`; **Dev UI** for live visualization.
10. **A2A** (`a2a` sample) — a **writer agent** as an **A2A server** at a local URL, consumed by an **A2A client**; inspected via the **agent card** (`/.well-known/agent-card.json`); mirrors Sava's NeMo agent card.
11. **Image generation** (`maf image-generation`) — **GPT-Image-2** wrapped as an agent **tool**; the agent calls the tool to generate an image.

## 📊 Notable Stats / Quotes
- *"These are the three lines that make the magic. Create the client and then get an `IChatClient`. That's it."*
- *"No keys. Don't use keys if you're using Foundry. Always go for default Azure credentials, CLI credentials, or whatever fits your scenario."*
- *"If you're using Foundry, this is the way to go."* (on integrated identity)
- *"This is how easy it is to change models."* (GPT-5 → Kimi K2 in one line)
- *"It's the same interface, the same procedure to work with local models… or cloud models."*
- *"MCP is a standard wire protocol created by Anthropic a couple of years ago. Everybody's on MCP right now."*
- *"If you have MCP clients with thousands of tools, that's going to use a lot of context — you maybe want to filter first."*
- *"An agent can be an LLM… that uses a set of system instructions to define how it behaves, and then uses tools… like memory or access to third-party services."*
- *"Streaming token by token gives the user the sense that 'oh, this is working' — I can see what's going on in real time."*
- *"A workflow is an agent"* — so you run it with `RunStreamingAsync`.
- *"It's all C# libraries… no black boxes there. It's all available for any .NET developer."*
- **Similarity scores:** 0–100 scale; *"98 is amazing"*, *"40 is maybe not a good one"*; Shrek demo scored ~0.49 (~50%).
- **Local embedding model sizes:** ~**50–80 MB** (ONNX/MiniLM).
- **Ollama port:** **11434**.
- **Models in the demo Foundry:** GPT-Image-2, GPT-5-mini, Grok, text-embedding-3-small, Kimi K2.
- **A2A origin:** created/open-sourced by **Google**, now under the **Linux Foundation**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone **Generative AI for Beginners – .NET** and run `rag-simple`, `data-ingestion-simple`, the `mcp` sample, and the `maf` agent/workflow samples.
  - Stand up **Foundry Local** (or Ollama) and run the *identical* chat code locally with **Phi-4-mini**; compare a tiny **ONNX/MiniLM** embedding model vs cloud **text-embedding-3-small**.
  - Wire the **Microsoft Learn MCP** into a chat client (enable **function invocation**) and test **tool filtering** when many tools are exposed.
  - Build a **writer → editor** multi-agent **workflow** and watch it in **Dev UI** (traces + tool calls).
  - Prototype an **A2A** server/client pair; inspect the **`/.well-known/agent-card.json`**; try registering a custom A2A agent in **Azure AI Foundry → Tools**.
  - Reproduce the Aspire **trace** view to confirm GenAI telemetry across services.
- [ ] Questions:
  - Exact current **GA version numbers** for `Microsoft.Agents.AI` / Microsoft.Extensions.AI packages (the demo didn't surface a clean number).
  - Best-practice **chunking + reranking + hybrid search** settings for production RAG on real PDFs/markdown.
  - Auth patterns for **GitHub / Hugging Face MCP** servers (OAuth/tokens) in .NET.
  - How **durable workflows / durable functions** integrate with Microsoft Agent Framework agents at scale.
  - What **AG-UI** adds and which companion session covers it.
- [ ] Relevant to:
  - Adding AI features (chat, RAG, agents) to existing **C#/.NET** and **Blazor** apps.
  - Internal **support/incident-analysis** tooling (mirrors the Sava scenario).
  - **Azure AI Foundry** adoption with **Entra ID** integrated identity (key-less).
  - Multi-vendor **agent interop** (Microsoft Agent Framework ↔ NVIDIA NeMo via A2A).
  - **.NET Aspire** observability for AI workloads.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[Microsoft.Extensions.AI]]
- [[Microsoft Agent Framework]]
- [[Model Context Protocol (MCP)]]
- [[Agent-to-Agent (A2A)]]
- [[Azure AI Foundry]]
- [[Foundry Local]]
- [[.NET Aspire]]
- [[RAG - Retrieval Augmented Generation]]
- Samples: *Generative AI for Beginners – .NET*
- Docs: *AI apps for .NET developers*
