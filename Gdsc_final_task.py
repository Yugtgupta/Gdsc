# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19nKso2KGwenxaq9al6wgGRjcak08jNss
"""

import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')

data = pd.read_csv('data.csv')

data.head()

stop_words = set(stopwords.words('english'))

def convert_text(Sentence):
    tokens = nltk.word_tokenize(Sentence) #idhar tokens me divide kardiya
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in string.punctuation] #punctuation marks removed
    tokens = [word for word in tokens if word not in stop_words] #stop words nikaal diye
    return ' '.join(tokens)

data['Converted_text'] = data['Sentence'].apply(convert_text)

data.head()

X = data['Converted_text']
y = data['Sentiment']

np.random.seed(42)

# Encode labels (positive, negative, neutral) to numerical values
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

tfidf_vectorizer = TfidfVectorizer(max_features=1000)

X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

from sklearn.linear_model import LogisticRegression
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train_tfidf, y_train);

y_pred = logistic_regression.predict(X_test_tfidf)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1}')
print('Classification Report:')
print(report)

