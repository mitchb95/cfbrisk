from pymongo import MongoClient
from datetime import date

dateStart = date(2018, 4, 30)
dateEnd = date.today()
delta = dateEnd - dateStart
NUM_DAYS = delta.days

def writeActiveUsers(days, teams):
    participationFile = open('active_users.csv', 'w')

    participationFile.write('Team,')
    for day in days:
        participationFile.write('Day ' + day + ',')

    participationFile.write('\n')

    for team in teams:
        participationFile.write(team + ',')
        for day in days:
            participationFile.write(str(votes.find({'day' : str(day), 'team' : team}).count()) + ',')
            
        participationFile.write('\n')

    participationFile.write('TOTAL,')
    for day in days:
        participationFile.write(str(votes.find({'day' : str(day)}).count()) + ',')

    participationFile.write('\n')

def writeVotingHistory(users, days, teams):
    votingHistoryFile = open('voting_history.csv', 'w')
    votingHistoryFile.write('Username, Team, ')
    for day in days:
        votingHistoryFile.write('Day ' + str(day) + ',')
    votingHistoryFile.write('\n')

    for user in users:
        votingHistoryFile.write(user + ',')
        for day in days:
            print str(day) + " " + user
            vote = votes.find_one({'day' : str(day), 'username' : user})
            if vote is None:
                votingHistoryFile.write('N/A,')
            else:
                votingHistoryFile.write(vote['territory'] + ',')
        votingHistoryFile.write('\n')
    
    votingHistoryFile.close()

def writeActiveStars(days, teams):
    participationFile = open('active_stars.csv', 'w')

    participationFile.write('Team,')
    for day in days:
        participationFile.write('Day ' + day + ',')

    participationFile.write('\n')

    for team in teams:
        participationFile.write(team + ',')
        for day in days:
            teamStars = 0
            for vote in votes.find({'day' : str(day), 'team' : team}):
                teamStars = teamStars + vote['stars']
            participationFile.write(str(teamStars) + ',')
            
        participationFile.write('\n')

    participationFile.write('TOTAL,')
    for day in days:
        participationFile.write(str(votes.find({'day' : str(day)}).count()) + ',')

    participationFile.write('\n')

    participationFile.close()

    participationFile.close()


client = MongoClient('192.168.1.200', 27017)
votes_db = client.test_votes_db
votes = votes_db.votes

teams = votes.distinct('team')
users = votes.distinct('username')

#writeActiveUsers(days, teams)
#writeActiveStars(days, teams)
writeVotingHistory(users, range(1, NUM_DAYS+1), ['Florida'])

