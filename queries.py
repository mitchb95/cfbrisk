import pymongo
from pymongo import MongoClient
from sets import Set
import pprint

client = MongoClient('192.168.1.200', 27017)
votes_db = client.test_votes_db
votes = votes_db.votes

users = Set()
for vote in votes.find({"team" : "Florida"}):
    users.add(vote['username'])

outputFile = open('users.csv', 'w')
for user in users:
    outputFile.write(user + '\n')
outputFile.close()

outputFile = open('stars_user.csv', 'w')
for user in users:
    vote = votes.find_one({'username' : user}, sort=[('stars', pymongo.DESCENDING)])
    outputFile.write(str(vote['stars']) + ", " + user + "\n")
outputFile.close()

