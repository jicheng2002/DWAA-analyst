import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress
plt.rcParams.update({'font.size': 18})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# Initialize dictionary to store the total count per year
yearly_counts = {year: {'dry_to_wet_count': 0, 'wet_to_dry_count': 0} for year in range(1980, 2021)}

# Define the folder path where the event data is stored
folder_path = r"D:\A-Projects\DWAA Project\DWAA_Events"

# Process each station folder
for station_folder in os.listdir(folder_path):
    station_path = os.path.join(folder_path, station_folder)
    if os.path.isdir(station_path):
        # Process both "dry-to-wet" and "wet-to-dry" event files
        for event_type in ["dry_to_wet_events.csv", "wet_to_dry_events.csv"]:
            file_path = os.path.join(station_path, event_type)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                # Convert the "Start_Date" column to datetime format
                df["Start_Date"] = pd.to_datetime(df["Start_Date"])

                # Iterate over each row in the CSV
                for _, row in df.iterrows():
                    start_date = row["Start_Date"]
                    year = start_date.year

                    # Check if the year is within the range 1980-2020
                    if 1980 <= year <= 2020:
                        if event_type == "dry_to_wet_events.csv":
                            yearly_counts[year]["dry_to_wet_count"] += 1
                        elif event_type == "wet_to_dry_events.csv":
                            yearly_counts[year]["wet_to_dry_count"] += 1

# Convert the results into lists for analysis
years = list(yearly_counts.keys())
dry_to_wet_counts = [yearly_counts[year]["dry_to_wet_count"] for year in years]
wet_to_dry_counts = [yearly_counts[year]["wet_to_dry_count"] for year in years]

# Perform linear regression for both event types
slope_dtw, intercept_dtw, r_value_dtw, p_value_dtw, std_err_dtw = linregress(years, dry_to_wet_counts)
slope_wtd, intercept_wtd, r_value_wtd, p_value_wtd, std_err_wtd = linregress(years, wet_to_dry_counts)

# Plot the results with trend lines
plt.figure(figsize=(14, 5))
plt.plot(years, dry_to_wet_counts, label="DTW", color="#ea801c", marker="o",linewidth=3, markersize='8')  # Orange for DTW
plt.plot(years, wet_to_dry_counts, label="WTD", color="#1a80bb", marker="o",linewidth=3, markersize='8')  # Blue for WTD

# Add labels and title
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.legend()
plt.grid(False)
plt.tight_layout()

# Save the plot
output_path = r'D:\A-Projects\DWAA Project\Figure\yearly_dwaa_event_trend.png'
plt.savefig(output_path, dpi=300)
plt.plot()
# Print trend analysis results
print("Dry to Wet Events Trend:")
print(f"  Slope: {slope_dtw:.3f}")
print(f"  p-value: {p_value_dtw:.5f}")

print("Wet to Dry Events Trend:")
print(f"  Slope: {slope_wtd:.3f}")
print(f"  p-value: {p_value_wtd:.5f}")

# Check if trends are significant
if p_value_dtw < 0.05:
    print("Dry to Wet event count shows a statistically significant trend.")
else:
    print("Dry to Wet event count does not show a statistically significant trend.")

if p_value_wtd < 0.05:
    print("Wet to Dry event count shows a statistically significant trend.")
else:
    print("Wet to Dry event count does not show a statistically significant trend.")
