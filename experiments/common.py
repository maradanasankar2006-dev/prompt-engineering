import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT_DIR / "results"
MODEL_NAME = "gemini-2.5-flash"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_api_key():
    load_dotenv(ROOT_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Set it in your environment or add "
            "GEMINI_API_KEY=your_key_here to a local .env file."
        )
    return api_key


def create_client():
    api_key = load_api_key()
    from google import genai

    return genai.Client(api_key=api_key)


def result_path(filename):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / filename


def read_result(filename):
    path = result_path(filename)
    if not path.exists():
        return {"experiment": filename, "runs": []}
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def save_result(filename, document):
    path = result_path(filename)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(document, file, ensure_ascii=False, indent=2)
        file.write("\n")
    temporary_path.replace(path)


def start_run(filename, experiment, entries):
    document = read_result(filename)
    run = {
        "run_id": str(uuid.uuid4()),
        "model": MODEL_NAME,
        "started_at": utc_now(),
        "completed_at": None,
        "status": "running",
        "api_calls_attempted": 0,
        "api_calls_succeeded": 0,
        "entries": entries,
    }
    document["experiment"] = experiment
    document.setdefault("runs", []).append(run)
    save_result(filename, document)
    return document, run


def save_run(filename, document, run):
    run["completed_at"] = utc_now()
    statuses = []
    for entry in run["entries"]:
        if "status" in entry:
            statuses.append(entry["status"])
        else:
            statuses.extend(
                value["status"]
                for value in entry.values()
                if isinstance(value, dict) and "status" in value
            )
    if statuses and all(status == "succeeded" for status in statuses):
        run["status"] = "succeeded"
    elif any(status in ("succeeded", "invalid") for status in statuses):
        run["status"] = "partial"
    elif any(status == "failed" for status in statuses):
        run["status"] = "failed"
    else:
        run["status"] = "blocked"
    save_result(filename, document)


def error_details(error):
    message = str(error)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        message = message.replace(api_key, "[REDACTED]")
    return {"type": type(error).__name__, "message": message}


def extract_sentiment_label(text):
    matches = re.findall(r"\b(positive|negative|neutral)\b", text, re.IGNORECASE)
    labels = {match.lower() for match in matches}
    if len(labels) != 1:
        return None
    return labels.pop().capitalize()


def extract_final_number(text):
    number = r"-?\d[\d,]*(?:\.\d+)?"
    emphasized = re.findall(
        rf"(?i)(?:final\s+answer|answer|therefore|thus|so)\s*[:=]?\s*[^0-9\-]*({number})",
        text,
    )
    matches = emphasized or re.findall(number, text)
    if not matches:
        return None
    return matches[-1].replace(",", "")


def validate_structured_payload(payload):
    errors = []
    if not isinstance(payload, dict):
        return ["The response must be a JSON object."]
    if set(payload) != {"name", "date", "amount"}:
        errors.append("The object must contain exactly name, date, and amount.")
    if not isinstance(payload.get("name"), str):
        errors.append("'name' must be a string.")
    if not isinstance(payload.get("date"), str):
        errors.append("'date' must be a string.")
    amount = payload.get("amount")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        errors.append("'amount' must be a number.")
    return errors


def write_report():
    from reports.generate_report import generate_report

    generate_report()
