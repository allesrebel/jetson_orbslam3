import re
import pandas as pd
from datetime import datetime, timedelta

# Read the perf script output
with open('perf_script_output.txt', 'r') as file:
    lines = file.readlines()

# Initialize lists to store timestamps and cache misses
timestamps = []
cache_misses = []

# Regular expression to match the cache misses event for a specific executable
executable_name = "stereo_euroc"
cache_miss_pattern = re.compile(rf"\s+{executable_name}\s+\d+\s+\[\d+\]\s+(\d+\.\d+):\s+(\d+)\s+cache-misses:")

# Parse the lines to extract timestamps and cache misses
for line in lines:
    match = cache_miss_pattern.search(line)
    if match:
        timestamp = float(match.group(1))
        misses = int(match.group(2))
        # Convert timestamp to datetime assuming it is in seconds since the epoch
        timestamps.append(datetime.fromtimestamp(timestamp))
        cache_misses.append(misses)

# Debug: Check if lists are populated
if not timestamps or not cache_misses:
    print("No cache misses were recorded.")
else:
    print(f"Recorded {len(timestamps)} cache miss events.")

# Convert the lists to a DataFrame
df = pd.DataFrame({'timestamp': timestamps, 'misses': cache_misses})

# Set the 'timestamp' column as the index
df.set_index('timestamp', inplace=True)

# Debug: Check if the DataFrame is populated
if df.empty:
    print("DataFrame is empty after setting the timestamp index.")
else:
    print("DataFrame is populated.")
    print(df.head())

# Save the results to a CSV file
df.to_csv('cache_misses.csv', columns=['misses'], index=True)
