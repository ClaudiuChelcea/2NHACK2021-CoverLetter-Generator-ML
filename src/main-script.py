from nltk import tokenize
from operator import itemgetter
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

import requests
import urllib.request
from urllib.request import urlopen
import nltk
from bs4 import BeautifulSoup

# Get X keywords
# Define your X
X = 0
while 1:
    try:
        X = int(input("How many keywords do you want: "))
        break
    except:
        continue

# Input url
url = input("Url: ")

# Get html code
html = urlopen(url).read()

# Remove html
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())

# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

doc = text

def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

nltk.data.load('tokenizers/punkt/english.pickle')
stop_words=get_stop_words("resources/stopwords.txt")

total_words = doc.split()
total_word_length = len(total_words)
#print(total_word_length)

total_sentences = tokenize.sent_tokenize(doc)
total_sent_len = len(total_sentences)
# print(total_sent_len)

tf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in tf_score:
            tf_score[each_word] += 1
        else:
            tf_score[each_word] = 1

# Dividing by total_word_length for each dictionary element
tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
#print(tf_score)

def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

idf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in idf_score:
            idf_score[each_word] = check_sent(each_word, total_sentences)
        else:
            idf_score[each_word] = 1

# Performing a log and divide
idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

#print(idf_score)

tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
#print(tf_idf_score)

def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
    return result

#link https://www.bestjobs.eu/en/job/c-gameplay-programmer

for key2remove in stop_words:
    try:
        tf_idf_score.pop(key2remove)
    except:
        continue;

for key in get_top_n(tf_idf_score, X):
    print(key)


