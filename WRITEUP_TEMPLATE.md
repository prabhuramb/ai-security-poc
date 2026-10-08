# EXHIBIT 23.6 — AI SECURITY VALIDATION: DEMONSTRATED PROOF-OF-CONCEPT

Author: Prabhuram Balaraman
Status: Demonstrated proof-of-concept, self-built and self-measured
[not part of any employer engagement -- confirm and state this]
Extends: The taxonomy specified at Exhibit 23.3 and the governance pattern
at Exhibit 23.4
Supports: Section IV.C of the Brief in Support of Petition (proposed
endeavor, component two)

## 1. Summary

[One paragraph: what you built, what it demonstrates, one-sentence result.
Mirror the tone of Exhibit 23.1 Part A.1 -- plain, factual, no adjectives
doing the work of the numbers.]

## 2. Purpose and scope

Exhibit 23.3 specified a taxonomy of AI security risk categories in the
abstract. To test whether that taxonomy translates into a working validation
method rather than remaining a paper design, I built a small demonstration
system and ran the taxonomy's test techniques against it.

This proof-of-concept is intentionally narrow in scope: [state exactly which
1-2 taxonomy categories you tested -- e.g., "prompt injection and instruction
override" and "sensitive information disclosure"]. It is not a claim to have
validated the full taxonomy, and I do not present it as one.

## 3. System under test

[Describe the toy HR assistant in your own words: what it does, what data
it has access to, that all data is synthetic and self-created for this
demonstration, containing no employer or client information.]

## 4. Method

[Describe, in your own words: the baseline vs. hardened comparison, what the
hardened configuration actually adds (system-prompt rule + output filter),
and that the same 7 test cases were run against both.]

## 5. Measured outcomes

[Insert your actual results.json numbers here as a table, in the same
format as Exhibit 23.1's Measured Outcomes tables, e.g.:]

| Measure | Baseline (unprotected) | Hardened (control added) |
|---|---|---|
| Adversarial cases resulting in disclosure of synthetic confidential data | [X] of 5 | [Y] of 5 |
| Benign control cases incorrectly blocked | [X] of 2 | [Y] of 2 |

## 6. Basis of the figures, and what they do not establish

[This section matters most -- it's what made Exhibit 23.1 credible. Be
explicit and conservative, e.g.:]

- These figures come from a single run [or: the runs on DATE(S)] of a
  self-built demonstration system, not a production environment.
- The system contains only synthetic data I created for this purpose. No
  employer or client data, code, or configuration appears anywhere in this
  exhibit.
- The output filter is a simple pattern-match against known synthetic
  values, described in full at [file/section]. I make no claim that this
  mechanism would generalize to unknown or differently-formatted sensitive
  data without further engineering.
- [State plainly if any run was inconsistent, or if you re-ran anything,
  and why.]
- I am not able to submit [nothing here, actually -- unlike the employer
  engagements, all code and results ARE submittable, since this is your own
  standalone work. Consider attaching the actual code files and results.json
  as sub-exhibits, the way Figure 1/2 were attached as diagrams.]

## 7. Relevance to the proposed endeavor

[Tie back explicitly: this demonstrates that the design specified at Exhibit
23.3 can be operationalized and produces a measurable before/after result,
using the same evidentiary discipline (stated baseline, stated result,
stated basis) as the non-AI work at Exhibit 23.1. State plainly that this
remains a small-scale demonstration, not a production deployment, and that
it establishes feasibility and execution capability rather than
comprehensive security coverage.]
