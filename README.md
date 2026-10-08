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
3. Write full results, including the actual model responses, to `results.json`.

A full run typically takes 1-3 minutes depending on your machine and the
model chosen.

## What to do with the results

1. Open `results.json` and read through the actual responses -- confirm for
   yourself that the leak/safe classifications are correct (the automated
   marker-matching in `harness.py` is a simple safeguard, not a substitute
   for your own review).
2. Fill in `WRITEUP_TEMPLATE.md` with your actual numbers from this run.
3. That completed write-up, together with `results.json`, becomes your new
   sub-exhibit documenting demonstrated (not merely specified) work.

## Honesty notes for the write-up

- This is a toy system built specifically for this demonstration, not a
  production deployment. Say so plainly in the write-up, the same way
  Exhibit 23.1 and 23.2 state their own scope and limits.
- The output-filter logic here is intentionally simple (pattern matching on
  known synthetic values) so that the mechanism is fully auditable. State
  that plainly too -- don't imply it's more sophisticated than it is.
- Run it more than once if a result looks surprising (LLM outputs vary run
  to run). If results are inconsistent, report that honestly rather than
  cherry-picking the run that tells the cleanest story.
