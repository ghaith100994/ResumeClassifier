import os
import ResumeSegmenter

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

def createdataset(labeled_files_dic,pdf_files_dic):
    data={}
    y_data={}
    pdf_files=getfilelist(pdf_files_dic)
    labeled_files=getfilelist(labeled_files_dic)
    for filename in pdf_files:
        unnormlaize_pdf_dict=ResumeSegmenter.read_pdf_miner_charts(filename)
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
