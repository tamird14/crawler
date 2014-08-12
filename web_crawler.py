import time

__author__ = 'Tamir'

import urllib2
import pymongo
from bs4 import BeautifulSoup
import re


class DataBaseFull(RuntimeError):
    def __init__(self, arg):
        self.args = arg


def get_questions(url, collection):
    """
    Adding questions to the database
    :type collection: pymongo.collection.Collection
    :type url: str
    :param url: The URL of the page with the questions
    :param collection: The DataBase collection
    """
    content = BeautifulSoup(urllib2.urlopen(url).read())
    _title = content.title.string
    tag = [td_tag for td_tag in content.find_all('td') if td_tag.get('class') == [unicode("postcell")]][0]
    body = tag.div.div.get_text()
    _id = url.split("/")[4]
    collection.insert({"Title": _title[0:len(_title) - 17], "Body": body, "Id": _id})


def get_pages(collection):
    """
    Going over the pages in the 'votes' section
    :param collection: The DataBase collection
    :raise Exception: We've reach the limit of questions in the Database
    """
    preface = re.compile('/questions/[0-9]+')
    i = 1
    while True:
        website = "http://stackoverflow.com/questions?page=" + str(i) + "&sort=votes"
        response = urllib2.urlopen(website)
        soup = BeautifulSoup(response.read())
        links = [a_tag.get('href') for a_tag in soup.find_all('a')]
        for link in links:
            if collection.count() == MAX_QUESTIONS:
                raise DataBaseFull("Finish")
            if preface.match(str(link)):
                get_questions('http://stackoverflow.com' + link, collection)
        i += 1


MAX_QUESTIONS = 4321

client = pymongo.MongoClient()
sof = client.stack_over_flow
col = sof.questions
t1 = time.clock()
try:
    get_pages(col)
except DataBaseFull:
    t2 = time.clock()
    print "total time =", t2 - t1
print col.count()