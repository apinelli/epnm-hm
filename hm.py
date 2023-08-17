import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import re
from datetime import datetime
import  zipfile

def extract_timestamp(line):
    # Regular expression pattern to extract timestamp in the format "08/02/23 20:47:16"
    pattern = r'\d{2}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}'
    match = re.search(pattern, line)
    if match:
        return match.group()
    return None

def search_log_files(directory):
    timestamp_list = []

    # Unzip the logs.zip file if it exists
    zip_file_path = os.path.join(directory, 'logs.zip')
    if os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(directory)

    # Create the path for the log files
    log_file_dir = os.path.join(directory, 'logs')

    # Get a list of log files in the specified directory
    log_files = [file for file in os.listdir(log_file_dir) if file.endswith('.log')]

    for log_file in log_files:
        log_file_path = os.path.join(log_file_dir, log_file)
        with open(log_file_path, 'r') as file:
            for line in file:
                if "failed to exchange heartbeat" in line:
                    timestamp_str = extract_timestamp(line)
                    if timestamp_str:
                        # Convert the timestamp string to a datetime object
                        timestamp = datetime.strptime(timestamp_str, "%m/%d/%y %H:%M:%S")
                        # Convert the datetime object back to the desired string format
                        formatted_timestamp = timestamp.strftime("%m/%d/%y %H:%M:%S")
                        timestamp_list.append(formatted_timestamp)

    return timestamp_list

if __name__ == "__main__":
    directory_path = "/home/devasc/epnm/hm"
    timestamps = search_log_files(directory_path)
    print(timestamps)


# Convert timestamps to datetime objects
data = pd.to_datetime(timestamps)

# Create a DataFrame
df = pd.DataFrame(data, columns=['timestamp'])

# Set the frequency bins for the histogram (per hour)
frequency_bins = pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='1H')

plt.hist(df['timestamp'], bins=frequency_bins, edgecolor='black')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Timestamp Histogram')
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))  # Format the x-axis as hour:minute
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent x-axis label clipping
plt.show()
