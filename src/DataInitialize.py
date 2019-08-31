#We used two libraries:
#os: This library used for get operating system operations.
#pickle: This library used for saving and loading files and classifiers.

#We also used the "ResumeSegmenter" class that we have created.

import os
import pickle

import ResumeSegmenter

#This function takes two paramters.
#First paramter is the folder path which may contains files or folders or both.
#Second paramter is the files extension which this function will return as a list, default is 'None' which means all files.
#Opens this file as 'CSV' file.
#Returns all the files with the specified extension if its passed or all the files in case it was default as a list.
#in case there is no folder/s in the specified folder path it returns only its files.
#in case there is a folder or multiple folders inside the specified folder path it will returns all their files.
def getFileList(path, extension = None):
    dirs = os.listdir(path)
    filenames = []
    for i in next(os.walk(path))[2]:
        if (extension):
            if i.endswith(extension):
                filenames.append(os.path.join(path, i))
        else:
            filenames.append(os.path.join(path, i))
    for dir in dirs:
        new_path = os.path.join(path, dir)
        for i in next(os.walk(new_path))[2]:
            if (extension):
                if i.endswith(extension):
                    filenames.append(os.path.join(new_path, i))
            else:
                filenames.append(os.path.join(new_path, i))
    return filenames

#This function takes two paramters.
#First paramter is the labeled CVs as a dictionary.
#Second paramter is the raw CVs as a dictionary.
#We get all the file names of both dictionaries by passing them to the previous function (getfilelist).

#for each file of raw CVs we call (read_pdf_miner_chars) from the (ResumeSegmenter) class in order to get the unnormalized dictionary .
#then we normalize and clean that dictionary by calling (text_normalize) & (update_text_normalize) from the same class (ResumeSegmenter).

#Returns a dictionary concatinating both dictionaries. 
#in other words it returns each sentence of the CV with its font size and type in addition to the manually labeled value.
def createDataset(labeled_files_dict, pdf_files_dict):
    data = {}
    y_data = {}
    pdf_files = getFileList(pdf_files_dict)
    labeled_files = getFileList(labeled_files_dict)

    for filename in pdf_files:
        unnormlaized_pdf_dict = ResumeSegmenter.readPDFMinerChars(filename)
        normlaized_pdf_dict = ResumeSegmenter.textNormalize(unnormlaized_pdf_dict)
        ResumeSegmenter.updateTextNormalize(normlaized_pdf_dict)
        data[filename.split('\\')[-1].split('.')[0]] = normlaized_pdf_dict.copy()

    for labeled_file in labeled_files:
        f = open(labeled_file, "r")
        result = f.read()
        final_result=result.split('\n')
        y_data[labeled_file.split('\\')[-1].split('.')[0]] = final_result.copy()

    for cv in y_data:
        y = y_data[cv]
        for index in range(len(y)):
            data[cv][index].append(y[index])
    return data

#This function takes two parameters.
#First paramter is the labeled CVs dictionary.
#Second paramter is the raw CVs dictionary.
#Calls the previous function to get the data and save it.
def dumpdataset(labeled_files_dict, pdf_files_dict):
    data = createDataset(labeled_files_dict, pdf_files_dict)
    with open('PersonalResume.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol = pickle.HIGHEST_PROTOCOL)

##This function takes no parameter.
#Loads the data by using (pickle) library.
def loadDataset():
    with open('PersonalResume.pickle', 'rb') as handle:
        return pickle.load(handle)
