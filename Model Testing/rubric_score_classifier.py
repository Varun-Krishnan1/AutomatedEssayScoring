# import the necessary packages
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, train_test_split, validation_curve, learning_curve, ShuffleSplit, cross_val_score, KFold
from sklearn.metrics import make_scorer, classification_report
from sklearn.metrics import confusion_matrix as cm
from sklearn.manifold import LocallyLinearEmbedding, TSNE
from sklearn.ensemble import AdaBoostClassifier
from metrics import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from keras.models import Sequential, Model, load_model
from keras.layers.core import Dense, Dropout
from keras.layers import BatchNormalization, Input
from keras.regularizers import l2, l1, l1_l2
from keras.callbacks import ModelCheckpoint, EarlyStopping
from eli5.sklearn import PermutationImportance
import eli5
from random import sample
from datetime import datetime


timestamp = datetime.now().strftime("(%Y-%m-%d@%H.%M.%S)")
logs = pd.DataFrame(columns=['phase', 'iteration', 'loss', 'qwk', 'exact', 'adj', 'adj2'])
MIN_SCORE = 0
MAX_SCORE = 6


def aes():
    l1_rate = 0.0095
    l2_rate = 0.0035
    initializer='glorot_normal'
    activation='selu'
    optimizer='SGD'
    model = Sequential()
    model.add(BatchNormalization(input_shape=(397,)))
    model.add(Dense(397, kernel_initializer=initializer, kernel_regularizer=l1_l2(l1=l1_rate, l2=l2_rate), activation=activation))
    model.add(Dense(16, kernel_initializer=initializer, kernel_regularizer=l1_l2(l1=l1_rate, l2=l2_rate), activation=activation))
    model.add(Dense(MAX_SCORE-MIN_SCORE+1, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    return model


def log(phase, iteration, human_scores, machine_scores, loss=float('NaN')):
    global logs
    entry = {
        'phase': phase, 
        'iteration': iteration,
        'loss': loss, 
        'qwk': quadratic_weighted_kappa(rater_a=machine_scores, rater_b=human_scores,min_rating=MIN_SCORE, max_rating=MAX_SCORE),
        'exact': exact_match(rater_a=machine_scores, rater_b=human_scores),
        'adj': adjacent_match(rater_a=machine_scores, rater_b=human_scores),
        'adj2': adjacent_match2(rater_a=machine_scores, rater_b=human_scores)
    }
    print(entry)
    logs = logs.append(entry, ignore_index=True)


RUBRIC_1 = 11
RUBRIC_2 = 12
RUBRIC_3 = 13
RUBRIC_4 = 14
HOLISTIC = 15

ITERATIONS = 5

EPOCHS = 1000
BATCH_SIZE = 128
TEST_SIZE = 0.20
VAL_SIZE = 0.15
N_SPLITS = 5

N1 = np.loadtxt("../data/d7-training-gamet-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,13)))
N2 = np.loadtxt("../data/d7-training-seance-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,98)))
N3 = np.loadtxt("../data/d7-training-taaco-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,77)))
N4 = np.loadtxt("../data/d7-training-taaled-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,15)))
N5 = np.loadtxt("../data/d7-training-taales-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,109)))
N6 = np.loadtxt("../data/d7-training-taassc-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,80)))
N7 = np.loadtxt("../data/d7-training-taassc-components-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,6)))
N8 = np.loadtxt("../data/d7-training-taassc-sca-filtered.csv", dtype='str', delimiter=',', max_rows=1, usecols=tuple(range(1,7)))
feature_names = np.concatenate((N1,N2,N3,N4,N5,N6,N7,N8))

feature_dict = {}
for i in range(len(feature_names)):
    feature_dict['x' + str(i)] = feature_names[i]

X1 = np.loadtxt("../data/d7-training-gamet-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,13)))
X2 = np.loadtxt("../data/d7-training-seance-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,98)))
X3 = np.loadtxt("../data/d7-training-taaco-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,77)))
X4 = np.loadtxt("../data/d7-training-taaled-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,15)))
X5 = np.loadtxt("../data/d7-training-taales-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,109)))
X6 = np.loadtxt("../data/d7-training-taassc-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,80)))
X7 = np.loadtxt("../data/d7-training-taassc-components-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,6)))
X8 = np.loadtxt("../data/d7-training-taassc-sca-filtered.csv", dtype='float', delimiter=',', skiprows=1, usecols=tuple(range(1,7)))
X = np.concatenate((X1,X2,X3,X4,X5,X6,X7,X8), axis=1)
Y = np.loadtxt("../data/d7-training-grades.csv", dtype='int64', delimiter=',', skiprows=1, usecols=RUBRIC_1)

lb = LabelBinarizer()
Y = lb.fit_transform(Y)

# class_weights = np.log2(float(len(Y))/np.bincount(Y))
# class_weights = float(len(Y))/np.bincount(Y)
# class_weight_dict = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1}
class_weight_dict = None
# class_weight_dict = {}
# for i in range(len(class_weights)):
#     class_weight_dict[i] = class_weights[i]

es_callback = EarlyStopping(monitor='val_loss', min_delta=0.01, patience=100, verbose=1)

for ith_iteration in range(1, ITERATIONS+1):
    print("Iteration " + str(ith_iteration) + " out of " + str(ITERATIONS))
    (trainX, testX, trainY, testY) = train_test_split(X, Y, test_size=TEST_SIZE, random_state=123)
    (train_subsetX, valX, train_subsetY, valY) = train_test_split(trainX, trainY, test_size=VAL_SIZE)

    train_model = aes()
    train_checkpoint = ModelCheckpoint('../model/train_model' + str(ith_iteration) + timestamp + '.hdf5', monitor='val_loss', verbose=1, save_best_only=True)
    train_hist = train_model.fit(train_subsetX, train_subsetY, validation_data=(valX, valY), epochs=EPOCHS, batch_size=BATCH_SIZE, class_weight=class_weight_dict, callbacks=[train_checkpoint, es_callback], verbose=2)
    train_model = load_model('../model/train_model' + str(ith_iteration) + timestamp + '.hdf5')
    train_loss = train_model.evaluate(train_subsetX, train_subsetY, verbose=0)
    machine_scores = train_model.predict(train_subsetX, batch_size=BATCH_SIZE)
    machine_scores = lb.inverse_transform(machine_scores)
    
    human_scores = lb.inverse_transform(train_subsetY)

    log(phase='training', iteration=ith_iteration, human_scores=human_scores, machine_scores=machine_scores, loss=train_loss[0])

    # Manual cross-validation
    # kfold = KFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    kfold = KFold(n_splits=N_SPLITS, shuffle=True)
    val_loss = np.zeros(EPOCHS, dtype=np.float32)
    train_ensemble_predictions = np.zeros(trainX.shape[0], dtype=np.float32)
    test_ensemble_predictions = np.zeros(testX.shape[0], dtype=np.float32)
    ith_fold = 0
    for train, test in kfold.split(trainX, trainY):
        ith_fold = ith_fold + 1
        cv_model = aes()
        cv_checkpoint = ModelCheckpoint('../model/cv' + str(ith_iteration) + str(ith_fold) + timestamp + '.hdf5', monitor='val_loss', verbose=1, save_best_only=True)
        cv_hist = cv_model.fit(trainX[train], trainY[train], validation_data=(trainX[test], trainY[test]), epochs=EPOCHS, batch_size=BATCH_SIZE, class_weight=class_weight_dict, callbacks=[cv_checkpoint, es_callback], verbose=2)
        cv_model = load_model('../model/cv' + str(ith_iteration) + str(ith_fold) + timestamp + '.hdf5')
        cv_loss = cv_model.evaluate(trainX[test], trainY[test], verbose=0)
        machine_scores = cv_model.predict(trainX[test], batch_size=BATCH_SIZE)
        machine_scores = lb.inverse_transform(machine_scores)
        
        human_scores = lb.inverse_transform(trainY[test])

        log(phase='cv', iteration=ith_iteration, human_scores=human_scores, machine_scores=machine_scores, loss=cv_loss[0])

        # val_loss = val_loss + cv_hist.history["val_loss"]

        predictions = cv_model.predict(trainX, batch_size=BATCH_SIZE)
        train_ensemble_predictions = train_ensemble_predictions + lb.inverse_transform(predictions)
        
        predictions = cv_model.predict(testX, batch_size=BATCH_SIZE)
        test_ensemble_predictions = test_ensemble_predictions + lb.inverse_transform(predictions)

        # Shows training and validation loss curves
        # plt.style.use("ggplot")
        # plt.figure()
        # plt.plot(np.arange(0, len(train_hist.history["loss"])), train_hist.history["loss"], label="train_loss")
        # plt.plot(np.arange(0, len(cv_hist.history["val_loss"])), cv_hist.history["val_loss"], label="val_loss (cv)")
        # plt.title("Training/Validation Loss")
        # plt.xlabel("Epoch #")
        # plt.ylabel("Loss")
        # plt.ylim((0, 5))
        # plt.legend()
        # plt.show()

    # val_loss = val_loss / float(N_SPLITS)

    # Shows training and validation loss curves
    # plt.style.use("ggplot")
    # plt.figure()
    # plt.plot(np.arange(0, EPOCHS), train_hist.history["loss"], label="train_loss")
    # plt.plot(np.arange(0, EPOCHS), val_loss, label="val_loss (cv)")
    # plt.title("Training/Validation Loss")
    # plt.xlabel("Epoch #")
    # plt.ylabel("Loss")
    # plt.ylim((0, 5))
    # plt.legend()
    # plt.show()
    
    train_ensemble_predictions = np.rint(train_ensemble_predictions / float(N_SPLITS))

    human_scores = lb.inverse_transform(trainY)
    log(phase='training_ensemble', iteration=ith_iteration, human_scores=human_scores, machine_scores=train_ensemble_predictions)

    test_ensemble_predictions = np.rint(test_ensemble_predictions / float(N_SPLITS))
    human_scores = lb.inverse_transform(testY)
    log(phase='testing_ensemble', iteration=ith_iteration, human_scores=human_scores, machine_scores=test_ensemble_predictions)

    # Evaluating training model (not CV) on testing set
    machine_scores = train_model.predict(testX)
    machine_scores = lb.inverse_transform(machine_scores)
    testing_loss = train_model.evaluate(testX, testY, verbose=0)
    human_scores = lb.inverse_transform(testY)
    log(phase='testing', iteration=ith_iteration, human_scores=human_scores, machine_scores=machine_scores, loss=testing_loss[0])

# Prints logs to files
logs.to_csv('../log/performance_raw' + timestamp + '.csv', index=False)
logs.groupby(['phase', 'iteration']).mean().reset_index().to_csv('../log/performance_val' + timestamp + '.csv', index=False)
logs.groupby('phase').mean().reset_index().to_csv('../log/performance_avg' + timestamp + '.csv', index=False)

# Feature importance
qwk = make_scorer(quadratic_weighted_kappa, greater_is_better=True)
exact = make_scorer(exact_match, greater_is_better=True)
adj = make_scorer(adjacent_match, greater_is_better=True)
adj2 = make_scorer(adjacent_match2, greater_is_better=True)

(trainX, testX, trainY, testY) = train_test_split(X, Y, test_size=TEST_SIZE, random_state=123)
(train_subsetX, valX, train_subsetY, valY) = train_test_split(trainX, trainY, test_size=VAL_SIZE)

feature_importance_model = KerasClassifier(aes)
es_callback = EarlyStopping(monitor='val_loss', min_delta=0.01, patience=50, verbose=1)
feature_importance_model.fit(train_subsetX, train_subsetY, validation_data=(valX, valY), epochs=EPOCHS, batch_size=BATCH_SIZE, class_weight=class_weight_dict, callbacks=[es_callback], verbose=2)
predictions = feature_importance_model.predict(testX, batch_size=BATCH_SIZE)
perm = PermutationImportance(feature_importance_model, scoring=exact, cv='prefit').fit(testX, lb.inverse_transform(testY))
feature_importance = eli5.explain_weights_df(perm)
feature_importance = feature_importance.replace(to_replace=feature_dict, value=None)
feature_importance.to_csv('../log/feature_importance' + timestamp + '.csv', index=True)
np.savetxt('../log/confusion_matrix' + timestamp + '.csv', cm(lb.inverse_transform(testY), predictions), delimiter=',')
with open('../log/classification_report' + timestamp + '.txt', 'w') as file:
    file.write(classification_report(lb.inverse_transform(testY), predictions))
