#!/bin/bash

# Ensure cpdf is installed and in the PATH
if ! command -v /home/midhun/softwares/cpdfs/cpdf &> /dev/null
then
    echo "cpdf could not be found, please install it first."
    exit
fi

# Input and output PDF files
input_pdf="in.pdf"
output_pdf="output.pdf"

# Get the dimensions of the first page (assuming all pages have the same dimensions)
dimensions=$(cd /home/midhun/softwares/cpdfs/cpdf -pageinfo "$input_pdf" 1 | grep "MediaBox" | awk '{print $3, $4}')
width=$(echo $dimensions | awk '{print $1}')
height=$(echo $dimensions | awk '{print $2}')

# Calculate the height of the 10% offset
offset_height=$(echo "$height * 0.3" | bc)

# Add a white rectangle at the bottom 10% of the page
/home/midhun/softwares/cpdfs/cpdf "$input_pdf" -add-rectangle "0 0 $width $offset_height black" -o "$output_pdf"

echo "Black background added to the bottom 10% of each page in $output_pdf"

