# Research Notes

Checked 2026-11-06. These notes record what already exists on multi-agent systems teaching and evidence, what the credible sources actually claim (with the numbers as reported, never rounded into stronger claims), and the gap this course fills. Framework and tool statements are dated 2026-11-06 and should be re-checked before being quoted later.

## The gap this course fills

As of 2026-11-06, multi-agent teaching splits into three camps, and none of them does what a builder most needs:

- **Framework courses and docs** (LangGraph, CrewAI, AutoGen, Microsoft Agent Framework) teach an API well, but the coordination claims are the framework's own, the examples need hosted models or keys, and the failure and cost behaviour of the student's own design is never measured.
- **General agent courses** (Microsoft's AI Agents for Beginners, Hugging Face's Agents Course) give multi-agent one or two lessons inside a broader syllabus, with hosted-model notebooks.
- **The research literature** (Anthropic's production write-up, Google's scaling study, the MAST failure taxonomy) reports strong, sometimes contradictory findings, but ships no runnable course a builder can reproduce the trade-offs with.

No existing offering found combines: a complete free course on coordination itself, framework-free and offline, deterministic stand-ins instead of API keys, every design claim measured by bundled code on bundled fixtures, an honest lesson where multi-agent loses, and a capstone graded against gates fixed in writing before the build. That combination is this course.

## What exists (checked 2026-11-06)

### Courses and structured teaching

- **Microsoft, AI Agents for Beginners**: 18 lessons; multi-agent design patterns appear in one lesson. Strong breadth, Azure-oriented tooling, hosted models. This course goes deep where that one goes wide.
- **LangChain Academy, Introduction to LangGraph**: dozens of short lessons covering multi-agent patterns (subgraphs, handoffs, router patterns) inside one framework. Framework fluency is its goal; framework independence is this course's.
- **Hugging Face, Agents Course**: a free community course with a multi-agent and multi-agent-system unit; smolagents-centric, hosted models.
- **freeCodeCamp, LangGraph, MCP, A2A and Ollama book/course (2025)**: a project-based tour of the current stack; tooling-first.
- **AI Engineering from Scratch**: a large phases-based curriculum including a multi-agent systems phase (around 25 lessons, Python and TypeScript). Build-from-scratch comparisons are the closest neighbour in spirit; this course differs by pricing every architecture on one shared fixture set and by the gated capstone.
- **IBM, AI Agents specialisation (Coursera)**: a multi-course series including multi-agent content; paid certificates, framework notebooks.
- **CrewAI and AutoGen documentation and examples**: the practical canon for role-based crews and conversational agents; vendor material by definition.

### Frameworks and protocols (state as of 2026-11-06)

- **AutoGen** (Microsoft Research; Wu et al. 2023, arXiv:2308.08155): conversational multi-agent framework; the reference for agent-to-agent message passing patterns.
- **MetaGPT** (Hong et al. 2023, arXiv:2308.00352): role-specialised software company simulation with a shared message pool; the blackboard pattern's modern reference.
- **LangGraph** (LangChain): graph-structured agent orchestration, stateful by design; handoffs and subgraphs are first-class.
- **CrewAI**: role, goal, and backstory crews; process types (sequential, hierarchical) map directly onto this course's Module 2 vocabulary.
- **OpenAI Swarm** (October 2024, experimental): routines and handoffs as the minimal multi-agent vocabulary; superseded in spirit by the Agents SDK, still the clearest teaching artifact for handoffs.
- **Agent2Agent (A2A) protocol** (Google, announced April 2025): interoperability between agents built by different teams; the standardisation direction for the message schemas of Module 3.
- **Model Context Protocol (MCP)**: the tool and context interface layer; adjacent to this course (see the companion Build MCP Servers course), not its subject.
- **Microsoft Agent Framework**: Microsoft's unified agent framework, reported at a 1.0 release in secondary coverage in 2025; treated here as the enterprise framework reference point, with version claims deliberately kept soft.

## Evidence the course teaches from (figures as reported by their sources)

- **Anthropic, "How we built our multi-agent research system" (June 2025)**: a lead agent (Muse) with Sonnet 4 subagents outperformed a single Opus 4 agent by 90.2 percent on their internal research evaluation. Token usage alone explained 80 percent of the performance variance on BrowseComp, rising to 95 percent with tool-call counts and model choice. Agents use about 4x more tokens than chat interactions; multi-agent systems about 15x. Subagents returned condensed summaries of 1,000 to 2,000 tokens. Parallel subagents cut research time by up to 90 percent on complex queries. The course teaches both halves of this: the gain, and the 15x.
- **Kim, Y. et al., "Towards a Science of Scaling Agent Systems" (Google, December 2025, arXiv:2512.08296)**: 180 configurations across five canonical architectures, three model families, four benchmarks. A centralised architecture improved parallelisable financial reasoning by 80.8 percent over a single agent, while every multi-agent variant degraded sequential reasoning performance by 39 to 70 percent. Independent agents amplified errors 17.2x; a centralised architecture contained amplification to 4.4x. Coordination gains saturated once single-agent baselines passed roughly 45 percent, and a predictive model of the optimal strategy (R-squared 0.524) predicted the best configuration for 87 percent of held-out setups. Lessons 05, 20, 25, and 26 are built around these findings, reproduced at stand-in scale.
- **Cemri, M. et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST, NeurIPS 2025 workshop track, arXiv:2503.13657)**: 1,642 annotated execution traces across seven frameworks; failure rates from 41 to 86.7 percent. Three categories: specification and system design (44.2 percent of failures, including step repetition 15.7 percent, unaware of termination conditions 12.4 percent, disobedience of task specification 11.8 percent), inter-agent misalignment (32.3 percent, including reasoning-action mismatch 13.2 percent), and task verification (23.5 percent, including incorrect verification 9.1 percent). Inter-annotator agreement kappa 0.88. Adding a verification step to a ChatDev configuration improved its success rate by 15.6 points. Lesson 28 profiles the course's own failures in this taxonomy.
- **Cognition, "Don't Build Multi-Agents" (June 2025)**: a widely discussed practitioner counterpoint arguing for shared context and against splitting actions across agents with partial views. The course treats it as a design constraint to answer (Lessons 15 and 26), not a slogan to obey or dismiss.

## How the course answers the evidence

- Every architecture the literature argues about is implemented once, in `mas/systems.py`, and priced on the same twelve-order fixture set, so the arguments become measurements (Lessons 06 to 13, 24).
- The sequential penalty, error amplification, and verification effects from the papers are reproduced at stand-in scale and reported whether or not they flatter multi-agent designs (Lessons 05, 17, 20, 21).
- The capstone's gates are set from the course's own baseline measurements, fixed in a dated file before the build, and the failed first verdict is printed, mirroring the literature's standard that negative results are results (Lessons 29 to 31).

## Sources

- Anthropic engineering blog, "How we built our multi-agent research system", June 2025. anthropic.com/engineering/multi-agent-research-system
- Kim, Y. et al., arXiv:2512.08296, December 2025.
- Cemri, M. et al., arXiv:2503.13657, March 2025 (NeurIPS 2025 Datasets and Benchmarks track).
- Wu, Q. et al., arXiv:2308.08155 (AutoGen). Hong, S. et al., arXiv:2308.00352 (MetaGPT).
- Cognition engineering blog, "Don't Build Multi-Agents", June 2025.
- OpenAI Swarm repository (experimental), October 2024. Google A2A announcement, April 2025.
- Microsoft AI Agents for Beginners repository; LangChain Academy; Hugging Face Agents Course; framework documentation for LangGraph, CrewAI, AutoGen (all checked 2026-11-06).
