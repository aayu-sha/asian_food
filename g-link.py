from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def download_images_from_drive(folder_link, save_path):
    creds = None

    # The file token.json stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Get the folder ID from the folder link
    folder_id = folder_link.split('/')[-1]

    # List files in the folder
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found.')
    else:
        print('Downloading files...')
        for file in files:
            file_id = file['id']
            file_name = file['name']
            mime_type = file['mimeType']

            # Download images only (you can modify this condition based on your file types)
            if 'image' in mime_type:
                request = service.files().get_media(fileId=file_id)
                fh = open(os.path.join(save_path, file_name), 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f'Downloaded {status.progress() * 100:.2f}% of {file_name}')

        print('Download complete.')

# Example usage
folder_link = 'https://drive.google.com/drive/folders/1zMJwAYa3vZ4Bl6J77YzJemL7iqwZAAzc?usp=drive_link'
save_path = 'g-output'
download_images_from_drive(folder_link, save_path)
