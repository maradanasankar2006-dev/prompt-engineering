from experiments.common import (
    MODEL_NAME,
    create_client,
    error_details,
    extract_final_number,
    save_result,
    save_run,
    start_run,
    write_report,
)

RESULT_FILE = "math_results.json"
PROBLEMS = [
    {
        "problem": "A shop has 48 notebooks and sells 19. How many notebooks remain?",
        "expected_answer": "29",
    },
    {
        "problem": "Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost?",
        "expected_answer": "81",
    },
    {
        "problem": "A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours?",
        "expected_answer": "300",
    },
    {
        "problem": "A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price?",
        "expected_answer": "1800",
    },
    {
        "problem": "A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain?",
        "expected_answer": "59",
    },
]


def make_prompt(problem, step_by_step):
    if step_by_step:
        return (
            f"Solve this word problem. Show a concise, numbered solution with "
            f"the calculations and finish with 'Final answer: <number>'.\n\n{problem}"
        )
    return (
        f"Solve this word problem and state the final numerical answer clearly.\n\n"
        f"{problem}"
    )


def run_experiment():
    entries = [
        {
            **problem,
            "direct": {
                "status": "pending",
                "prompt": make_prompt(problem["problem"], step_by_step=False),
            },
            "step_by_step": {
                "status": "pending",
                "prompt": make_prompt(problem["problem"], step_by_step=True),
            },
        }
        for problem in PROBLEMS
    ]
    document, run = start_run(RESULT_FILE, "Multi-step math reasoning", entries)
    try:
        client = create_client()
    except Exception as error:
        detail = error_details(error)
        for entry in entries:
            for mode in ("direct", "step_by_step"):
                entry[mode].update({"status": "blocked", "error": detail})
        run["setup_error"] = detail
        save_run(RESULT_FILE, document, run)
        write_report()
        print(detail["message"])
        return run

    for entry in entries:
        for mode in ("direct", "step_by_step"):
            prompt = entry[mode]["prompt"]
            result = {"prompt": prompt}
            run["api_calls_attempted"] += 1
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME, contents=prompt
                )
                raw_output = response.text
                final_number = (
                    extract_final_number(raw_output)
                    if isinstance(raw_output, str)
                    else None
                )
                result.update(
                    {
                        "status": "succeeded" if final_number is not None else "invalid",
                        "raw_output": raw_output,
                        "extracted_final_answer": final_number,
                        "correct": final_number == entry["expected_answer"],
                    }
                )
                run["api_calls_succeeded"] += 1
                if final_number is None:
                    result["validation_error"] = (
                        "Gemini returned no extractable final numerical answer."
                    )
            except Exception as error:
                result.update({"status": "failed", "error": error_details(error)})
            entry[mode] = result
            save_result(RESULT_FILE, document)
    save_run(RESULT_FILE, document, run)
    write_report()
    return run


if __name__ == "__main__":
    completed = run_experiment()
    print(
        f"Math run {completed['status']}: "
        f"{completed['api_calls_succeeded']}/{completed['api_calls_attempted']} "
        "Gemini responses received."
    )
