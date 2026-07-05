# Hallucination detection methods - how they work

| Method | Needs | How it works | Cost | Best for |
|---|---|---|---|---|
| **NLI / entailment** | retrieved context | Run each answer sentence vs context through an entailment model; not-entailed = unsupported | Low (small model) | RAG faithfulness |
| **LLM-as-a-judge** | context or a rubric | Ask a strong model to list unsupported/unverifiable claims | Medium (1 extra call) | RAG + open-ended, fast to ship |
| **Self-consistency (SelfCheckGPT)** | nothing (sampling) | Sample N answers; measure agreement (NLI, n-gram, or QA); high disagreement = hallucination | High (N samples) | reference-free QA/generation |
| **Semantic entropy** | nothing (sampling) | Sample N answers; cluster by bidirectional entailment (meaning, not tokens); entropy over clusters | High (N samples + clustering) | state-of-the-art reference-free |
| **Token log-probs / uncertainty** | model logprobs | Low-probability tokens correlate weakly with hallucination | ~Free | a feature to combine, not standalone |

## Notes

- **Consistency methods need sampling** (temperature > 0, N in the 5-10 range). They do not work on a single deterministic output.
- **Semantic entropy vs raw self-consistency:** raw string agreement penalizes wording differences ("Paris" vs "the capital, Paris"). Semantic entropy clusters by meaning first, so it isolates *factual* uncertainty. That is why it detects better, at the cost of the clustering step.
- **Latency:** inline sampling of N answers multiplies latency by ~N. For real-time flows, prefer a single LLM-as-judge or NLI pass; reserve sampling methods for offline/async scoring or high-stakes answers.

## Libraries

- Faithfulness / RAG: [Ragas](https://github.com/vibrantlabsai/ragas), [DeepEval](https://github.com/confident-ai/deepeval) (both have faithfulness + hallucination metrics).
- LLM-as-judge: built into most observability platforms (Langfuse, Phoenix, Opik, Braintrust).
- SelfCheckGPT: reference implementation exists on GitHub (`potsawee/selfcheckgpt`).
- Semantic entropy: reference code from the Oxford OATML group (see the Nature paper's linked repo).
