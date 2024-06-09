import csv
from collections import defaultdict

def sum_purchases(csv_file_path):
    # Dictionary to store the total purchases for each item
    purchases = defaultdict(float)
    
    # Read the CSV file
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header if there is one
        header = next(reader, None)
        
        for row in reader:
            if len(row) != 2:
                continue  # Skip rows that don't have exactly 2 columns
            item, amount = row
            try:
                amount = float(amount)
            except ValueError:
                continue  # Skip rows where the amount is not a valid number
            purchases[item] += amount
    
    return dict(purchases)

# Example usage:
csv_file_path = 'purchases.csv'
total_purchases = sum_purchases(csv_file_path)
print(total_purchases)
