from pymongo import MongoClient
from datetime import date
from googleapiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from os.path import expanduser
import scraper

dateStart = date(2018, 4, 30)
dateEnd = date.today()
delta = dateEnd - dateStart
NUM_DAYS = delta.days

VOTES_FILE_ID = '120dt3ilg4HwlNaYwgeER_k_H9Gu1xVJ_eDPzQTH5ulE'
TEAMS_FILE_ID = '135_Y2k18ZutKJaOJbOjdUsY1BDwftdavBCRXU0410EA'
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage(expanduser('~') + '/credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(expanduser('~') + '/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

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

def writeTeamHistory(users, days, teams):
    teamsHistoryFile = open('teams_history.csv', 'w')
    teamsHistoryFile.write('Username, ')
    for day in days:
        teamsHistoryFile.write('Day ' + str(day) + ',')
    teamsHistoryFile.write('\n')

    for user in users:
        teamsHistoryFile.write(user + ',')
        for day in days:
            vote = votes.find_one({'day' : str(day), 'username' : user})
            if vote is None:
                teamsHistoryFile.write('N/A,')
            else:
                teamsHistoryFile.write(vote['team'] + ',')
        teamsHistoryFile.write('\n')
    
    teamsHistoryFile.close()

    currentFile = service.files().get(fileId=TEAMS_FILE_ID).execute()

    file_metadata = {
        'name': 'CFB Risk Full Teams History',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }

    media = MediaFileUpload('teams_history.csv',
            mimetype='text/csv',
            resumable=True)

    updatedFile = service.files().update(
            fileId=TEAMS_FILE_ID,
            body=file_metadata,
            media_body=media).execute()

    sheetsService = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
    sheet_metadata = sheetsService.spreadsheets().get(spreadsheetId=TEAMS_FILE_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    title = sheets[0].get("properties", {}).get("title", "CFB Risk Full Team History")
    sheetId = sheets[0].get("properties", {}).get("sheetId", 0)
    print sheetId

    reqs = {'requests': [
        # frozen row 1
        {'updateSheetProperties': {
            'properties': { 'sheetId' : sheetId, 'gridProperties': {'frozenRowCount': 1}},
            'fields': 'gridProperties.frozenRowCount',
        }},
        # embolden row 1
        {'repeatCell': {
            'range': {'sheetId' : sheetId, 'endRowIndex': 1},
            'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
            'fields': 'userEnteredFormat.textFormat.bold',
        }}
    ]}

    res = sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=TEAMS_FILE_ID, body=reqs).execute()

def writeVotingHistory(users, days, teams):
    votingHistoryFile = open('voting_history.csv', 'w')
    votingHistoryFile.write('Username, Team, ')
    for day in days:
        votingHistoryFile.write('Day ' + str(day) + ',')
    votingHistoryFile.write('\n')

    for user in users:
        votingHistoryFile.write(user + ',')
        vote = votes.find_one({'username' : user})
        votingHistoryFile.write(vote['team'] + ',')
        for day in days:
            vote = votes.find_one({'day' : str(day), 'username' : user})
            if vote is None:
                votingHistoryFile.write('N/A,')
            else:
                votingHistoryFile.write(vote['territory'] + ',')
        votingHistoryFile.write('\n')
    
    votingHistoryFile.close()

    currentFile = service.files().get(fileId=VOTES_FILE_ID).execute()

    file_metadata = {
        'name': 'CFB Risk Full Voting History',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }

    media = MediaFileUpload('voting_history.csv',
            mimetype='text/csv',
            resumable=True)

    updatedFile = service.files().update(
            fileId=VOTES_FILE_ID,
            body=file_metadata,
            media_body=media).execute()

    sheetsService = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
    sheet_metadata = sheetsService.spreadsheets().get(spreadsheetId=VOTES_FILE_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    title = sheets[0].get("properties", {}).get("title", "CFB Risk Full Voting History")
    sheetId = sheets[0].get("properties", {}).get("sheetId", 0)
    print sheetId

    reqs = {'requests': [
        # frozen row 1
        {'updateSheetProperties': {
            'properties': { 'sheetId' : sheetId, 'gridProperties': {'frozenRowCount': 1}},
            'fields': 'gridProperties.frozenRowCount',
        }},
        # embolden row 1
        {'repeatCell': {
            'range': {'sheetId' : sheetId, 'endRowIndex': 1},
            'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
            'fields': 'userEnteredFormat.textFormat.bold',
        }}
    ]}

    res = sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=VOTES_FILE_ID, body=reqs).execute()

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

#writeVotingHistory(users, range(1, NUM_DAYS+1), ['Florida'])
writeTeamHistory(users, range(1, NUM_DAYS+1), ['Florida'])

