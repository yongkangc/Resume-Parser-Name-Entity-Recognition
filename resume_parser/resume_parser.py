"""
Parses Resume and returns skill,education,work experience
"""


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import spacy
import pickle
import random
import sys, fitz
import docx
import docx2txt
import os
from utils import constants as cs
import re


def parse_resume(file_path):
    text= get_text(file_path)
    segment = classify_resume(text)
    return segment

def tokenize(text):
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(text)
    noun_chunks = nlp_text.noun_chunks
    return nlp_text,noun_chunks

def extract_skills(text):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    nlp_text, noun_chunks = tokenize(text)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_education(nlp_text):
    '''
    Helper function to extract education from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found else only returns education degree
    '''
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]
     # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

#Extract text from DOCX
def get_text_doc(file_path):
    '''
    Helper function to extract the plain text from .docx files

    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    '''
    temp = docx2txt.process(file_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)
    

# Get text from pdf
def get_text_pdf(file_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    '''
    doc = fitz.open(file_path)
    txt = ""
    for page in doc:
        txt = txt + str(page.getText())
    # print(txt)
    text = " ".join(txt.split('\n'))
    # print(text)
    return text


def get_text(file_path):
    '''
    Wrapper function to detect the file extension and call text extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    ext = os.path.splitext(file_path)[1]
    if ext==".pdf":
        txt = get_text_pdf(file_path)
        
    elif ext==".doc" or ext==".docx":
        txt=get_text_doc(file_path)
        print(txt)

    return txt

def classify_resume(txt):
    """
    Classifying the resume using NER
    """
    nlp_model = spacy.load('nlp_ner_model')
    # Applying the model
    doc = nlp_model(txt)
    skills = extract_skills(txt)
    education = extract_education(txt)
    segment = ""
    for ent in doc.ents:
        segment += (f'{ent.label_.upper():{30}}- {ent.text}\n')
    segment += f"{'SKILLS':{30}}- {','.join(skills)}\n"
    segment += f"{'EDUCATION':{30}}- {','.join(education)}\n"
    return segment


if __name__ == "__main__":
    print(parse_resume("./data/resume/ivan_machine_learning_engineer.pdf"))