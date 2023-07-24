import numpy as np
import pandas as pd 
from map_predictions import map_predictions_rubric

# Authors: 
# R1 - Ideas : Is the story told with ideas that are clearly focused on the topic and are thoroughly developed with specific, relevant details?
# R2 - Organization : Are organization and connections between ideas and/or events clear and logically sequenced?
# R3 - Style :Does the command of language, including effective and compelling word choice and varied sentence structure, clearly support the writer’s purpose and audience?
# R4 - Conventions: Is the use of conventions of Standard English for grammar, usage, spelling, capitalization, and punctuation consistent and appropriate for the grade level?

# Ours: 
# R1 - CONTENT: Inclusion and elaboration of ideas and sense of audience and purpose.
# R2 - ORGANISATION: Coherence and cohesion
# R3 - GRAMMAR: Use of syntactic patterns and grammatical accuracy
# R4 - VOCABULARY: Range and appropriateness
# R5 - SPELLING AND PUNCTUATION

# Organization (Rubric 2 - Organization(author) vs Rubric 2 - ORGANIZATION(ours))
AUTHOR_RUBRIC_NAME = 'Rubric2'
OUR_RUBRIC_NAME = 'Marking Key 2 Score'
OUR_RUBRIC_MAX_SCORE = 4

## Grammar (Rubric 4 - Conventions(author) vs Rubric 3 - GRAMMAR(ours))
# AUTHOR_RUBRIC_NAME = 'Rubric4'
# OUR_RUBRIC_NAME = 'Marking Key 3 Score'
# OUR_RUBRIC_MAX_SCORE = 5

## Spelling and Punctuation (Rubric 4 - Conventions(author) vs Rubric 5 - SPELLING AND PUNCTUATION(ours))
# AUTHOR_RUBRIC_NAME = 'Rubric4'
# OUR_RUBRIC_NAME = 'Marking Key 5 Score'
# OUR_RUBRIC_MAX_SCORE = 2

## Style (Rubric 3 - Style(author) vs Rubric 4 - VOCABULARY(ours))
# AUTHOR_RUBRIC_NAME = 'Rubric3'
# OUR_RUBRIC_NAME = 'Marking Key 4 Score'
# OUR_RUBRIC_MAX_SCORE = 5

# --- Get Actual Lables --- 
Y_all = pd.read_csv("SampleEssayLabels/SampleEssaylabels.csv")

# Remove filename labels that are not in the 277 samples (they were filtered out due to TAALED limitatinos)
acceptable_files = pd.read_csv("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv")

# Filter rows in Y_all based on 'filename' column in acceptable_files
Y_filtered = Y_all[Y_all['filename'].isin(acceptable_files['filename'])]

# To get labels we need to read in the corresponding rubric column
Y = Y_filtered[OUR_RUBRIC_NAME].values

print("Y: ")
print(Y)
print(f"New Y Shape: {Y.shape}")

# --- Creating ceiling for our true labels --- 
# Suhaib pointed out there is an error where some labels can be higher than the max 
# possible marking score let's fix this 

# Clip array elements to a maximum of the max rubric score
Y = np.clip(Y, None, OUR_RUBRIC_MAX_SCORE) # arr, min, max 
print("Clipped Y")
print(Y) 

print(f"True Scores (Clipped): {Y}")
print(f"True Scores (Clipped) Shape: {Y.shape}")

# -- Read in Predicted Labels -- 

predicted_label_file = f'PredictedLabels/{AUTHOR_RUBRIC_NAME}EssayToUnMappedPredictedScores.csv'
predicted_scores = pd.read_csv(predicted_label_file)
predicted_scores = predicted_scores['pred_score'].values
# --- Get Statistics for Our Labels ---
# See distribution of our rubric

import matplotlib.pyplot as plt 

# unique, counts = np.unique(Y, return_counts=True)
# plt.bar(unique, counts)
# plt.xlabel('Labels')
# plt.ylabel('Count')
# plt.title('Distribution of Labels')
# plt.show()

# --- Checking Correlation --- 
# Do this before mapping for accurate correlation

import matplotlib.pyplot as plt
# plt.plot(Y)
# plt.plot(predicted_scores)
# plt.show()

correlation = np.corrcoef(Y, predicted_scores)[0, 1] # Organization: r=0.47, Grammar r=0.42, Style = 0.51
print(f"Correlation : {correlation}")

# -- Mapping Predictons ---

mapped_predictions = map_predictions_rubric(predicted_scores, our_max_score=OUR_RUBRIC_MAX_SCORE)
print("Mapped Predictions: ")
print(mapped_predictions)

# Save mapped preditions 
# Save in format 0.txt : pred_score, 7.txt: pred_score, etc... to ensure we know order of scores
import csv
acceptable_files = pd.read_csv("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv")
file_names = acceptable_files['filename'].values
essay_to_predicted_scores = {file_names[i]:mapped_predictions[i] for i in range(len(file_names))}

header = ['essay', 'mapped_pred_score']
save_file = f'PredictedLabels/{AUTHOR_RUBRIC_NAME}EssayTo{OUR_RUBRIC_NAME.replace(" ","")}MappedPredictedScores.csv'
with open(save_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(essay_to_predicted_scores.items())

# --- Evaluating our Mapped Predicted Labels --- 
# Use Metrics from Author's File
# Evaluate vs. a Majority Classifier (Naive Classifier)

# -- Majority Classifier 
from scipy import stats
# Determine the majority class
majority_class = stats.mode(Y)[0][0]
# Create a majority classifier prediction array
majority_predictions = np.full(Y.shape, majority_class)

# --- Calculate the Metrics ---
import metrics # author's file 

from sklearn.metrics import classification_report

def evaluate(actual_labels, predictions, title): 
    print(f"\n---{title}---") 

    print(classification_report(actual_labels, predictions)) 

    # Print the percentage of exact matches (accuracy)
    accuracy = metrics.exact_match(actual_labels, predictions)
    print(f"Accuracy (percentage of exact matches): {accuracy * 100}%")

    # Spot-check validation 
    if AUTHOR_RUBRIC_NAME == 'Rubric2' and title == 'Mapped Prediction Evaluation:':
        assert round(accuracy, ndigits=3) == .390

    # Print the percentage of adjacent matches with distance 1 
    adjacent_accuracy_1 = metrics.adjacent_match(actual_labels, predictions)
    print(f"Percentage of adjacent matches for distance 1: {adjacent_accuracy_1 * 100}%")

    # Print the percentage of adjacent matches with distance 2 
    adjacent_accuracy_2 = metrics.adjacent_match2(actual_labels, predictions)
    print(f"Percentage of adjacent matches for distance 2: {adjacent_accuracy_2 * 100}%")

evaluate(Y, mapped_predictions, title="Mapped Prediction Evaluation:")
evaluate(Y, majority_predictions, title="Majority Classifier Evaluation:")