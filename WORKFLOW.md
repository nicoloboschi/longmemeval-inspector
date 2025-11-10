# LongMemEval Inspector - Data Processing Workflow

This document describes the workflow for managing the LongMemEval Inspector data and HTML generation.

## Files Overview

- `longmemeval_s_cleaned.json` - Full dataset from HuggingFace (265MB, gitignored)
- `data.json` - Processed dataset with answer annotations (14MB, gitignored)
- `inspector_empty.html` - Template HTML without embedded data (17KB, tracked in git)
- `inspector.html` - Final HTML with embedded data (14MB, **tracked in git for GitHub Pages**)

## Scripts

### 1. Download Dataset
```bash
./download_dataset.sh
```
Downloads the full LongMemEval dataset from HuggingFace to `longmemeval_s_cleaned.json`.

### 2. Process Dataset
```bash
./process_dataset.py
```
Transforms the full dataset into the inspector-ready format:
- Filters haystack sessions to only keep those containing answers
- Adds `has_answer` field to each message (True if message contains the answer text)
- Removes metadata fields (haystack_dates, haystack_session_ids)
- Outputs to `data.json`

### 3. Generate Inspector HTML
```bash
./generate_inspector.sh
```
Injects `data.json` into `inspector_empty.html` to create the final `inspector.html`.

## Complete Workflow

To regenerate everything from scratch:

```bash
# 1. Download the dataset
./download_dataset.sh

# 2. Process it
./process_dataset.py

# 3. Generate the HTML
./generate_inspector.sh
```

## Customization

### Modify the Data
1. Edit `data.json` manually or use `process_dataset.py`
2. Run `./generate_inspector.sh` to regenerate the HTML

### Modify the HTML Template
1. Edit `inspector_empty.html`
2. Run `./generate_inspector.sh` to regenerate the HTML

## Data Structure

### Source Dataset (longmemeval_s_cleaned.json)
```json
{
  "question_id": "...",
  "question_type": "...",
  "question": "...",
  "question_date": "...",
  "answer": "...",
  "answer_session_ids": ["..."],
  "haystack_dates": ["..."],
  "haystack_session_ids": ["..."],
  "haystack_sessions": [[...]]
}
```

### Processed Dataset (data.json)
```json
{
  "question_id": "...",
  "question_type": "...",
  "question": "...",
  "question_date": "...",
  "answer": "...",
  "answer_session_ids": ["..."],
  "haystack_sessions": [
    [
      {
        "role": "user|assistant",
        "content": "...",
        "has_answer": true|false
      }
    ]
  ]
}
```

The `has_answer` field indicates whether a message contains the answer text (case-insensitive match).
