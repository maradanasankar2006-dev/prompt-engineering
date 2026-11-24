# Prompt Engineering Mastery Lab: Experiment Report

## Project introduction

This project compares prompt strategies for sentiment classification and math reasoning, and tests schema-constrained JSON extraction with the Google Gemini API. Raw model responses are preserved in the result files and reproduced below without paraphrasing.

## Objectives

- Compare zero-shot and few-shot sentiment classification on five labeled reviews.
- Compare direct and explicitly step-by-step solutions on five math problems.
- Validate Gemini JSON-mode extraction for five messy payment records.
- Record API failures as failures; no generated or mock outputs are substituted.

## Model and experiment date

- **Configured Gemini model:** `gemini-2.5-flash`
- **Recorded run date(s), UTC:** 2026-11-24T06:16:05.529942+00:00, 2026-11-24T06:16:05.548367+00:00, 2026-11-24T06:16:05.562852+00:00
- A model response is only reported where a successful API response was received.

## Experiment 1: Zero-shot vs few-shot sentiment prompting

**Status:** blocked  
**Started (UTC):** 2026-11-24T06:16:05.529942+00:00  
**API responses received:** 0 / 0 attempted calls

**Accuracy among received API responses:** zero-shot not measurable (0 responses); few-shot not measurable (0 responses).
**Consistency (valid single-label responses):** zero-shot not measurable (0 responses); few-shot not measurable (0 responses).

| Review | Expected | Zero-shot label | Zero-shot correct | Few-shot label | Few-shot correct |
|---|---|---|---|---|---|
| The package arrived early and the product works perfectly. | Positive | — | — | — | — |
| The item broke after one use and support never replied. | Negative | — | — | — | — |
| The order arrived today. I have not tried it yet. | Neutral | — | — | — | — |
| Good quality, but it took far too long to arrive. | Negative | — | — | — | — |
| Exactly what I needed; I would happily buy it again. | Positive | — | — | — | — |

### Zero-shot prompts and raw Gemini outputs

#### Case 1

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Review: "The package arrived early and the product works perfectly."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 2

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Review: "The item broke after one use and support never replied."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 3

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Review: "The order arrived today. I have not tried it yet."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 4

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Review: "Good quality, but it took far too long to arrive."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 5

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Review: "Exactly what I needed; I would happily buy it again."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

### Few-shot prompts and raw Gemini outputs

#### Case 1

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Examples:
Review: "The screen is bright and easy to read."
Sentiment: Positive
Review: "It stopped working the same day."
Sentiment: Negative
Review: "The parcel is on my desk; I have not opened it."
Sentiment: Neutral
Review: "The food tasted fresh and arrived warm."
Sentiment: Positive

Review: "The package arrived early and the product works perfectly."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 2

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Examples:
Review: "The screen is bright and easy to read."
Sentiment: Positive
Review: "It stopped working the same day."
Sentiment: Negative
Review: "The parcel is on my desk; I have not opened it."
Sentiment: Neutral
Review: "The food tasted fresh and arrived warm."
Sentiment: Positive

Review: "The item broke after one use and support never replied."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 3

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Examples:
Review: "The screen is bright and easy to read."
Sentiment: Positive
Review: "It stopped working the same day."
Sentiment: Negative
Review: "The parcel is on my desk; I have not opened it."
Sentiment: Neutral
Review: "The food tasted fresh and arrived warm."
Sentiment: Positive

Review: "The order arrived today. I have not tried it yet."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 4

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Examples:
Review: "The screen is bright and easy to read."
Sentiment: Positive
Review: "It stopped working the same day."
Sentiment: Negative
Review: "The parcel is on my desk; I have not opened it."
Sentiment: Neutral
Review: "The food tasted fresh and arrived warm."
Sentiment: Positive

Review: "Good quality, but it took far too long to arrive."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

#### Case 5

**Prompt:**

```text
Classify the customer review as exactly one of Positive, Negative, or Neutral. Respond with only the label.

Examples:
Review: "The screen is bright and easy to read."
Sentiment: Positive
Review: "It stopped working the same day."
Sentiment: Negative
Review: "The parcel is on my desk; I have not opened it."
Sentiment: Neutral
Review: "The food tasted fresh and arrived warm."
Sentiment: Positive

Review: "Exactly what I needed; I would happily buy it again."
Sentiment:
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked

### Comparison

The table reports exact label matches against the predefined review labels. Consistency is measured as returning one unambiguous supported label; this run does not claim repeated-run stability.

## Experiment 2: Multi-step math reasoning

**Status:** blocked  
**Started (UTC):** 2026-11-24T06:16:05.548367+00:00  
**API responses received:** 0 / 0 attempted calls

**Accuracy among received API responses:** direct not measurable (0 responses); step-by-step not measurable (0 responses).

| Problem | Expected | Direct extracted answer | Direct correct | Step-by-step extracted answer | Step-by-step correct |
|---|---:|---:|---:|---:|---:|
| A shop has 48 notebooks and sells 19. How many notebooks remain? | 29 | — | — | — | — |
| Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost? | 81 | — | — | — | — |
| A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours? | 300 | — | — | — | — |
| A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price? | 1800 | — | — | — | — |
| A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain? | 59 | — | — | — | — |

### Direct prompts and raw Gemini outputs

#### Problem 1: A shop has 48 notebooks and sells 19. How many notebooks remain?

**Prompt:**

```text
Solve this word problem and state the final numerical answer clearly.

A shop has 48 notebooks and sells 19. How many notebooks remain?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 29.

#### Problem 2: Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost?

**Prompt:**

```text
Solve this word problem and state the final numerical answer clearly.

Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 81.

#### Problem 3: A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours?

**Prompt:**

```text
Solve this word problem and state the final numerical answer clearly.

A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 300.

#### Problem 4: A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price?

**Prompt:**

```text
Solve this word problem and state the final numerical answer clearly.

A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 1800.

#### Problem 5: A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain?

**Prompt:**

```text
Solve this word problem and state the final numerical answer clearly.

A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 59.

### Step-by-step prompts and raw Gemini outputs

#### Problem 1: A shop has 48 notebooks and sells 19. How many notebooks remain?

**Prompt:**

```text
Solve this word problem. Show a concise, numbered solution with the calculations and finish with 'Final answer: <number>'.

A shop has 48 notebooks and sells 19. How many notebooks remain?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 29.

#### Problem 2: Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost?

**Prompt:**

```text
Solve this word problem. Show a concise, numbered solution with the calculations and finish with 'Final answer: <number>'.

Mira buys 3 pens for 12 rupees each and a notebook for 45 rupees. What is the total cost?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 81.

#### Problem 3: A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours?

**Prompt:**

```text
Solve this word problem. Show a concise, numbered solution with the calculations and finish with 'Final answer: <number>'.

A bus travels 180 kilometers in 3 hours at a constant speed. How far will it travel in 5 hours?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 300.

#### Problem 4: A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price?

**Prompt:**

```text
Solve this word problem. Show a concise, numbered solution with the calculations and finish with 'Final answer: <number>'.

A jacket costs 2400 rupees and is discounted by 25 percent. What is the sale price?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 1800.

#### Problem 5: A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain?

**Prompt:**

```text
Solve this word problem. Show a concise, numbered solution with the calculations and finish with 'Final answer: <number>'.

A baker makes 8 trays with 12 muffins on each tray and sells 37 muffins. How many muffins remain?
```

**Raw API output:**

```text
Not returned (blocked).
```

**Status:** blocked; independently verified expected answer: 59.

## Experiment 3: Structured JSON extraction

**Status:** blocked  
**Started (UTC):** 2026-11-24T06:16:05.562852+00:00  
**API responses received:** 0 / 0 attempted calls

Schema: `{"name":"string","date":"string","amount":"number"}`

**Schema-valid success rate:** not measurable; 0/5 API responses received.

### Input 1

**Messy text:** John paid 2500 rupees on 12 November 2026.

**Prompt:**

```text
Extract the payer name, transaction date, and amount from the text. Return only a JSON object matching the supplied schema. Preserve the date as written in the text and return amount as a number.

Text: John paid 2500 rupees on 12 November 2026.
```

**Raw Gemini response:**

```text
Not returned (blocked).
```

**Status:** blocked

**Validation errors:** []

### Input 2

**Messy text:** Payment of Rs. 1500 was made by Priya on 15 November 2026.

**Prompt:**

```text
Extract the payer name, transaction date, and amount from the text. Return only a JSON object matching the supplied schema. Preserve the date as written in the text and return amount as a number.

Text: Payment of Rs. 1500 was made by Priya on 15 November 2026.
```

**Raw Gemini response:**

```text
Not returned (blocked).
```

**Status:** blocked

**Validation errors:** []

### Input 3

**Messy text:** On 18 November 2026, Rahul transferred 3500.

**Prompt:**

```text
Extract the payer name, transaction date, and amount from the text. Return only a JSON object matching the supplied schema. Preserve the date as written in the text and return amount as a number.

Text: On 18 November 2026, Rahul transferred 3500.
```

**Raw Gemini response:**

```text
Not returned (blocked).
```

**Status:** blocked

**Validation errors:** []

### Input 4

**Messy text:** An amount of 800 was paid by Anjali on 20 November 2026.

**Prompt:**

```text
Extract the payer name, transaction date, and amount from the text. Return only a JSON object matching the supplied schema. Preserve the date as written in the text and return amount as a number.

Text: An amount of 800 was paid by Anjali on 20 November 2026.
```

**Raw Gemini response:**

```text
Not returned (blocked).
```

**Status:** blocked

**Validation errors:** []

### Input 5

**Messy text:** Suresh made a payment of 4200 rupees dated 22 November 2026.

**Prompt:**

```text
Extract the payer name, transaction date, and amount from the text. Return only a JSON object matching the supplied schema. Preserve the date as written in the text and return amount as a number.

Text: Suresh made a payment of 4200 rupees dated 22 November 2026.
```

**Raw Gemini response:**

```text
Not returned (blocked).
```

**Status:** blocked

**Validation errors:** []

### Structured output results

| Input | Status | Parsed JSON |
|---|---|---|
| 1 | blocked | null |
| 2 | blocked | null |
| 3 | blocked | null |
| 4 | blocked | null |
| 5 | blocked | null |

## Analysis: what worked and what did not

- **Sentiment:** No Gemini responses were received. Run status is `blocked`. Setup error: GEMINI_API_KEY is missing. Set it in your environment or add GEMINI_API_KEY=your_key_here to a local .env file.
- **Math:** No Gemini responses were received. Run status is `blocked`. Setup error: GEMINI_API_KEY is missing. Set it in your environment or add GEMINI_API_KEY=your_key_here to a local .env file.
- **Structured output:** No Gemini responses were received. Run status is `blocked`. Setup error: GEMINI_API_KEY is missing. Set it in your environment or add GEMINI_API_KEY=your_key_here to a local .env file.

## Conclusion and lessons learned

This report distinguishes actual API responses from calls that were blocked or failed. Accuracy and schema success rates are calculated from saved run data, and can be improved by rerunning the experiments after correcting configuration or transient API errors. No conclusion about model performance is asserted when actual responses are absent.

_Report generated at 2026-11-24T06:18:02.438527+00:00._
