'''
See how well GPT4 did with predictions. Use evaluation function for our model from Kumar et al. 
'''
from pandas import pd


# --- Get Actual Labels --- 

OUR_RUBRIC_NAME = 'Marking Key 2 Score'
Y_all = pd.read_csv("SampleEssayLabels/SampleEssaylabels.csv")
# To get labels we need to read in the corresponding rubric column
Y = Y_all[OUR_RUBRIC_NAME].values

# --- Get GPT Labels --- 
P1 =
P2 =
P3 =
P4 =
P5 =
P6 =
P7 =
P8 =
P9 =
P10 =
P11 =
P12 =
P13 =
P14 =
P15 =

# --- Calculate the Metrics  ---
from sklearn.metrics import classification_report

# Use our evaluate function from our other file and use path append to do this for workaround 
# (ideally would be structured as pkg so wouldn't have to do this)
import sys 
sys.path.insert(1, "../../Model Testing/evaluate_preds.py")
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