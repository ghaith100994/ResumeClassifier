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
def getfilelist(path, extension=None):
    dir=os.listdir(path)
    filenames = []
    for i in next(os.walk(path))[2]:
        if (extension):
            if i.endswith(extension):
                filenames.append(os.path.join(path, i))
        else:
            filenames.append(os.path.join(path, i))
    for d in dir:
        new_path=os.path.join(path, d)
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
#We get both dictionaries by passing them to the previous function (getfilelist).

#for each file of raw CVs we call (read_pdf_miner_chars) from the (ResumeSegmenter) class in order to get the unnormalized dictionary .
#then we normalize and clean that dictionary by calling (text_normalize) & (update_text_normalize) from the same class (ResumeSegmenter).

#Returns a dictionary concatinating both dictionaries. 
#in other words it returns each sentence of the CV with its font size and type in addition to the manually labeled value.
def createdataset(labeled_files_dic,pdf_files_dic):
    data={}
    y_data={}
    pdf_files=getfilelist(pdf_files_dic)
    labeled_files=getfilelist(labeled_files_dic)
    for filename in pdf_files:
        unnormlaize_pdf_dict=ResumeSegmenter.read_pdf_miner_chars(filename)
        normlaize_pdf_dict=ResumeSegmenter.text_normalize(unnormlaize_pdf_dict)
        ResumeSegmenter.update_text_normalize(normlaize_pdf_dict)
        data[filename.split('\\')[-1].split('.')[0]]=normlaize_pdf_dict.copy()
    for lb_file in labeled_files:
        f = open(lb_file, "r")
        result=f.read()
        final_result=result.split('\n')
        y_data[lb_file.split('\\')[-1].split('.')[0]]=final_result.copy()
    for cv in y_data:
        y=y_data[cv]
        for index in range(len(y)):
            data[cv][index].append(y[index])
    return data


def dumpdataset(labeled_files_dic,pdf_files_dic):
    data=createdataset(labeled_files_dic,pdf_files_dic)
    with open('PersonalResume.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def loaddataset():
    with open('PersonalResume.pickle', 'rb') as handle:
        return pickle.load(handle)
