#!/bin/bash

# Check if input file is provided as argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_list.txt>"
    exit 1
fi

# Input file containing list of files to copy
file_list="$1"

# Check if input file exists
if [ ! -f "$file_list" ]; then
    echo "Error: Input file '$file_list' not found."
    exit 1
fi

# Create a directory to store the archived files
archive_dir="archive"
mkdir -p "$archive_dir"

# Get today's date in YYYY-MM-DD format
today=$(date +%Y-%m-%d)

# Process each file listed in the input file
while IFS= read -r file; do
    # Check if file exists
    if [ -f "$file" ]; then
        # Copy file to archive directory
        cp "$file" "$archive_dir/"
        echo "Copied '$file' to '$archive_dir/'"
    else
        echo "Warning: File '$file' not found."
    fi
done < "$file_list"

# Zip the copied files
zip_file="archive_${today}.zip"
zip -r "$zip_file" "$archive_dir"

# Clean up: Remove copied files and directory
rm -rf "$archive_dir"

echo "Archived files in '$zip_file'"

