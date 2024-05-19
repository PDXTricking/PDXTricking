import csv

def read_names_from_csv(file_path):
    """
    Reads names from a CSV file and returns a list of names.
    Assumes that the CSV file has one name per line.
    """
    names = []
    try:
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:
                    names.append(row[0])  # Assuming single column CSV
        return names
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def create_1v1_bracket(names):
    # Ensure the number of names is even
    if len(names) % 2 != 0:
        print("Ignoring the last name since the number of names is odd.")
        names.pop()

    # Shuffle the names randomly (optional)
    import random
    random.shuffle(names)

    # Create pairs for the bracket
    pairs = [(names[i], names[i + 1]) for i in range(0, len(names), 2)]

    # Print the bracket
    print("1v1 Bracket:")
    for i, (player1, player2) in enumerate(pairs, start=1):
        print("Match {0}: {1} vs {2}".format(i,player1,player2))

# Example usage
if __name__ == "__main__":
    csv_file_path = "path/to/your/names.csv"  # Replace with your actual CSV file path
    player_names = read_names_from_csv(csv_file_path)
    if player_names:
        create_1v1_bracket(player_names)
    else:
        player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Boice"]
        create_1v1_bracket(player_names)