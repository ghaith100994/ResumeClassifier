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
#Returns the keywords of the table header as a list of strings.
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
#Stores shared resources of this file such as fonts using (PDFResourceManager) library.
#Translates the PDFResourceManager result into charts using (PDFDevice) library.
#Process the page contents using (PDFPageInterpreter) library.
#Converts the document which contains the data into pages using (PDFPage) library, (create_pages) function for sure.
#Process each page separately, and for each page it process each line separately, and for each line it process each sentence separately.
#Returns a dictionary mapping between each sentence number and its words in the same chart.
def read_pdf_miner_charts(fileObj):
    charts_dict={}
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
    charts=[]
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
                            charts.clear()
                            for chart_obj in  line_obj._objs:
                                if isinstance(chart_obj, pdfminer.layout.LTChar):
                                    charts.append([chart_obj.get_text(),int(chart_obj.size),chart_obj.fontname])
                            sentences.append(charts.copy())
                charts_dict[sentences_num]=sentences.copy()
                sentences_num+=1
        page_num += 1
    return charts_dict

#This function takes one paramter which is a 'PDF' file.
#Fetches the data from this file using (PDFParser) library.
#Stores the parsing result into a ducument using (PDFDocument) library.
#Stores shared resources of this file such as fonts using (PDFResourceManager) library.
#Translates the PDFResourceManager result into charts using (PDFDevice) library.
#Process the page contents using (PDFPageInterpreter) library.
#Converts the document which contains the data into pages using (PDFPage) library, (create_pages) function for sure.
#Process each page separately, and for each page it process each layout separately, and for each layout it process each sentence separately.
#Returns a dictionary mapping between a unique id number and the text words of the same layout.
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
#Process each page separately, and for each page it process each line separately, and for each line it process each sentence separately.
#Returns a dictionary mapping between the page number and the text words of the same layout in this page.
def read_pdf_miner_pages(fileObj):
    text_prop_dict = {}
    page_dict={}
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
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBoxHorizontal):
                text_prop_dict[id] = lt_obj
                id += 1
        page_dict[page_num]=text_prop_dict.copy()
        text_prop_dict.clear()
        page_num += 1
    return page_dict

#This function takes one parameter which is an unnormalaized 'PDF' dictionary.
#Normalaizes chars array of this dictionary by looking to the previous char 'Size' and the previous char 'Font'.
#Returns normalaized 'PDF' dictionary.
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
#Process each paragraph in this dictionary separately, and process each sentence of the paragraph separately.
#Returns all text sizes in this 'PDF' dictionary as a dictionary mapping between each sentence and its font size.
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
