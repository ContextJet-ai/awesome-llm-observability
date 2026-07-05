---
name: annotate-traces-for-review
description: Use this to set up human review and annotation of LLM traces, so people (often domain experts) can label outputs, do error analysis, and build a trustworthy golden dataset. Trigger on "review my LLM outputs", "have an expert label these", "error analysis", "annotate traces", "build a golden dataset", or when automated evals are not enough for a high-stakes or specialized domain. Looking at your data is the highest-ROI thing you can do.
license: CC0-1.0
---

# Annotate and review traces

Automated metrics are downstream of one thing: a human deciding what "good" means. For specialized or high-stakes domains (finance, health, legal), and for early-stage apps, structured human review of real traces is the single highest-ROI activity. It produces the golden labels every other eval depends on, and it surfaces failure modes you did not know to look for.

## Set up the review loop

1. **Pull a sample of traces** to review. Stratify (by topic, difficulty, low online-eval score, thumbs-down) so reviewers see the interesting cases, not 100 easy ones.
2. **Give reviewers the full context** the model had: input, retrieved docs, tool results, output. Redact PII first for regulated data (`redact-pii-for-tracing`).
3. **Use a simple, consistent schema:** pass/fail (or a small rubric score) + a **free-text failure reason** + a category tag. The free-text is where you discover new failure modes; the categories let you count them.
4. **Use the tooling** rather than spreadsheets where possible: annotation queues exist in Langfuse, Phoenix, Opik, LangSmith and let annotations attach to the trace.

## Do error analysis (not just labeling)

The point is not a score, it is understanding. After a review pass:
- **Read the free-text reasons and cluster them** into failure categories (retrieval miss, hallucination, formatting, refusal, tone, ...). Count each.
- **Fix the biggest category first.** A few categories usually explain most failures.
- This is the loop that turns "the app is kind of bad" into "34% of failures are retrieval misses, here is the fix."

## Turn reviews into durable assets

- Reviewed pass/fail labels become your **golden eval dataset** (`build-eval-dataset`) and regression cases (`trace-based-testing`).
- Reviewed labels also **calibrate your LLM-as-judge**: check the automated judge agrees with the humans; fix the rubric until it does (`add-llm-evals`). Then the judge can scale what humans validated.

## Verify

- Reviewers see full context and use a consistent schema.
- Failure reasons are clustered into categories with counts, not just an average score.
- Reviewed items feed the eval set and calibrate the automated judge.

## Anti-patterns

- Never looking at your actual data, only at aggregate metrics (you miss the failure modes).
- Reviewing without the retrieved context/tool results (you cannot tell why it failed).
- Pass/fail with no reason text (you get a number, not an insight).
- Labels that never become an eval set or judge calibration (wasted expert time).

## Grounding

"Look at your data" and error analysis are the core of practitioner eval methodology: Hamel Husain, [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/); human labels are the ground truth that automated LLM-as-a-judge is calibrated against (Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)).
