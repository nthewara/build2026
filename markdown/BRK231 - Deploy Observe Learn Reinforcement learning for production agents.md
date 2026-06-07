---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/reinforcement-learning
  - topic/agents
  - topic/ai-foundry
  - topic/fine-tuning
  - topic/ai
source: https://www.youtube.com/watch?v=uyxSyo7PJ7k
session_code: BRK231
event: Microsoft Build 2026
speakers: Alicia Frame (Product Lead, Model Customization, Microsoft Foundry), Omkar Mule (Engineering, Microsoft Foundry)
duration_min: 48
aliases:
  - Deploy. Observe. Learn. Reinforcement learning for production agents
---

# BRK231 — Deploy. Observe. Learn. Reinforcement learning for production agents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Alicia Frame (Product Lead, Model Customization, Microsoft Foundry) · Omkar Mule (Engineering counterpart, Microsoft Foundry)  
> **Duration:** ~48 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=uyxSyo7PJ7k)

## 🎯 TL;DR
A hands-on tour of **fine-tuning and reinforcement learning for production agents** in **Microsoft Foundry**, framed around the *deploy → observe → learn* loop: you ship an agent, capture its production traces, and use those traces to build models that are **cheaper, faster, and smarter**. Agents consume 20–30× more tokens per turn than old chat, so swapping frontier models for **fine-tuned small models (10–30× cheaper)** keeps quality up while the budget balances. The talk walks a single retail customer-service / refunds scenario up a "hill-climbing" leaderboard through four escalating techniques — **distillation (SFT)** → **reinforcement fine-tuning (RFT)** → a new **low-level interactive training API ("PyTorch as a service")** → a **natural-language fine-tuning skill** for coding agents. Each step is demoed live in the Foundry UI and SDK, lifting a quality score from a frontier-class ~74% baseline up past **84%**, ultimately beating an o4-mini fine-tune with a fine-tuned **Qwen 3 32B** OSS model. The closing message dispels two myths: frontier models keep getting *bigger/slower/more expensive* (so fine-tuning still wins on quality+latency+cost and keeps your IP in *your* weights), and fine-tuning is cheap — the **median SFT job costs ~$1**, with **developer-tier training at 50% off** and **developer-tier hosting with no hosting fee**.

## 🔑 Key Takeaways
- **Fine-tuning is the answer to agent economics.** Agents burn 20–30× more tokens per turn than chat; a third of enterprise apps plan to embed agentic AI within 2 years (speaker thinks higher/sooner), and ~half of teams already run a production agent. Fine-tuning lets you swap a frontier model for one **10–30× cheaper** so even at 30× the tokens, the budget still balances.
- **Fine-tuning now means three things, not just "teach my domain":** make models **cheaper**, **faster** (small models stream tokens quicker), and **smarter** (bake prompt instructions into the weights — *call the right tool at the right time with the right inputs*).
- **The deploy→observe→learn loop is the product story.** Foundry-hosted agents auto-capture full **traces/trajectories** (which tools were called, in what order, with what outcome); those traces become the raw material for evals **and** training.
- **Evals come first and are reused everywhere.** The same graders you write to evaluate the baseline are reused to score fine-tuned models *and* as the RL reward signal. "If you can't grade it, you can't learn from it."
- **Distillation (the first technique):** capture a large "teacher" model's traffic (e.g. GPT-5.4), filter/dedupe/redact-PII into a training set, and **supervised fine-tune (SFT)** a small "student" (4.1 mini/nano). Easy, but you can **never get smarter than the teacher**.
- **Reinforcement fine-tuning / RFT (the second technique):** the model learns from its *own* mistakes. It generates multiple samples (**rollouts**), a grader scores them, and the trainer reinforces the best — letting the model **exceed the teacher**. Requires a **verifiable/gradable task** (refunds qualify).
- **Reward hacking is the central RFT failure mode.** A penalized model can learn the degenerate policy "never call a tool." Mitigate with tool-coverage in the grader (penalize answers that skip required tools) and by watching telemetry (tool-calls-per-rollout dips, **KL divergence**).
- **RFT trains *with* live tools, not transcripts.** Unlike SFT (which copies spelled-out trajectories), RFT only gets the user message + ground truth; the **training run itself invokes real tools** (hosted on an Azure Function App / MCP server) — your "RL harness/environment" — and grades the actual results.
- **Watch the right RFT metrics:** train **and** validation **reward** trending up, **reasoning-token mean per step** (often falls over training → cheaper final model), and **tool-calls-per-rollout** (a dip = something's wrong, iterate the grader).
- **New: low-level interactive training API ("PyTorch as a service").** Exposes training primitives — **sample / forward pass / backward pass / optimizer step / sync** — so you control the algorithm, recipe, grader (even a **C# grader**), tools, and full hyper-parameters, while Foundry manages the **GPU compute** (no vLLM/NCCL cluster pain).
- **The low-level API supports advanced RL workflows:** custom rollout environments, real-world tool/environment interaction, **GRPO** by default (compute advantages from sample means) but swappable to **PPO/DPO**, **curriculum learning** (easy→hard tasks), and **mid-run interactive changes** (e.g. switch sampling strategy on the fly).
- **It runs locally but stays inside Foundry.** The recipe launches via a script as a **tmux** session on your own CPU machine (laptop or Azure VM); a shipped **local dashboard** shows fine-grained telemetry (reward, accuracy, **entropy**, **grad norm**, **KL divergence**, group composition). Runs/models still register in Foundry for hosted agents + evals.
- **Natural-language fine-tuning skill (the fourth technique).** A **fine-tuning skill** for coding agents (part of **GitHub Copilot for Azure**, or a standalone download) lets you describe goals in plain English — "make a grader, give partial credit, run a distillation autopilot, make it cheaper+faster" — and it picks models, algorithms, and hyper-parameters, runs experiments, reads the logs, and iterates if results regress.
- **Guardrails preserve base capabilities.** Including default graders (intent resolution, task completion) during fine-tuning confirms you didn't erode the base model — fixing the classic fear "I made it better at X but worse at everything else."
- **Real production proof, not demoware:** **Decagon AI** (CX-agent-as-a-service) distilled to smaller/cheaper models; **Discovery Bank** cut latency from **6s → 1.5s** in its banking app; **DocuSign** (a top token customer) saw a **50% cost reduction** in AI document processing.
- **Cost objections answered:** **developer tier training** = spot/low-priority VMs at **50% off**; the **median SFT job costs ~$1**; **developer-tier hosting** has **no hosting fee** — cheap experimentation bridges you to production where savings compound.
- **Two myths busted at close:** (1) "Frontier models keep getting smarter so I don't need fine-tuning" — but they also get **bigger, slower, costlier**, and fine-tuned small models can **outperform frontier-class** while keeping **your IP in your weights**; (2) "Fine-tuning is expensive" — it isn't, given developer tiers and ~$1 median jobs.
- **The business stakes framing:** US online returns are an **~$900B/yr** problem; the demo narrative tracks "money still being lost" at each quality tier (74% → still >$100B; 84% → still ~$90B) to motivate each harder technique.
- **Optimization is a journey, not a switch:** prompt → context management (grounding + memory) → tools → continuous evaluation → *then* optimize (fine-tune) when the model is wrong, too slow, or too expensive. This talk focuses on the **evaluate + optimize** right-hand side of that curve.

## 📚 Detailed Notes

### Framing: who's talking and what's the promise
Alicia Frame (product lead for model customization in Microsoft Foundry) and Omkar Mule (her engineering counterpart) co-present. The core promise: you can **deploy, observe, and learn from your production agents** to get models that are *better, smarter, cheaper, and faster*. The plan is ~5 minutes of fundamentals, then four escalating demos — distillation, reinforcement learning, an interactive low-level training API preview, and a natural-language fine-tuning skill.

### Where this sits in Microsoft Foundry
Foundry is Microsoft's **agent platform**. Its foundation is **models** — there are **over 11,000 models in Foundry** — which power an **agent runtime** that lets you deploy/host agents, observe them, and give them tools. On top of that, Foundry offers tooling to **evaluate** agents (know if they do what you want) and **optimize** them (improve performance based on what you observed). This talk lives in the **evaluate + optimize** box.

### Why fine-tuning, why now: the agent token problem
Fine-tuning has been around a while, but **agents have made it urgent**. Agents helped build the very slide deck and demos in this talk. Stats cited: ~**a third of enterprise software apps** say they'll embed agentic AI within 2 years (Alicia thinks the real number is higher and sooner), and ~**half of teams already have a production agent**. The catch: **agents consume 20–30× more tokens per turn** than an old-fashioned chat interaction. Suddenly there are far more models, for far more use cases, burning far more tokens — "you've broken the bank, your credit card is maxed out." If agents are token-consuming machines, **fine-tuning lets you build a reliable agent without breaking the bank.**

### What fine-tuning actually buys you (cheaper / faster / smarter)
Customizing a model gives three benefits:
- **Smarter** — historically people fine-tuned to teach a domain (e.g. "fine-tune GPT-3.5 Turbo for my domain"). Today, especially for agents, "smarter" means **calling the right tool at the right time with the right inputs** — baking the instructions from your prompt **into the weights** of the model.
- **Cheaper** — companies (Harvey, UiPath were cited from other sessions) fine-tune **smaller, cheaper, faster** models to match a frontier model's quality at a fraction of the price. Fine-tuning targets are often **10–30× cheaper** than a frontier model (e.g. replace GPT-5.4 with **4.1 Nano** or a **Qwen** model). At 30× cheaper, even 30× the token consumption still balances the budget.
- **Faster** — big frontier models can be slow ("we've all sat there watching Claude churn… I'm bored"). **Small models stream tokens faster**, so agentic workflows respond more quickly. Net result: a model that knows what tools to call *and* is cheaper *and* faster.

### Fine-tuning is your "cheat code" to a foundation model
How foundation models are built: **pre-training** (massive unlabeled data, next-token prediction) → **instruction tuning** (prompt/response, task-specific data to teach how to respond) → **alignment tuning** (human-preference data + reward models to steer responses). Stack those three and you get a frontier model. **Fine-tuning skips the most expensive/hardest part** — you pick up a generic off-the-shelf model that's already pretty good, then choose to do **supervised fine-tuning** (teach it to behave/copy from data), **alignment**, or **both**. You get a head start on the customization journey, add your data, and **create your own IP**.

### The optimization journey (where fine-tuning fits)
In Foundry you typically progress: (1) build the agent + get the **prompt** right; (2) add **context management** — data, grounding, memory; (3) give it **tools** to take actions / call external things; while continuously **evaluating** (is it doing what I want? how's it performing?). **Then** comes **optimize**: is the model doing the wrong stuff, too expensive, or too slow? That's where fine-tuning enters. About **half of developers** say they want to replace out-of-the-box models with fine-tuning — a shift from the "out-of-the-box is amazing, I'm good" era, driven by people now looking at **balance sheets and CSAT**. The decision is ultimately about **quality, latency, and cost** compounding in the agentic loop.

### The running scenario: retail refunds customer-service agent
All demos use **one customer scenario**: a retailer's **customer-service agent that processes refunds**. A customer calls asking for a refund on an item; the agent must decide whether the **request is valid**, whether the item **can be returned**, and whether it should be **replaced or refunded**. The agent has tools to look at **order details**, **fulfillment status**, **policy details**, and to **process payments**. Getting it wrong loses the retailer **money or customers** — and **US online returns were ~$900 billion last year**, so accuracy is critical. This scenario anchors a leaderboard the speakers "hill-climb" throughout.

### Demo 1 — Distillation (cheaper + faster via SFT)
**Concept:** take a large, smart **teacher** model (e.g. GPT-5.4), **capture its traffic** as training data, then take **traces from your production agent**, filter/curate them, build a training set, and produce a small **student** model that's *as good as* the frontier model.

**Walkthrough (Foundry UI + SDK):**
- The **Foundry UI** is a simple no-code way to build agents and fine-tune models — but everything is also possible from code.
- Omkar built a **hosted agent** using **GPT-5.4** as its base. Foundry hosted agents let you bring **any agent platform** (Semantic Kernel, LangGraph, etc.) and host it on Foundry. He runs an example: a customer wants to **return an unused yoga mat** and get a refund. The request resolves, and you can open the **traces**.
- **User view vs. trajectories:** the user view shows the request + final outcome; the **trajectory** shows *which tools were invoked* — here `get_order_details` → `fulfillment_status` → `check_resolution_policy` → final outcome. This is **rich data** for evaluating *and* improving models.
- The agent had been running a few days with **~1,000+ traces** captured. First question: **can I just swap the large model for a smaller one?** So they build an **evaluation** to see how models stack up *before* any fine-tuning ("we're not lying — start with smaller and cheaper, no fine-tuning, see how it works").
- **Graders:** Foundry offers **out-of-the-box LLM graders** (task resolution, intent resolution) that inspect the trajectory and judge intent/completion. For more control you write your own graders — **LLM-backed or pure Python**. Omkar wrote a **Python grader** scoring on three fronts: **decision correctness** (was the refund correctly approved/rejected) — **50% weight**; **accuracy of the dollar amount** (refunding $500 on a $50 item is wrong); and **format** — **20% weight**, because downstream systems depend on output format. Without graders you can't know if the agent works *or* whether fine-tuning helped or hurt — "the most foundational stuff."
- He submits an **eval run for the base models**; SDK-generated artifacts **auto-register in the UI** for a clean view. **Baseline result:** **o4-mini** and **GPT-4.4** do reasonably OK (~**65%** quality), but the smaller **4.1 mini** and **Nano** perform **really poorly** — you can't just swap them in to save cost/latency. ("So what do we do?" — "Cry?")
- **Fine-tune to the rescue, via UI:** open the agent → **traces** → **Create dataset**. This converts raw traces into datasets usable for **evaluation, reinforcement fine-tuning, or supervised fine-tuning**, and does smart prep: **removes duplicates**, drops non-interesting conversations, and **redacts PII** before training.
- He chooses **supervised fine-tuning** with **~1,400 traces** (SFT guidance: **at least ~1,000 samples**; RFT can do more with less). He selects **GPT-4.1 mini/nano** and configures the SFT run:
  - **Training type / tier** governs data residency and cost. His favourite: **developer preview** tier — training at **half the cost** of a standard-tier job (runs on **low-priority VMs**, can take longer, great for developers).
  - **Data zone SKU** — **introduced at Build today** — gives **residency guarantees in the US** (he uses standard for now).
  - Datasets are **preloaded** from the converted traces (nothing to add). Option to **auto-deploy** the model after job completion (skipped). A few **hyper-parameters** are tweakable (more control comes in later demos). "Here is really just easy mode."
- He opens an **already-completed distillation run** → **Monitor** tab: **loss reducing**, **accuracy increasing**. You also get **checkpoints** for interesting cases (e.g. where reward spiked before the final step) that you can deploy. Need more? **Continuous fine-tuning** lets you submit another run with more data.
- He had pre-deployed this model, built an agent on it, and run the eval (in the interest of time). **Result:** a **new winner** — **GPT-4.1 mini (fine-tuned)** *outperforms* o4-mini **and** GPT-5.4, at a **fraction of the cost**, **faster**, and slightly more performant.
- **Guardrail point (Alicia):** the eval included the **default graders** (resolution, task completion). They weren't fine-tuning to improve those, but fine-tuning **didn't erode** the base model's capabilities — addressing the fear "maybe I made it better here but worse elsewhere."
- **Leaderboard now: 74%.** Budget is down, still holding frontier-model standard — but at $900B, losing 74% still means **>$100B lost to spurious refunds**. Not good enough → need a new technique.

### Why distillation hits a ceiling
With distillation you have a **frontier-class teacher** generate data and **SFT** a small student — super easy, but you can **never get smarter than your teacher**. The teacher's performance is the mark you're aiming at. If 74% isn't good enough for the business, you need something that can **exceed** the teacher — **reinforcement learning**.

### Demo 2 — Reinforcement fine-tuning (RFT): learn from your own mistakes
**Concept:** the model **learns from its own mistakes**. You define a **grader** (reusing all the eval work), use it to score the **model's own responses**, and learn from those scores. The model generates sample results → you score them → it learns from the best-performing ones → over time it learns to **reason through chained tool calls**. **Caveat:** RL needs a **verifiable task** — you grade whether a response is good and learn from that signal; *if you can't grade it, you can't learn from it.* Refunds are gradable ("yes you should have refunded that" / "no, that was terrible"), so it fits.

**Under the hood (30-second explainer):** send a prompt to the model → it generates **multiple samples called rollouts** (e.g. three candidates) → the **grader scores** them. Grader quality determines success: if everything is graded all-right or all-wrong there's **no signal and nowhere to go** — you need a grader that *grades the outcome you want* **and** *leaves room for improvement*. The quality scores feed the **trainer**, which **reinforces the correct answers** so the model learns to reason about a new domain.

**SFT vs RFT (Omkar):** SFT is **learning by seeing/copying** a smarter person — the teacher's full trajectories (which tools, what responses) are spelled out as the training set. In RFT you **don't** give the exact trajectories/prescription; instead the **training process invokes the tools on the fly**, takes the tool responses, grades them against the eval grader, and continuously reasons toward better decisions. "You give the model the tools to answer the questions and the model figures it out on its own."

**RFT walkthrough (SDK):**
- **Config + data:** training and validation data again come **from the traces**, but the training data **doesn't include the full tool-call history** — only the **actual user message** plus **ground truth** for the grader (e.g. the final score to be defended), *not* which tools to call or the message body to write. Upload to Foundry.
- **The RFT grader (most important part):** reuse the eval grader or tweak it. Omkar **added tool-coverage**: e.g. don't give a high score to a response where `get_orders` was never invoked. This controls grader behaviour and is **critical for avoiding reward hacking**.
- **Reward hacking (Alicia):** a real failure mode they hit — because the model was **penalized for calling the wrong tool**, it learned the degenerate policy **"I will never call a tool."** Telemetry/metrics later reveal when this happens.
- **Giving the training run tools:** all tools are hosted on a **Function App** (real, invokable tool calls) — effectively your **RL harness / RL environment**. You can also use **MCP servers** or anywhere else tools are hosted.
- **Hyper-parameters (RFT-specific, esp. for a reasoning model like OpenAI):** **reasoning effort** (low/medium/high — how much chain-of-thought, with token-cost implications), **number of epochs**, **evaluation interval**, and the **tool/Function App wiring**. "This is the *real* training run" — during training the tools are actually invoked and those results are used (vs. copying in SFT).
- **Monitor tab — metrics to watch:**
  - **Reward over time** (primary) — are train **and validation** rewards increasing? (Here: both increasing — good.)
  - **Reasoning-token mean per step** — model spent lots of reasoning early, **less later**, so the **final checkpoint uses far less reasoning** than the base model (cheaper inference). Early on it's "calling a whole bunch of tools trying to figure it out."
  - **Tool-calls per rollout** — if the model decided to **stop calling tools**, you'll see a **dip**, signalling something's wrong; you then **iterate on the grader**.
- **Result:** another **new winner** — **o4-mini at 84%**, a huge jump from ~73–75%; **intent resolution and task completion** also increased or stayed stable. "The more effort you put in, the better what you get" — RFT takes more effort (correct graders, longer runs) but the outcome is **substantial**. And **o4-mini is still smaller/cheaper than the GPT-5.4 teacher**, so it stays true to *better, cheaper, faster.* This maps to the **keynote's hill-climbing narrative** — "on our way up the hill."

### Real-world production use cases (not demoware)
Customers already use these techniques in production:
- **Decagon AI** — builds **customer-support-agent-as-a-service**; used **distillation + fine-tuning** on Foundry to switch to smaller/cheaper/faster models.
- **Discovery Bank** — used distillation + fine-tuning for a smaller, lower-latency model in its banking app; customers texting the app went from **6 seconds down to ~1.5 seconds** response time — huge for customer satisfaction.
- **DocuSign** — one of Foundry's **biggest token customers**; distilled to achieve a **50% reduction in cost** for AI document processing.
Takeaway: distillation, fine-tuning, and RL are critical tools for making agents **economically viable and delightful to use**. Still at 84% → ~**$90B** potentially still lost → "what if we need more control?"

### Demo 3 — The new low-level interactive training API ("PyTorch as a service")
**Why:** everything so far was **managed fine-tuning** via simple UI / high-level APIs. Data/AI scientists may want to **define their own rollout environment, their own algorithm, and full hyper-parameter control**. Enter a **sneak-peek interactive training API**.

**Managed vs. new API (the key contrast):**
- **Managed fine-tuning:** *you* pick the model, technique (SFT/RFT), and provide data, then **submit to the service**. Inside the **service boundary** it does the rollouts, grades, computes loss, updates weights, and iterates as a **closed loop** before returning a checkpoint. **You can't touch what happens inside that boundary.**
- **New training API:** *you* set up the **config/recipe**, **invoke the rollout engine**, **compute the loss**, **update the weights**, and **update the grader** — all **outside** the service boundary. You control the **algorithm, training primitives, and every aspect of the job except the GPU infrastructure**. If you've ever tried (and failed) to set up **vLLM** / GPU clusters — sync vs async, aggregated vs disaggregated — Foundry **abstracts that pain away**; you focus on the algorithm, they manage compute.

**What a recipe looks like (Omkar):**
- Take the dataset → **generate multiple samples** per request (e.g. 10–20 options per conversation) via the **sample API**, which runs on **GPUs with a pre-loaded base LLM** and returns responses.
- **Write/invoke your own grader** to score those samples — no longer limited to supported graders; you can write a **C# grader** or something completely different. You also get **full control over invoking tools in the sampling process** — so tools that *aren't* compatible with the high-level APIs (not on an MCP server, custom formats) work here. Alicia: "Or I could even have **interactions with an environment** — execute the rollout, call real tools in the real world, and see what happens."
- **GRPO step:** compute **advantages** (take the **mean of the samples**, see which are better), then run **forward/backward pass** to compute gradients.
- **Two nodes behind the scenes:** a **training node** (runs forward/backward, computes gradients) and a **sampling node**; calling **sync** pushes the updated **LoRAs** from training node to sampling node. All of this needs heavy **telemetry** — hard work you don't have to do (no NCCL/vLLM issues to debug). When done, call **sync checkpoint** to save for later training.
- **Still inside Foundry:** it appears as a **run** in Foundry; the resulting models work like any other Foundry model — usable with **hosted agents** and **evaluation**. The whole ecosystem is there.

**Running it:** a **launcher script** starts the recipe as a **tmux session** you can inspect. It all runs **locally on your own CPU machine** (laptop, or an **Azure VM** for long-running sessions). Foundry ships a **small local dashboard** (training runs on your machine, so fine-grained logs live there). Opening a completed low-level run shows **reward and accuracy increasing**, plus richer detail: **entropy reducing**, **grad norm reducing**, **KL divergence**, and **group composition** improving over time. Alicia: **KL divergence** is the **#1 investigation for reward hacking** — invisible before, visible now.

**Advanced control unlocked:** full telemetry on your side; **mid-run interactive changes** (e.g. switch sampling strategy partway — "that's where the *interactive* comes in"); **curriculum learning** (start simple, graduate to harder tasks); and swap **GRPO** for **PPO/DPO** or other mechanisms while reusing the same primitives. **Final leaderboard result:** a fine-tuned **Qwen 3 32B** OSS model **beats even the o4-mini fine-tune** — a much cheaper, smaller model, with agents that are faster, cheaper, **and** smarter. "Full hard mode — congratulations, you're writing the training algorithm yourself."

### Demo 4 — The fine-tuning skill (natural language for coding agents)
**Why:** "writing the training algorithm yourself" makes non-data-scientists anxious. Common complaints: "I don't even have the data," and "I tried fine-tuning once, made the model worse, never again." Answer: a **fine-tuning skill** — use your favourite **coding agent** + **natural language** to say what you want; it figures out the rest.

**Walkthrough (run ahead of time; Alicia doesn't fully trust Claude/Copilot CLI to do it live, and a non-fine-tuned model is slow):**
- **Step 1 — baseline (mirrors Omkar's Demo 1):** she gives the skill the **address of her hosted agent** and says: I have an agent, figure out how well it does; **make a grader** that checks it calls the right tools, gives **partial credit**; then **report performance**. No need to learn the API/SDK or click the UI — the skill **knows how to build graders and call the APIs**. It produced a grader (full credit for asking clarification or getting it right; partial credit for some correct tool calls) and graded the teacher (**GPT-5.4**): **mean score 8.37**, **pass-rate@8 ~78%**.
- **Step 2 — fine-tune:** she says "kick off a **distillation run**," goal = **cheaper + faster** (which helps it pick models), take the agent **traces**, export/filter/dedupe them, and run a **fine-tuning autopilot**. Autopilot **decides which models to run, which algorithm, and runs several experiments**. In parallel she ran the same **honesty check** on the smaller/cheaper base models. Result: a **winner — fine-tuned 4.1 mini** (it picked **mini and nano** because she said smaller/cheaper, and **chose hyper-parameters itself**), with **almost the same mean score** and a **slightly higher pass@8** than the teacher.
- This is part of the **GitHub Copilot for Azure** skill, or downloadable as a **standalone fine-tuning skill**. It makes fine-tuning **accessible** — and if a run made things worse, it **reads the logs and decides next steps** (generate more data, try a different experiment) and iterates until it gets it right.

### Closing: two myths busted + getting started
**Myth 1 — "Frontier models keep getting smarter, so I don't need to fine-tune."** They're getting smarter **but also bigger, slower, and more expensive**; the keynote showed fine-tuned **small/cheap models outperforming frontier-class** models. Plus, when you fine-tune, **your IP / business knowledge / domain goes into *your* custom model** — not into a Frontier Lab's weights for them to monetize. You keep your IP, get a smarter model, and better performance.

**Myth 2 — "Fine-tuning is too expensive (train + host)."** Reality: **developer tier training** = **spot capacity, 50% off**; the **median SFT job on the platform costs ~$1**; **developer-tier hosting** has **no hosting fee**, so experimentation is easy and bridges you to production where savings compound as usage ramps.

**Get started:** the **sample notebooks** from the demos are in a repo; you can **sign up for the preview** of the training API Omkar showed; and there are **three hands-on labs tomorrow** to do RL yourself with the demo example, plus other breakouts and lightning talks.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the agent platform hosting models, the agent runtime, evaluation, and optimization; home for all the fine-tuning tooling in this talk (formerly Azure AI Foundry).
- **Foundry model catalog** — **11,000+ models** available to power agents and serve as fine-tuning bases.
- **Foundry agent runtime / hosted agents** — deploy and host agents (bring **Semantic Kernel**, **LangGraph**, or any agent platform), give them tools, and auto-capture traces.
- **Traces / trajectories** — captured records of agent runs (tools invoked, order, outcome) used for evaluation and as training data.
- **Create dataset (from traces)** — Foundry feature converting raw traces into datasets for eval / SFT / RFT, with **dedupe, noise removal, and PII redaction**.
- **Evaluations + graders** — out-of-the-box LLM graders (**task resolution**, **intent resolution**, **task completion**) plus custom **LLM-backed or pure-Python graders**; SDK runs auto-register in the UI.
- **Supervised fine-tuning (SFT)** — train a student to copy spelled-out trajectories; recommended **~1,000+ samples**.
- **Distillation** — capture a frontier teacher's traffic to build the SFT training set for a small student.
- **Reinforcement fine-tuning (RFT)** — model generates rollouts, a grader scores them, the trainer reinforces the best; trains **with live tools**, requires a **verifiable task**.
- **Reward models / alignment tuning** — named as the foundation-model alignment step that fine-tuning can replicate.
- **Continuous fine-tuning** — submit a follow-up run with more data to keep improving a model.
- **Checkpoints** — intermediate models saved during training (e.g. where reward spiked) that can be deployed.
- **Training tiers / SKUs** — **standard**, **developer preview tier** (low-priority/spot VMs, ~50% off), and the newly introduced **data zone SKU** (US residency guarantees).
- **Developer-tier hosting** — model hosting with **no hosting fee** for cheap experimentation.
- **Interactive / low-level training API** — "PyTorch as a service"; exposes **sample / forward pass / backward pass / optimizer step / sync / sync-checkpoint** primitives with user-controlled algorithm, recipe, grader, and tools; Foundry manages GPU compute. (**Preview — sign-up available.**)
- **GRPO / PPO / DPO** — RL algorithms; **GRPO** (advantage = sample mean) is default in the low-level API, swappable to **PPO/DPO**.
- **Curriculum learning** — train easy-to-hard tasks progressively, supported by the low-level API.
- **LoRA** — low-rank adapters synced from the training node to the sampling node during low-level training.
- **Local training dashboard** — shipped local UI showing fine-grained telemetry (reward, accuracy, **entropy**, **grad norm**, **KL divergence**, group composition).
- **Fine-tuning skill** — natural-language skill for coding agents; part of **GitHub Copilot for Azure** or a **standalone download**; builds graders, calls APIs, runs a **fine-tuning autopilot**, and iterates from logs.
- **Function App / MCP servers** — host the real tools the RFT/low-level training runs invoke (the "RL harness/environment").
- **tmux** — the launcher runs the low-level recipe as a tmux session for inspection.
- **vLLM / NCCL** — GPU-serving / comms stacks whose setup pain Foundry abstracts away.
- **Models referenced as bases/targets:** **GPT-5.4** (teacher), **GPT-4.4**, **o4-mini**, **GPT-4.1 mini**, **GPT-4.1 Nano**, **Qwen / Qwen 3 32B** (OSS), generic **OSS models**.

## 🚀 Announcements / What's New
- **Interactive / low-level training API ("PyTorch as a service") — PREVIEW (sneak-peek + sign-up).** New API exposing low-level training primitives (sample/forward/backward/optimizer/sync) with user-controlled algorithm, grader, and tools while Foundry manages GPU compute; supports custom rollout environments, real-world tool/environment interaction, GRPO/PPO/DPO, and curriculum learning. Sign up for the preview.
- **Data zone SKU for training — "introduced at Build today."** New training SKU offering **data-residency guarantees in the US**.
- **Fine-tuning skill (natural-language)** — available as part of **GitHub Copilot for Azure** and as a **standalone download**; presented as current/available.
- **Developer-tier training (50% off, spot/low-priority VMs)** and **developer-tier hosting (no hosting fee)** — highlighted as available cost options (presented as in-product; not explicitly framed as new today).
- Note: GPT-5.4 / GPT-4.1 mini / Nano / o4-mini / Qwen 3 32B appear as **available base models** in the catalog rather than as new announcements in this session.

## 💡 Demos
- **Demo 1 — Distillation / SFT (cheaper + faster):** Built a GPT-5.4 hosted refunds agent, captured ~1,000+ traces, ran a baseline eval (custom Python grader: 50% decision / accuracy / 20% format) showing small models fail (4.1 mini/nano poor; o4-mini & GPT-4.4 ~65%), then UI-converted traces → dataset → SFT of GPT-4.1 mini. **Proved:** a fine-tuned 4.1 mini can **beat o4-mini and the GPT-5.4 teacher** at a fraction of cost/latency *without eroding* base capabilities. **Leaderboard → 74%.**
- **Demo 2 — Reinforcement fine-tuning (RFT):** SDK config where training data has only user message + ground truth; grader extended with **tool-coverage** to prevent reward hacking; tools hosted on a **Function App** invoked live during training; tuned reasoning effort/epochs; Monitor showed train+val **reward rising**, **reasoning tokens falling**, healthy tool-calls-per-rollout. **Proved:** RL lets the model **exceed the teacher** — **o4-mini → 84%** (up from ~73–75%), still cheaper than GPT-5.4.
- **Demo 3 — Low-level interactive training API:** A recipe launched via script as a **tmux** session running locally, sampling 10–20 candidates/request on GPU-backed sample API, custom grader + live tool calls, **GRPO** advantages, forward/backward on a training node, LoRA **sync** to a sampling node; a **local dashboard** exposed entropy, grad norm, **KL divergence**, group composition. **Proved:** full algorithmic control yields a fine-tuned **Qwen 3 32B** that **beats the o4-mini fine-tune** — cheaper, smaller, smarter.
- **Demo 4 — Fine-tuning skill (natural language):** Pre-recorded coding-agent run: plain-English prompts to build a partial-credit grader, baseline the **GPT-5.4** teacher (mean **8.37**, pass@8 ~**78%**), then a **distillation autopilot** that auto-picked mini/nano + hyper-parameters and produced a **fine-tuned 4.1 mini** matching the teacher's mean with a slightly higher pass@8. **Proved:** end-to-end distillation with **no API/SDK/UI knowledge required**, self-iterating from logs.

## 📊 Notable Stats / Quotes
- **Agents consume 20–30× more tokens per turn** than an old-fashioned chat interaction.
- **~1/3 of enterprise software apps** plan to embed agentic AI within **2 years** (speaker believes it's higher and sooner); **~half of teams** already have a production agent.
- Fine-tuning targets are often **10–30× cheaper** than a frontier model.
- **~Half of developers** say they want to replace out-of-the-box models with fine-tuning.
- **Over 11,000 models** in Foundry.
- **US online returns ≈ $900 billion** last year (the scenario's stakes).
- **Leaderboard progression:** baseline small models ~**65%** → SFT/distilled 4.1 mini **74%** → RFT o4-mini **84%** → fine-tuned **Qwen 3 32B** beats the o4-mini fine-tune.
- **SFT guidance:** at least **~1,000 samples** (RFT needs less); demo used **~1,400 traces** (1,000 selected).
- **Grader weights:** decision correctness **50%**, format **20%** (remainder on dollar-amount accuracy).
- **Customer results:** Discovery Bank **6s → 1.5s** latency; DocuSign **50% cost reduction** in AI document processing; Decagon AI switched to smaller/cheaper models.
- **Developer tier training = 50% off**; **median SFT job ≈ $1**; **developer-tier hosting = no hosting fee**.
- Fine-tuning-skill baseline: GPT-5.4 mean score **8.37**, **pass@8 ~78%**.
- **Quotes:** "If you can't grade it, you can't learn from it." · "You give the model the tools to answer the questions and the model figures it out on its own." · "Fine-tuning is really just your cheat code to building a foundation model." · "You keep your IP — it's not going into that Frontier Labs' weights for them to make money off of you." · (on swapping a small model in cold) "— So what do we do?" "Cry?"

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up a Foundry hosted agent, let it accrue ~1,000+ traces, then use **Create dataset** (with PII redaction) → UI **SFT** of GPT-4.1 mini/nano and compare to the frontier base on a custom Python grader.
  - Write a 3-axis grader (decision 50% / amount / format 20%) and reuse it as the **RFT reward**; add **tool-coverage** rules to block reward hacking.
  - Host tools on an **Azure Function App** (or MCP server) as an RL environment and run an **RFT** job; watch reward (train+val), reasoning-token mean, and tool-calls-per-rollout.
  - **Sign up for the low-level training API preview**; try **GRPO** then experiment with **PPO/DPO** and **curriculum learning**; monitor **KL divergence** for reward hacking via the local dashboard.
  - Install the **fine-tuning skill** (GitHub Copilot for Azure or standalone) and drive a **distillation autopilot** purely in natural language.
  - Try **developer-tier training (50% off)** + **developer-tier hosting (no fee)** to keep experimentation near ~$1/job.
- [ ] Questions:
  - What models/regions are eligible for the low-level training API preview, and how does pricing for sample/forward/backward primitives work?
  - Which base models support **data zone SKU** US residency, and is non-US residency on the roadmap?
  - Practical floor for RFT sample counts vs SFT's ~1,000? How low can RFT really go?
  - How are **C# graders** executed/sandboxed in the low-level pipeline?
  - Does **continuous fine-tuning** stack cleanly on an RFT checkpoint, and how are checkpoints versioned/governed?
- [ ] Relevant to:
  - Cost/latency optimization for any production agent burning frontier-model tokens (refunds, support, doc processing).
  - Teams with verifiable/gradable tasks wanting models that **exceed** a teacher via RL.
  - Data/AI scientists needing algorithmic control without owning GPU/vLLM infra.

## 🔗 Related
- [[DEM322 - Smaller faster smarter Distilling models with fine-tuning]] — sibling deep-dive on the exact distillation/SFT technique demoed here.
- [[BRKSP91 - Turn foundation models into production AI on Foundry]] — turning base/foundation models into production-grade models on Foundry.
- [[DEM320 - Hugging Face open-source models to production on Foundry]] — taking OSS models (like the Qwen 3 32B used here) to production on Foundry.
- [[DEM323 - Under the hood of Microsoft AI models]] — background on how Microsoft's models are built (pre-train → instruction → alignment).
- [[BRK252 - From observability to ROI for AI agents on any framework]] — the observe half of deploy→observe→learn: traces/evals → ROI.
- [[DEM361 - Understand and fix Agent Framework apps with observability and evals]] — evals + observability that feed the fine-tuning/reward loop.
- [[BRK246 - Foundry IQ Fuel agents with enterprise knowledge]] — the grounding/knowledge step earlier in the optimization journey.
- [[BRK241 - From prototype to production build and run agents at scale]] — productionizing the hosted agents you then fine-tune.
- Source list: [[2026 Build Session List]]
