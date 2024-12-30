import argparse
import pandas as pd

# Argument parser to take input range
parser = argparse.ArgumentParser(description="Generate graph.host file based on user input range.")
parser.add_argument("--start", type=int, required=True, help="Start of the user ID range (inclusive).")
parser.add_argument("--end", type=int, required=True, help="End of the user ID range (exclusive).")
args = parser.parse_args()

# Load datasets
ratings = pd.read_csv('../data/train_ratings.csv')

# Define the file path to save the output
output_file = "graph.host"

# Extract user IDs for the specified range
user_ids = range(args.start, args.end)

# Filter ratings for the specified user IDs
filtered_ratings = ratings[ratings['userId'].isin(user_ids)]

# Format the user nodes
user_nodes = [(int(f"1{user_id}"), int(f"1{user_id}")) for user_id in user_ids]

# Extract all unique movie IDs from filtered ratings
movie_ids = filtered_ratings['movieId'].unique()
movie_nodes = [(int(f"2{movie_id}"), int(f"2{movie_id}")) for movie_id in movie_ids]

# Format the edges directly from filtered_ratings
edges = [
    (int(f"3{index}"), int(f"1{row['userId']}"), int(f"2{row['movieId']}"), int(row['rating']))
    for index, row in filtered_ratings.iterrows()
]

# Write to file
with open(output_file, "w") as file:
    file.write('[\n')
    # Write user nodes
    for node in user_nodes:
        file.write(f'\t({node[0]}, \"{node[1]}_\")\n')
    # Write movie nodes
    for node in movie_nodes:
        file.write(f'\t({node[0]}, \"{node[1]}\")\n')
    # Separator
    file.write('\t|\n')
    # Write edges
    for edge in edges:
        file.write(f"\t{edge}\n")
    file.write(']')

print(f"Graph saved to {output_file}")
