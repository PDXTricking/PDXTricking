import pandas as pd

# Load the CSV file
file_path = 'unified_payments.csv'  # Replace with the actual file path if needed
data = pd.read_csv(file_path)

# Filter rows where "Checkout Line Item Summary" contains "Rose City Gathering"
filtered_data = data[data['Checkout Line Item Summary'].str.contains("Rose City Gathering", na=False)]

# Select the required columns
result = filtered_data[["Card Name", "Amount", "Created date (UTC)", "Checkout Line Item Summary", "Customer Email"]]

# Display the result
print(result)

# Optionally, save the result to a new CSV file
result.to_csv('filtered_data.csv', index=False)
