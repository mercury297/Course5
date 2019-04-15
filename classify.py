import json

data = []
with open("data.json", "r") as read_file:
    data = json.load(read_file)


import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')


def lemmatized(text):
    doc_sample = text
    # print('original document: ')
    words = []
    result = []
    for word in doc_sample.split(' '):
        words.append(word)
    # print(words)
    # print('\n\n tokenized and lemmatized document: ')
    stemmer = SnowballStemmer("english")
    for i in range(len(words)):
        if(words[i] not in gensim.parsing.preprocessing.STOPWORDS and len(words[i]) > 3):
            result.append(stemmer.stem(words[i]))
    return result

lem_dict = []
cnt = 0
for i in data:
    temp = lemmatized(i)
    lem_dict.append(temp)

dictionary = gensim.corpora.Dictionary(lem_dict)

count = 0
# for k, v in dictionary.iteritems():
#     print(k, v)
#     count += 1
#     if count > 20:
#         break


dictionary.filter_extremes(no_below=20, no_above=0.5, keep_n=1000)

# print(dictionary)

bow_corpus = [dictionary.doc2bow(doc) for doc in lem_dict]

tfidf = models.TfidfModel(bow_corpus)


corpus_tfidf = tfidf[bow_corpus]

# print(corpus_tfidf)

lda_model_tfidf = gensim.models.LdaModel(corpus_tfidf, num_topics=15, id2word=dictionary)

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

buckets = ['Battery Life','Picture Quality','Value for Money','Sound Quality','Fingerprint']
bucket_res = []
for i in buckets:
    temp = lemmatized(i)
    bucket_res.append(temp)

print(bucket_res)

test_data = []

with open("data_100.json", "r") as read_file:
    test_data = json.load(read_file)

bucket_dict = {}
cnt = 0
for i in buckets:
    bucket_dict.update({cnt:[]})
    cnt += 1

cnt = 0
for i in test_data:
    if(cnt == 5):
        break
    temp = i
    bow_vector = dictionary.doc2bow(lemmatized(i))
    for index, score in sorted(lda_model_tfidf[bow_vector], key=lambda tup: -1 * tup[1]):
        # print("Score: {}\t Topic: {}".format(score, lda_model_tfidf.print_topic(index, 5)))
        # print(lda_model_tfidf.print_topic(index, 5))
        string = lda_model_tfidf.print_topic(index, 5).split('+')
        for i in range(len(string)):
            fl = string[i].split('*')
            temp = fl[1].replace('"', '')
            string[i] = temp
        for i in bucket_res:
            for j in i:
                if(j in string):
                    ind = bucket_res.index(i)
                    bucket_dict[ind].append(temp)
                    break

# print(bucket_dict)

tops = json.dumps(bucket_dict)
out = open('classified.json', 'w')
out.write(tops)

