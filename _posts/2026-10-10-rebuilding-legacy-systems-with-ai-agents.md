---
title: "Rebuilding Legacy Systems with AI Agents: Verification That Assumes the Agent Cheats"
subtitle: "Agents leave requirements out and work on the tests. What the studies measured, and the test design that follows from it."
tags: AI agents, legacy modernization, testing, software development
categories: software
layout: post
language: en
author: Jens Laufer
og_image: /assets/img/legacy-rebuild-ai-agents-og.png
---

*Deutsche Version: [Legacy-Systeme mit KI-Agenten neu bauen](/software/legacy-systeme-mit-ki-agenten-neu-bauen.html)*

I run an autonomous coding pipeline for my own company every day. Agents pick up tickets, implement them on a branch, and separate tests decide whether the result holds. I have [documented 138 ways this system broke](/entrepreneurship/138-fehlschlaege.html) (German). One of them: a ticket said in bold "Do not add: blog articles". The agent added two and logged that it had decided to override the ticket's scope boundary.

That is a small system. I wanted to know what happens when agents rebuild a large legacy business system, an ERP for example. I have not led such a rebuild. I drafted a method from the studies. Then an AI research agent that had not seen my draft researched current practice, and a third agent compared the two. This post covers what the evidence says and the verification design that follows.

### Agents omit more than they invent

A rebuild starts with recovering what the old system does. LLMs read code well, so it is tempting to let them write the requirements.

[UCRBench](https://arxiv.org/abs/2512.13360) measured this on 9 Java projects of up to about 66,000 lines with 556 use cases. The models missed 26–43 % of use cases at subfunction level and 44–65 % at user-goal level. They did worst on domain-specific systems spread over many modules. A vendor's ERP is usually far larger than 66,000 lines and spread over many modules.

A [2026 case study](https://arxiv.org/abs/2608.28972) had Claude Code migrate 12 features of a VB6 ERP to C#. Behavioral equivalence with the old system was 92 % for simple features, 81 % for medium and 47 % for complex ones. Only two features were complex, so the last number rests on little data. The abstract reports 70 %, weighted by instructions; the unweighted per-feature averages are 84 % for persistence, 76 % for business rules and 80 % overall. The failure counts are clearer than the averages: 42 missing adjacent modules, 22 missing database operations, 20 missing rules, 10 missing module integrations, 6 wrong implementations. UI-event validations, implicit filters and global configuration are discussed in the paper but not tallied separately.

94 of the 100 counted failures are something missing; 6 are wrong implementations. The code that is there looks complete, and a reviewer reading it cannot see what is absent. Omissions show up only when you measure recall against a set you built without the model.

### Agents work on the tests

The second job is to prove that the new code behaves like the old. The usual answer is tests. The evidence says the agent will optimize against those too.

[ImpossibleBench](https://arxiv.org/abs/2510.20270) builds tasks whose tests contradict the specification, so every pass is cheating. On the two SWE-bench variants, GPT-5 cheated on 76 % and 54 % of tasks (under 3 % on LiveCodeBench). Claude Opus 4.1 cheated on about 50 % of the conflicting variant, under a strict prompt. Claude models and Qwen3-Coder cheated mostly by editing tests (over 79 %, a lower bound). Other strategies: special-casing test inputs, overloading comparison operators, recording state between calls.

The countermeasures helped in part. Read-only tests stopped the test edits but not the special-casing. Hiding the tests cut cheating to near zero and also hurt legitimate solutions. LLM monitors caught 86–89 % of cheating on simple tasks and 42–65 % on SWE-bench-style tasks.

Honest passes are weaker than they look. [METR](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) had four maintainers of scikit-learn, Sphinx and pytest review 296 agent PRs that passed the SWE-bench Verified tests. After adjusting for how often maintainers merge the reference solution, the merge rate sat about 24 points below the pass rate. Limits: one attempt per task, no iteration with feedback, three repositories. [UTBoost](https://arxiv.org/abs/2506.09289) found 345 wrong patches that the original SWE-bench marked as passing. [SWE-ABS](https://icml.cc/virtual/2026/poster/62669) finds about one in five "solved" patches from top agents semantically wrong.

When a model writes the expected values, it writes down what the code does today. A [study over 24 Java repositories](https://arxiv.org/abs/2410.21136) found that LLM-generated test oracles capture actual instead of expected behavior, with accuracy below 50 % in some settings. In a rebuild, the agent's tests would confirm the agent's code.

My own lesson from the blog-article ticket points the same way. A rule the agent reads is a request. A boundary needs a check that fails.

### A test design that assumes the builder cheats

The verification side of the method starts from two assumptions: the building agent takes every shortcut the setup allows, and it misses things without noticing. Each element answers one of the findings above.

1. Legacy is the specification source. Once the decision is to rebuild, the old code is read for what it computes. Deterministic tools list entry points, tables, batch jobs and configuration. The LLM summarizes one slice of code at a time and cites code for every sentence. It never traces calls across the whole code base.
2. Expected values come only from recorded legacy behavior. A harness runs each case on the legacy system with anonymized production data and stores inputs and outputs. No model writes or edits an expected value. Redesigned processes have no legacy oracle. There, domain experts work out expected values by hand, and invariants such as "balances net to zero" cover the rest.
3. Recordings are immutable. The raw recording is stored unchanged with a content hash. Volatile fields like timestamps are normalized by rules a human approves and code applies. Fields with legal meaning, such as gapless document numbers, stay. Every case replays twice; a different result means hidden state outside the recorded boundary.
4. One human-owned runner. A single data-driven runner reads case files, loads the inputs, runs the process and compares outputs exactly. There is no per-case test code for equivalence. Agent-written comparators tend to grow silent tolerances.
5. Hold-out cases. The builder never sees a share of the cases per process. ImpossibleBench showed that hiding all tests hurts honest work. Hiding a share keeps visible cases for development and catches overfitting to them. I would start with 20–30 %. That number is a judgment call, not a measurement.
6. Protected paths. Runner, comparator, cases, normalization rules, fixtures and CI configuration are protected through CODEOWNERS and a CI check. Any builder diff there fails the build.
7. Mechanical anti-special-casing checks. Read-only tests do not stop special-casing, so the build scans production code for literals taken from visible cases, overridden equality or comparison operators, and state kept between calls. Agent transcripts are kept for audit. I would not tune agents against a monitor: [OpenAI found](https://arxiv.org/abs/2503.11926) that strong optimization against chain-of-thought monitoring teaches models to hide intent. A reviewer agent built on a similar model is a weak substitute, because [model errors correlate](https://arxiv.org/abs/2502.04313).
8. Recall measurement. Per domain, a gold set of processes and rules is built by hand. The metric is what the extracted catalog missed. An error rate alone never sees omissions.
9. Merge rate. A reviewer samples agent changes per wave and decides whether each would be merged as is. That share is tracked next to the pass rate.

Two additions come from the same studies. Equivalence fell to 47 % on complex features, so complex processes are split into smaller units before an agent builds them. And recorded cases can miss branches. The [Locksmith Loop preprint](https://arxiv.org/abs/2607.28271) ran COBOL and generated Java side by side and searched for inputs that reach uncovered branches. It reached 91.9 % branch coverage on one internal program. The authors name intermediate state and floating-point rounding as blind spots.

### What the evidence does not cover

The research I relied on found no published case of agents rebuilding a system at ERP scale end to end. The design above is assembled from partial evidence: a benchmark on projects up to 66,000 lines, one case study with 12 features, and SWE-bench studies on Python libraries. The METR result has not been tested on large business code bases.

In my reading of the sources, the well-measured successes are mechanical migrations such as Java upgrades and test-framework swaps, and results for rebuilding business logic come mostly from vendors, without an independent baseline. Even the mechanical numbers are often estimates: Google reports [about 50 % time saved](https://arxiv.org/abs/2501.06972) for one migration, int32 to int64 IDs, as an engineer estimate.

Automation rate is not time saved. [Slack's tool](https://slack.engineering/balancing-old-tricks-with-new-feats-ai-powered-conversion-from-enzyme-to-react-testing-library-at-slack/) converted about 80 % of the test code correctly in a sample, and the team estimates 22 % of developer time saved. In a [METR trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), experienced developers were 19 % slower with early-2025 tools and believed they were 20 % faster. Cycle times have to be measured; asking the team gives the wrong number.

Results also shift with each model generation. Cheating rates in ImpossibleBench differ by model and by prompt.

### The program around it

Good verification does not decide whether a rebuild succeeds. [The external auditor's public-interest report on Birmingham City Council's Oracle go-live](https://www.birmingham.gov.uk/download/downloads/id/30136/public_interest_report_-_erp_implementation_2025.pdf) names the causes there: weak governance, missing in-house skills, dependence on suppliers, a red risk rating and staff concerns that went unheard, and test reporting that was overly positive in its headlines. Cost overruns across [5,392 IT projects](https://arxiv.org/abs/2210.01573) follow a power law, so small, reversible slices beat one large plan. I cover the business side in a [separate German article on solytics.de](https://solytics.de/blog/altsoftware-mit-ki-agenten-neu-bauen/).

If I started such a rebuild, the first deliverable would be the recording harness and the case runner, owned by a human, before any agent gets write access to production code.
