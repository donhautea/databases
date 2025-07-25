# drive_utils.py

import os
import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

@st.cache_resource(show_spinner=False)
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_drive"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

def upload_db_to_drive(local_file_path, drive_folder_id):
    service = get_drive_service()
    file_metadata = {
        "name": os.path.basename(local_file_path),
        "parents": [drive_folder_id]
    }
    media = MediaFileUpload(local_file_path, mimetype="application/x-sqlite3", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def download_db_from_drive(file_id, destination_path):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
 
