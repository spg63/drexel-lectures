# CS 4550 / 6550 · Modern AI Application Development · Lecture outline

**Status:** draft v1 (2026-11-19). Plans 14 decks shared by both sections. First offering August 2027; decks due by mid-February 2027.

**How decks are used:** each deck has two halves (A, B) with a seam between them.
- Undergrad: half A in session 1, half B in session 2.
- Grad: the whole deck in one session.

Each half is about 75 minutes of material. Assignments, exams and grad milestones are out of scope here; the **Arc** lines only note what each week sets up.

**Running app (the spine):** one codebase over the course dataset (TBD), grown week by week. Each week's demo is that week's increment. Undergrad assignments and grad milestones later fork from the same tags.

---

## Through-lines

Threads that run across weeks. Each deck should name the thread when it picks one up.

| Thread | Introduced | Returns |
|---|---|---|
| **Cost & latency** | W1 token economics, meter in every demo | W10 caching/routing, W14 local serving |
| **Evaluation** | W3 schema validation as the first "test" | W5 retrieval metrics, W10 eval harness, W11 harm evals |
| **Security** | W2 delimiters and instruction boundaries | W7 tool sandboxing, W12 injection and guardrails |
| **Specs, not vibes** | W2B spec-driven development | Every assignment ships or requires a `SPEC.md` |
| **The gateway abstraction** | W1 every model call goes through one interface | W10 model-tier routing, W14 swap the backend to a local model in one line |

---

## Block 1 · MaaS foundations & systematic prompt design

### W01 · Foundation models as a service
**A. The MaaS landscape**
- From training models to consuming them: what changed and what didn't.
- Tokens as the unit of everything: tokenization, context windows, input vs. output pricing, cached-input discounts.
- Provider landscape and how to compare it: capability, price, latency, rate limits, data policies.
- Non-determinism as the defining engineering constraint; the rest of the course is about engineering around it.

**B. Calling models like an engineer**
- Anatomy of an API call: messages, roles, parameters (temperature, max tokens, stop).
- Streaming and why UX depends on it (time to first token vs. total time).
- Failure handling: rate limits, timeouts, retries with exponential backoff and jitter, idempotency, not losing state mid-stream.
- The gateway pattern: one internal interface, many providers (LiteLLM-style).

**Demo:** streaming chat over the course dataset's README; a cost meter on every call; kill the network mid-stream and recover.
**Figures:** the token pipeline; a price-vs-capability scatter; the retry timeline.
**Arc:** setup checkpoint (keys, gateway, first streaming call).

### W02 · Systematic prompt design & spec-driven development
*Not in the syllabus yet. Todoist has the syllabus edit.*

**A. Prompts as engineered artifacts**
- Prompt anatomy: system instructions, context, task, output contract.
- Structural delimiters (XML/markdown) to separate instructions from data. This is the first security lesson.
- Few-shot selection, ordering effects, and when examples hurt.
- Prompt templates under version control; prompts are code.
- Metaprompting: models drafting and critiquing prompts.

**B. Spec-driven development**
- The failure mode: one-shot "build me X" prompts to coding agents, where the code silently becomes the spec.
- The loop: spec → plan → tasks → implement → verify against the spec.
- What a good spec contains: goal, non-goals, interfaces, acceptance criteria that become tests. One page.
- Tooling (Spec Kit as the reference point), framed as practice, not product. Include the critique: specs that turn into theater, the waterfall worry.
- How the course uses it: `SPEC.md` with every assignment.

**Demo:** the same feature built twice with a coding agent, once from a one-line prompt and once from a spec; compare the results against the acceptance tests.
**Figures:** prompt anatomy diagram; the SDD loop; a spec template.
**Arc A** begins.

### W03 · Structured outputs & application integration
**A. Making stochastic output typed**
- Why free text breaks software; the output contract.
- JSON mode vs. schema-constrained decoding (how constrained decoding works, briefly).
- Pydantic models as the contract; validation, repair loops, and when to fail loudly.
- Schema design that models handle well: enums, required fields, descriptions as instructions.

**B. Integration patterns**
- Function calling as structured output: the model chooses a function and arguments. W7 adds the loop that executes them.
- Middleware that intercepts and coerces model output into typed objects.
- Validation failure rates as a first metric (the evaluation thread starts here).

**Demo:** extract typed records from messy dataset documents; a validation failure, then the repair loop; a validation-rate counter.
**Figures:** free text vs. structured pipeline; constrained-decoding token mask.

---

## Block 2 · Context augmentation & data orchestration

### W04 · RAG foundations
**A. Why retrieval**
- Knowledge cutoffs, private data, hallucination: what RAG fixes and what it doesn't.
- Embeddings as geometry: similarity, what the dimensions don't mean, embedding model choice.
- Chunking: fixed vs. structural vs. semantic, overlap, metadata. Chunking decides retrieval quality more than the vector store does.

**B. Building the pipeline**
- Ingest → chunk → embed → index → retrieve → assemble context → generate with citations.
- Vector stores: what they are (an ANN index plus metadata), FAISS/Chroma, and why the choice matters less than people think.
- Context assembly: ordering, budget, and the lost-in-the-middle effect.
- The naive-RAG failure catalog, which sets up W5.

**Demo:** the spine answers questions over the dataset with citations; show three chunking strategies on the same question.
**Figures:** the RAG pipeline; embedding space projection; chunking strategies side by side.
**Dataset must be fixed before this deck.**

### W05 · Advanced retrieval & hybrid search
**A. When dense retrieval fails**
- Exact-match failures: IDs, codes, names, numbers. Show one from the dataset.
- Sparse retrieval: BM25 intuition and math (TF saturation, length normalization).
- Hybrid search and rank fusion: Reciprocal Rank Fusion, and why it beats score averaging.

**B. Multi-stage retrieval & measuring it**
- Bi-encoders vs. cross-encoders; re-ranking as the precision stage.
- Query transformation: rewriting, multi-query, HyDE.
- Retrieval metrics: recall@k, MRR, nDCG on a small labeled query set. This set becomes the grading harness.

**Demo:** a query that dense retrieval misses, then BM25 finds it, then RRF combines both, then a cross-encoder re-ranks; recall@k before and after each stage.
**Figures:** two-stage retrieval funnel; RRF worked example; metric definitions.

### W06 · Multimodal ingestion
**A. Documents aren't text**
- Where document pipelines break: tables, charts, scanned pages, layouts.
- Parsing approaches: text extraction (PyMuPDF), layout-aware parsers (Unstructured-style), VLM page understanding.
- Tables: extract to structure vs. describe in text; chart-to-data.

**B. Multimodal retrieval & cost**
- Image and page embeddings (CLIP-style; ColPali-style page retrieval).
- Audio: transcription with timestamps, aligning transcript to slides or documents.
- Unified context records: text, table, figure and audio chunks with shared metadata.
- Cost and latency of image tokens (the cost thread).

**Demo:** ingest a table- and chart-heavy PDF from the dataset; ask a question only answerable from the table; compare text-only vs. VLM ingestion.
**Figures:** ingestion router diagram; table extraction before and after.
**Arc A** ends, **Arc B** begins (W5–7).

---

## Block 3 · Agentic architectures & stateful orchestration

### W07 · Reasoning & tool use
*Undergrad midterm is ~Week 7. Decide whether it takes a session (see open questions).*

**A. From chains to agents**
- Chain-of-thought and reasoning models: what "thinking" buys, and what it costs.
- ReAct: reason → act → observe, built from scratch in ~40 lines so nothing is magic.
- Native tool calling: the execution loop W3 left out; parallel calls; stop conditions.

**B. Tools in practice**
- MCP (Model Context Protocol): tools as servers, not code pasted into prompts. *Not in the syllabus; it's the 2026 standard and belongs here.*
- Writing tools models use well: names, descriptions, error messages written for the model.
- Sandboxing model-generated code; least privilege for tools (the security thread).

**Demo:** a hand-built ReAct loop over dataset search, then the same thing with native tool calling, then the dataset exposed as an MCP server.
**Figures:** the ReAct loop; tool-call message sequence; MCP client/server diagram.

### W08 · Stateful orchestration: chains to graphs
**A. Why graphs**
- Where linear chains break: loops, retries, branching, long-running work.
- State machines as the mental model: nodes, edges, conditional routing, shared state.
- LangGraph as one implementation; the concepts transfer to other frameworks.

**B. Reliability patterns**
- Self-correction loops (validation failure → fix node).
- Checkpointing and persistence: resume after a crash, inspect any step.
- Bounding agents: step limits, budgets, timeouts.

**Demo:** the spine becomes a graph: route → retrieve → answer → validate → retry; crash it mid-run and resume from the checkpoint.
**Figures:** the spine's graph; state flowing through nodes.
**Arc B** ends.

### W09 · Multi-agent systems & human-in-the-loop
**A. Multiple agents**
- Topologies: supervisor/worker, pipeline, debate/critic, hierarchical.
- When multi-agent is worse than one agent: error compounding, cost multiplication, coordination overhead.
- Agent-to-agent communication (A2A-style protocols), briefly.

**B. Humans in the loop**
- Interrupt and approve: pausing a graph for a human decision.
- Time travel: rewinding state to debug or branch.
- Designing approval points: what needs a human, and alert fatigue.

**Demo:** planner/writer/verifier agents on a dataset task; an approval interrupt before a consequential action; rewind and branch.
**Figures:** topology gallery; the interrupt/resume sequence.
**Arc C** (team) begins.

---

## Block 4 · The production frontier

### W10 · LLMOps: evaluation & observability
**A. Testing non-deterministic systems**
- Why unit tests aren't enough; what is still deterministic (schemas, routing, retrieval).
- Golden sets, reference-free metrics, LLM-as-judge (G-Eval-style rubrics).
- Calibrating a judge against human labels, and judge biases (position, verbosity, self-preference).
- Regression testing across prompt and model versions in CI.

**B. Observability & cost control**
- Tracing: spans per LLM and tool call (OpenTelemetry, Langfuse/LangSmith).
- Latency distributions (p50/p95/p99), token velocity, per-request cost.
- Cost levers: prompt caching, semantic caching, batching, model-tier routing (the cost thread pays off).

**Demo:** trace the spine end to end; run the eval suite against two prompt versions; route easy queries to a cheap model and show cost vs. quality.
**Figures:** a trace waterfall; judge calibration plot; cost/quality frontier.
**Grad:** benchmarking methodology for the final report comes from this deck.

### W11 · Responsible AI: bias, harm & hallucination
**A. Measuring harm**
- Hallucination vs. groundedness: faithfulness scoring against retrieved context.
- Bias probes: counterfactual substitution, demographic parity checks on application outputs.
- Toxicity classifiers and their own biases.

**B. Beyond the model**
- Data provenance and licensing; what "trained on" means for an application.
- Socioeconomic impact of agentic automation: who the app replaces, who it serves.
- Harm evals as part of the W10 suite, not a separate audit.

**Demo:** counterfactual sweep over the spine; groundedness scores on answers with and without retrieval.
**Figures:** a bias sweep heatmap; faithfulness scoring diagram.

### W12 · Application security & guardrails
**A. Attacks**
- Direct prompt injection; indirect injection via retrieved documents (poison the dataset live).
- System-prompt exfiltration, data exfiltration through tool calls.
- OWASP Top 10 for LLM applications as the map.

**B. Defenses & the exercise**
- Defense in depth: input/output classifiers, privilege separation, tool allow-lists, human approval.
- Why there is no complete fix for injection, and how to design for that.
- Hackathon rules of engagement.

**Demo:** a planted document hijacks the spine's agent; add guardrails; attack again.
**Undergrad:** half B is mostly the team adversarial exercise. Lecture content must fit half A plus a short B.
**Arc C** ends.

---

## Block 5 · Adaptation & scaling

### W13 · Model adaptation: fine-tuning & preference alignment
**A. When to adapt weights**
- Decision framework: prompting vs. RAG vs. fine-tuning (knowledge vs. behavior vs. format).
- PEFT and LoRA: the low-rank update ($W + BA$), why it's cheap, QLoRA.
- Data: instruction formatting, curation, how much is enough; reading loss curves.

**B. Preference alignment**
- RLHF pipeline at a conceptual level (reward model, PPO).
- DPO: the objective without a reward model; preference pairs.
- When alignment matters for an application, and when it's overkill.

**Demo:** LoRA fine-tune a small open model on dataset-formatted examples (Colab-sized); before/after on held-out prompts.
**Figures:** LoRA decomposition; RLHF vs. DPO pipelines; decision tree.

### W14 · Enterprise scaling: local serving & hybrid infrastructure
**A. Serving open-weights models**
- Why go local: privacy, cost at volume, control, latency.
- Inference mechanics: KV cache, continuous batching, PagedAttention, quantization.
- Serving stacks (vLLM, Ollama) and choosing a model size for the hardware.

**B. Hybrid architectures & wrap-up**
- Routing private data to local models, hard cases to cloud.
- Migrating the spine to a local backend through the W1 gateway: one config change.
- Course synthesis: the whole architecture on one slide.

**Demo:** the spine running on a local model; the same eval suite from W10; compare quality, cost and latency.
**Figures:** KV cache and batching diagram; hybrid routing architecture; the full spine architecture.

---

## Grad seed readings

Candidates to seed the paper list, not final.

| Week | Papers |
|---|---|
| W2 | DSPy (Khattab et al., 2023) |
| W3 | Constrained decoding / grammar-based generation (e.g., Outlines, Willard & Louf, 2023) |
| W4 | RAG (Lewis et al., 2020); Lost in the Middle (Liu et al., 2023) |
| W5 | ColBERT (Khattab & Zaharia, 2020); Reciprocal Rank Fusion (Cormack et al., 2009) |
| W6 | ColPali (Faysse et al., 2024); Whisper (Radford et al., 2022) |
| W7 | Chain-of-Thought (Wei et al., 2022); ReAct (Yao et al., 2022); Toolformer (Schick et al., 2023) |
| W8–9 | Reflexion (Shinn et al., 2023); AutoGen (Wu et al., 2023) |
| W10 | G-Eval (Liu et al., 2023); Judging LLM-as-a-Judge (Zheng et al., 2023) |
| W11 | Stochastic Parrots (Bender et al., 2021); Red Teaming LMs with LMs (Perez et al., 2022) |
| W12 | Indirect Prompt Injection (Greshake et al., 2023) |
| W13 | LoRA (Hu et al., 2021); QLoRA (Dettmers et al., 2023); InstructGPT (Ouyang et al., 2022); DPO (Rafailov et al., 2023) |
| W14 | vLLM / PagedAttention (Kwon et al., 2023) |

---

## Open questions

1. **Midterm vs. Week 7.** If the undergrad midterm takes a session in Week 7, undergrads lose half of W07. Options:
   - move the midterm to Week 8 and make W08B lighter
   - make W07 a one-half deck
   - hold the exam outside class
2. **Grad paper presentations.** Do they happen in class? With one grad session a week, every presentation slot takes lecture time from that session.
3. **Guest lecture slot.** Which week? W09 (multi-agent) or W14 (industry deployment) fit best. It needs a fallback deck either way.
4. **MCP and A2A** are absent from the syllabus. MCP is in W07 here; add it to the syllabus edit task?
5. **Dataset** still TBD; it blocks W04 onward.
6. **Hackathon in W12:** half B for undergrad; what does grad do with the equivalent time?
