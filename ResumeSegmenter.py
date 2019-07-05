import nltk
import csv
import re
import pdfminer
from io import StringIO
from collections import defaultdict
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTTextBoxHorizontal, LTTextBoxVertical
from pdfminer.converter import PDFPageAggregator,TextConverter

#This function takes one paramter which is a file.
#Opens this file as 'CSV' file.
#Returns the first column keywords from the table as a list of strings.
def read_csv_keywords(input_file):
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        segment_keywords=[]
        for row in csv_reader:
            segment_keywords.append(row[0])
        return segment_keywords

#This function takes one paramter which is a 'CSV' file.
#Reads from the file row by row.
#Returns each row as a list of strings.
def read_csv(input_file):
    file = open(input_file, 'r')
    reader = csv.reader(file)
    return reader

#This function takes one paramter which is a 'PDF' file.
#Fetches the data from this file using (PDFParser) library.
#Stores the parsing result into a ducument using (PDFDocument) library.
#Stores shared resources of this file such as font's size and type using (PDFResourceManager) library.
#Translates the PDFResourceManager result into layouts using (PDFDevice) library.
#Process the page contents using (PDFPageInterpreter) library.
#Converts the document which contains the data into pages using (PDFPage) library, (create_pages) function for specific.
#for each line in the PDF it reads char by char.
#Returns each char with its font size and type.
def read_pdf_miner_chars(fileObj):
    chars_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams=laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)
    page_num = 1
    id = 0
    sentences_num=0
    chars=[]
    sentences=[]
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for layout_obj in layout:
            if isinstance(layout_obj, LTTextBoxHorizontal):
                id += 1
                sentences.clear()
                for line_obj in layout_obj._objs:
                    if isinstance(line_obj,pdfminer.layout.LTTextLine):
                        sent=line_obj.get_text()
                        if sent.strip():
                            chars.clear()
                            for char_obj in  line_obj._objs:
                                if isinstance(char_obj, pdfminer.layout.LTChar):
                                    chars.append([char_obj.get_text(),int(char_obj.size),char_obj.fontname])
                            sentences.append(chars.copy())
                chars_dict[sentences_num]=sentences.copy()
                sentences_num+=1
        page_num += 1
    return chars_dict

#This function takes one paramter which is a 'PDF' file.
#Fetches the data from this file using (PDFParser) library.
#Stores the parsing result into a ducument using (PDFDocument) library.
#Stores shared resources of this file such as fonts using (PDFResourceManager) library.
#Translates the PDFResourceManager result into charts using (PDFDevice) library.
#Process the page contents using (PDFPageInterpreter) library.
#Converts the document which contains the data into pages using (PDFPage) library, (create_pages) function for sure.
#for each sentence in the PDF it reads this sentence.
#Returns the PDF file as list of lists.
def read_pdf_miner_texts(fileObj):
    #text_prop_dict = {}
    text_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams=laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)
    page_num = 1
    id = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for layout_obj in layout:
            if isinstance(layout_obj, LTTextBoxHorizontal):
                text_dict[id] = layout_obj.get_text()
                id += 1
        page_num += 1
    return text_dict

#This function takes one paramter which is a 'PDF' file.
#Fetches the data from this file using (PDFParser) library.
#Stores the parsing result into a ducument using (PDFDocument) library.
#Stores shared resources of this file such as fonts using (PDFResourceManager) library.
#Translates the PDFResourceManager result into charts using (PDFDevice) library.
#Process the page contents using (PDFPageInterpreter) library.
#Converts the document which contains the data into pages using (PDFPage) library, (create_pages) function for sure.
#for each object layout in the PDF it stores the object and its dimensions.
#Returns each object with its dimensions.
def read_pdf_miner_layouts(fileObj):
    text_prop_dict = {}
    layout_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams=laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)
    layout_num = 1
    id = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBoxHorizontal):
                text_prop_dict[id] = lt_obj
                id += 1
        layout_dict[layout_num]=text_prop_dict.copy()
        text_prop_dict.clear()
        layout_num += 1
    return layout_dict

#This function takes one parameter which is an unnormalaized 'PDF' dictionary.
#Normalaizes chars array of this dictionary by looking to the previous char 'Font Size' and 'Font Type' and assemble them into one word.
#Returns normalaized 'PDF' dictionary which contains each sentence and its font size and type.
def text_normalize(unnormlaize_pdf_dict):
    normlaize_pdf_dict={}
    for chars_arry in unnormlaize_pdf_dict.items():
            pre_char_size=0
            pre_char_font=""
            newchars=[]
            for sent in chars_arry[1]:
                for char in sent:
                    if(char[1]==pre_char_size and char[2]==pre_char_font):
                        newchars[-1][0]+=char[0]
                    else:
                        newchars.append(char.copy())
                        pre_char_size=char[1]
                        pre_char_font=char[2]
                newchars[-1][0]+="\n"
            normlaize_pdf_dict[chars_arry[0]]=newchars.copy()
    return normlaize_pdf_dict

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Removes the '/n' character.
#Returns the sentences which belongs to the same block as a list sparated by ','.
def update_text_normalize(normlaize_pdf_dict):
    for sent in normlaize_pdf_dict:
        for sub_sent in normlaize_pdf_dict[sent]:
            line=sub_sent[0]
            line=re.sub('\n','',line)
            lines=nltk.sent_tokenize(line)
            sub_sent[0]=lines.copy()
            lines.clear()

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Process each paragraph in this dictionary separately, and process each sentence of the paragraph separately.
#Returns all text font sizes in this 'PDF' dictionary as a dictionary mapping between each sentence and its font size.
def find_allsize_in_text(normlaize_pdf_dict):
    sizes=defaultdict(int)
    for paragraph in normlaize_pdf_dict.values():
        for sent in paragraph:
            if(not sent[0].isspace()):
                sizes[sent[1]]+=1
    return sizes

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Process each paragraph in this dictionary separately, and process each sentence of the paragraph separately.
#Returns all text fonts types in this 'PDF' dictionary as a dictionary mapping between each sentence and its font type.
def find_allfont_in_text(normlaize_pdf_dict):
    fonts=defaultdict(int)
    for pharagraph in normlaize_pdf_dict.values():
        for sent in pharagraph:
            if(not sent[0].isspace()):
                fonts[sent[2]]+=1
    return fonts
    

work_experience_segment=read_csv_keywords('wordList\\work_experience_segment.csv')
skill_segment=read_csv_keywords('wordList\\skill_segment.csv')
education_segment=read_csv_keywords('wordList\\education_segment.csv')
project_segment=read_csv_keywords('wordList\\project_segment.csv')
