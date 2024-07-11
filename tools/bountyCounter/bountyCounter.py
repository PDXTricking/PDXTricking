import pandas as pd

csvFile = "unified_payments.csv"

def load_csv_to_dataframe(file_path):
    """
    Loads a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A Pandas DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except pd.errors.ParserError:
        print("Error parsing the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def combine_and_sum(df, x_col, y_col):
    """
    Combine rows with the same value in 'x_col' and sum the corresponding values in 'y_col'.
    Cast 'y_col' to integer before summing.
    
    Parameters:
    - df (DataFrame): Input DataFrame.
    - x_col (str): Column name to group by.
    - y_col (str): Column name to sum (will be cast to int).
    
    Returns:
    - DataFrame: DataFrame with combined rows and summed values.
    """
    # Cast 'y_col' to integer
    df[y_col] = df[y_col].astype(int)
    
    # Group by 'x_col' and sum 'y_col'
    grouped_df = df.groupby(x_col)[y_col].sum().reset_index()
    
    return grouped_df

def calculate_bounty_total(df, x_col):
    """
    Calculate 'bountyTotal' by multiplying values in 'x_col' by 5 and store in a new column.
    
    Parameters:
    - df (DataFrame): Input DataFrame.
    - x_col (str): Column name to multiply by 5.
    
    Returns:
    - DataFrame: DataFrame with 'bountyTotal' column added.
    """
    # Create a new column 'bountyTotal' with values multiplied by 5
    price = 5
    df['bountyTotal'] = df[x_col] * price
    
    return df

def export_to_text(df, file_path):
    """
    Export DataFrame to a text file.
    
    Parameters:
    - df (DataFrame): Input DataFrame.
    - file_path (str): File path including the filename to save the text file.
    
    Returns:
    - None
    """
    df.to_csv(file_path, sep='\t', index=False)
    print(f"DataFrame successfully exported to {file_path}")

def main():
    df = load_csv_to_dataframe(csvFile)

    #Filter to columns we need
    filtered_df = df.filter(items=['id', 'Amount', 'Description', 'Customer Description', 'Customer Email'])
    #remove rows with NaN in Description Column
    filtered_df = filtered_df.dropna(subset=['Description'])

    # Filter rows with '-bounty' in the Description column
    bounty_df = filtered_df[filtered_df['Description'].str.contains('-bounty')]
    # Extract the two characters after '-bounty'
    bounty_df['Post-bounty'] = bounty_df['Description'].str.extract(r'-bounty\)(.{4})')
        # Extract the two characters after '-bounty'
    bounty_df['Post-bounty'] = bounty_df['Post-bounty'].apply(lambda x: x[-1])

    # Extract the part of the string before '-bounty', stopping at a space if present
    bounty_df['Before-bounty'] = bounty_df['Description'].str.extract(r'(\S+)-bounty\)')

    print(bounty_df.head())

    filtered_bounty_df = combine_and_sum(bounty_df, 'Before-bounty','Post-bounty')
    print(filtered_bounty_df.head())

    filtered_bounty_df = calculate_bounty_total(filtered_bounty_df, 'Post-bounty')
    print(filtered_bounty_df.head())

    export_to_text(filtered_bounty_df,"bountyResults.txt")

if __name__ == '__main__':
    main()