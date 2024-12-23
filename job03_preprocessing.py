import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

df = pd.read_csv('./crawling_data/naver_headline_news20241219_KKW.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df['titles']
Y = df['category']

print(X[0])
okt = Okt()
okt_x = okt.morphs(X[0], stem=True)
print('Okt :', okt_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:3])

label = encoder.classes_
print(label)

with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_y)
print(onehot_Y)

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
print(X)

stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)
print(stopwords)

for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:
            if X[sentence][word] not in list(stopwords['stopword']):
                words.append(X[sentence][word])
    X[sentence] = ' '.join(words)

print(X[:5])

token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1
print(wordsize)

print(tokened_X[:5])

max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

with open('./models/news_token_max_{}.pickle'.format(max), 'wb') as f:
    pickle.dump(token, f)

X_pad = pad_sequences(tokened_X, max)
print(X_pad)
print(len(X_pad[0]))

X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

np.save('./crawling_data/news_data_X_train_wordsize_{}_max_{}'.format(wordsize, max), X_train)
np.save('./crawling_data/news_data_Y_train_wordsize_{}_max_{}'.format(wordsize, max), Y_train)
np.save('./crawling_data/news_data_X_test_wordsize_{}_max_{}'.format(wordsize, max), X_test)
np.save('./crawling_data/news_data_Y_test_wordsize_{}_max_{}'.format(wordsize, max), Y_test)

























