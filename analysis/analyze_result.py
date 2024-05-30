import plotly.graph_objects as go
import pandas as pd
import sys
from datetime import datetime, timedelta
import re

def parse_timedelta(timedelta_str):
    # Extract the days, seconds, and microseconds from the string
    days_match = re.search(r'days=(\d+)', timedelta_str)
    seconds_match = re.search(r'seconds=(\d+)', timedelta_str)
    microseconds_match = re.search(r'microseconds=(\d+)', timedelta_str)

    days = int(days_match.group(1)) if days_match else 0
    seconds = int(seconds_match.group(1)) if seconds_match else 0
    microseconds = int(microseconds_match.group(1)) if microseconds_match else 0

    return timedelta(days=days, seconds=seconds, microseconds=microseconds)

def parse_datetime(datetime_str):
    # Extract numbers from the string and convert to datetime
    nums = list(map(int, re.findall(r'\d+', datetime_str)))
    return datetime(*nums)

def convert_to_dataframe(file_path):
    # Initialize an empty list to store the data
    data = []

    # Open the file and read each line
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Convert datetime and timedelta explicitly
            line = re.sub(r"datetime\.datetime\(([^)]+)\)", r"parse_datetime('\1')", line)
            line = re.sub(r"datetime\.timedelta\(([^)]+)\)", r"parse_timedelta('\1')", line)
            # Evaluate the line in the context of the functions defined above
            record = eval(line, {"parse_datetime": parse_datetime, "parse_timedelta": parse_timedelta, "timedelta": timedelta, "datetime": datetime})
            data.append(record)
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Ensure the 'time' column exists
    if 'time' not in df.columns:
        raise KeyError("The 'time' column is missing from the DataFrame.")
    
    # Calculate offsets
    min_timestamp = df['time'].min()
    df['time'] = df['time'] - min_timestamp
    
    # Convert time column to seconds
    df['time'] = df['time'].dt.total_seconds()

    return df

# collect cache misses from perf output
def get_cache_misses(file_path):
    with open(file_path, 'r') as file:
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

    # Convert the 'timestamp' column to datetime and set it as the index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Resample the data to every 100 milliseconds and calculate the mean
    df_resampled = df.resample('100L').mean().reset_index()

    # Set the first timestamp to 0 and calculate offsets
    df_resampled['timestamp'] = (df_resampled['timestamp'] - df_resampled['timestamp'].min()).dt.total_seconds()

    # Debug: Check the DataFrame
    if df_resampled.empty:
        print("DataFrame is empty after resampling.")
    else:
        print("DataFrame is populated.")
        print(df_resampled.head())

    return df_resampled

# Function to load data
def load_data(directory, file_name):
    file_path = f"{directory}/{file_name}"
    try:
        # Attempt to read the CSV file
        data = pd.read_csv(file_path)

        # Ensure the first row can be used as header
        if data.empty:
            raise ValueError("First row of the file does not contain headers or is not in expected format")
        
        return data
    except Exception as e:
        print(f"Error processing file {file_name}: {str(e)}")
        return pd.DataFrame()

def main(directory, fps):
    # Define file names
    files = {
        # 'LocalMapTimeStats.txt': 'Local Map Time Stats',
        'TrackingTimeStats.txt': 'Tracking Time Stats',
        'jtop_stats.log': 'System Stats',
        'perf_script_output.txt': 'Cache Misses'
        # 'LBA_Stats.txt': 'LBA Stats'
    }
    
    # Create a figure for plotting
    fig = go.Figure()

    # Load and plot data for each file
    for file_name, label in files.items():
        if( file_name == 'TrackingTimeStats.txt' ):
            data = load_data(directory, file_name)

            for col in data.columns:
                x_values = [i * (1/fps) for i in range(len(data))]
                fig.add_trace(go.Scatter(x=x_values, y=data[col], mode='lines+markers', name=f"{label}: {col}", visible='legendonly'))

        if( file_name == 'jtop_stats.log' ):
            data = convert_to_dataframe(f"{directory}/{file_name}")
            for col in data.columns:
                if col != 'time':  # Avoid plotting the time column itself
                    fig.add_trace(go.Scatter(x=data['time'], y=data[col], mode='lines+markers', name=f"{label}: {col}", visible='legendonly'))

        if( file_name == 'perf_script_output.txt'):
            data = get_cache_misses(f"{directory}/{file_name}")
            for col in data.columns:
                if col != 'timestamp':  # Avoid plotting the time column itself
                    fig.add_trace(go.Scatter(x=data['timestamp'], y=data[col], mode='lines+markers', name=f"{label}: {col}", visible='legendonly'))

    # Update the layout
    fig.update_layout(
        title="ORB SLAM3 Metrics Timeline",
        xaxis_title="Time (seconds)",
        yaxis_title="Time (ms)",
        legend_title="Metric",
        hovermode="x"
    )

    fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python this_script.py <path_to_directory_with_files> <fps>")
        sys.exit(1)

    fps = float(sys.argv[2])
    main(sys.argv[1], fps)

