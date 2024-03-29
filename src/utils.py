#We used the following libraries:

#collections: This library used for getting the default dictionary.

#We also used the "ResumeHelper" and the "ResumeSegmenter" classes that we have created.

from collections import defaultdict

import ResumeHelper
import ResumeSegmenter

#Converts a list of dictionaries to a vector contains a numbers representing the features.
def numericFeatures(feat):
    Normalized_Feat = []

    if (feat['Contain_Date'] == False and feat['Contain_Phone'] == False and feat['Contain_URL'] == False and feat['Contain_email'] == False):
        Normalized_Feat.append(0)
    else:
        Normalized_Feat.append(1)

    if(feat['IsEducationSegment'] == False):
        Normalized_Feat.append(0)
    else:
        Normalized_Feat.append(1)

    if(feat['IsProjectSegment'] == False):
        Normalized_Feat.append(0)
    else:
        Normalized_Feat.append(1)

    if(feat['IsSkillSegment'] == False):
        Normalized_Feat.append(0)
    else:
        Normalized_Feat.append(1)

    if(feat['IsWorkSegment'] == False):
        Normalized_Feat.append(0)
    else:
        Normalized_Feat.append(1)

    if(feat['Font_Family'].__contains__("Bold")):
        Normalized_Feat.append(1)
    else:
        Normalized_Feat.append(0)

    if(feat['pre_Font_Family'].__contains__("Bold")):
        Normalized_Feat.append(1)
    else:
        Normalized_Feat.append(0)

    Normalized_Feat.append(feat['Font_Size'])
    Normalized_Feat.append(feat['pre_Font_Size'])
    Normalized_Feat.append(feat['Word_Count'])
    Normalized_Feat.append(feat['PhargraphNumber'])
    Normalized_Feat.append(feat['prevtag'])
    return Normalized_Feat

#Extracting the features for a specific section from the CV and that for getting the final result.
def sentenceFeaturesExtractionForTest(sentences_info, paragraph_num, prev_x_result, prev_y_result):
    Contain_email       = False
    Contain_Phone       = False
    Contain_URL         = False
    Contain_Date        = False
    IsExperienceSegment = False
    IsSkillSegment      = False
    IsEducationSegment  = False
    IsProjectSegment    = False

    Font_Size = defaultdict(int)
    Font_Family = defaultdict(int)
    Word_Count = 0

    if paragraph_num == 0:
        prevtag = -1
        pre_Font_Size = 0
        pre_Font_Family = "<START>"
    else:
        prevtag = prev_y_result[-1]
        pre_Font_Size = prev_x_result[-1]["Font_Size"]
        pre_Font_Family = prev_x_result[-1]["Font_Family"]

    for sent_info in sentences_info:
        for sub_sent in sent_info[0]:
            if ResumeHelper.getUrl(sub_sent) != None:
                Contain_URL = True

            if ResumeHelper.getEmail(sub_sent) != None:
                Contain_email = True

            if ResumeHelper.getDate(sub_sent.lower()) != None:
                Contain_Date = True

            if ResumeHelper.getNumber(sub_sent) != None:
                Contain_Phone = True

            for word in ResumeSegmenter.work_experience_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsExperienceSegment = True

            for word in ResumeSegmenter.skill_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsSkillSegment = True

            for word in ResumeSegmenter.education_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsEducationSegment = True

            for word in ResumeSegmenter.project_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsProjectSegment = True

            Word_Count += len(sub_sent.split(' '))
            for word in sub_sent.split():
                Font_Size[sent_info[1]] += 1
                Font_Family[sent_info[2]] += 1

    most_iterate_size_value = 0
    most_iterate_size = 0

    for size in Font_Size:
        if(most_iterate_size_value<Font_Size[size]):
            most_iterate_size_value = Font_Size[size]
            most_iterate_size = size

    most_iterate_fontfamily_value = 0
    most_iterate_fontfamily = ""

    for family in Font_Family:
        if(most_iterate_fontfamily_value<Font_Family[family]):
            most_iterate_fontfamily_value = Font_Family[family]
            most_iterate_fontfamily = family

    features = {}
    features["Contain_email"]      = Contain_email
    features["Contain_Phone"]      = Contain_Phone
    features["Contain_Date"]       = Contain_Date
    features["Contain_URL"]        = Contain_URL
    features["prevtag"]            = prevtag
    features["PhargraphNumber"]    = paragraph_num
    features["Word_Count"]         = Word_Count
    features["IsWorkSegment"]      = IsExperienceSegment
    features["IsSkillSegment"]     = IsSkillSegment
    features["IsEducationSegment"] = IsEducationSegment
    features["IsProjectSegment"]   = IsProjectSegment
    features["Font_Family"]        = most_iterate_fontfamily
    features["Font_Size"]          = most_iterate_size
    features["pre_Font_Size"]      = pre_Font_Size
    features["pre_Font_Family"]    = pre_Font_Family
    return features
