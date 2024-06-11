#!/bin/bash

# Ensure cpdf is installed and in the PATH
if ! command -v cpdf &> /dev/null
then
    echo "cpdf could not be found, please install it first."
    exit
fi

# Input and output PDF files
input_pdf="input.pdf"
output_pdf="output.pdf"

# Get the dimensions of the first page (assuming all pages have the same dimensions)
dimensions=$(cpdf -pageinfo "$input_pdf" 1 | grep "MediaBox" | awk '{print $3, $4}')
width=$(echo $dimensions | awk '{print $1}')
height=$(echo $dimensions | awk '{print $2}')

# Calculate the coordinates for the triangle
x1=$(echo "$width / 2" | bc)
y1=$(echo "$height / 2 + ($height / 10)" | bc)
x2=$(echo "$x1 - ($width / 10)" | bc)
y2=$(echo "$height / 2 - ($height / 10)" | bc)
x3=$(echo "$x1 + ($width / 10)" | bc)

# Add a red-filled triangle at the middle of the page
cpdf "$input_pdf" -add-text "q 1 0 0 rg $x1 $y1 m $x2 $y2 l $x3 $y2 l f Q" -o "$output_pdf"

echo "Red-filled triangle added to the middle of each page in $output_pdf"

