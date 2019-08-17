import ResumeHelper
import SegementerClassifier
import nltk
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_validate,train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,confusion_matrix
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.svm import SVC

def TrainNaiveBayesClassifier(X_train,y_train):
    classifier=nltk.NaiveBayesClassifier.train(ResumeHelper.merge(X_train,y_train))
    return classifier


def dumpClassifier(model,model_name):
    joblib.dump(model, "Models/"+model_name+".pkl")

def loadClassifier(model_name):
    model = joblib.load("Models/"+model_name+".pkl")
    return model

def print_confusion_matrix(y_test,y_test_predict):
    confusion_mc = confusion_matrix(y_test, y_test_predict)
    df_cm = pd.DataFrame(confusion_mc, index = [i for i in range(0,13)],columns = [i for i in range(0,13)])
    plt.figure(figsize = (9.5,9))
    sns.heatmap(df_cm, annot=True)
    plt.title('Accuracy:{0:.3f}'.format(accuracy_score(y_test,y_test_predict)))
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def NaiveBayes(data):
    x_data,y_data=SegementerClassifier.splitdata(data)
    X_train, X_test, y_train, y_test = train_test_split(x_data,y_data, random_state=0)
    classifier=TrainNaiveBayesClassifier(X_train,y_train)
    accuracy=nltk.classify.accuracy(classifier,ResumeHelper.merge(X_test,y_test))
    y_test_predict = classifier.classify_many(X_test)
    print(accuracy)
    print_confusion_matrix(y_test,y_test_predict)
    dumpClassifier(classifier,"NaiveBayesClassifier")

def RandomForest(data):
    X,Y=SegementerClassifier.prepare_data_for_training(data)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=0)
    classifier=RandomForestClassifier(max_features='sqrt', n_estimators=110)
    classifier.fit(X_train,y_train)
    accuracy_score = np.mean(cross_validate(classifier, X_test,y_test, cv=10)['test_score'])
    print('Accuracy score: ' + str(accuracy_score) + '\n')
    y_test_predict = classifier.predict(X_test)
    print_confusion_matrix(y_test,y_test_predict)
    dumpClassifier(classifier,"RandomForestClassifier")

def SVM(data):
    X,Y=SegementerClassifier.prepare_data_for_training(data)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=0)
    kernels=['linear','rbf','poly']
    Cs=[1,10,100]
    gammas=[0.01,0.1,1,10]
    for kernel in kernels:
        for C in Cs:
            for gamma in gammas:
                classifier=SVC(kernel=kernel, C=C,gamma=gamma).fit(X_train,y_train)
                accuracy_score=classifier.score(X_test, y_test)
                print('kernel is: ' + str(kernel))
                print('gamma is: ' + str(gamma))
                print('C is: ' + str(C))
                print('Accuracy score: ' + str(accuracy_score) + '\n')
                y_test_predict = classifier.predict(X_test)
                print_confusion_matrix(y_test,y_test_predict)
                dumpClassifier(classifier,"SVMClassifier_"+str(kernel)+"_"+str(C)+"_"+str(gamma))




