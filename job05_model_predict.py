import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

df = pd.read_csv('./crawling_data/naver_headline_news_20241223.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df['titles']
Y = df['category']

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

label = encoder.classes_
print(label)

labeled_y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_y)
print(onehot_Y)

okt = Okt()

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

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 16:
        tokened_X[i] = tokened_X[i][:16]
X_pad = pad_sequences(tokened_X, 16)

print(X_pad[:5])

model = load_model('./models/news_category_classfication_model_0.6832844614982605.h5')
preds = model.predict(X_pad)

predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    predicts.append(most)
df['predict'] = predicts

print(df.head(30))

















