'''
Predicting Rubric Scores of Our Sample Essays using Author's Pre-Trained Models

Change Global Variables depending on which Rubric you would like to evaluate
'''
import csv
import pprint
import numpy as np
import pandas as pd 
from tensorflow.keras.models import load_model
import map_predictions 
# --- Global variables ---

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

## Organization (Organization(author) vs ORGANIZATION(ours))
AUTHOR_RUBRIC_NAME = 'Rubric2'
OUR_RUBRIC_NAME = 'Marking Key 2 Score'
MODEL_PATH = "PreTrainedModels/Rubric2/train_model5(2019-11-21@21.51.01).hdf5"
OUR_RUBRIC_MAX_SCORE = 4

## Grammar (Conventions(author) vs GRAMMAR(ours))
# AUTHOR_RUBRIC_NAME = 'Rubric4'
# OUR_RUBRIC_NAME = 'Marking Key 3 Score'
# OUR_RUBRIC_MAX_SCORE = 5
# MODEL_PATH = "PreTrainedModels/Rubric4/train_model5(2019-11-21@22.48.32).hdf5"

## Style (Style(author) vs VOCABULARY(ours))
# AUTHOR_RUBRIC_NAME = 'Rubric3'
# OUR_RUBRIC_NAME = 'Marking Key 4 Score'
# OUR_RUBRIC_MAX_SCORE = 5
# MODEL_PATH = "PreTrainedModels/Rubric3/train_model5(2019-11-21@22.18.57).hdf5"

# --- Get Features --- 

# Using the way their way of creating the input array 
X1 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-seance-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaco-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaled-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taales-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taassc-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-components-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-sca-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X_our = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)
print(X_our)

# --- Get Labels ---
Y_all = pd.read_csv("SampleEssayLabels/SampleEssaylabels.csv")

# To get labels we need to read in the corresponding rubric column but remove filenames that are not in the 277 
acceptable_files = pd.read_csv("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv")

# Filter rows in Y_all based on 'filename' column in acceptable_files
Y_filtered = Y_all[Y_all['filename'].isin(acceptable_files['filename'])]
print(acceptable_files['filename'])
# Read in Rubric 2 column 
Y = Y_filtered[OUR_RUBRIC_NAME].values

# -- Validate Shapes -- 
print(X_our.shape)
print(Y.shape)
print("Unclipped Y:")
print(Y)

# --- Load the saved model --- 
model = load_model(MODEL_PATH)

# Predict the scores
predicted_scores = model.predict(X_our)
print(predicted_scores[0])

# The raw outputs from the model are probabilities for each score,
# so we need to convert these to actual scores. This can be done by
# choosing the score with the highest probability.
predicted_scores = np.argmax(predicted_scores, axis=1)
print("Predicted Scores:")
print(predicted_scores)

# --- Creating ceiling for our labels --- 
# Suhaib pointed out there is an error where some labels can be higher than the max 
# possible marking score let's fix this 

# Clip array elements to a maximum of the max rubric score
Y = np.clip(Y, None, OUR_RUBRIC_MAX_SCORE) # arr, min, max 
print("Clipped Y")
print(Y) 


# --- Checking Correlation --- 
import matplotlib.pyplot as plt
# plt.plot(Y)
# plt.plot(predicted_scores)
# plt.show()

# See distribution of our rubric
unique, counts = np.unique(Y, return_counts=True)

plt.bar(unique, counts)
plt.xlabel('Labels')
plt.ylabel('Count')
plt.title('Distribution of Labels')
plt.show()


correlation = np.corrcoef(Y, predicted_scores)[0, 1] # Organization: r=0.47, Grammar r=0.42, Style = 0.51
print(f"Correlation : {correlation}")

# --- Save Labels (for manual checking) --- 
file_names = acceptable_files['filename'].values
essay_to_predicted_scores = {file_names[i]:predicted_scores[i] for i in range(len(file_names))}
save_file = f'PredictedLabels/{AUTHOR_RUBRIC_NAME}/EssayToPredictedScores.csv'
with open(save_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(essay_to_predicted_scores.items())

mapped_predictions = map_predictions.map_predictions_rubric(predicted_scores, our_max_score=OUR_RUBRIC_MAX_SCORE)
print("Mapped Predictions: ")
print(mapped_predictions)

# Evaluating our Heuristic Mapped Labels 
from sklearn.metrics import classification_report, accuracy_score

print(classification_report(Y, mapped_predictions)) 

# Print the percentage of exact matches (accuracy)
accuracy = accuracy_score(Y, mapped_predictions)
print(f"Accuracy (percentage of exact matches): {accuracy * 100}%")

assert round(accuracy, ndigits=3) == .390
# Function to calculate percentage of adjacent matches
def calculate_adjacent_accuracy(y_true, y_pred, distance=1):
    return np.mean(np.abs(np.array(y_true) - np.array(y_pred)) <= distance)

# Print the percentage of adjacent matches for distance 1 and 2
adjacent_accuracy_1 = calculate_adjacent_accuracy(Y, mapped_predictions, distance=1)
print(f"Percentage of adjacent matches for distance 1: {adjacent_accuracy_1 * 100}%")

adjacent_accuracy_2 = calculate_adjacent_accuracy(Y, mapped_predictions, distance=2)
print(f"Percentage of adjacent matches for distance 2: {adjacent_accuracy_2 * 100}%")

from scipy import stats

# Determine the majority class
majority_class = stats.mode(Y)[0][0]

# Create a majority classifier prediction array
majority_predictions = np.full(Y.shape, majority_class)

# Print the confusion matrix
print(classification_report(Y, majority_predictions))

# Print the percentage of exact matches (accuracy)
accuracy = accuracy_score(Y, majority_predictions)
print(f"Majority Classifier Accuracy (percentage of exact matches): {accuracy * 100}%")

# Print the percentage of adjacent matches for distance 1 and 2
adjacent_accuracy_1 = calculate_adjacent_accuracy(Y, majority_predictions, distance=1)
print(f"Majority Classifier Percentage of adjacent matches for distance 1: {adjacent_accuracy_1 * 100}%")

adjacent_accuracy_2 = calculate_adjacent_accuracy(Y, majority_predictions, distance=2)
print(f"Majority Classifier Percentage of adjacent matches for distance 2: {adjacent_accuracy_2 * 100}%")

# --- Clipping of Predicted Scores --- 

# Our max marking key for organization is a score of 4  
# Their max marking key for organization is a score of 6 
# Our Key : Their Key 
# 1       : 1
# 2       : 2
# 3       : 3
# 4       : 4,5,6

# def clip_predictions(predictions):
#     clipped_predictions = []
#     for prediction in predictions:
#         if prediction in [1]:
#             clipped_predictions.append(1)
#         elif prediction == 2:
#             clipped_predictions.append(2)
#         elif prediction in [3]:
#             clipped_predictions.append(3)
#         elif prediction in [4, 5, 6]:
#             clipped_predictions.append(4)
#     return clipped_predictions

# clipped_predictions = clip_predictions(predicted_scores)
# print("Clipped Predictions: ")
# print(clipped_predictions)

# # Evaluating our Clipped Labels 

# print(classification_report(Y, clipped_predictions)) 
