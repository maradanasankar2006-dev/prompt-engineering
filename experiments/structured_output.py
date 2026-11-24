import json

from experiments.common import (
    MODEL_NAME,
    create_client,
    error_details,
    save_result,
    save_run,
    start_run,
    validate_structured_payload,
    write_report,
)

RESULT_FILE = "structured_output_results.json"
SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "name": {"type": "STRING"},
        "date": {"type": "STRING"},
        "amount": {"type": "NUMBER"},
    },
    "required": ["name", "date", "amount"],
    "propertyOrdering": ["name", "date", "amount"],
}
INPUTS = [
    "John paid 2500 rupees on 12 November 2026.",
    "Payment of Rs. 1500 was made by Priya on 15 November 2026.",
    "On 18 November 2026, Rahul transferred 3500.",
    "An amount of 800 was paid by Anjali on 20 November 2026.",
    "Suresh made a payment of 4200 rupees dated 22 November 2026.",
]


def make_prompt(text):
    return (
        "Extract the payer name, transaction date, and amount from the text. "
        "Return only a JSON object matching the supplied schema. Preserve the "
        "date as written in the text and return amount as a number.\n\n"
        f"Text: {text}"
    )


def run_experiment():
    entries = [
        {"input_text": text, "prompt": make_prompt(text), "status": "pending"}
        for text in INPUTS
    ]
    document, run = start_run(
        RESULT_FILE, "Structured JSON information extraction", entries
    )
    try:
        client = create_client()
        from google.genai import types
    except Exception as error:
        detail = error_details(error)
        for entry in entries:
            entry.update({"status": "blocked", "error": detail})
        run["setup_error"] = detail
        save_run(RESULT_FILE, document, run)
        write_report()
        print(detail["message"])
        return run

    for entry in entries:
        run["api_calls_attempted"] += 1
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=entry["prompt"],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SCHEMA,
                ),
            )
            raw_output = response.text
            entry["raw_output"] = raw_output
            run["api_calls_succeeded"] += 1
            if not isinstance(raw_output, str):
                entry.update(
                    {
                        "status": "invalid",
                        "validation_errors": [
                            "Gemini returned no text to parse as JSON."
                        ],
                    }
                )
            else:
                try:
                    payload = json.loads(raw_output)
                except json.JSONDecodeError as error:
                    entry.update(
                        {
                            "status": "invalid",
                            "validation_errors": [
                                f"Invalid JSON: {error.msg} at character {error.pos}."
                            ],
                        }
                    )
                else:
                    validation_errors = validate_structured_payload(payload)
                    entry["parsed_json"] = payload
                    entry["validation_errors"] = validation_errors
                    entry["status"] = "succeeded" if not validation_errors else "invalid"
        except Exception as error:
            entry.update({"status": "failed", "error": error_details(error)})
        save_result(RESULT_FILE, document)
    save_run(RESULT_FILE, document, run)
    write_report()
    return run


if __name__ == "__main__":
    completed = run_experiment()
    print(
        f"Structured-output run {completed['status']}: "
        f"{completed['api_calls_succeeded']}/{completed['api_calls_attempted']} "
        "Gemini responses received."
    )
