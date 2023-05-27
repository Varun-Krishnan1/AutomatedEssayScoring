'''
Predicting Rubric Scores of Our Sample Essays using Author's Pre-Trained Models

Change Global Variables depending on which Rubric you would like to evaluate
'''
import csv
import numpy as np
import pandas as pd 
from tensorflow.keras.models import load_model
# --- Global variables ---

## Author Rubric 2 - Organization 
# AUTHOR_RUBRIC_NAME = 'Rubric2'
# MODEL_PATH = "PreTrainedModels/Rubric2train_model5(2019-11-21@21.51.01).hdf5"

## Author Rubric 4 - Conventions 
# AUTHOR_RUBRIC_NAME = 'Rubric4'
# MODEL_PATH = "PreTrainedModels/Rubric4train_model5(2019-11-21@22.48.32).hdf5"

## Author Rubric 3 - Style
# AUTHOR_RUBRIC_NAME = 'Rubric3'
# MODEL_PATH = "PreTrainedModels/Rubric3train_model5(2019-11-21@22.18.57).hdf5"

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
print("Features (X): ")
print(X_our)

# -- Validate Shapes -- 
print(f"X Shape: {X_our.shape}")

# --- Load the saved model --- 
model = load_model(MODEL_PATH)

# --- Predict the scores --- 
predicted_scores = model.predict(X_our)
print("First element of predicted scores: ")
print(predicted_scores[0])

# The raw outputs from the model are probabilities for each score,
# so we need to convert these to actual scores. This can be done by
# choosing the score with the highest probability.
predicted_scores = np.argmax(predicted_scores, axis=1)
print("Predicted Scores:")
print(predicted_scores)
print(f"Predicted Scores: {predicted_scores.shape}")

# --- Save Scores for Analysis --- 

# Save in format 0.txt : pred_score, 7.txt: pred_score, etc... to ensure we now order of scores
acceptable_files = pd.read_csv("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv")
file_names = acceptable_files['filename'].values
essay_to_predicted_scores = {file_names[i]:predicted_scores[i] for i in range(len(file_names))}

header = ['essay', 'pred_score']
save_file = f'PredictedLabels/{AUTHOR_RUBRIC_NAME}EssayToUnMappedPredictedScores.csv'
with open(save_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(essay_to_predicted_scores.items())
