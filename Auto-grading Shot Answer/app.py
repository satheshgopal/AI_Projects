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


app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/quiz'
mongo = PyMongo(app)



@app.route("/")
def index():
    try:        
        questions = mongo.db.questions.find()
        results_count = questions.count()        
        return render_template('index.html', quest = questions)
    except Exception as e:
        return dumps({'error' : str(e)})

def clean_text(text):   
    text_nonum = re.sub(r'\d+', '', text)    
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation])
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_no_doublespace
    
stopwords = list(get_stop_words('en'))

@app.route('/questions', methods=['POST', 'GET'])
def questions(): 
    msg = ''
    if request.method == 'POST' and 'question' in request.form and 'answer' in request.form :
        question = request.form['question']
        answer = request.form['answer']
        id = mongo.db.questions.insert({'question':question,'answer':answer})
        msg = 'Question successfully insert !'        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('questions.html', msg = msg)


@app.route("/user")
def user():
    try:        
        questions = mongo.db.questions.find()
        results_count = questions.count()        
        return render_template('user.html', quest = questions)
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/result',methods=['POST', 'GET'])
def result():
    msg = ''
    if request.method == 'POST':        
        questions = mongo.db.questions.find()
        quest = mongo.db.questions.find()
        results_count = questions.count()
        ques_id = request.form.getlist('id[]')        
        ques_ans = request.form.getlist('youranswer[]')        
        

        tmplist = []    
        for questions in questions:
            doc = nlp(questions['answer'])
            tmplist.append(doc)

        youranslist = []
        for uq in ques_ans:
            doc1 = uq           
            doc1str = str(doc1)            
            doc1strclean = clean_text(doc1str)            
            youranslist.append(nlp(doc1strclean))

                         
        similaritylist = []
        passfaillist = []    
        for x in range(results_count):
            answer_user_input = str(ques_ans[x])
            answer_db_input = str(tmplist[x])            
            print('-------String-------')   
            print("User Answer: ", answer_user_input)
            print("Database Answer: ", answer_db_input)
            print('-------Clean Text-------')   
            answer_user=clean_text(answer_user_input) 
            answer_db=clean_text(answer_db_input)   
            print("Clean Text User: ",answer_user)
            print("Clean Text Database: ",answer_db)
            print('-------Speller-------')
            spell=Speller(lang='en')    
            Corrected_text_user=spell(answer_user)
            Corrected_text_db=spell(answer_db)  
            print("Text after spell check User: ",Corrected_text_user)
            print("Text after spell check Database: ",Corrected_text_db)
            print('-------Tokenize-------') 
            tokens_user=word_tokenize(Corrected_text_user)
            tokens_db=word_tokenize(Corrected_text_db)  
            print("User: ",tokens_user)
            print("Database: ",tokens_db)
            print('-------Upper to lower-------')   
            lower_output_user=[w.lower() for w in tokens_user]
            lower_output_db=[w.lower() for w in tokens_db]
            print("User: ",lower_output_user)
            print("Database: ",lower_output_db)
            #print('-------Stopword Removal-------')    
            #stopwords_user=[w for w in lower_output_user if not w in stopwords]
            #print("Text after stopword removal User:- ","\n",stopwords_user)
            print('-------PorterStemmer-------')
            porter=PorterStemmer()  
            stemmed_user=[porter.stem(word) for word in lower_output_user] 
            stemmed_db=[porter.stem(word) for word in lower_output_db] 
            print("User: ",stemmed_user)
            print("Database: ",stemmed_db)
            print('-------Arry to String-------')
            def convert(lst):     
                return ' '.join(lst)                
            stemmed_string_user = convert(stemmed_user)
            stemmed_string_db = convert(stemmed_db) 
            print(stemmed_string_user)
            print(stemmed_string_db)
            print('-------NLP-------')            
            nlp_string_user = nlp(stemmed_string_user)
            nlp_string_db = nlp(stemmed_string_db)

            print(nlp_string_db)
            print(nlp_string_user)
            print('-------Similarity-------')
            similarity = nlp_string_db.similarity(nlp_string_user)*100,"%"    
            passfail = nlp_string_db.similarity(nlp_string_user)*100
            print(similarity)
            similaritylist.append(similarity)
            passfaillist.append(passfail)
            
                 
            

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('result.html', msg = msg,quest = quest,youranslist = youranslist,similaritylist=similaritylist,passfaillist=passfaillist)   






if __name__ == "__main__":
    app.run(debug=True)
