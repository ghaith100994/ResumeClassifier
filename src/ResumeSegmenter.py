#We used the following libraries:

#nltk: Natural Language Tool Kit, we used this library for tokenization.
#csv: Comma Separated Value, we used this library for dealing with CSV files.
#re: This library used for applying Regular Expression operations, for example (re.search) to find a specific text.
#collections: This library used for getting the default dictionary.

#pdfminer: This library used for dealing with PDF files.
#PDFParser: This library used for fetches the data from this PDF file.
#PDFDocument: This library used for stores the parsing result into a ducument.
#PDFResourceManager: This library used for stores shared resources of the PDF file such as font's size and type.
#PDFDevice: This library used for translates the PDFResourceManager result into layouts.
#PDFPageInterpreter: This library used for process the page contents.
#PDFPage: This library used for converts the document which contains the data into pages using the (create_pages).

import nltk
import csv
import re
import pdfminer

from collections import defaultdict
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTTextBoxHorizontal, LTTextBoxVertical
from pdfminer.converter import PDFPageAggregator, TextConverter

#This function takes one paramter which is a file.
#Opens this file as 'CSV' file.
#Returns the first column keywords from the table as a list of strings.
def readCSVKeywords(input_file):
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        segment_keywords=[]
        for row in csv_reader:
            segment_keywords.append(row[0])
        return segment_keywords

#This function takes one paramter which is a 'CSV' file.
#Reads from the file row by row.
#Returns each row as a list of strings.
def readCSV(input_file):
    file = open(input_file, 'r')
    reader = csv.reader(file)
    return reader

#This function takes one paramter which is a 'PDF' file.
#for each line in the PDF it reads char by char.
#Returns each char with its font size and type.
def readPDFMinerChars(fileObj):
    chars_dict = {}
    file_pointer = open(fileObj, 'rb')

    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams = laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)
    page_num = 1
    id = 0
    sentences_num = 0
    chars = []
    sentences = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for layout_obj in layout:
            if isinstance(layout_obj, LTTextBoxHorizontal):
                id += 1
                sentences.clear()
                for line_obj in layout_obj._objs:
                    if isinstance(line_obj, pdfminer.layout.LTTextLine):
                        sent = line_obj.get_text()
                        if sent.strip():
                            chars.clear()
                            for char_obj in line_obj._objs:
                                if isinstance(char_obj, pdfminer.layout.LTChar):
                                    chars.append([char_obj.get_text(), int(char_obj.size), char_obj.fontname])
                            sentences.append(chars.copy())
                chars_dict[sentences_num] = sentences.copy()
                sentences_num += 1
        page_num += 1
    return chars_dict

#This function takes one paramter which is a 'PDF' file.
#for each sentence in the PDF it reads this sentence.
#Returns the PDF file as list of lists.
def readPDFMinerTexts(fileObj):
    text_dict = {}
    file_pointer = open(fileObj, 'rb')

    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams = laparams)
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
#for each object layout in the PDF it stores the object and its dimensions.
#Returns each object with its dimensions.
def readPDFMinerLayouts(fileObj):
    text_prop_dict = {}
    layout_dict = {}
    file_pointer = open(fileObj, 'rb')

    parser = PDFParser(file_pointer)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
   
    resourceManager = PDFResourceManager()
    device = PDFDevice(resourceManager)
    laparams = LAParams()
    device = PDFPageAggregator(resourceManager, laparams = laparams)
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
        layout_dict[layout_num] = text_prop_dict.copy()
        text_prop_dict.clear()
        layout_num += 1
    return layout_dict

#This function takes one parameter which is an unnormalaized 'PDF' dictionary.
#Normalaizes chars array of this dictionary by looking to the previous char 'Font Size' and 'Font Type' and assemble them into one word.
#Returns normalaized 'PDF' dictionary which contains each sentence and its font size and type.
def textNormalize(unnormlaized_pdf_dict):
    normlaize_pdf_dict = {}
    for chars_arry in unnormlaized_pdf_dict.items():
            pre_char_size = 0
            pre_char_font = ""
            newchars = []
            for sent in chars_arry[1]:
                for char in sent:
                    if(char[1] == pre_char_size and char[2] == pre_char_font):
                        newchars[-1][0] += char[0]
                    else:
                        newchars.append(char.copy())
                        pre_char_size = char[1]
                        pre_char_font = char[2]
                newchars[-1][0] += "\n"
            normlaize_pdf_dict[chars_arry[0]] = newchars.copy()
    return normlaize_pdf_dict

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Removes the '/n' character.
#Returns the sentences which belongs to the same block as a list sparated by ','.
def updateTextNormalize(normlaize_pdf_dict):
    for sent in normlaize_pdf_dict:
        for sub_sent in normlaize_pdf_dict[sent]:
            line = sub_sent[0]
            line = re.sub('\n', '', line)
            lines = nltk.sent_tokenize(line)
            sub_sent[0] = lines.copy()
            lines.clear()

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Process each paragraph in this dictionary separately, and process each sentence of the paragraph separately.
#Returns all text font sizes in this 'PDF' dictionary as a dictionary mapping between each sentence and its font size.
def findAllSizeInText(normlaized_pdf_dict):
    sizes = defaultdict(int)
    for paragraph in normlaized_pdf_dict.values():
        for sent in paragraph:
            if(not sent[0].isspace()):
                sizes[sent[1]] += 1
    return sizes

#This function takes one parameter which is an normalaized 'PDF' dictionary.
#Process each paragraph in this dictionary separately, and process each sentence of the paragraph separately.
#Returns all text fonts types in this 'PDF' dictionary as a dictionary mapping between each sentence and its font type.
def findAllFontInText(normlaized_pdf_dict):
    fonts = defaultdict(int)
    for pharagraph in normlaized_pdf_dict.values():
        for sent in pharagraph:
            if(not sent[0].isspace()):
                fonts[sent[2]] += 1
    return fonts
    
#Those are the words lists (dictionaries) of the basic sections of the CV (Work experiences - Skills - Education - Projects)
work_experience_segment = readCSVKeywords('wordList\\work_experience_segment.csv')
skill_segment = readCSVKeywords('wordList\\skill_segment.csv')
education_segment = readCSVKeywords('wordList\\education_segment.csv')
project_segment = readCSVKeywords('wordList\\project_segment.csv')
