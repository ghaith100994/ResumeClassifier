import re
from keras.preprocessing.text import text_to_word_sequence

def get_email(line):
    email = None
    match = re.search(r'[A-Za-z][a-zA-Z0-9_\.\+-]*@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9\.]{2,}',line)
    if match is not None:
        email = match.group(0)
    return email

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

def get_url(line):
    url = None
    match = re.search(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#\+\&])*',line)
    if match is not None:
        url = match.group(0)
    return url

def get_number(line):
    number = None
    match = re.search(r'\+?\(?\d{2,4}\)?[\d\s-]{7,}',line)
    if match is not None:
        number = match.group(0)
    return number

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
