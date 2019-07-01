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

def read_csv_keywords(input_file):
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        segment_keywords=[]
        for row in csv_reader:
            segment_keywords.append(row[0])
        return segment_keywords

def read_csv(input_file):
    file = open(input_file, 'r')
    reader = csv.reader(file)
    return reader

def read_pdf_miner_charts(fileObj):
    #text_prop_dict = {}
    chars_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 1
    id = 0
    sentences_num=0
    chars=[]
    sentences=[]
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBoxHorizontal):
                #text_dict[id] = lt_obj.get_text()
                #text_prop_dict[id] = lt_obj
                id += 1
                sentences.clear()
                for line_obj in lt_obj._objs:
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
        #page_dict[page_num]=text_prop_dict.copy()
        #text_prop_dict.clear()
        page_num += 1
    return chars_dict

def read_pdf_miner_texts(fileObj):
    #text_prop_dict = {}
    text_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 1
    id = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBoxHorizontal):
                text_dict[id] = lt_obj.get_text()
                #text_prop_dict[id] = lt_obj
                id += 1
        #page_dict[page_num]=text_prop_dict.copy()
        #text_prop_dict.clear()
        page_num += 1
    return text_dict

def read_pdf_miner_pages(fileObj):
    text_prop_dict = {}
    page_dict={}
    file_pointer = open(fileObj,'rb')
    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
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

def find_allsize_in_text(normlaize_pdf_dict):
    sizes=defaultdict(int)
    for pharagraph in normlaize_pdf_dict.values():
        for sent in pharagraph:
            if(not sent[0].isspace()):
                sizes[sent[1]]+=1
    return sizes

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