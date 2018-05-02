from googleapiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from os.path import expanduser

FILE_ID = '1p_wGW4VdSSHqaUFmxtlRSFnZ0-YCVwwa014ncVXNPfk'

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
    'name': 'CFB Risk',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

media = MediaFileUpload('results.csv',
        mimetype='text/csv',
        resumable=True)

updatedFile = service.files().update(
        fileId=FILE_ID,
        body=file_metadata,
        media_body=media).execute()

# TODO: Change code below to process the `response` dict:
print updatedFile.get('id')
