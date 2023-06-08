import string
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import json
from nltk.tokenize import word_tokenize
import datefinder
import calendar


dic_month = {month: index for index, month in enumerate(calendar.month_abbr) if month}

def normalization(textlist):
    normalized_text = []

    for text in textlist:
     text = text.lower()
     text = text.replace('$', ' dollar ')
     text = text.replace('%', ' percent ')
     normalized_text.append(text)
    return normalized_text
def removePuncs(textlist):
    cleaned_text = []
    for text in textlist:
        cleaned_string = ''.join(c for c in text if c not in string.punctuation)
        if cleaned_string != '':
            cleaned_text.append(cleaned_string)
    return cleaned_text

def removeAcronomy(textlist):
    cleaned_text = []
    with open("acronyms.json", "r") as f:
        acronyms = json.load(f)
    for word in textlist:
        if word in acronyms:
            cleaned_text.append(acronyms[word])
        else:
            cleaned_text.append(word)

    return cleaned_text

def remove_stopwords(text):
    filtered_sentence = []
    stop_words = stopwords.words('english')
    for word in text:
        if not word in stop_words :
            filtered_sentence.append(word)
    return filtered_sentence





def date_processor(text):
    try:
        match = datefinder.find_dates(text, source=1)

        for item in match:
            replacement = ""

            if (item[1].len() > 4) and not ('PM' in item[1]) and not ('AM' in item[1]) and (
                    any(ch.isdigit() for ch in item[1])):
                replacement += str(item[0].day)
                replacement += "/"
                if type(item[0].month) == int:
                    replacement += str(item[0].month)
                else:
                    replacement += dic_month[item[0].month]
                replacement += "/"
                replacement += str(item[0].year)
                text = text.replace(item[1], replacement)


    except:
        pass

    return text


# def execute(text):
#
#
#     for x in text:
#         z = [jj for jj in sp(x).doc if jj.ent_type_ == "DATE"]
#         idx = 0
#         for zz in z:
#
#             tmp = list(datefinder.find_dates("default " + zz.text + " default"))
#
#             # print(tmp, "   ", zz)
#             if len(tmp) > 0:
#                 text[idx] += " " + sp(tmp[0].date().strftime("%Y/%m/%d")).text
#                 # print(mps[idx])
#         idx += 1
#         return text









# stemming # #
def stemmer(textlist):
    filtered_sentence = []
    for text in textlist:
        ps = PorterStemmer()
        stemmed_text = ps.stem(text)
        filtered_sentence.append(stemmed_text)

    return filtered_sentence

# # lemmatization # #
def lemmatizer(sentence):
    filtered_sentence = []
    wnl = WordNetLemmatizer()
    for word, tag in pos_tag(sentence):
        if tag.startswith("NN"):
            filtered_sentence.append(wnl.lemmatize(word, pos='n'))
        elif tag.startswith('VB'):
            filtered_sentence.append( wnl.lemmatize(word, pos='v'))
        elif tag.startswith('JJ'):
            filtered_sentence.append( wnl.lemmatize(word, pos='a'))
        else:
            filtered_sentence.append(word)
    return filtered_sentence

def preProcess(text):

    text=word_tokenize(text)
    text=removePuncs(text)
    text=removeAcronomy(text)
    text =normalization(text)
    text=remove_stopwords(text)
    text = stemmer(text)
    text = lemmatizer(text)

    return text