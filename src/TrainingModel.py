#We used the following libraries:

#nltk: Natural Language Tool Kit, we used this library for tokenization.
#joblib: we used this library to save the trained classifier models and load it.
#RandomForestClassifier: we used this library to train a "RandomForest" classifier based on our dataset.
#cross_validate: we used this library to apply cross validation approach on any classifier.
#train_test_split: we used this library to split the dataset to train and test datasets.
#accuracy_score: we used this library to get the accuracy score of the trained classifier.
#confusion_matrix: we used this library to print the confusion matrix of the trained model.
#pandas: we used this library to help us with the plotting of the confusion matrix of the trained model.
#numpy: This library used for dealing with numeric values and all the functions which using these values.
#seaborn: This library is a data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.
#matplotlib: This library used for determining the confusin matrix axes.
#SVC: This library used for training "SVM" classifiers.

#We also used the "ResumeHelper" and the "SegementerClassifier" classes that we have created.

import nltk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.svm import SVC

import ResumeHelper
import SegementerClassifier

#This function takes two paramters.
#First paramter is the X_train part of the data.
#Second paramter is the Y_train part of the data.
#It trains a Naive Bayes classifier using the "nltk" library.
#Returns the classifier after it trains it.
def trainNaiveBayesClassifier(X_train, Y_train):
    classifier = nltk.NaiveBayesClassifier.train(ResumeHelper.merge(X_train, Y_train))
    return classifier

#This function takes two paramters.
#First paramter is the model which will be saved.
#Second paramter is the name of that model which will be saved.
#It saves the model which passed as a first paramter with the name which passed as a second paramter using the "joblib" library.
def dumpClassifier(model, model_name):
    joblib.dump(model, "Models/" + model_name + ".pkl")

#This function takes one paramter.
#The paramter is the name of that model which we want to load.
#It loads the model which its name passed as a paramter using the "joblib" library, and returns it.
def loadClassifier(model_name):
    model = joblib.load("Models/" + model_name + ".pkl")
    return model

#This function takes two paramters.
#First paramter is the actual result we have.
#Second paramter is the predicted result.
#It prints the accuracy of the training, in addition to the confusion matrix of the "True label" and "Predicted label" values.
def printConfusionMatrix(y_test, y_test_predict):
    confusion_mat = confusion_matrix(y_test, y_test_predict)
    
    data_frame_confusion_matrix = pd.DataFrame(confusion_mat, index = [i for i in range(0, 13)], columns = [i for i in range(0, 13)])
    plt.figure(figsize = (9.5, 9))
    sns.heatmap(data_frame_confusion_matrix, annot = True)

    plt.title('Accuracy:{0:.3f}'.format(accuracy_score(y_test, y_test_predict)))
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

#This function takes one paramter.
#The paramter is the data we want this function to train the "NaiveBayes" classifier on.
#It trains a "NaiveBayes" classifier on the data passed as a paramter and prints the accuracy and the confusion matrix and saves the model.
def NaiveBayes(data):
    x_data, y_data = SegementerClassifier.splitData(data)
    X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, random_state = 0)

    classifier = trainNaiveBayesClassifier(X_train, y_train)
    accuracy = nltk.classify.accuracy(classifier, ResumeHelper.merge(X_test, y_test))

    y_test_predict = classifier.classify_many(X_test)
    print(accuracy)
    printConfusionMatrix(y_test, y_test_predict)

    dumpClassifier(classifier, "NaiveBayesClassifier")

#This function takes one paramter.
#The paramter is the data we want this function to train the "RandomForest" classifier on.
#It trains a "RandomForest" classifier on the data passed as a paramter and prints the accuracy and the confusion matrix and saves the model.
def RandomForest(data):
    X, Y = SegementerClassifier.prepareDataForTraining(data)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state = 0)

    classifier = RandomForestClassifier(max_features = 'sqrt', n_estimators = 110)
    classifier.fit(X_train, y_train)

    accuracy_score = np.mean(cross_validate(classifier, X_test, y_test, cv = 10)['test_score'])
    print('Accuracy score: ' + str(accuracy_score) + '\n')

    y_test_predict = classifier.predict(X_test)
    printConfusionMatrix(y_test, y_test_predict)

    dumpClassifier(classifier, "RandomForestClassifier")

#This function takes one paramter.
#The paramter is the data we want this function to train the "SVM" classifier on.
#It trains a "SVM" classifier on the data passed as a paramter and prints the accuracy and the confusion matrix and saves the model.
#We trained a "SVM" with the three most important kernels (Linear - RBF - Poly).
#And for each kernel we test a multible values for the paramter "C" (1 - 10 - 100) and a multible values fo the paramter "Gamma" (0.01 - 0.1 - 1 - 10). .
def SVM(data):
    X, Y = SegementerClassifier.prepareDataForTraining(data)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 0)

    kernels = ['linear', 'rbf', 'poly']
    Cs = [1, 10, 100]
    gammas = [0.01, 0.1, 1, 10]

    for kernel in kernels:
        for C in Cs:
            for gamma in gammas:
                classifier = SVC(kernel = kernel, C = C, gamma = gamma).fit(X_train, Y_train)
                accuracy_score=classifier.score(X_test, Y_test)

                print('kernel is: ' + str(kernel))
                print('gamma is: ' + str(gamma))
                print('C is: ' + str(C))
                print('Accuracy score: ' + str(accuracy_score) + '\n')

                y_test_predict = classifier.predict(X_test)
                printConfusionMatrix(Y_test, y_test_predict)

                dumpClassifier(classifier, "SVMClassifier_" + str(kernel) + "_" + str(C) + "_" + str(gamma))




