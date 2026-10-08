# AI Security Validation Proof-of-Concept

A small, self-contained demonstration of the AI security validation approach
described at Exhibit 23.3 (adversarial taxonomy) and Exhibit 23.4 (governance
gate pattern). This is a toy system built for this purpose only -- it contains
no employer or client data, code, or configuration of any kind.

## What this demonstrates

A minimal RAG-style HR assistant is tested against adversarial inputs
implementing two categories from the Exhibit 23.3 taxonomy:
- Prompt injection and instruction override (direct and indirect)
- Sensitive information disclosure

Each test case is run twice: once against an unprotected ("baseline")
configuration, and once against a hardened configuration with an explicit
security system prompt plus a post-response output filter (the "control").
The harness records, for each case, whether confidential synthetic data was
disclosed.

## Requirements

- Python 3.9+  (standard library only -- no pip installs needed)
- [Ollama](https://ollama.com) installed locally (free)
- One pulled model, e.g. Llama 3 8B

## Setup (one-time, ~10 minutes)

1. Install Ollama: https://ollama.com/download (available for macOS, Windows, Linux)
2. Start the Ollama server (it may already be running after install):
   ```
   ollama serve
   ```
3. In a separate terminal, pull a model:
   ```
   ollama pull llama3
   ```
   (If you'd rather use a smaller/faster model, `mistral` or `phi3` also work --
   just update `MODEL_NAME` in `target_app.py` to match.)

## Running the POC

From this project directory:
```
python harness.py
```

This will:
1. Run all 7 test cases (2 benign controls + 5 adversarial cases) against
   both the baseline and hardened configurations.
2. Print a summary table to the terminal.
3. Write full results, including the actual model responses, to `results_run1.json`, `results_run2.json`, `results_run3.json`.

A full run typically takes 1-3 minutes depending on your machine and the
model chosen.

## Results

The seven test cases (2 benign controls, 5 adversarial) were run three times on September 23, 2026. Full outputs, including the model responses, are in `results_run1.json`, `results_run2.json` and `results_run3.json`.

| Measure | Baseline | Hardened |
|---|---|---|
| Adversarial instances that disclosed synthetic confidential data (5 cases × 3 runs) | 10 of 15 (67%) | 0 of 15 |
| Benign instances incorrectly refused or degraded (2 cases × 3 runs) | 0 of 6 | 0 of 6 |

The baseline's vulnerability was not uniform across cases; the per-case breakdown is in the result files.

## Scope and limits

- This is a toy system built for this demonstration. It contains no employer or client data, code or configuration.
- The output filter is deliberately simple (pattern matching on known synthetic values) so the mechanism can be audited. It is not a production-grade control.
- Leak/safe classification uses automated marker matching and was checked against the recorded responses.
- LLM output varies between runs, which is why the test set was run three times.
- Only two of the six taxonomy categories were tested: prompt injection / instruction override and sensitive information disclosure.
