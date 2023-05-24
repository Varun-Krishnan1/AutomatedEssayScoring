import numpy as np 
from tensorflow.keras.models import load_model

X1 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-gamet-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-seance-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-taaco-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-taaled-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-taales-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-taassc-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-components-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/Cheating-SampleEssays-sca-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X_our = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)

# Load the saved model
# model_RUBRIC_2 = load_model('PreTrainedModels/train_model5(2019-11-21@21.51.01).hdf5')

# Predict the scores
# predicted_scores = model_RUBRIC_2.predict(X_our)

# The raw outputs from the model are probabilities for each score,
# so we need to convert these to actual scores. This can be done by
# choosing the score with the highest probability.
# predicted_scores = np.argmax(predicted_scores, axis=1)


