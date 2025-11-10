#!/bin/bash

# Script to download the LongMemEval dataset from HuggingFace

set -e

DATASET_URL="https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json"
OUTPUT_FILE="longmemeval_s_cleaned.json"

echo "Downloading LongMemEval dataset from HuggingFace..."
echo "URL: $DATASET_URL"
echo "Output: $OUTPUT_FILE"
echo ""

if [ -f "$OUTPUT_FILE" ]; then
    echo "Warning: $OUTPUT_FILE already exists"
    read -p "Do you want to overwrite it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Download cancelled."
        exit 0
    fi
fi

curl -L -o "$OUTPUT_FILE" "$DATASET_URL"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Download completed successfully!"
    echo "  File: $OUTPUT_FILE"
    echo "  Size: $(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
else
    echo ""
    echo "✗ Download failed!"
    exit 1
fi
