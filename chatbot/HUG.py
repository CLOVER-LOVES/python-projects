import random
import csv
import os

# Load verbs from CSV file
def load_verbs():
    verbs = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "verbs.csv")
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            verbs.append(row)  # Each row is [Verb, Meaning, Example]
    return verbs

# Get 10 random verbs
def get_random_verbs():
    verbs = load_verbs()
    return random.sample(verbs, 10)

# Display verbs
for verb in get_random_verbs():
    print(f"Verb: {verb[0]}\nMeaning: {verb[1]}\nExample: {verb[2]}\n")
