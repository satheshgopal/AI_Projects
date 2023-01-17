from flask import Flask, render_template, request
from flask import url_for, redirect, render_template_string
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_paginate import Pagination, get_page_args
from flask_mongoengine import MongoEngine
import en_core_web_lg
import en_core_web_sm
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from stop_words import get_stop_words
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import spacy
import en_core_web_lg
nlp = spacy.load("en_core_web_sm")
import glob
import pandas as pd
from spacy.matcher import Matcher
from spacy import displacy
import visualise_spacy_tree
from IPython.display import Image, display
nlp=spacy.load('en_core_web_sm',disable=['ner','textcat'])
import os, pdb
import unidecode 
import string
from autocorrect import Speller
from bs4 import BeautifulSoup 
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import regex as re
from spacy.tokens import Doc
from spacy.vocab import Vocab
nltk.download('tagsets')
nltk.help.upenn_tagset('NN')
from nltk import pos_tag
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import TweetTokenizer


def clean_text(text):   
    text_nonum = re.sub(r'\d+', '', text)    
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation])
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_no_doublespace


stopwords = list(get_stop_words('en'))



print('-------Question-------')
question_input = "Database Question: What is the capital of India ?"
print(question_input)

print('-------Answer-------')
answer_db_input = "Delhi"
answer_user_input = "noida 5"
print("Database Answer: ", answer_db_input)
print("User Answer: ", answer_user_input)


print('-------Clean Text-------') 
answer_db=clean_text(answer_db_input)
answer_user=clean_text(answer_user_input) 
print("Clean Text User: ",answer_db)
print("Clean Text Database: ",answer_user) 

print('-------Speller-------')
spell=Speller(lang='en')
Corrected_text_db=spell(answer_db)
Corrected_text_user=spell(answer_user)
print("Text after spell check User: ",Corrected_text_db)
print("Text after spell check Database: ",Corrected_text_user)

print('-------Tokenize-------')
tokens_db=word_tokenize(Corrected_text_db)
tokens_user=word_tokenize(Corrected_text_user)
print("User:",tokens_db)
print("Database: ",tokens_user)

print('-------Upper to lower-------')
lower_output_db=[w.lower() for w in tokens_db]
print("User:",lower_output_db)
lower_output_user=[w.lower() for w in tokens_user]
print("Database: ",lower_output_user)

print('-------Stopword Removal-------')
stopwords_db=[w for w in lower_output_db if not w in stopwords]
print("Text after stopword removal User:- ","\n",stopwords_db)
stopwords_user=[w for w in lower_output_user if not w in stopwords]
print("Text after stopword removal Database:- ","\n",stopwords_user)

print('-------PorterStemmer-------')
porter=PorterStemmer()
stemmed_db=[porter.stem(word) for word in stopwords_db]
stemmed_user=[porter.stem(word) for word in stopwords_user]
print("User:",stemmed_db)
print("Database: ",stemmed_user)


print('-------Arry to String-------')
def listToString(s): 
    str1 = ""  
    for ele in s: 
        str1 += ele  
    return str1 

stemmed_string_db = listToString(stemmed_db)
stemmed_string_user = listToString(stemmed_user)

print(stemmed_string_db)
print(stemmed_string_user)

print('-------NLP-------')

nlp_string_db = nlp(stemmed_string_db)
nlp_string_user = nlp(stemmed_string_user)

print(nlp_string_db)
print(nlp_string_user)

print('-------Similarity-------')
similarity = nlp_string_db.similarity(nlp_string_user)*100,"%"
print(similarity)