import ResumeHelper
import ResumeSegmenter
from collections import defaultdict

def sent_features(sentences_info,pharagraph_num,result):
    Contain_email=False
    Contain_Phone=False
    Contain_URL=False
    Contain_Date=False
    IsWorkSegment=False
    IsSkillSegment=False
    IsEducationSegment=False
    IsProjectSegment=False
    Font_Size=defaultdict(int)
    Font_Family=defaultdict(int)
    Word_Count=0
    if pharagraph_num==0:
        prevtag="<START>"
        pre_Font_Size=0
        pre_Font_Family="<START>"
    else:
        prevtag=result[-1]
        pre_Font_Size=result[-1]["Font_Size"]
        pre_Font_Family=result[-1]["Font_Family"]
    for sent_info in sentences_info:
        for sub_sent in sent_info[0]:
            if ResumeHelper.get_url(sub_sent)!=None:
                Contain_URL=True
            if ResumeHelper.get_email(sub_sent)!=None:
                Contain_email=True
            if ResumeHelper.get_date(sub_sent)!=None:
                Contain_Date=True
            if ResumeHelper.get_number(sub_sent)!=None:
                Contain_Phone=True
            for word in ResumeSegmenter.work_experience_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsWorkSegment=True
            for word in ResumeSegmenter.skill_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsSkillSegment=True
            for word in ResumeSegmenter.education_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsEducationSegment=True
            for word in ResumeSegmenter.project_segment:
                if sub_sent.lower().__contains__(word.lower()):
                    IsProjectSegment=True
            Word_Count+=len(sub_sent.split(' '))
            for word in sub_sent.split():
                Font_Size[sent_info[1]]+=1
                Font_Family[sent_info[2]]+=1
    most_iterate_size_value=0
    most_iterate_size=0
    for size in Font_Size:
        if(most_iterate_size_value<Font_Size[size]):
            most_iterate_size_value=Font_Size[size]
            most_iterate_size=size
    most_iterate_fontfamily_value=0
    most_iterate_fontfamily=""
    for family in Font_Family:
        if(most_iterate_fontfamily_value<Font_Family[family]):
            most_iterate_fontfamily_value=Font_Family[family]
            most_iterate_fontfamily=family
    features={}
    features["Contain_email"]=Contain_email
    features["Contain_Phone"]=Contain_Phone
    features["Contain_Date"]=Contain_Date
    features["Contain_URL"]=Contain_URL
    features["prevtag"]=prevtag
    features["PhargraphNumber"]=pharagraph_num
    features["Word_Count"]=Word_Count
    features["IsWorkSegment"]=IsWorkSegment
    features["IsSkillSegment"]=IsSkillSegment
    features["IsEducationSegment"]=IsEducationSegment
    features["IsProjectSegment"]=IsProjectSegment
    features["Font_Family"]=most_iterate_fontfamily
    features["Font_Size"]=most_iterate_size
    features["pre_Font_Size"]=pre_Font_Size
    features["pre_Font_Family"]=pre_Font_Family
    return features