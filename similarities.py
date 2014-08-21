__author__ = 'Tamir'

import numpy
import pymongo
import urllib2
import heapq
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_question():
    """
    Gets from the user an ID of a question from SOF
    Return the question
    :return: the question asked
    """
    while True:
        question_id = raw_input("Please enter the ID of the question: ")
        question_url = "http://stackoverflow.com/questions/" + question_id
        try:
            content = BeautifulSoup(urllib2.urlopen(question_url).read())
            tag = [td_tag for td_tag in content.find_all('td') if td_tag.get('class') == [unicode("postcell")]][0]
            body = tag.div.div.get_text()
            return body
        except:
            print "Oops! Something wrong with the ID. Try another one."


def get_best_similarities(docs):
    """
    :param docs: All the questions in the Database including the question searched
    :return: Arrays of the the questions' indexes, their scores and the last index of 'most_similar_
    """
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
    similar = cosine_similarity(tfidf_matrix[0], tfidf_matrix)[0]
    most_similar = heapq.nlargest(7, similar)
    _index = 1
    if int(most_similar[1]) == 1.0:
        _index += 1
    index_array = []
    for i in range(5):
        index_array.append(numpy.where(similar == most_similar[_index]))
        _index += 1
    return index_array, most_similar, _index


def print_matches(index_arr, best_results_arr, last_cell):
    """
    Prints the best 5 matches for the question given
    :param index_arr: Array of the questions' indexes
    :param best_results_arr: Array of the questions' scores
    :param last_cell: The last index in best_results
    """
    print "Best 5 matches are:"
    for i in range(5):
        print "http://stackoverflow.com/questions/" + col.find()[index_arr[i][0][0]]["Id"], "with", \
            str(round(best_results_arr[last_cell - 5 + i] * 100, 2)) + "%"


client = pymongo.MongoClient()
sof = client.stack_over_flow
col = sof.questions

question = get_question()
documents = [question] + [doc["Body"] for doc in col.find()]
index, best_results, cell = get_best_similarities(documents)
print_matches(index, best_results, cell)