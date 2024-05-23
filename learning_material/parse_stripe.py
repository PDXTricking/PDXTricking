import pandas as pd

# Read the CSV file
df = pd.read_csv('unified_payments.csv')

# Define the column where you want to filter for the substring
column_to_filter = 'Description'
columns_to_keep = ['Customer ID', 'Description']

# Filter for rows containing the substring "-bounty" in the specified column
filtered_df = df[df[column_to_filter].str.contains('-bounty', na=False)]

filtered_df = filtered_df[columns_to_keep]

# Print the filtered dataframe
print(filtered_df.head())

output_file = 'filtered_output.csv'
filtered_df.to_csv(output_file, index=False)
print(f"Filtered data saved to '{output_file}'")

#Next steps:
#from filtered csv, combine all outputs into a single string,
#Then use find substring functions for each different trick/bounty and add to a count.
#Save to a dictionary where key is trick name and value is number it appears
#(tak-full-switchblade-bounty)