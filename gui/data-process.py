from bs4 import BeautifulSoup
import re
import requests
import json
import nltk
#nltk.download('punkt')
from b_parser import RafiStemmer

def valid_bengali_letters(char):
    return ord(char) >= 2433 and ord(char) <= 2543


def get_replacement(char):
    if valid_bengali_letters(char):
        return char
    newlines = [10, 2404, 2405, 2551, 9576]
    if ord(char) in newlines:
        return ''
    return ' '


def get_valid_lines(line):
    copy_line = ''
    for letter in line:
        copy_line += get_replacement(letter)
    return copy_line


stopwords_file = open(
    './stop_words.txt', "r+", encoding='utf-8')
all_stopwords = stopwords_file.read()
stopwords_ready = [word.strip() for word in all_stopwords.split()]


def remove_stopwords(content):
    without_stopwords = []
    for word in content:
        if word not in stopwords_ready and len(word) > 2:
            without_stopwords.append(word)
    return without_stopwords


stemmer = RafiStemmer()

def stemming_data(content):
    for i, word in enumerate(content):
        content[i] = stemmer.stem_word(word)
    return content


def merge_to_string(content_list):
    strLine = ''
    for word in content_list:
        strLine += word + ' '
    return strLine


def single_data_preprocessor(content):
    content_valid = get_valid_lines(content)
    content_tokenized = nltk.word_tokenize(get_valid_lines(content_valid))
    content_without_stopwords = remove_stopwords(content_tokenized)
    content_stemmed = stemming_data(content_without_stopwords)
    content_str = merge_to_string(content_stemmed)

    return content_str


with open('./input.json', encoding='utf-8') as json_file:
    raw_data_json = json.load(json_file)
    raw_news_data = raw_data_json['news']
    data_processed = single_data_preprocessor(raw_news_data)
    print(data_processed)
