import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import warnings

#
#
#
# THIS SCRIPT RETURNS THE MOST -- X -- COMMON WORDS FROM THE INSERTED TEXTS
#
#
#

# Define your X
X = 0
while 1:
    try:
        X = int(input("How many common words do you want: "))
        break
    except:
        continue

# Prerequisites
warnings.simplefilter(action='ignore', category=FutureWarning)

# read json into a dataframe
doc = "data/stackoverflow-test.json"
doc = "data/job.json"
df_idf=pd.read_json(doc,lines=True)

#doc = "data/job.txt"

# our document that contains the text
#with open(doc, encoding="utf8") as f:
#    df_idf = f.read()


# print schema
# print("Schema:\n\n",df_idf.dtypes) # types, 20000 rows, 19 tags
# print("Number of questions,columns=",df_idf.shape)

def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results

df_idf['text'] = df_idf['title'] + df_idf['body']

########################################################################

# Display the nth test
# n = 2;
 #print(df_idf['text'][n])

#load a set of stop words
stopwords=get_stop_words("resources/stopwords.txt") #ignore most-common words

#get the text column
docs=df_idf['text'].tolist()
print(docs)

#create a vocabulary of words,
# ignore words that appear in 85% of documents,
# eliminate stop words
cv=CountVectorizer(max_df=0.6,stop_words=stopwords,max_features=10000,strip_accents=None) # all the common words
word_count_vector=cv.fit_transform(docs)

# Check top 10 vocabulary
# print(list(cv.vocabulary_.keys())[:X])

# Get Inverse Document Frequency
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

# print(word_count_vector)

# you only need to do this once, this is a mapping of index to
feature_names=cv.get_feature_names()
#print(feature_names)

#print(feature_names)

#generate tf-idf for the given document
# print(cv.transform(docs))
tf_idf_vector=tfidf_transformer.transform(cv.transform(docs))

#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())
#print(sorted_items)

#extract only the top n; n here is 10
keywords=extract_topn_from_vector(feature_names,sorted_items,X)

# now print the results
# print("\n=====Doc=====")
# print(doc)
print("\n===Keywords===")
for k in keywords:
    print(k,keywords[k])