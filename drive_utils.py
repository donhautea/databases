# drive_utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import streamlit as st
import io
import os

@st.cache_resource
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_drive"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

def download_db_from_drive(file_id, destination_path):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

def upload_db_to_drive(file_path, folder_id):
    service = get_drive_service()
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, mimetype="application/octet-stream", resumable=True)

    # Check if file already exists
    query = f"'{folder_id}' in parents and name = '{os.path.basename(file_path)}' and trashed = false"
    existing = service.files().list(q=query, fields="files(id)").execute()

    if existing["files"]:
        file_id = existing["files"][0]["id"]
        file = service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return file["id"]
