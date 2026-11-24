from experiments.common import (
    MODEL_NAME,
    create_client,
    error_details,
    extract_sentiment_label,
    save_result,
    save_run,
    start_run,
    write_report,
)

RESULT_FILE = "zero_shot_few_shot_results.json"
TEST_CASES = [
    {
        "review": "The package arrived early and the product works perfectly.",
        "expected": "Positive",
    },
    {
        "review": "The item broke after one use and support never replied.",
        "expected": "Negative",
    },
    {
        "review": "The order arrived today. I have not tried it yet.",
        "expected": "Neutral",
    },
    {
        "review": "Good quality, but it took far too long to arrive.",
        "expected": "Negative",
    },
    {
        "review": "Exactly what I needed; I would happily buy it again.",
        "expected": "Positive",
    },
]
FEW_SHOT_EXAMPLES = (
    'Review: "The screen is bright and easy to read."\nSentiment: Positive\n'
    'Review: "It stopped working the same day."\nSentiment: Negative\n'
    'Review: "The parcel is on my desk; I have not opened it."\nSentiment: Neutral\n'
    'Review: "The food tasted fresh and arrived warm."\nSentiment: Positive'
)


def make_prompt(review, few_shot):
    instruction = (
        "Classify the customer review as exactly one of Positive, Negative, or "
        "Neutral. Respond with only the label.\n"
    )
    examples = f"\nExamples:\n{FEW_SHOT_EXAMPLES}\n" if few_shot else ""
    return f'{instruction}{examples}\nReview: "{review}"\nSentiment:'


def run_experiment():
    entries = [
        {
            "review": case["review"],
            "expected": case["expected"],
            "zero_shot": {
                "status": "pending",
                "prompt": make_prompt(case["review"], few_shot=False),
            },
            "few_shot": {
                "status": "pending",
                "prompt": make_prompt(case["review"], few_shot=True),
            },
        }
        for case in TEST_CASES
    ]
    document, run = start_run(
        RESULT_FILE, "Zero-shot vs few-shot sentiment classification", entries
    )
    try:
        client = create_client()
    except Exception as error:
        detail = error_details(error)
        for entry in entries:
            for mode in ("zero_shot", "few_shot"):
                entry[mode].update({"status": "blocked", "error": detail})
        run["setup_error"] = detail
        save_run(RESULT_FILE, document, run)
        write_report()
        print(detail["message"])
        return run

    for entry in entries:
        for mode in ("zero_shot", "few_shot"):
            prompt = entry[mode]["prompt"]
            result = {"prompt": prompt}
            run["api_calls_attempted"] += 1
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME, contents=prompt
                )
                raw_output = response.text
                label = extract_sentiment_label(raw_output) if isinstance(raw_output, str) else None
                result.update(
                    {
                        "status": "succeeded" if label is not None else "invalid",
                        "raw_output": raw_output,
                        "label": label,
                    }
                )
                result["correct"] = result["label"] == entry["expected"]
                run["api_calls_succeeded"] += 1
                if label is None:
                    result["validation_error"] = (
                        "Gemini returned no unambiguous supported sentiment label."
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
        f"Sentiment run {completed['status']}: "
        f"{completed['api_calls_succeeded']}/{completed['api_calls_attempted']} "
        "Gemini responses received."
    )
