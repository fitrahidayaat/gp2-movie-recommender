#!/bin/bash

# Loop from 6 to 51 for the 'end' parameter
for end in {3..21..1}; do
    user=$((end-1))
    echo "Running Python script with --start 1 --end $end..."
    python3 main.py --start 1 --end $end

    # Add separator for recommender.gp2
    echo -e "recommender $user user" >> result.txt
    echo "Running gp2c with recommender.gp2 for --end $end..."
    { time gp2c recommender.gp2 graph.host > /dev/null; } 2>> result.txt

    # Add separator for recommender_rooted.gp2
    echo -e "\nrecommender_rooted $user user" >> result.txt
    echo "Running gp2c with recommender_rooted.gp2 for --end $end..."
    { time gp2c recommender_rooted.gp2 graph.host > /dev/null; } 2>> result.txt
    echo -e "\n" >> result.txt

    # Run accuracy.py and append its output to result.txt
    echo "Calculating accuracy for recommender_rooted.gp2..."
    python3 accuracy.py >> result.txt
    echo -e "==================================================" >> result.txt

    echo "Completed iteration for --end $end."
done

echo "All tasks completed. Results appended to result.txt."
