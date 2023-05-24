'''
This Script was modified from their rubric_score_classifier.py and just ensures that we have the same feature names as them for the model

The variables feature_names_author vs feature_names_our stores the author's selected feature names vs ours as values. When comparing the 
two dictionaries we confirm they are equal

WE also confirm the shape (397 features) are equal between both the author and us
'''

import numpy as np

N1 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-gamet-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,13)))
N2 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-seance-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,98)))
N3 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taaco-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,77)))
N4 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taaled-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,15)))
N5 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taales-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,109)))
N6 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,80)))
N7 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-components-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,6)))
N8 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-sca-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,7)))
feature_names_author = np.concatenate((N1,N2,N3,N4,N5,N6,N7,N8))

feature_dict_author = {}
for i in range(len(feature_names_author)):
    feature_dict_author['x' + str(i)] = feature_names_author[i]

X1 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-gamet-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-seance-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taaco-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taaled-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taales-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-components-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("../Feature Selection/AuthorFeaturesFiltered/d7-training-taassc-sca-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X_author = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)

N1 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,13)))
N2 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-seance-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,98)))
N3 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaco-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,77)))
N4 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaled-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,15)))
N5 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taales-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,109)))
N6 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taassc-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,80)))
N7 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-components-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,6)))
N8 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-sca-filtered-ordered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,7)))
feature_names_our = np.concatenate((N1,N2,N3,N4,N5,N6,N7,N8))

feature_dict_our = {}
for i in range(len(feature_names_our)):
    # Remove quotation marks for our dataset 
    feature_dict_our['x' + str(i)] = feature_names_our[i]

X1 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-gamet-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-seance-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaco-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taaled-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taales-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-taassc-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-components-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/Cheating-SampleEssays-sca-filtered-ordered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X_our = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)

print(X_author.shape)
print(X_our.shape) 
assert feature_dict_author == feature_dict_our

# print(feature_dict_author == feature_dict_our) 
# for key, value in feature_dict_author.items():
#     if value != feature_dict_our[key]:
#         print(value, feature_dict_our[key])

# Ensure the feature names are in the same order as well 
assert np.array_equal(feature_dict_author.keys(), feature_dict_author.keys())

# print(X_author[:,-1]) # Look at last file to spot-check
# print(X_our) # Normalized


