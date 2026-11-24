import json
import re
from datetime import datetime, timezone
from pathlib import Path

from experiments.common import MODEL_NAME, RESULTS_DIR, ROOT_DIR

REPORT_PATH = ROOT_DIR / "reports" / "final_experiment_report.md"
FILES = {
    "sentiment": ("zero_shot_few_shot_results.json", "Zero-shot vs few-shot"),
    "math": ("math_results.json", "Math reasoning"),
    "structured": ("structured_output_results.json", "Structured output"),
}


def latest_run(key):
    filename, _ = FILES[key]
    path = RESULTS_DIR / filename
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as file:
        document = json.load(file)
    runs = document.get("runs", [])
    return runs[-1] if runs else None


def code_block(value):
    text = "" if value is None else str(value)
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def markdown_cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def status_line(run):
    if run is None:
        return "Not run yet."
    return (
        f"**Status:** {run['status']}  \n"
        f"**Started (UTC):** {run['started_at']}  \n"
        f"**API responses received:** {run['api_calls_succeeded']} / "
        f"{run['api_calls_attempted']} attempted calls"
    )


def sentiment_section(run):
    lines = ["## Experiment 1: Zero-shot vs few-shot sentiment prompting", ""]
    lines.extend([status_line(run), ""])
    if run is None:
        lines.append("No experiment run has been recorded.")
        return lines
    zero_correct = few_correct = 0
    zero_valid = few_valid = 0
    zero_responses = few_responses = 0
    table = [
        "| Review | Expected | Zero-shot label | Zero-shot correct | Few-shot label | Few-shot correct |",
        "|---|---|---|---|---|---|",
    ]
    for entry in run["entries"]:
        zero = entry["zero_shot"]
        few = entry["few_shot"]
        zero_label = zero.get("label", "—")
        few_label = few.get("label", "—")
        zero_responses += int(zero.get("status") in ("succeeded", "invalid"))
        few_responses += int(few.get("status") in ("succeeded", "invalid"))
        zero_valid += int(zero_label in ("Positive", "Negative", "Neutral"))
        few_valid += int(few_label in ("Positive", "Negative", "Neutral"))
        zero_correct += int(zero.get("correct") is True)
        few_correct += int(few.get("correct") is True)
        table.append(
            "| "
            + " | ".join(
                markdown_cell(value)
                for value in (
                    entry["review"],
                    entry["expected"],
                    zero_label,
                    zero.get("correct", "—"),
                    few_label,
                    few.get("correct", "—"),
                )
            )
            + " |"
        )
    total = len(run["entries"])
    zero_accuracy = (
        f"{zero_correct}/{zero_responses}"
        if zero_responses
        else "not measurable (0 responses)"
    )
    few_accuracy = (
        f"{few_correct}/{few_responses}"
        if few_responses
        else "not measurable (0 responses)"
    )
    zero_consistency = (
        f"{zero_valid}/{zero_responses}"
        if zero_responses
        else "not measurable (0 responses)"
    )
    few_consistency = (
        f"{few_valid}/{few_responses}"
        if few_responses
        else "not measurable (0 responses)"
    )
    lines.extend(
        [
            f"**Accuracy among received API responses:** zero-shot {zero_accuracy}; "
            f"few-shot {few_accuracy}.",
            f"**Consistency (valid single-label responses):** zero-shot "
            f"{zero_consistency}; few-shot {few_consistency}.",
            "",
            *table,
            "",
            "### Zero-shot prompts and raw Gemini outputs",
            "",
        ]
    )
    for index, entry in enumerate(run["entries"], 1):
        result = entry["zero_shot"]
        lines.extend(
            [
                f"#### Case {index}",
                "",
                "**Prompt:**",
                "",
                code_block(result.get("prompt")),
                "",
                "**Raw API output:**",
                "",
                code_block(result.get("raw_output", f"Not returned ({result['status']}).")),
                "",
                f"**Status:** {result['status']}",
                "",
            ]
        )
    lines.extend(["### Few-shot prompts and raw Gemini outputs", ""])
    for index, entry in enumerate(run["entries"], 1):
        result = entry["few_shot"]
        lines.extend(
            [
                f"#### Case {index}",
                "",
                "**Prompt:**",
                "",
                code_block(result.get("prompt")),
                "",
                "**Raw API output:**",
                "",
                code_block(result.get("raw_output", f"Not returned ({result['status']}).")),
                "",
                f"**Status:** {result['status']}",
                "",
            ]
        )
    lines.extend(
        [
            "### Comparison",
            "",
            "The table reports exact label matches against the predefined review labels. "
            "Consistency is measured as returning one unambiguous supported label; "
            "this run does not claim repeated-run stability.",
            "",
        ]
    )
    return lines


def math_section(run):
    lines = ["## Experiment 2: Multi-step math reasoning", "", status_line(run), ""]
    if run is None:
        lines.append("No experiment run has been recorded.")
        return lines
    direct_correct = step_correct = 0
    direct_responses = step_responses = 0
    table = [
        "| Problem | Expected | Direct extracted answer | Direct correct | Step-by-step extracted answer | Step-by-step correct |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for entry in run["entries"]:
        direct = entry["direct"]
        step = entry["step_by_step"]
        direct_responses += int(direct.get("status") in ("succeeded", "invalid"))
        step_responses += int(step.get("status") in ("succeeded", "invalid"))
        direct_correct += int(direct.get("correct") is True)
        step_correct += int(step.get("correct") is True)
        table.append(
            "| "
            + " | ".join(
                markdown_cell(value)
                for value in (
                    entry["problem"],
                    entry["expected_answer"],
                    direct.get("extracted_final_answer", "—"),
                    direct.get("correct", "—"),
                    step.get("extracted_final_answer", "—"),
                    step.get("correct", "—"),
                )
            )
            + " |"
        )
    total = len(run["entries"])
    direct_accuracy = (
        f"{direct_correct}/{direct_responses}"
        if direct_responses
        else "not measurable (0 responses)"
    )
    step_accuracy = (
        f"{step_correct}/{step_responses}"
        if step_responses
        else "not measurable (0 responses)"
    )
    lines.extend(
        [
            f"**Accuracy among received API responses:** direct {direct_accuracy}; "
            f"step-by-step {step_accuracy}.",
            "",
            *table,
            "",
        ]
    )
    for label, field in (("Direct", "direct"), ("Step-by-step", "step_by_step")):
        lines.extend([f"### {label} prompts and raw Gemini outputs", ""])
        for index, entry in enumerate(run["entries"], 1):
            result = entry[field]
            lines.extend(
                [
                    f"#### Problem {index}: {entry['problem']}",
                    "",
                    "**Prompt:**",
                    "",
                    code_block(result.get("prompt")),
                    "",
                    "**Raw API output:**",
                    "",
                    code_block(result.get("raw_output", f"Not returned ({result['status']}).")),
                    "",
                    f"**Status:** {result['status']}; independently verified expected answer: "
                    f"{entry['expected_answer']}.",
                    "",
                ]
            )
    return lines


def structured_section(run):
    lines = [
        "## Experiment 3: Structured JSON extraction",
        "",
        status_line(run),
        "",
        "Schema: `{\"name\":\"string\",\"date\":\"string\",\"amount\":\"number\"}`",
        "",
    ]
    if run is None:
        lines.append("No experiment run has been recorded.")
        return lines
    responses = sum(
        entry["status"] in ("succeeded", "invalid") for entry in run["entries"]
    )
    successes = sum(entry["status"] == "succeeded" for entry in run["entries"])
    total = len(run["entries"])
    lines.extend(
        [
            (
                f"**Schema-valid success rate:** {successes}/{total} "
                f"({(successes / total * 100):.1f}%)."
                if responses
                else f"**Schema-valid success rate:** not measurable; "
                f"0/{total} API responses received."
            ),
            "",
        ]
    )
    for index, entry in enumerate(run["entries"], 1):
        lines.extend(
            [
                f"### Input {index}",
                "",
                f"**Messy text:** {entry['input_text']}",
                "",
                "**Prompt:**",
                "",
                code_block(entry.get("prompt")),
                "",
                "**Raw Gemini response:**",
                "",
                code_block(entry.get("raw_output", f"Not returned ({entry['status']}).")),
                "",
                f"**Status:** {entry['status']}",
                "",
                f"**Validation errors:** {json.dumps(entry.get('validation_errors', []), ensure_ascii=False)}",
                "",
            ]
        )
    table = [
        "| Input | Status | Parsed JSON |",
        "|---|---|---|",
    ]
    for index, entry in enumerate(run["entries"], 1):
        table.append(
            f"| {index} | {entry['status']} | "
            f"{markdown_cell(json.dumps(entry.get('parsed_json'), ensure_ascii=False))} |"
        )
    lines.extend(["### Structured output results", "", *table, ""])
    return lines


def generate_report():
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    runs = {key: latest_run(key) for key in FILES}
    all_runs = [run for run in runs.values() if run]
    dates = [run["started_at"] for run in all_runs]
    experiment_date = ", ".join(dates) if dates else "No API experiment has run yet."
    lines = [
        "# Prompt Engineering Mastery Lab: Experiment Report",
        "",
        "## Project introduction",
        "",
        "This project compares prompt strategies for sentiment classification and "
        "math reasoning, and tests schema-constrained JSON extraction with the "
        "Google Gemini API. Raw model responses are preserved in the result files "
        "and reproduced below without paraphrasing.",
        "",
        "## Objectives",
        "",
        "- Compare zero-shot and few-shot sentiment classification on five labeled reviews.",
        "- Compare direct and explicitly step-by-step solutions on five math problems.",
        "- Validate Gemini JSON-mode extraction for five messy payment records.",
        "- Record API failures as failures; no generated or mock outputs are substituted.",
        "",
        "## Model and experiment date",
        "",
        f"- **Configured Gemini model:** `{MODEL_NAME}`",
        f"- **Recorded run date(s), UTC:** {experiment_date}",
        "- A model response is only reported where a successful API response was received.",
        "",
        *sentiment_section(runs["sentiment"]),
        *math_section(runs["math"]),
        *structured_section(runs["structured"]),
        "## Analysis: what worked and what did not",
        "",
    ]
    for key, title in (("sentiment", "Sentiment"), ("math", "Math"), ("structured", "Structured output")):
        run = runs[key]
        if run is None:
            lines.append(f"- **{title}:** Not run; no result file exists yet.")
        elif run.get("api_calls_succeeded", 0) == 0:
            detail = run.get("setup_error")
            lines.append(
                f"- **{title}:** No Gemini responses were received. Run status is "
                f"`{run['status']}`. "
                + (f"Setup error: {detail['message']}" if detail else "See result JSON for errors.")
            )
        else:
            lines.append(
                f"- **{title}:** Received {run['api_calls_succeeded']} of "
                f"{run['api_calls_attempted']} attempted responses. Review the tables "
                "and raw outputs above for observed accuracy and validation outcomes."
            )
    lines.extend(
        [
            "",
            "## Conclusion and lessons learned",
            "",
            "This report distinguishes actual API responses from calls that were "
            "blocked or failed. Accuracy and schema success rates are calculated "
            "from saved run data, and can be improved by rerunning the experiments "
            "after correcting configuration or transient API errors. No conclusion "
            "about model performance is asserted when actual responses are absent.",
            "",
            f"_Report generated at {datetime.now(timezone.utc).isoformat()}._",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH


if __name__ == "__main__":
    print(generate_report())
