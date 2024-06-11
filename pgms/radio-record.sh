#!/bin/bash

# Directory to save the recordings
output_dir="/home/midhun/radio"
# Stream URL
stream_url="https://air.pc.cdn.bitgravity.com/air/live/pbaudio230/playlist.m3u8"
# Get the current date and time for the filename
current_date=$(date +"%Y-%m-%d_%H-%M-%S")
# Output file path
output_file="$output_dir/recording_$current_date.mp3"

# Duration in seconds (1 minute = 60 seconds)
duration=900

# Start recording the stream
ffmpeg -y -i "$stream_url" -t $duration -acodec mp3 "$output_file"

