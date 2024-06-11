#!/bin/bash

# Get a list of all files in the current directory
files=(*)

# Initialize a counter
counter=1

# Loop through each file
for file in "${files[@]}"; do
    # Check if it's a regular file
    if [ -f "$file" ]; then
        # Get the file extension
        extension="${file##*.}"
        
        # Format the counter with leading zeros (01, 02, ...)
        formatted_counter=$(printf "%02d" $counter)
        
        # Create the new filename
        new_filename="${formatted_counter}.${extension}"
        
        # Rename the file
        mv "$file" "$new_filename"
        
        # Increment the counter
        ((counter++))
    fi
done

