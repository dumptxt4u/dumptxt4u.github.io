#!/bin/bash

# URL of the M3U8 stream
stream_url="https://air.pc.cdn.bitgravity.com/air/live/pbaudio230/playlist.m3u8"

# Duration in seconds for the entire recording (15 minutes)
total_duration=900

# Segment duration in seconds (adjust if needed)
segment_duration=600

# Start time
start_time=$(date +%s)

# Loop until the total duration has passed
while [ $(($(date +%s) - start_time)) -lt $total_duration ]; do
    ffmpeg -timeout 900000000 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2 -i "$stream_url" -c:a libmp3lame -f segment -segment_time $segment_duration -segment_format mp3 output%d.mp3
    sleep 2
done
mv  output*.mp3 $start_time.mp3
