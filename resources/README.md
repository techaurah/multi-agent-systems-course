# Resources

Print these next to the lessons. Every claim in them traces to the course's fixtures or to a dated source in the root RESEARCH.md.

## The one-page decision card

- Independent, self-contained tasks: run one agent first. Adding agents to independent work buys latency, not quality (Lesson 26: the single agent wins the independent family outright).
- Sequential chains: expect the pipeline to tie the single agent and cost more. Split only where a stage genuinely differs (Lesson 05).
- Error-prone stages: put a check at the exit before adding agents at the entrance. A reviewer took the pipeline from 7 to 10 successes; orchestration matched it for 16.1 percent fewer tokens by reviewing selectively (Lessons 21 and 09).
- Agreement between different methods (debate, Lesson 13) was the only route to 12 of 12 among the unhardened systems, at the highest coordination price.
- Budget by family, not by fleet. The same system is the best and the worst choice depending on which family dominates your workload.

## Reading list (all checked 2026-11-06, see RESEARCH.md)

- Wu, Q. et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155. The framework that popularised conversational multi-agent systems.
- Hong, S. et al. (2023). MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework. arXiv:2308.00352. Role specialisation and shared message pools.
- Anthropic (2025). How we built our multi-agent research system. Engineering blog, June 2025. Production evidence: parallelism and delegation gains, and the 15x token cost stated plainly.
- Kim, Y. et al. (2025). Towards a Science of Scaling Agent Systems. arXiv:2512.08296. 180 controlled configurations; coordination helps parallelisable work and degrades sequential work; error amplification quantified.
- Cemri, M. et al. (2025). Why Do Multi-Agent LLM Systems Fail? arXiv:2503.13657. The MAST taxonomy used in Lesson 28: 1,642 traces, three failure categories.
- Cognition (2025). Don't Build Multi-Agents. Engineering blog, June 2025. The case for shared context and against fragile action-divided agents, from a team that tried both.
- Microsoft. Microsoft Agent Framework documentation; AI Agents for Beginners (18 lessons, one on multi-agent patterns). The framework-bound reference point this course is the offline companion to.
- OpenAI (2024). Swarm (experimental). Routines and handoffs: the minimal vocabulary for agent-to-agent transfer.
- Google (2025). Agent2Agent protocol announcement, April 2025. Interoperability between agents from different builders.

## Glossary

- **Topology**: the shape of who talks to whom: sequential, parallel, hierarchical, debate, blackboard, routed.
- **Coordination overhead**: the messages, tokens, and steps a system spends on organising work rather than doing it, priced by the ledger.
- **Handoff**: the transfer of a task and its state from one agent to another; lossy when the state is summarised into prose.
- **Escape**: a policy-violating output that leaves the system. The safety metric of this course.
- **Cost per success**: total coordination and work tokens divided by successful tasks; the only cost ranking this course trusts.
- **Makespan**: the elapsed steps of a parallel batch, set by the busiest worker.
- **Field check**: a verification pass that re-reads the source when an extraction looks thin; the capstone's hardening.
