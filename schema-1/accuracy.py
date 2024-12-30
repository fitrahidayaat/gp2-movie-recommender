import pandas as pd
import re

# Read ratings.csv
ratings_df = pd.read_csv('../data/test_ratings.csv')  # Assuming 'ratings.csv' has columns: userId, movieId, rating

# Read the output file
with open('gp2.output', 'r') as output_file:
    content_file = output_file.read()

# Extract the part after the '|' symbol
content_after_pipe = content_file.split('|')[1].strip()

# Use regex to find all the tuples in the extracted content
pattern = r'\((\d+), (\d+), (\d+), "(\S+)"\)'  # Assuming the format (user_id, movie_id, x, "y_z")
matches = re.findall(pattern, content_after_pipe)

# Convert matches to a list of tuples
gp2_tuples = [(int(x[0]), int(x[1]), int(x[2]), x[3]) for x in matches]

# Process each tuple to get the user and movie recommendation
processed_tuples = []
user_ids_with_recommendations = set()

for tup in gp2_tuples:
    last_element = tup[-1]
    split_elements = last_element.split('_')
    result_tuple = (int(split_elements[0][1:]), int(split_elements[1][1:]))  # Extract the last part and remove the first digit
    processed_tuples.append(result_tuple)
    user_ids_with_recommendations.add(result_tuple[0])  # Track users who have recommendations

# Prepare to calculate TP, FP, FN, TN
TP = FP = FN = TN = 0

# Iterate only over users who are in the gp2_tuples
for user_id in user_ids_with_recommendations:
    # Get all rated movies for the current user
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    rated_movies_with_good_rating = user_ratings[user_ratings['rating'] >= 80]['movieId'].values
    rated_movies_with_bad_rating = user_ratings[user_ratings['rating'] < 80]['movieId'].values

    # Get the recommended movies for the current user
    recommended_movies = [movie_id for u_id, movie_id in processed_tuples if u_id == user_id]

    # True Positives (TP): Recommended movies that are rated good
    TP += len(set(recommended_movies) & set(rated_movies_with_good_rating))

    # False Positives (FP): Recommended movies that are rated bad
    FP += len(set(recommended_movies) & set(rated_movies_with_bad_rating))

    # False Negatives (FN): Movies that are rated good but not recommended
    FN += len(set(rated_movies_with_good_rating) - set(recommended_movies))

    # True Negatives (TN): Movies that are rated bad and not recommended
    TN += len(set(rated_movies_with_bad_rating) - set(recommended_movies))

# Calculate accuracy
accuracy = (TP + TN) / (TP + FP + FN + TN)

# Calculate precision
precision = TP / (TP + FP) if (TP + FP) != 0 else 0

# Calculate recall
recall = TP / (TP + FN) if (TP + FN) != 0 else 0

# Calculate F1-score
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

# Display the results
print(f'True Positives (TP): {TP}')
print(f'False Positives (FP): {FP}')
print(f'False Negatives (FN): {FN}')
print(f'True Negatives (TN): {TN}')
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1-Score: {f1_score:.4f}')