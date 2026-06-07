---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/design-systems
  - topic/ui
  - topic/ai
  - topic/llm
  - topic/accessibility
  - topic/pdf
source: https://www.youtube.com/watch?v=XcI81nVWmWU
session_code: ODSP916
event: Microsoft Build 2026
speakers: Hisby (Software Engineer, PDF SDK team — iText / Apryse; speaker name & company caption-uncertain)
duration_min: 12
aliases:
  - Design systems for every user including people and LLMs
  - ODSP916
  - Tagged PDFs for humans and LLMs
---

# ODSP916 — Design systems for every user including people and LLMs

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Hisby — Software Engineer on a PDF SDK team (works on the iText SDK + PDF accessibility; speaker name and company "Price" are caption-uncertain, most consistent with **iText / Apryse**)  
> **Duration:** ~12 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=XcI81nVWmWU)

## 🎯 TL;DR
A short, focused partner talk arguing that **documents (specifically PDFs) now have two kinds of consumers — humans and LLMs — and both struggle with the same problem: missing semantic structure.** A raw PDF is just drawing instructions ("paint these glyphs at these pixels"), so the *meaning* (what's a heading, a table, a list) is implicit. Humans reconstruct that meaning automatically from visual cues; LLMs can't, so they either burn tokens on heavy OCR/vision or produce garbled, structureless output. The fix is **Tagged PDF** — an HTML-like semantic layer (H1, paragraph, table, list) embedded alongside the pixel-perfect rendering — which is exactly the same mechanism that makes PDFs *accessible* to assistive technology. The speaker demos extracting the same 4-page PDF two ways: **Docling (OCR/vision) takes ~18s and leaks a watermark + flattens sublists**, while **iText reading the embedded tags takes ~0.075s (≈200× faster), is clean, and preserves structure.** The thesis: **"Design for understanding, not just rendering"** — enabling tag embedding is a few minutes of work (often a single flag) and gives you free smart extraction, search, accessibility, *and* a competitive edge as you build AI infrastructure on your documents.

## 🔑 Key Takeaways
- **Documents are now consumed by both people AND LLMs** — design for both audiences, not just visual human readers.
- The four accessibility principles (**POUR: Perceivable, Operable, Understandable, Robust**) describe the *same* issues that trip up *both* humans and LLMs working with PDFs.
- **A PDF is a container format** (fonts, images, video, etc.) whose core is a **drawing language**: low-level instructions like "move to (x,y), draw these characters here." It guarantees pixel-perfect rendering but encodes **no meaning**.
- **Humans infer semantics for free** — reading order, "this is a title," "this is a list" — from visual/drawing artifacts (lines, list symbols, layout). We're "trained up on it."
- **LLMs only see pixels.** Without embedded metadata they can't apply semantic reasoning, so meaning has to be reconstructed expensively (heavy training/vision) or lost.
- **Plain LLMs are actually decent at raw extraction, but the output has no structure** — it can *guess* "annual report = title" but can't reliably know what means what; that's inefficient and error-prone to train on.
- **Add semantic meaning and everything gets easier:** the same content tagged as header / table / paragraph is far simpler for both LLMs *and* normal users to extract correctly.
- **Tagged PDF** is the built-in mechanism for this: it gives a document an **HTML-like structure tree** (H1 → paragraph → table) **while keeping pixel-perfect rendering**. As a developer you get it largely for free because low-level libraries do the tagging.
- Once structure + metadata exist, **assistive technology, search, and text extraction are all far easier** because you're working against a structured data model, not pixels.
- **Demo result — speed:** OCR/vision (Docling) ≈ **18 s** for 4 pages vs iText reading embedded text/tags ≈ **0.075 s** → **~200× faster.**
- **Demo result — quality/security:** OCR pulled in a **watermark** the author never intended as data (a training-data poisoning / **jailbreak-via-injection** risk) and **flattened sublists**; the tag-based path produced clean output and **preserved sublist hierarchy**.
- **OCR mistakes are silent and compounding** — hard to trace, they accumulate and eventually yield badly-wrong output formats; structured extraction avoids the whole class of error.
- **Accessibility isn't extra work.** Two cheap steps — (1) enable metadata/tag embedding (often a single flag), (2) make sure tags correctly convey the author's intent — give you smart extraction, easy search, and accessibility, all at once.
- **Strategic payoff:** making your documents accessible to *both* users and LLMs makes the AI infrastructure you build over the next years dramatically better at processing your data — **a competitive edge from accessibility.**

## 📚 Detailed Notes

### Framing: a PDF now has two audiences
The speaker (Hisby), a software engineer working on a PDF SDK and on **PDF accessibility**, opens with the core reframe: **PDF documents today are not only consumed by people — they are also consumed by LLMs.** Therefore a PDF should be **as accessible as possible for both consumers**. This is the whole session in one sentence: accessibility work and "AI-readiness" work are the same work.

### The accessibility lens — POUR — applies to machines too
He pulls in the classic accessibility principles. For content to be usable it needs to be:
- **Perceivable**
- **Operable**
- **Understandable**
- **Robust**

(These are the four **POUR** principles from web/document accessibility, e.g. WCAG.) His point in raising them: **these are exactly the kinds of issues that *both* humans and LLMs hit when working with PDF documents.** A document that fails these for a screen-reader user tends to fail an LLM for the same underlying reason — missing structure/meaning.

### What a PDF actually is: a container + a drawing language
- **PDF is a container format.** You can bundle different formats — fonts, images, video — together into one file.
- The most important part to understand is the **drawing language**: the PDF's content is fundamentally a set of **drawing instructions** you can render.
- Concretely, on a canvas (a PDF *page*) the instructions say things like **"move to this location, then draw these characters at this exact location."**
- The payoff of this design: when you open a PDF someone else created, **your PDF processor knows exactly which pixel to render which content on** → guaranteed faithful, pixel-perfect rendering everywhere.

### The gap: pixels/characters ≠ meaning
Pixels and characters are **very different from what we actually do when we look at a PDF.** When *humans* look at those rendered pixels, we automatically:
- assign a **reading order**,
- understand the **semantics**, and
- **infer the author's intended structure** from **drawing artifacts** — lines, list symbols, spacing, layout — e.g. "these bullets mean this is a list," "this big text up top is a title."

We do this effortlessly **because we're trained on it.** The meaning is *implicit* in the visual rendering, never explicitly stored.

### Why this breaks LLMs
- **An LLM, out of the box, has none of that meta information.** It "just looks at the page and sees pixels."
- So it's **very hard for an LLM to extract the data**, and to interpret the *actual meaning behind* those pixels.
- Two expensive escape routes, both bad:
  1. **Heavy training / vision** to reason directly over the rendered image → **lots of tokens**, costly.
  2. **Text extraction first**, then train the LLM on the extracted data — only as good as the extraction step.
- Important nuance he stresses: **plain LLMs are actually *quite good* at extracting this kind of data** from a raw page — **but the result has no structure.** It "doesn't really know what means what." It can *guess* ("annual report is probably a title") but it **can't apply semantic reasoning onto the context**, which makes it **inefficient and unreliable to train on.**

### The before/after: same content, with vs without semantics
He contrasts two views of *the exact same document*:
- **Left (no structure):** raw extracted content. No idea which part is a header, which is a table — meaning is guessed at best.
- **Right (with semantics):** the same content **tagged** — *this* is a header, *this* is a table — making it **far easier for both the LLM and the normal user to extract the semantic meaning.**

### Tagged PDF: the fix that serves both audiences
- Historically, **normal PDFs didn't have a system to tag content with semantic meaning** — meaning lived only in the pixels.
- **PDF evolved**, and now includes a mechanism for exactly this: **Tagged PDF.**
- As a **developer you get the advantage largely for free**, because **low-level tools do the tagging for you.**
- What it looks like in practice: open a tagged PDF and on one side you have the **pixel-perfect rendering (left)**, and on the other you now have a **text/structure tree (right)** — **the same kind of structure you'd know from HTML.** You can see definitively that, e.g., **the blue text is an `H1`**, below it is a **paragraph**, then a **table**.
- Net result: **pixel-perfect rendering AND complete semantic information + metadata about the document, together.**

### Why structure changes the economics of tooling
Once a document carries that semantic layer:
- **Building tools on top of PDFs becomes far easier** — you just inspect the structure tree to see what text/elements are there.
- **Assistive technology, search, and extraction are all far easier to implement**, because you now have a **structured model of the displayed data** instead of raw pixels.
- **Text extraction** is called out as one of the most interesting wins, since **lots of developers need to process large volumes of PDFs.**

### The demo pipeline (two approaches compared)
He builds a small **LLM data pipeline** and runs the **same PDF** through two extraction strategies, converting each to **Markdown** (chosen because Markdown is **information-dense** — it carries the semantic structure compactly, ideal to feed an LLM):

1. **OCR / vision path — Docling (`docling`).** Open-source, "the most well-used and one of the best tools out there." It analyzes the rendered pixels/pictures.
2. **Embedded-text path — iText SDK (Java).** Instead of analyzing pictures, it **leverages the embedded text/tag system inside the PDF** (the metadata) to pull out exactly the content you want.

**Test document:** a normal summary PDF with tables, lists, and deliberate **stress tests** — including a **watermark** and some **very tiny text**.

- **Docling run:** the script (Python, "quite easy") reads the PDF and calls the right library functions to convert to Markdown. There's a one-time **model warm-up/load** (only once per Docling process), then the actual conversion runs and **takes ~18 seconds** for the 4 pages (because it's processing the OCR / the pixels).
- **Docling output quality:** **actually quite good** — gets the tables, the lists, even **difficult languages** — **but it also extracts the watermark**, which was **not** intended as real content. (See security note below.)
- **iText run (Java):** **0.075 seconds** (he corrects himself from "0.75" to **0.075 s**) → **~200× faster than the OCR implementation.**
- **iText output quality:** **tables look exactly the same, content looks the same** — but **the watermark is correctly absent** (the author never intended it as data), which is **better for security**. Crucially, comparing the **"budget notes" list**: **OCR/Docling failed to recognize that some items were *sublists*** and flattened them, **because the semantic meaning was lost from the rendered page.** Using the **embedded metadata**, the **sublist is reconstructed correctly.**

### Why the OCR failure mode is dangerous, not just slower
- The **watermark leaking into the Markdown** isn't a cosmetic bug. If that polluted Markdown becomes **training data**, the stray text can be **used or abused to jailbreak your LLM** — i.e. OCR can **spoil/poison your training data** with content the author never meant to expose. (A practical document-level **prompt-injection / data-poisoning** vector.)
- The **flattened sublists** illustrate a deeper problem: **OCR generates mistakes that are very hard to trace, and those mistakes compound over time**, eventually producing **very wrong output formats.** Structured (tag-based) extraction sidesteps this entire error class.

### The takeaway: design for understanding, not just rendering
Both paths produced the *same kind* of Markdown to train LLM models on to extract the business data you need — but only the structured path did it fast, clean, and safe. So the actionable rule is **"design for understanding, not just rendering,"** especially for PDFs. Concretely, **two steps**:
1. **When producing a PDF, enable that the metadata is embedded.** In most PDF libraries this is **a single flag.**
2. **Make sure the tags are correct** and genuinely **convey the author's intent** for the document.

Do those two things and you get, **for free:**
- **smart data extraction**,
- **easy search**, and
- **accessible PDF documents** (for assistive technology / people with disabilities).

### Closing thesis
**"Accessibility isn't extra work."** What you do now is **only a few more minutes of work**, but it means the **AI infrastructure you build over the coming years will be far better at processing all your documents** — so you **gain a competitive edge simply because you made your data accessible to both users and LLMs.** He closes by inviting questions and offering follow-up help (contact him or the company, "Price"/iText).

## 🛠️ Products / Features / Technologies Mentioned
- **PDF (Portable Document Format)** — a **container format** (fonts, images, video, …) whose core content is a **drawing language** of low-level paint instructions; guarantees pixel-perfect rendering but stores no inherent semantics.
- **Tagged PDF** — the PDF mechanism that adds an **HTML-like semantic structure tree** (e.g. `H1`, paragraph, table, list) and metadata *alongside* the rendering; the foundation for both accessibility and machine extraction.
- **iText SDK** — the PDF library the speaker works on (demoed in **Java**); reads the **embedded text/tags + metadata** to extract structured content extremely fast (~0.075 s for 4 pages). Owned by **iText Group / Apryse** (the company name "Price" in the captions is uncertain; iText/Apryse is the most consistent fit).
- **Docling (`docling`)** — open-source, widely-used **OCR/vision-based** document-extraction tool; analyzes rendered pixels and converts to Markdown (~18 s for 4 pages; leaked the watermark and flattened sublists in the demo).
- **Markdown** — chosen output format for the LLM pipeline because it is **information-dense** and preserves semantic structure compactly.
- **POUR accessibility principles** — Perceivable, Operable, Understandable, Robust — the lens used to argue humans and LLMs face the same document problems (WCAG-style principles).
- **OCR (Optical Character Recognition)** — the pixel-analysis approach contrasted unfavorably with reading embedded tags.
- **Assistive technology** — screen readers etc., the accessibility consumers that benefit from the same tag structure LLMs need.
- **Python** — used to drive the Docling extraction script.

## 🚀 Announcements / What's New
None explicitly announced. This is an educational/best-practices partner talk; no new product, preview, GA, or roadmap items were revealed. Tagged PDF and the tools shown (iText, Docling) are existing technologies.

## 💡 Demos
- **OCR vs. embedded-tags extraction, head to head.** The same stress-test PDF (4 pages; tables, lists, a watermark, very tiny text) was converted to Markdown two ways:
  - **Docling (OCR/vision, Python):** after a one-time model warm-up, conversion took **~18 seconds**. Output was "quite good" (tables, lists, even difficult languages) **but** it **included the watermark** (unintended, a poisoning/jailbreak risk) and **failed to detect sublists**, flattening the "budget notes" hierarchy because semantic meaning wasn't available.
  - **iText (embedded text/tags, Java):** conversion took **~0.075 seconds — ≈200× faster.** Tables and content matched, the **watermark was correctly excluded**, and the **sublist structure was reconstructed correctly** from the embedded metadata.
  - **Point proved:** reading a document's *semantic layer* is dramatically faster, cleaner, safer, and structurally accurate compared with reconstructing meaning from pixels via OCR — and OCR's errors are silent and compounding.

## 📊 Notable Stats / Quotes
- **~18 seconds** — Docling/OCR to convert the 4-page PDF to Markdown (after model warm-up).
- **~0.075 seconds** — iText reading embedded text/tags for the same document (speaker corrects himself from "0.75 s" to **0.075 s**).
- **~200× faster** — the embedded-tags path vs the OCR path.
- **4 principles — Perceivable, Operable, Understandable, Robust** (POUR) — framed as the shared failure modes for humans *and* LLMs.
- **2 steps** to readiness — (1) enable metadata/tag embedding (often a single flag), (2) ensure tags convey author intent.
- > "Design for understanding, not just rendering." *(the session's central maxim)*
- > "Accessibility isn't extra work… only a few more minutes of work… your AI infrastructure will be so much better at processing all your documents… you will gain a competitive edge just because you made your data accessible to both users and LLMs."
- > "The LLM just looks at the page and sees pixels." *(why raw PDFs are hard for models)*
- > A leaked watermark in OCR output "might be used or abused to jailbreak your LLM." *(document-level injection/poisoning risk)*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Re-run the demo's premise on real corpora: extract a folder of tagged vs untagged PDFs with **iText (embedded tags)** vs **Docling (OCR)** and measure speed + structural fidelity (especially nested lists/tables).
  - Check whether our PDF-generation pipeline **enables the Tagged-PDF / accessibility flag** — confirm the single-flag setting in whatever library we use, and validate the produced tag tree.
  - Build a quick **tag-correctness audit** (does the structure tree actually match author intent: headings level-correct, tables/lists not flattened, no decorative artifacts mis-tagged).
  - Treat OCR'd document text as **untrusted input** in any RAG/training pipeline — sanitize/strip watermarks & decorative layers to avoid prompt-injection / data-poisoning.
- [ ] Questions:
  - Confirm the **speaker's name** ("Hisby") and **company** ("Price") — almost certainly **iText / Apryse** given the iText SDK demo; verify before citing.
  - For *scanned* (image-only) PDFs with **no embedded text**, OCR is unavoidable — what's the recommended hybrid (OCR + post-tagging) so downstream consumers still get structure?
  - How well does iText's tag-based extraction handle **complex/merged tables** and **multi-column** layouts vs OCR?
  - Does enabling tagging meaningfully increase **file size**, and are there tools to **auto-tag** large legacy untagged archives?
- [ ] Relevant to:
  - Any **RAG / document-ingestion** pipeline feeding LLMs from PDFs (cleaner, faster, safer extraction).
  - **Accessibility/compliance** work (PDF/UA, WCAG) — the same effort now also yields AI-readiness.
  - **Design-system / UI metadata for machines** theme — same core idea (make structure machine-readable) applied to documents; pairs with ODSP902's design-systems-for-AI angle.
  - Teams generating customer-facing PDFs (reports, statements) who want them both accessible *and* agent-consumable.

## 🔗 Related
- Design systems made machine-consumable (UI side of the same idea): [[ODSP902 - Build AI-driven UIs in NET MAUI with design systems]]
- Extracting/serving unstructured data to LLMs (RAG over documents): [[ODSP925 - Deliver production-ready AI search on unstructured data with RAG]]
- Connecting documents & tools into agent workflows: [[BRK242 - Turn your agents into action Connect tools APIs documents]]
- Designing data structure for AI consumption (rows → reasoning): [[BRK223 - From rows to reasoning]]
- Document data foundations / open-source document store: [[OD821 - Building Azure DocumentDB on Open-Source Foundations]]
- Source list: [[2026 Build Session List]]
