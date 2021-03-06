from googleapiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from os.path import expanduser

FILE_ID = '1p_wGW4VdSSHqaUFmxtlRSFnZ0-YCVwwa014ncVXNPfk'
FULL_FILE_ID = '1IabFOGN4rLEBEcLBqBmypouP7buTotxaG2cjku-eJ38'
TEAM_FILE_ID = '1ganoHOif2wmrK5jCkwiFwWFH97O9J3ENODYcF6e2LEc'

# TODO: Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
#
# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/spreadsheets'
# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage(expanduser('~') + '/credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(expanduser('~') + '/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

currentFile = service.files().get(fileId=FILE_ID).execute()

file_metadata = {
    'name': '/r/ForidaGatorsPREMIUM Counterintelligence',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

media = MediaFileUpload('results.csv',
        mimetype='text/csv',
        resumable=True)

updatedFile = service.files().update(
        fileId=FILE_ID,
        body=file_metadata,
        media_body=media).execute()

sheetsService = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

# INTERNAL VOTING HISTORY
sheet_metadata = sheetsService.spreadsheets().get(spreadsheetId=FILE_ID).execute()
sheets = sheet_metadata.get('sheets', '')
title = sheets[0].get("properties", {}).get("title", "/r/FloridaGatorsPREMIUM Counterintelligence")
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
        spreadsheetId=FILE_ID, body=reqs).execute()

# FULL VOTING HISTORY

currentFile = service.files().get(fileId=FULL_FILE_ID).execute()

file_metadata = {
    'name': 'CFB Risk Full Voting History',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

media = MediaFileUpload('resultsFull.csv',
        mimetype='text/csv',
        resumable=True)

updatedFile = service.files().update(
        fileId=FULL_FILE_ID,
        body=file_metadata,
        media_body=media).execute()

sheet_metadata = sheetsService.spreadsheets().get(spreadsheetId=FULL_FILE_ID).execute()
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
        spreadsheetId=FULL_FILE_ID, body=reqs).execute()

# FULL TEAM HISTORY
currentFile = service.files().get(fileId=TEAM_FILE_ID).execute()

file_metadata = {
    'name': 'CFB Risk Full Team History',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

media = MediaFileUpload('resultsTeamFull.csv',
        mimetype='text/csv',
        resumable=True)

updatedFile = service.files().update(
        fileId=TEAM_FILE_ID,
        body=file_metadata,
        media_body=media).execute()

sheet_metadata = sheetsService.spreadsheets().get(spreadsheetId=TEAM_FILE_ID).execute()
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
        spreadsheetId=TEAM_FILE_ID, body=reqs).execute()

