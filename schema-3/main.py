import argparse
import pandas as pd

# Argument parser to take input range
parser = argparse.ArgumentParser(description="Generate graph.host file based on user input range.")
parser.add_argument("--start", type=int, required=True, help="Start of the user ID range (inclusive).")
parser.add_argument("--end", type=int, required=True, help="End of the user ID range (exclusive).")
args = parser.parse_args()

# Load datasets
movies = pd.read_csv('../data/movies.csv')
ratings = pd.read_csv('../data/train_ratings.csv')

# Define the file path to save the output
output_file = "graph.host"

# Extract user IDs for the specified range
user_ids = range(args.start, args.end)

# Filter ratings for the specified user IDs
filtered_ratings = ratings[ratings['userId'].isin(user_ids)]

# Format the user nodes
user_nodes = [(int(f"1{user_id}"), f"1{user_id}_") for user_id in user_ids]

# Extract all unique movie IDs from filtered ratings
movie_ids = filtered_ratings['movieId'].unique()
movie_nodes = [(int(f"2{movie_id}"), f"2{movie_id}") for movie_id in movie_ids]

# Format the edges directly from filtered_ratings
edges = [
    (int(f"5{index}"), int(f"1{row['userId']}"), int(f"2{row['movieId']}"), int(row['rating']))
    for index, row in filtered_ratings.iterrows()
]

# Extract unique genres only for movies in the filtered ratings
def extract_genres(genres_str):
    return genres_str.split('|') if pd.notna(genres_str) else []

movies['genres_list'] = movies['genres'].apply(extract_genres)
filtered_movies = movies[movies['movieId'].isin(movie_ids)]
genres = set(genre for genres_list in filtered_movies['genres_list'] for genre in genres_list)
genre_nodes = [(int(f"3{index}"), genre) for index, genre in enumerate(genres, start=1)]

# Map movies to their genres
movie_genre_edges = []
edge_id = 1
for _, row in filtered_movies.iterrows():
    movie_id = row['movieId']
    for genre in row['genres_list']:
        genre_id = next(node[0] for node in genre_nodes if node[1] == genre)
        movie_genre_edges.append((int(f"4{edge_id}"), int(f"2{movie_id}"), genre_id, "empty"))
        edge_id += 1


exist = False
# Write to file
with open(output_file, "w") as file:
    file.write('[\n')

    # Write user nodes
    for node in user_nodes:
        if not exist:
            file.write(f'\t({node[0]}, \"{node[1]}\" # green)\n')
            exist = True
        else:
            file.write(f'\t({node[0]}, \"{node[1]}\")\n')

    # Write movie nodes
    for node in movie_nodes:
        file.write(f'\t({node[0]}, "{node[1]}")\n')

    # Write genre nodes
    for node in genre_nodes:
        file.write(f'\t({node[0]}, "{node[1]}")\n')

    # Separator
    file.write('\t|\n')

    # Write movie-genre edges
    for edge in movie_genre_edges:
        file.write(f'\t({edge[0]}, {edge[1]}, {edge[2]}, {edge[3]})\n')

    # Write user-movie edges
    for edge in edges:
        file.write(f'\t({edge[0]}, {edge[1]}, {edge[2]}, {edge[3]})\n')

    file.write(']')

print(f"Graph saved to {output_file}")
