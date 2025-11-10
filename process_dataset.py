#!/usr/bin/env python3
"""
Script to process the LongMemEval dataset and add has_answer annotations.

This script reads the full dataset (longmemeval_s_cleaned.json) and:
1. For each question, identifies which haystack sessions contain the answer
2. Adds a 'has_answer' field to each message in the haystack sessions
3. Saves the processed dataset to data.json
"""

import json
import sys
from typing import Dict, List, Any


def message_contains_answer(message_content: str, answer: str) -> bool:
    """
    Check if a message contains the answer (case-insensitive).

    Note: This is a simple substring match. The original data.json may have used
    a more sophisticated annotation method (manual annotation, NLP, etc.).
    This script provides a reasonable approximation for most cases.

    Args:
        message_content: The content of the message
        answer: The answer string to look for

    Returns:
        True if the message contains the answer, False otherwise
    """
    return answer.lower() in message_content.lower()


def add_has_answer_annotations(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter to only answer sessions and add has_answer field to each message.

    This function:
    1. Filters haystack_sessions to only keep sessions that are in answer_session_ids
    2. Marks messages with has_answer=True if they contain the answer text

    Args:
        data: List of questions from the dataset

    Returns:
        List of questions with filtered sessions and has_answer annotations
    """
    processed_data = []

    for idx, item in enumerate(data):
        if (idx + 1) % 100 == 0:
            print(f"Processing question {idx + 1}/{len(data)}...", file=sys.stderr)

        # Get the answer and answer session IDs
        answer = item.get('answer', '')
        answer_session_ids = set(item.get('answer_session_ids', []))
        haystack_session_ids = item.get('haystack_session_ids', [])
        haystack_sessions = item.get('haystack_sessions', [])

        # Filter to only keep sessions that contain the answer
        filtered_sessions = []
        for session_idx, session_id in enumerate(haystack_session_ids):
            if session_id in answer_session_ids and session_idx < len(haystack_sessions):
                session = haystack_sessions[session_idx]

                # Process each message in the session
                processed_session = []
                for message in session:
                    # Check if this message contains the answer
                    has_answer = message_contains_answer(message['content'], answer)

                    processed_message = {
                        'role': message['role'],
                        'content': message['content'],
                        'has_answer': has_answer
                    }
                    processed_session.append(processed_message)

                filtered_sessions.append(processed_session)

        # Create the processed item (without haystack_dates and haystack_session_ids)
        processed_item = {
            'question_id': item['question_id'],
            'question_type': item['question_type'],
            'question': item['question'],
            'question_date': item['question_date'],
            'answer': item['answer'],
            'answer_session_ids': item['answer_session_ids'],
            'haystack_sessions': filtered_sessions
        }

        processed_data.append(processed_item)

    return processed_data


def main():
    input_file = 'longmemeval_s_cleaned.json'
    output_file = 'data.json'

    print(f"Loading dataset from {input_file}...", file=sys.stderr)
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please run download_dataset.sh first.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(data)} questions", file=sys.stderr)

    print("Processing dataset and adding has_answer annotations...", file=sys.stderr)
    processed_data = add_has_answer_annotations(data)

    print(f"Writing processed data to {output_file}...", file=sys.stderr)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False)

    print(f"✓ Processing complete!", file=sys.stderr)
    print(f"  Input: {input_file}", file=sys.stderr)
    print(f"  Output: {output_file}", file=sys.stderr)
    print(f"  Questions processed: {len(processed_data)}", file=sys.stderr)


if __name__ == '__main__':
    main()
