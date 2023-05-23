import numpy as np

N1 = np.loadtxt("AuthorFeaturesFiltered/d7-training-gamet-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,13)))
N2 = np.loadtxt("AuthorFeaturesFiltered/d7-training-seance-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,98)))
N3 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taaco-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,77)))
N4 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taaled-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,15)))
N5 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taales-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,109)))
N6 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,80)))
N7 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-components-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,6)))
N8 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-sca-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,7)))
feature_names = np.concatenate((N1,N2,N3,N4,N5,N6,N7,N8))

feature_dict = {}
for i in range(len(feature_names)):
    feature_dict['x' + str(i)] = feature_names[i]

print(feature_dict)

X1 = np.loadtxt("AuthorFeaturesFiltered/d7-training-gamet-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("AuthorFeaturesFiltered/d7-training-seance-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taaco-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taaled-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taales-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-components-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("AuthorFeaturesFiltered/d7-training-taassc-sca-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)

print(X)
print(X.shape) 