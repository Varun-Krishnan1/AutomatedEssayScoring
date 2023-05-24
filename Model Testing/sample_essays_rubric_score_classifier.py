import csv
import pprint
import numpy as np
import pandas as pd 
from tensorflow.keras.models import load_model

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

RUBRIC_2 = 'Marking Key 2 Score'
Y_all = pd.read_csv("SampleEssayLabels/SampleEssaylabels.csv")

# To get labels we need to read in rubric 2 column but remove filenames that are not in the 277 
acceptable_files = pd.read_csv("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv")

# Filter rows in Y_all based on 'filename' column in acceptable_files
Y_filtered = Y_all[Y_all['filename'].isin(acceptable_files['filename'])]
print(acceptable_files['filename'])
# Read in Rubric 2 column 
Y = Y_filtered[RUBRIC_2].values

# -- Validate Shapes -- 
print(X_our.shape)
print(Y.shape)

# --- Load the saved model --- 
model_RUBRIC_2 = load_model('PreTrainedModels/train_model5(2019-11-21@21.51.01).hdf5')

# Predict the scores
predicted_scores = model_RUBRIC_2.predict(X_our)

# The raw outputs from the model are probabilities for each score,
# so we need to convert these to actual scores. This can be done by
# choosing the score with the highest probability.
predicted_scores = np.argmax(predicted_scores, axis=1)
print("Predicted Scores:")
print(predicted_scores)

# --- Creating ceiling for our labels --- 
# Suhaib pointed out there is an error where some labels can be higher than the max 
# possible marking score let's fix this 

# Clip array elements to a maximum of 4
Y = np.clip(Y, None, 4) # arr, min, max 
print("Clipped Y")
print(Y) 


# --- Checking Correlation --- 
import matplotlib.pyplot as plt
plt.plot(Y)
plt.plot(predicted_scores)
plt.show()
correlation = np.corrcoef(Y, predicted_scores)[0, 1] # r=0.47
print(f"Correlation : {correlation}")

# --- Save Labels (for manual checking) --- 
file_names = acceptable_files['filename'].values
essay_to_predicted_scores = {file_names[i]:predicted_scores[i] for i in range(len(file_names))}
save_file = 'PredictedLabels/Rubric2/EssayToPredictedScores.csv'
with open(save_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(essay_to_predicted_scores.items())

# --- Heuristic Mapping of Labels to Predicted Scores --- 

# Our max marking key for organization is a score of 4  
# Their max marking key for organization is a score of 6 
# Our Key : Their Key 
# 1       : 1
# 2       : 2
# 3       : 3-4
# 4       : 5-6
# macro avg       0.31, weighted avg       0.47      
# Our Key : Their Key 
# 1       : 1,2
# 2       : 3
# 3       : 4
# 4       : 5,6
# macro avg       0.32, weighted avg       0.40 


def map_predictions(predictions):
    mapped_predictions = []
    for prediction in predictions:
        if prediction in [1,2]:
            mapped_predictions.append(1)
        elif prediction in [3]:
            mapped_predictions.append(2)
        elif prediction in [4]:
            mapped_predictions.append(3)
        elif prediction in [5,6]:
            mapped_predictions.append(4)
    return mapped_predictions

mapped_predictions = map_predictions(predicted_scores)
print("Mapped Predictions: ")
print(mapped_predictions)

# Evaluating our Heuristic Mapped Labels 
from sklearn.metrics import classification_report

print(classification_report(Y, mapped_predictions)) 

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
