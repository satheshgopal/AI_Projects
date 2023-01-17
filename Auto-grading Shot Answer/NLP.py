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



def purifytext(answer_db_input, answer_user_input):

	

	print('-------String-------')	
	print("User Input: ", answer_user_input)


	print('-------Clean Text-------') 	
	answer_user=clean_text(answer_user_input)	
	print("Clean Text User: ",answer_user) 

	print('-------Speller-------')
	spell=Speller(lang='en')	
	Corrected_text_user=spell(answer_user)	
	print("Text after spell check User: ",Corrected_text_user)

	print('-------Tokenize-------')	
	tokens_user=word_tokenize(Corrected_text_user)	
	print("User: ",tokens_user)

	print('-------Upper to lower-------')	
	lower_output_user=[w.lower() for w in tokens_user]
	print("User: ",lower_output_user)

	#print('-------Stopword Removal-------')	
	#stopwords_user=[w for w in lower_output_user if not w in stopwords]
	#print("Text after stopword removal User:- ","\n",stopwords_user)

	print('-------PorterStemmer-------')
	porter=PorterStemmer()	
	stemmed_user=[porter.stem(word) for word in lower_output_user]	
	print("User: ",stemmed_user)


	print('-------Arry to String-------')
	def convert(lst):     
	   	return ' '.join(lst)

	stemmed_string_user = convert(stemmed_user)	
	print(stemmed_string_user)

	print('-------NLP-------')

	nlp_string_db = nlp(answer_db_input)
	nlp_string_user = nlp(stemmed_string_user)

	print(nlp_string_db)
	print(nlp_string_user)

	print('-------Similarity-------')
	similarity = nlp_string_db.similarity(nlp_string_user)*100,"%"
	passfail = nlp_string_db.similarity(nlp_string_user)*100
	print(passfail)

	print('-------Result-------')
	if passfail >= 75:
		print("Pass")
	else:
		print("Fail")	

	return similarity


print('-------Final Result-------')
final = purifytext("hello how are you","hello how 2313131")
print(final)

