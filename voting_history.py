import pymongo
from pymongo import MongoClient
from sets import Set
import pprint

client = MongoClient('192.168.1.200', 27017)
votes_db = client.test_votes_db
votes = votes_db.votes

