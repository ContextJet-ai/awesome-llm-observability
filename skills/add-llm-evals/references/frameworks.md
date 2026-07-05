# Eval framework quick-starts

## promptfoo (YAML, great for CI)

`promptfooconfig.yaml`:
```yaml
prompts:
  - "Answer using only the context.\n\nContext: {{context}}\nQ: {{question}}"
providers:
  - openai:gpt-4o-mini
tests:
  - vars: { context: "The capital of France is Paris.", question: "Capital of France?" }
    assert:
      - type: contains
        value: "Paris"
      - type: llm-rubric          # LLM-as-a-judge
        value: "answers only from the provided context; no outside facts"
```
Run in CI: `npx promptfoo eval --no-cache` (non-zero exit on failed asserts → gates the build).

## DeepEval (pytest-style)

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

def test_rag_answer():
    tc = LLMTestCase(
        input="Capital of France?",
        actual_output=my_app("Capital of France?"),
        retrieval_context=["The capital of France is Paris."],
    )
    assert_test(tc, [FaithfulnessMetric(threshold=0.8), AnswerRelevancyMetric(threshold=0.7)])
```
Run: `deepeval test run test_rag.py`.

## Ragas (RAG metrics)

Use `faithfulness`, `answer_relevancy`, `context_precision`, `context_recall` over a dataset of {question, answer, contexts, ground_truth}. Good for scoring a whole RAG pipeline offline.
