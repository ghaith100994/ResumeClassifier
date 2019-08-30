import utils
import ResumeSegmenter
import ResumeHelper
import pandas as pd
import os
from typing import *

class InfoExtractor:
    def __init__(self, model, SpacyModelParser):
        self.classifier = utils.loadClassifier(model)
        self.SpacyModel=SpacyModelParser
    
    def extractFromFile(self, filename):
        unnormlaize_pdf_dict=ResumeSegmenter.read_pdf_miner_chars(filename)
        normlaize_pdf_dict=ResumeSegmenter.text_normalize(unnormlaize_pdf_dict)
        ResumeSegmenter.update_text_normalize(normlaize_pdf_dict)
        finalList=normlaize_pdf_dict.copy()
        pre_x_result=[]
        x_data=[]
        y_data=[]
        for pharagraph_num in finalList:
            test_data=utils.sentence_features_extraction_for_test(finalList[pharagraph_num],pharagraph_num,pre_x_result,y_data)
            pre_x_result.append(test_data)
            x_data.append(utils.numeric_feat(test_data))
            y_data.append(self.classifier.predict(x_data)[-1])
        self.extractFromText(finalList, y_data)

    def extractFromText(self, finalList, y_data):
        name=None
        email=None
        number=None
        city=None
        gender=None
        Links=[]
        skillset=[]
        for pharagraph_num in finalList:
            if (y_data[pharagraph_num]==3 or y_data[pharagraph_num]==9):
                if(name==None):
                    name = self.findName(finalList[pharagraph_num])
                if(email==None):
                    email = self.findEmail(finalList[pharagraph_num])
                if(number==None):
                    number = self.findNumber(finalList[pharagraph_num])
                if(city==None):
                    city = self.findCity(finalList[pharagraph_num])
                if(gender==None):
                    gender = self.findGender(finalList[pharagraph_num])
                self.findLink(Links,finalList[pharagraph_num])
            if (y_data[pharagraph_num]==5 or y_data[pharagraph_num]==11):
                self.extractSkills(skillset,finalList[pharagraph_num])
        skills=[i.capitalize() for i in set([i.lower() for i in skillset])]
        if city is None:
            city = ""
        if gender is None:
            gender = ""
        if name is None:
           name=""
        if email is None:
            email = ""    
        if number is None:
            number = ""         
        print("Name: %s" % name)
        print("Email: %s" % email)
        print("Number: %s" % number)
        print("City/Country: %s" % city)
        print("Gender: %s" % gender)
        print("Links: %s" % Links)
        print("Skills:")
        print(skills)
         
    def findName(self,text) -> Optional[str]:
        to_chain=False
        all_names = []
        person_name = None
        for sent in text:
            for sub_sent in sent[0]:
                doc=self.SpacyModel(sub_sent)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        if not to_chain:
                            person_name = ent.text.strip()
                            to_chain = True
                        else:
                            person_name = person_name + " " + ent.text.strip()
                    elif ent.label_ != "PERSON":
                        if to_chain:
                            all_names.append(person_name)
                            person_name = None
                            to_chain = False
                if (to_chain and person_name!=None):
                    all_names.append(person_name)
                    person_name = None
                    to_chain = False
        if all_names:
            return all_names[0]
        else:
            return None

    def findEmail(self,text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                Email=ResumeHelper.get_email(sub_sent)
                if(Email!=None):
                    return Email
        return None   

    def findNumber(self,text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                Number=ResumeHelper.get_number(sub_sent)
                if(Number!=None):
                    return Number
        return None
    
    def findCity(self,text) -> Optional[str]:
        counter = Counter()
        for sent in text:
            for sub_sent in sent[0]:
                doc=self.SpacyModel(sub_sent)
                for ent in doc.ents:
                    if ent.label_ == "GPE":
                        counter[ent.text] += 1
        if len(counter) >= 1:
            return counter.most_common(1)[0][0]
        return None

    def findGender(self,text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                gender=ResumeHelper.get_gender(sub_sent)
                if(gender!=None):
                    return gender
        return None  
    
    def findLink(self,links,text):
        for sent in text:
            for sub_sent in sent[0]:
                url=ResumeHelper.get_url(sub_sent)
                if(url!=None):
                    links.append(url)
    
    def extractSkills(self,skillset,text) -> List[str]:
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "wordList/skills.csv")
        )
        skills = list(data.columns.values)
        for sent in text:
            for sub_sent in sent[0]:
                doc=self.SpacyModel(sub_sent)
                tokens = [token.text for token in doc if not token.is_stop]
                for token in tokens:
                    if token.lower() in skills:
                        skillset.append(token)
                for token in doc.noun_chunks:
                    token = token.text.lower().strip()
                    if token in skills:
                        skillset.append(token)
        