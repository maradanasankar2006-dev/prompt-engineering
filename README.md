# Prompt Engineering Mastery Lab

Python scripts for running real Gemini API experiments on prompting strategies,
math reasoning, and structured JSON extraction. The scripts save raw Gemini
responses, record errors without substituting mock data, and regenerate a
Markdown report after every run.

## Setup

1. Use Python 3.10 or newer. This project was validated with Python 3.13 x64.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Configure the API key without putting it in source control. Either set the
   `GEMINI_API_KEY` environment variable or copy `.env.example` to `.env` and
   replace the placeholder with your key.

## Run experiments

Run all three experiments in sequence:

```powershell
python -m experiments.run_all
```

Or run one experiment:

```powershell
python -m experiments.zero_shot_few_shot
python -m experiments.math_reasoning
python -m experiments.structured_output
```

The configured model is `gemini-2.5-flash`. Each run is appended to its result
JSON file under `results/`, including prompts, raw outputs, validation results,
and failures. Rerunning creates a new run instead of silently replacing earlier
records. The report at `reports/final_experiment_report.md` is regenerated from
the latest saved run for each experiment.

If the key is missing, the scripts record a blocked run and print instructions
for configuring it. No API output is fabricated; after fixing the configuration,
rerun the experiment(s) to collect actual results.

On this machine, dependency installation was not successful with Python 3.15
ARM64 because a compatible `cryptography` wheel was unavailable and the MSVC
linker was not installed. Python 3.13 x64 has the required dependencies and was
used for validation.
