---
name: red-team-llm-app
description: Use this to adversarially test an LLM/agent app before attackers do - prompt injection, jailbreaks, data exfiltration, tool misuse, and unsafe output. Trigger on "red team my LLM", "test for prompt injection", "is my agent secure", "jailbreak testing", "security review of my AI app", especially before shipping anything customer-facing or with tools/data access. Test systematically against the known attack classes, not ad-hoc.
license: CC0-1.0
---

# Red-team an LLM app

Red-teaming is structured adversarial testing: try to make the app misbehave, on purpose, so you find the holes before users or attackers do. Cover the known attack classes systematically rather than trying a few clever prompts.

## Why LLM apps are attackable

LLMs process instructions and data in the **same channel** with no hard separation, so an attacker can smuggle input the model treats as a new instruction. That single property is behind most of the attack classes below, and it is why "just prompt it not to" is not a real defense.

## Test these attack classes (OWASP LLM Top 10, prioritized)

1. **Direct prompt injection** - user input that overrides the system prompt ("ignore previous instructions and..."). The #1 risk.
2. **Indirect prompt injection** - malicious instructions hidden in *retrieved* content (a web page, PDF, email, RAG doc) that the model then follows. The dangerous one for agents with tools/browsing.
3. **Jailbreaks** - roleplay/obfuscation/encoding tricks to bypass safety ("you are DAN", base64, translation).
4. **Sensitive data disclosure** - getting the model to leak the system prompt, secrets, other users' data, or PII.
5. **Excessive agency / tool misuse** - tricking an agent into calling tools destructively (delete, transfer, email) or with attacker-chosen args.
6. **Output-handling exploits** - model output that becomes an injection downstream (XSS/SQL if you render or execute it unsanitized).

## How to run it

1. **Build an attack set** per class above (start from a public jailbreak/injection dataset, add app-specific ones). Version it in the repo.
2. **Automate it** - run the attack set as an eval suite. Tools: [promptfoo](https://github.com/promptfoo/promptfoo) (built-in red-team/`redteam` mode), [DeepTeam](https://github.com/confident-ai/deepteam), [garak](https://github.com/NVIDIA/garak), [PyRIT](https://github.com/Azure/PyRIT).
3. **Score with a judge** - did the attack succeed (leaked/obeyed/mis-tooled)? An LLM-as-judge grades each attempt; measure attack success rate per class.
4. **Gate in CI** - fail the build if attack success rate rises. Re-run after every prompt/model change (model updates can regress safety).

## Fix what you find (defense in depth)

No single fix is enough; layer them. Add **input + output guardrails** (see `add-llm-guardrails`), separate untrusted content from instructions, least-privilege tools with human-in-the-loop for destructive actions, and sanitize output before rendering/executing. Then **observe** attack attempts in production (see `add-llm-guardrails` telemetry) so you see when injection attempts rise.

## Verify

- Every attack class has at least a handful of test cases.
- The suite runs in CI and reports attack success rate per class.
- A known injection string that used to succeed now fails after your fix.

## Anti-patterns

- Testing only direct injection, ignoring indirect (the real risk for tool-using agents).
- "The system prompt says don't reveal secrets" as your only defense.
- One-time manual red-team, never re-run - a model upgrade silently regresses safety.
- Giving an agent broad tool access with no human gate on destructive actions.

## Grounding

Attack taxonomy: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (prompt injection is LLM01). Automated attacks: *Automatic and Universal Prompt Injection Attacks against LLMs* ([arXiv:2403.04957](https://arxiv.org/abs/2403.04957)). LLM cyber-risk evaluation: Meta *CyberSecEval 3* ([arXiv:2408.01605](https://arxiv.org/abs/2408.01605)).
