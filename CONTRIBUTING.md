# Contributing

Thanks for helping keep this list high-quality and trustworthy.

## What gets listed

The list is only useful if it's shorter than the search results. A few things have to be true
before an entry earns a row:

- **Open source / open-core** - at least **250 GitHub stars**, and a commit in the last 6 months.
  Below that, or dormant, it's too early for a curated list. Projects from a recognized lab or
  organization are judged on the work rather than the star count.
- **Commercial (no public repo)** - the product has to be publicly verifiable: real documentation
  plus either self-serve signup or a published pricing page. Demo-request-only pages aren't
  something a reader can evaluate, so they don't get a row yet.
- **Clean links** - the URL points at the docs or the repo, with no `utm_*`, referral, or
  affiliate parameters attached.
- **In scope** - it does LLM/agent observability, evaluation, prompt management, gateways,
  instrumentation, or guardrails. Adjacent tooling with no tracing or eval story is a good
  project in the wrong list.

Falling short today isn't a permanent no - come back when the project clears the bar and the
entry is welcome.

## Adding a tool

Open a pull request that adds one entry to the most appropriate section, as a table row:

```
| <marker> [Name](https://link) | ⭐ | License | One-line neutral description. |
```

- **Marker**: `🟢` open-source · `🔵` open-core/hybrid · `🟠` commercial (public repo is an SDK/client only).
- **Description**: factual and neutral - no marketing language, no superlatives.
- **Placement**: pick the single best-fit category; don't list the same tool in multiple sections (cross-reference in prose instead).
- **Ordering**: within a section, keep roughly descending by GitHub stars.
- Verify the link works and the tool is real and maintained. A wrong entry or dead link discredits the whole list.

## Guidelines

- One tool per PR keeps review easy.
- Self-promotion is fine **if** you disclose it in the PR, the tool clears the bar above, and the
  description stays neutral.
- Removing dead/abandoned projects is a welcome contribution too.
