import json
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import pickle
import re
import numpy as np
def clean_text(text):
    text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)
    text = re.sub(r'[^\w\s]','',text)
    text = text.replace(r'http(\S)+', r'')
    text = text.replace(r'http ...', r'')
    text = text.replace(r'(RT|rt)[ ]*@[ ]*[\S]+',r'')
    text = text.replace(r'@[\S]+',r'')
    text = text.replace(r'_[\S]?',r'')
    text = text.replace(r'[ ]{2, }',r' ')
    text = text.replace(r'&amp;?',r'and')
    text = text.replace(r'&lt;',r'<')
    text = text.replace(r'&gt;',r'>')
    text = text.replace(r'([\w\d]+)([^\w\d ]+)', r'\1 \2')
    text = text.replace(r'([^\w\d ]+)([\w\d]+)', r'\1 \2')
    text = text.lower()
    text = text.strip()
    return text

def text_preprocessing(string):
    string = string.strip().lower().replace('\ufeff','')
    string = re.sub(r"[(),.!?\'\`]", " ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(" +", " ", string)
    string = string.rstrip().lstrip()
    string = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), string, flags=re.IGNORECASE)
    return string

def preprocess(text):
    print(type(text))
    text = text.lower().strip()
    text = clean_text(text)
    text = text_preprocessing(text)
    return txt

def count_words_fast(text):	
	text = text.lower()
	skips = [".", ", ", ":", ";", "'", '"']
	for ch in skips:
		text = text.replace(ch, "")
	word_counts = Counter(text.split(" "))
	return word_counts
# word_counts = count_words_fast(text)
def word_stats(word_counts):	
	num_unique = len(word_counts)
	counts = word_counts.values()
	return (num_unique, counts)


import pandas as pd

df1 = pd.read_csv('data_baoNhanDan.csv', usecols=['Title'])
df1['label'] = [0] * len(df1)
df2 = pd.read_csv('data_Thoisu_viettan2.csv',usecols=['Title'])
df2['label'] = [1] * (len(df2))
frames = [df1, df2]
df = pd.concat(frames)
df = df.sample(frac = 1)
print("Num of positive and negative:\t" + str(len(df1)) + "\t" + str(len(df2)))
print(df.head(5))



