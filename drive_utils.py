from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import streamlit as st

@st.cache_resource
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_drive"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

def upload_db_to_drive(db_path, folder_id):
    service = get_drive_service()

    file_metadata = {
        "name": os.path.basename(db_path),
        "parents": [folder_id]
    }

    media = MediaFileUpload(db_path, mimetype="application/octet-stream", resumable=True)

    # Check if file already exists (replace instead of duplicate)
    query = f"'{folder_id}' in parents and name = '{os.path.basename(db_path)}' and trashed = false"
    existing_files = service.files().list(q=query, spaces="drive", fields="files(id)").execute()

    if existing_files["files"]:
        file_id = existing_files["files"][0]["id"]
        file = service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return file["id"]
