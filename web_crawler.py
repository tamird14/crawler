__author__ = 'Tamir'

import urllib2
import pymongo
from bs4 import BeautifulSoup


client = pymongo.MongoClient()
sof = client.stack_over_flow
col = sof.questions

WEBSITE = 'http://stackoverflow.com/'
response = urllib2.urlopen(WEBSITE)
soup = BeautifulSoup(response.read())
print soup.get_text()