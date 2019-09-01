#We used two libraries:
#os: This library used for get operating system operations.
#re: This library used for applying regular expression operations, for example (re.search) to find a specific text.
#pandas: we used this library to help us with the plotting of the confusion matrix of the trained model.
#typing: 
#datetime: This library used for calculating experience month lenght.
#relativedelta: 

#We also used the "ResumeHelper", "ResumeSegmenter". "TrainingModel" and "utils" classes that we have created.

import os
import re
import pandas as pd

from typing import *
from datetime import datetime
from dateutil import relativedelta

import ResumeSegmenter
import ResumeHelper
import TrainingModel
import utils


class InfoExtractor:
    def __init__(self, model, SpacyModelParser):
        self.classifier = TrainingModel.loadClassifier(model)
        self.SpacyModel = SpacyModelParser
    
    #It transefers the PDF file to text and then it calls the trained model and that for doing the classification.
    def extractFromFile(self, filename):
        unnormlaized_pdf_dict = ResumeSegmenter.readPDFMinerChars(filename)
        normlaized_pdf_dict = ResumeSegmenter.textNormalize(unnormlaized_pdf_dict)
        ResumeSegmenter.updateTextNormalize(normlaized_pdf_dict)

        finalList = normlaized_pdf_dict.copy()
        pre_x_result = []
        x_data = []
        y_data = []
        for pharagraph_num in finalList:
            test_data=utils.sentenceFeaturesExtractionForTest(finalList[pharagraph_num],pharagraph_num,pre_x_result,y_data)
            pre_x_result.append(test_data)
            x_data.append(utils.numericFeatures(test_data))
            y_data.append(self.classifier.predict(x_data)[-1])
        self.extractFromText(finalList, y_data)

    #It calls all the functions responsible for fetching the personal information of the CV user, 
    #and that applied on the output of the previous function
    def extractFromText(self, finalList, y_data):
        name   = None
        email  = None
        number = None
        city   = None
        gender = None
        Links = []
        skillset = []
        eduicationset = []
        projectset = []
        experienceset = []

        for pharagraph_num in finalList:
            if (y_data[pharagraph_num] == 3 or y_data[pharagraph_num] == 9):
                if(name == None):
                    name = self.findName(finalList[pharagraph_num])

                if(email == None):
                    email = self.findEmail(finalList[pharagraph_num])

                if(number == None):
                    number = self.findNumber(finalList[pharagraph_num])

                if(city == None):
                    city = self.findCity(finalList[pharagraph_num])

                if(gender == None):
                    gender = self.findGender(finalList[pharagraph_num])

                self.findLink(Links,finalList[pharagraph_num])

            elif (y_data[pharagraph_num] == 5 or y_data[pharagraph_num] == 11):
                self.extractSkills(skillset,finalList[pharagraph_num])

            elif (y_data[pharagraph_num] == 0 or y_data[pharagraph_num] == 6):
                self.extractEducations(eduicationset,finalList[pharagraph_num])

            elif (y_data[pharagraph_num] == 4 or y_data[pharagraph_num] == 10):
                self.extractProjects(projectset,finalList[pharagraph_num])

            elif (y_data[pharagraph_num] == 1 or y_data[pharagraph_num] == 7):
                self.extractExperience(experienceset,finalList[pharagraph_num])

        skills=[i.capitalize() for i in set([i.lower() for i in skillset])]
        if city is None:
            city = ""

        if gender is None:
            gender = ""

        if name is None:
            name = ""

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
        for skill in skills:
            print(" - " + skill)

        print("Educations:")
        for edu in eduicationset:
            print(" -      ")
            for e in edu:
                print("        - " + e)

        print("Projcets:")
        for pro in projectset:
            print(" - " + ", ".join(pro))

        totalWorkExperience = self.getTotalExperienceFormatted(experienceset)
        print("Work Experience:")
        print(totalWorkExperience)
        print("Experience:")
        for exp in experienceset:
            print(" - " + ", ".join(exp))

    #Find any person name inside the CV in the personal information section.
    def findName(self, text) -> Optional[str]:
        to_chain = False
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
                if (to_chain and person_name != None):
                    all_names.append(person_name)
                    person_name = None
                    to_chain = False
        if all_names:
            return all_names[0]
        else:
            return None

    #Find any email inside the CV in the personal information section.
    def findEmail(self, text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                Email = ResumeHelper.getEmail(sub_sent)
                if(Email != None):
                    return Email
        return None   

    #Find any phone number inside the CV in the personal information section.
    def findNumber(self, text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                Number = ResumeHelper.getNumber(sub_sent)
                if(Number != None):
                    return Number
        return None
    
    #Find any city inside the CV in the personal information section.
    def findCity(self, text) -> Optional[str]:
        counter = Counter()
        for sent in text:
            for sub_sent in sent[0]:
                doc = self.SpacyModel(sub_sent)
                for ent in doc.ents:
                    if ent.label_ == "GPE":
                        counter[ent.text] += 1
        if len(counter) >= 1:
            return counter.most_common(1)[0][0]
        return None

    #Find any gender inside the CV in the personal information section.
    def findGender(self, text) -> Optional[str]:
        for sent in text:
            for sub_sent in sent[0]:
                gender = ResumeHelper.getGender(sub_sent)
                if(gender != None):
                    return gender
        return None  
    
    #Find any URL link inside the CV in the personal information section.
    def findLink(self, links, text):
        for sent in text:
            for sub_sent in sent[0]:
                url = ResumeHelper.getUrl(sub_sent)
                if(url != None):
                    links.append(url)
    
    #Classify the words in the "Skills" section inside the CV to a class represent the actuall skills that the CV user skilled.
    def extractSkills(self, skillset, text) -> List[str]:
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "wordList/skills.csv")
        )

        skills = list(data.columns.values)
        for sent in text:
            for sub_sent in sent[0]:
                doc = self.SpacyModel(sub_sent)

                tokens = [token.text for token in doc if not token.is_stop]
                for token in tokens:
                    if token.lower() in skills:
                        skillset.append(token)
                        
                for token in doc.noun_chunks:
                    token = token.text.lower().strip()
                    if token in skills:
                        skillset.append(token)

    #Classify the words in the "Education" section inside the CV to the following classes (Degree, Major, University).
    def extractEducations(self, eduicationset, text) -> List[str]:
        degree_category = [token.lower().strip() for token in ResumeSegmenter.readCSVKeywords('wordList\\degree_category.csv')]
        educational_major = [token.lower().strip() for token in ResumeSegmenter.readCSVKeywords('wordList\\educational_major.csv')]
        
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "wordList/qualification_degree_list.csv")
        )

        qualification_degree_list=[token.lower().strip() for token in data['Associate of Arts']]
        
        chunks = set()
        for sent in text:
            for sub_sent in sent[0]:
                if(sub_sent.__contains__('niversity') or sub_sent.__contains__('ollage')):
                    chunks.add(sub_sent)

                if(sub_sent.lower() in qualification_degree_list):
                    chunks.add(sub_sent)

                data = ResumeHelper.getDate(sub_sent)
                if(data!=None):
                    chunks.add(sub_sent)

                doc = self.SpacyModel(sub_sent)
                tokens = [token.text for token in doc if not token.is_stop]
                for token in tokens:
                    if token.lower() in degree_category:
                        chunks.add("Degree: " + token.lower())
                    elif token.lower() in educational_major:
                        chunks.add("Major: " + token.lower())

                for token in doc.noun_chunks:
                    token = token.text.lower().strip()
                    if token in degree_category:
                        chunks.add("Degree: " + token.lower())
                    elif token.lower() in educational_major:
                        chunks.add("Major: " + token.lower())

        if(len(chunks) != 0):
            eduicationset.append(chunks)
 
    #Extract all of the projects that the CV user had done i his career.
    def extractProjects(self, projectset, text) -> List[str]:
        project_segment = [token.lower().strip() for token in ResumeSegmenter.readCSVKeywords('wordList\\project_segment.csv')]
        unique_char_regex = "[^\sA-Za-z0-9\.\/\(\)\,\-\|]+"
        chunks = set()
        for sent in text:
            for sub_sent in sent[0]:
                if(sub_sent.lower() in project_segment):
                    continue
                chunks.add(sub_sent)
                has_dot = re.findall(unique_char_regex, sub_sent)
                if(has_dot):
                    if('●' in chunks):
                        chunks.remove('●')
                    if(len(chunks) != 0):
                        projectset.append(chunks.copy())
                        chunks.clear()

        if('●' in chunks):
            chunks.remove('●')

        if(len(chunks) != 0):
            projectset.append(chunks)

    #Extract an experience or a service that the CV user had gained in his life.
    def extractExperience(self, experienceset, text) -> List[str]:
        project_segment = [token.lower().strip() for token in ResumeSegmenter.readCSVKeywords('wordList\\work_experience_segment.csv')]
        unique_char_regex = "[^\sA-Za-z0-9\.\/\(\)\,\-\|]+"
        chunks = set()
        for sent in text:
            for sub_sent in sent[0]:
                if(sub_sent.lower() in project_segment):
                    continue
                chunks.add(sub_sent)
                has_dot = re.findall(unique_char_regex, sub_sent)
                if(has_dot):
                    if('●' in chunks):
                        chunks.remove('●')
                    if(len(chunks) != 0):
                        experienceset.append(chunks.copy())
                        chunks.clear()
        if('●' in chunks):
            chunks.remove('●')
        if(len(chunks) != 0):
            experienceset.append(chunks)

    #Extract all of the experiences and services that the CV user had gained in his life by calling the previous function for each experience.
    def getTotalExperience(self, experience_list) -> int:
        """
        Wrapper function to extract total months of experience from a resume

        :param experience_list: list of experience text extracted
        :return: total months of experience
        """
        exp_ = []
        for sets in experience_list:
            for line in sets:
                line = line.lower().strip()
                # have to split search since regex OR does not capture on a first-come-first-serve basis
                experience = re.search(
                    r"(?P<fyear>\d{4})\s*(\s|-|to)\s*(?P<syear>\d{4}|present|date|now)",
                    line,
                    re.I,
                )

                if experience:
                    d = experience.groupdict()
                    exp_.append(d)
                    continue

                experience = re.search(
                    r"(?P<fmonth>\w+(?P<fh>.)\d+)\s*(\s|-|to)\s*(?P<smonth>\w+(?P<sh>.)\d+|present|date|now)",
                    line,
                    re.I,
                )

                if experience:
                    d = experience.groupdict()
                    exp_.append(d)
                    continue

                experience = re.search(
                    r"(?P<fmonth_num>\d+(?P<fh>.)\d+)\s*(\s|-|to)\s*(?P<smonth_num>\d+(?P<sh>.)\d+|present|date|now)",
                    line,
                    re.I,
                )

                if experience:
                    d = experience.groupdict()
                    exp_.append(d)
                    continue

        experience_num_list = [self.getNumberOfMonths(i) for i in exp_]
        total_experience_in_months = sum(experience_num_list)
        return total_experience_in_months

    #Extract all of the experiences and services that the CV user had gained in his life by calling the previous function for all experiences and then formatted them on their dates.
    def getTotalExperienceFormatted(self, exp_list) -> str:
        months = self.getTotalExperience(exp_list)
        if months < 12:
            return str(months) + " months"

        years = months // 12
        months = months % 12
        return str(years) + " years " + str(months) + " months"

    #Extracting the exact months number of an experience.
    def getNumberOfMonths(self,datepair) -> int:
        """
        Helper function to extract total months of experience from a resume

        :param date1: Starting date
        :param date2: Ending date
        :return: months of experience from date1 to date2
        """
        # if years
        # if years
        date2_parsed = False
        if datepair.get("fh", None) is not None:
            gap = datepair["fh"]
        else:
            gap = ""
        try:
            present_vocab = ("present", "date", "now")
            if "syear" in datepair:
                date1 = datepair["fyear"]
                date2 = datepair["syear"]

                if date2.lower() in present_vocab:
                    date2 = datetime.now()
                    date2_parsed = True

                try:
                    if not date2_parsed:
                        date2 = datetime.strptime(str(date2), "%Y")
                    date1 = datetime.strptime(str(date1), "%Y")
                except:
                    pass
            elif "smonth_num" in datepair:
                date1 = datepair["fmonth_num"]
                date2 = datepair["smonth_num"]

                if date2.lower() in present_vocab:
                    date2 = datetime.now()
                    date2_parsed = True

                for stype in ("%m" + gap + "%Y", "%m" + gap + "%y"):
                    try:
                        if not date2_parsed:
                            date2 = datetime.strptime(str(date2), stype)
                        date1 = datetime.strptime(str(date1), stype)
                        break
                    except:
                        pass
            else:
                date1 = datepair["fmonth"]
                date2 = datepair["smonth"]

                if date2.lower() in present_vocab:
                    date2 = datetime.now()
                    date2_parsed = True

                for stype in (
                    "%b" + gap + "%Y",
                    "%b" + gap + "%y",
                    "%B" + gap + "%Y",
                    "%B" + gap + "%y",
                ):
                    try:
                        if not date2_parsed:
                            date2 = datetime.strptime(str(date2), stype)
                        date1 = datetime.strptime(str(date1), stype)
                        break
                    except:
                        pass

            months_of_experience = relativedelta.relativedelta(date2, date1)
            months_of_experience = (
                months_of_experience.years * 12 + months_of_experience.months
            )
            return months_of_experience
        except Exception as e:
            return 0
