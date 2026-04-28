import os

import kagglehub
import pandas as pd

# Load the data (Method 2 from earlier)
folder_path = kagglehub.dataset_download(
    "adrianjuliusaluoch/daily-google-search-trends-us"
)
csv_filename = [f for f in os.listdir(folder_path) if f.endswith(".csv")][0]
df = pd.read_csv(os.path.join(folder_path, csv_filename))

# Print the column names so you know what you are working with
print("--- COLUMN NAMES ---")
print(df.columns)

# Look at the first 5 rows to see what the data actually looks like
print("\n--- FIRST 5 ROWS ---")
print(df.tail())

sports_data = df[df["categories"].str.lower() == "sports"]

print(sports_data.head(20))
