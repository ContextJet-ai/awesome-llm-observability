---
name: monitor-rag-quality
description: Use this to measure and monitor the quality of a RAG (retrieval-augmented generation) pipeline - whether it retrieves the right context and answers faithfully. Trigger on "my RAG gives wrong answers", "is my retrieval any good", "the chatbot makes things up", "evaluate my RAG", "improve RAG accuracy". Diagnose whether the failure is in retrieval or generation - they need different fixes.
license: CC0-1.0
---

# Monitor & improve RAG quality

Most "the LLM is wrong" bugs in a RAG app are actually **retrieval** bugs - the model was handed the wrong context and did its best. Measure both halves separately.

## The 4 metrics that matter (RAG quartet)

| Metric | Question | Which half |
|---|---|---|
| **Context precision** | Are the retrieved chunks relevant (not noise)? | Retrieval |
| **Context recall** | Did retrieval find *all* the needed info? | Retrieval |
| **Faithfulness** | Is the answer grounded in the retrieved context (no made-up facts)? | Generation |
| **Answer relevance** | Does the answer actually address the question? | Generation |

[Ragas](https://github.com/vibrantlabsai/ragas) implements all four; [DeepEval](https://github.com/confident-ai/deepeval) and most observability platforms (Langfuse, Phoenix, Opik) have RAG evaluators too.

## Diagnose: retrieval vs generation

Read a failing trace (see `debug-agent-from-traces`):

- **Low context recall/precision** → fix **retrieval**: chunking strategy, embedding model, top-k, reranking, query rewriting, metadata filters. No amount of prompt tuning fixes missing context.
- **Good context but low faithfulness** → fix **generation**: prompt the model to answer *only* from context, add a groundedness guardrail, lower temperature, cite sources.
- **Good context, hallucinates anyway** → the model is ignoring context: tighten the prompt, or the context is too long and it's getting lost ("lost in the middle").

## Set it up

1. **Build a small RAG eval set** - 20-50 {question, ground-truth answer, ideal source docs} from real usage. Version it.
2. **Score offline in CI** with the RAG quartet; set thresholds (e.g. faithfulness ≥ 0.8) that fail the build on regression.
3. **Score online** - sample production traffic and run faithfulness + answer-relevance as LLM-as-a-judge on live traces; alert on drops.
4. **Log retrieval details** in traces - query, retrieved doc IDs + scores - so every failure is diagnosable after the fact.

## Verify

- Intentionally remove a needed doc from the index → context recall drops (proves the metric works).
- Intentionally prompt the model to ignore context → faithfulness drops.
- A dashboard shows the four metrics over time with alert thresholds.

## Anti-patterns

- "Improving the prompt" when the real problem is retrieval returning garbage.
- Only measuring the final answer, never the retrieved context (you can't tell which half failed).
- Increasing top-k to "get more context" → adds noise, hurts precision, raises cost.
- No RAG eval set → every change is a vibe, regressions ship silently.
