#!/bin/bash

# Script to inject data.json into inspector_empty.html to create inspector.html

set -e

if [ ! -f "data.json" ]; then
    echo "Error: data.json not found"
    exit 1
fi

if [ ! -f "inspector_empty.html" ]; then
    echo "Error: inspector_empty.html not found"
    exit 1
fi

echo "Generating inspector.html from inspector_empty.html and data.json..."

# Read the JSON data and escape it properly for sed
json_data=$(cat data.json)

# Find the line number where we need to insert the script
# We need to insert BEFORE the <script> tag that contains the main code
# Look for the line with "let allQuestions = [];" and go back to before the <script> tag
insert_line=$(grep -n "let allQuestions = \[\];" inspector_empty.html | cut -d: -f1)
insert_line=$((insert_line - 2))

# Create the embedded data script
cat > /tmp/embedded_script.txt << 'EOF'

    <script id="embedded-data">
        // EMBEDDED DATA - This file is completely self-contained
        const embeddedData =
EOF

# Add the JSON data
cat data.json >> /tmp/embedded_script.txt

# Close the script tag
cat >> /tmp/embedded_script.txt << 'EOF'
;
    </script>
EOF

# Insert the script into the HTML
head -n "$insert_line" inspector_empty.html > inspector.html
cat /tmp/embedded_script.txt >> inspector.html
tail -n "+$((insert_line + 1))" inspector_empty.html >> inspector.html

# Cleanup
rm /tmp/embedded_script.txt

echo "✓ inspector.html generated successfully!"
echo "  Size: $(ls -lh inspector.html | awk '{print $5}')"
