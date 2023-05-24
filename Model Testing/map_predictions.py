'''
This script has functions for mapping predicted lables to the range of our rubric scores
'''

# --- Heuristic Mapping of Labels to Predicted Scores --- 

# Organization Rubric: 
# Our range is [1,4]
# Their range is [0,6]     
# Our Key : Their Key 
# 1       : 0,1
# 2       : 2,3
# 3       : 4
# 4       : 5,6
# macro avg       0.30, weighted avg       0.45 
# Our Key : Their Key 
# 1       : 0,1
# 2       : 2
# 3       : 3,4
# 4       : 5,6
# macro avg       0.31, weighted avg       0.47

# Grammar Rubric: 
# Our range is [1,5]
# Their range is [0,6] 
# Our Key : Their Key 
# 1       : 0,1
# 2       : 2
# 3       : 3
# 4       : 4
# 5       : 5,6
# macro avg       .21, weighted avg .35    
# # Our Key : Their Key 
# 1       : 0,1,2
# 2       : 3
# 3       : 4
# 4       : 5
# 5       : 6
# macro avg       .25, weighted avg .36    

# Style Rubric: 
# Our range is [1,5]
# Their range is [0,6]  
# # Our Key : Their Key 
# 1       : 0,1,2
# 2       : 3
# 3       : 4
# 4       : 5
# 5       : 6
# macro avg       .24, weighted avg .45  

def map_predictions_rubric(predictions, our_max_score):
    mapping = {} 
    if our_max_score == 4:
        mapping = {
            0: 1,
            1: 1,
            2: 2,
            3: 3,
            4: 3,
            5: 4,
            6: 4
        }
    elif our_max_score == 5:
        mapping = {
            0: 1,
            1: 1,
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5
        }
    else:
        raise ValueError("our_max_score out of range!")
    
    mapped_predictions = [mapping[prediction] for prediction in predictions]
    return mapped_predictions
