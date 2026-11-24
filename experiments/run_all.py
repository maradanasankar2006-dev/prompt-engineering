from experiments.math_reasoning import run_experiment as run_math
from experiments.structured_output import run_experiment as run_structured
from experiments.zero_shot_few_shot import run_experiment as run_sentiment
from reports.generate_report import generate_report


def main():
    runs = [run_sentiment(), run_math(), run_structured()]
    generate_report()
    attempted = sum(run["api_calls_attempted"] for run in runs)
    succeeded = sum(run["api_calls_succeeded"] for run in runs)
    print(
        f"Experiment runs recorded. API calls: {attempted} attempted; "
        f"{succeeded} responses received."
    )


if __name__ == "__main__":
    main()
