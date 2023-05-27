'''
See how well GPT4 did with predictions. Use evaluation function for our model from Kumar et al. 
'''
import pandas as pd
import numpy as np 


# --- Get Actual Labels --- 

OUR_RUBRIC_NAME = 'Marking Key 3 Score'
Y_all = pd.read_csv("../../Model Testing/SampleEssayLabels/SampleEssaylabels.csv")
# To get labels we need to read in the corresponding rubric column
Y = Y_all[OUR_RUBRIC_NAME].values

# --- Get GPT Labels --- 
P1 = [5, 1, 1, 3, 2, 1, 1, 4, 3, 3, 4, 4, 2, 3, 2, 4, 5, 4, 5, 4]
P2 = [3, 2, 1, 2, 2, 2, 2, 3, 1, 2, 4, 2, 2, 1, 3, 1, 2, 2, 3, 2]
P3 = [3, 2, 4, 3, 4, 3, 2, 3, 2, 3, 3, 2, 4, 3, 1, 3, 2, 4, 3, 4]
P4 = [2, 4, 4, 3, 1, 3, 2, 3, 1, 3, 2, 2, 4, 1, 1, 2, 2, 2, 3, 3]
P5 = [4, 4, 3, 3, 3, 2, 4, 2, 3, 2, 3, 3, 3, 3, 2, 2, 4, 3, 2, 4]
P6 = [3, 4, 2, 1, 4, 2, 3, 1, 3, 1, 3, 2, 1, 3, 2, 2, 3, 3, 2, 2]
P7 = [5, 4, 3, 3, 4, 1, 2, 4, 3, 4, 2, 3, 4, 4, 3, 3, 4, 3, 2, 3]
P8 = [2, 4, 2, 4, 4, 5, 1, 3, 2, 3, 4, 2, 1, 3, 2, 1, 3, 2, 3, 2]
P9 = [4, 3, 3, 2, 2, 2, 3, 3, 2, 2, 4, 1, 2, 3, 3, 1, 2, 2, 2, 2]
P10 =[5, 4, 4, 3, 2, 3, 2, 3, 3, 3, 2, 2, 1, 1, 2, 3, 1, 4, 2, 3]
P11 =[3, 4, 2, 1, 2, 1, 4, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 3, 1, 2]
P12 =[3, 3, 4, 2, 2, 2, 3, 4, 1, 2, 3, 3, 2, 3, 1, 2, 1, 3, 1, 4]
P13 =[3, 2, 2, 3, 3, 2, 3, 4, 2, 2, 4, 4, 3, 2, 4, 3, 2, 3, 2, 3]
P14 =[3, 4, 1, 2, 2, 3, 3, 2, 3, 2, 3, 2, 3, 1, 1, 3, 2, 2, 3, 4]
P15 =[3, 2, 4, 1, 1, 3, 1, 1, 2, 1, 2, 2, 2, 4]
gpt_preds = np.concatenate([P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P4, P15])
print(gpt_preds.shape)
print(Y.shape)
# --- Calculate the Metrics  ---
from sklearn.metrics import classification_report

# Use our evaluate function from our other file and use path append to do this for workaround 
# (ideally would be structured as pkg so wouldn't have to do this)
import sys 
sys.path.append("../../Model Testing/")
import metrics

def evaluate(actual_labels, predictions, title): 
    print(f"\n---{title}---") 

    print(classification_report(actual_labels, predictions)) 

    # Print the percentage of exact matches (accuracy)
    accuracy = metrics.exact_match(actual_labels, predictions)
    print(f"Accuracy (percentage of exact matches): {accuracy * 100}%")

    # Print the percentage of adjacent matches with distance 1 
    adjacent_accuracy_1 = metrics.adjacent_match(actual_labels, predictions)
    print(f"Percentage of adjacent matches for distance 1: {adjacent_accuracy_1 * 100}%")

    # Print the percentage of adjacent matches with distance 2 
    adjacent_accuracy_2 = metrics.adjacent_match2(actual_labels, predictions)
    print(f"Percentage of adjacent matches for distance 2: {adjacent_accuracy_2 * 100}%")

evaluate(Y, gpt_preds, title="Mapped Prediction Evaluation:")