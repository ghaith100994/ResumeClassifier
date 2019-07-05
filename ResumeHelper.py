#We used two libraries:
#re: This library used for applying regular expression operations, for example (re.search) to find a specific text.
#text_to_word_sequence: This library used to convert a specific text to a sequence of words.
import re
from keras.preprocessing.text import text_to_word_sequence

#This function extracts any 'email' link from a specific text using a regular expression. 
#The regular expression contains all the forms that the 'email' link could take.
def get_email(line):
    email = None
    match = re.search(r'[A-Za-z][a-zA-Z0-9_\.\+-]*@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9\.]{2,}',line)
    if match is not None:
        email = match.group(0)
    return email

#This function extracts the 'gender' type from a specific text.
def get_gender(line):
    parts = text_to_word_sequence(line)
    gender = None
    if 'male' in parts:
        gender = 'male'
        return gender
    elif 'female' in parts:
        gender = 'female'
        return gender
    elif 'trans' in parts:
        gender = 'trans'
        return gender
    else:
        return 'Not Found.'

#This function extracts any 'URL' link from a specific text using a regular expression. 
#The regular expression contains all the forms that the 'URL' link could take.
def get_url(line):
    url = None
    match = re.search(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#\+\&])*',line)
    if match is not None:
        url = match.group(0)
    return url

#This function extracts any 'Number'from a specific text using a regular expression. 
#The regular expression contains all the forms that the 'Number' could take.
def get_number(line):
    number = None
    match = re.search(r'\+?\(?\d{2,4}\)?[\d\s-]{7,}',line)
    if match is not None:
        number = match.group(0)
    return number

#This function extracts any 'date' from a specific text using a collection of regular expressions.

#The regular expressions contain all the elements of the 'date'.
#Day: This regular expression contains all the forms that the 'Day' could take.
#MonthNum: This regular expression contains all the forms that the numeric 'Month' could take.
#MonthStr: This regular expression contains all the forms that the string 'Month' could take.
#MonthStrShortCut: This regular expression contains all the forms that the shortcut (first three letters) 'Month' could take.
#Year: This regular expression contains the only form that the 'Year' could take.
#Separator: This regular expression contains all the forms that the date's 'Separator' could take, could be (space - '/' - '-' - ',' or nothing).

#Then we have the two most popular types of date formats:
#DMY: Appreviation of (day - month - year).
#MDY: Appreviation of (month - day - year).
def get_date(line):
    date = None
    Day="((0?[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))?"
    MonthNum="((0?[1-9])|(1[0-2]))"
    MonthStr="((january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december))"
    MonthStrShortCut="((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec))"
    Year="(\d{4})"
    Separator="([\s\/\-\,])*"
    DMY = Day+Separator+"("+MonthNum+"|"+MonthStr+"|"+MonthStrShortCut+")"+Separator+Year
    MDY = "("+MonthNum+"|"+MonthStr+"|"+MonthStrShortCut+")"+Separator+Day+Separator+Year
    match = re.search(r"("+DMY+")|"+"("+MDY+")",line)
    if match is not None:
        date = match.group(0)
    return date

#datetypeCM="(([Jj][aA][nN][uU][aA][rR][Yy])|([Ff][eE][Bb][rR][uU][aA][rR][Yy])|([mM][aA][rR][cC][hH])|([aA][pP][rR][iI][lL])|([mM][aA][Yy])|([Jj][uU][nN][eE])|([Jj][uU][lL][Yy])|([aA][uU][gG][uU][sS][tT])|([sS][eE][pP][Tt][eE][mM][Bb][eE][rR])|([oO][cC][tT][oO][Bb][eE][rR])|([nN][oO][vV][eE][mM][Bb][eE][rR])|([dD][eE][cC][eE][mM][Bb][eE][rR]))"
#datetypeMMM="(([jJ][Aa][nN])|([Ff][eE][bB])|([Mm][Aa][Rr])|([Aa][Pp][Rr])|([Mm][Aa][yY])|([jJ][Uu][nN])|([jJ][Uu][Ll])|([Aa][Uu][gG])|([Ss][eE][Pp])|([Oo][Cc][tT])|([nN][Oo][Vv])|([Dd][eE][Cc]))"
