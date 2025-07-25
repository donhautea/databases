from drive_utils import download_db_from_drive, upload_db_to_drive

DB_FILE_NAME = "ohlc_bbdata.db"
DRIVE_FILE_ID = "1FWoXxyUSgnOZkC7Gxt_Vjpco0G2L1VJo"  # Replace with your actual file ID
DRIVE_FOLDER_ID = "1ajjaIMmHobK-kU0NxUfk_cBrhy7ZPGmR"  # Replace with your destination folder ID

# Optional: Download latest copy from Google Drive
if not os.path.exists(DB_FILE_NAME):
    with st.spinner("Downloading latest DB from Google Drive..."):
        download_db_from_drive(DRIVE_FILE_ID, DB_FILE_NAME)
        st.success("Downloaded database from Google Drive.")

# ---- Your Streamlit app logic runs here ----
# You can use DB_FILE_NAME as `db_path` in your app

# Optional: Upload back to Drive after changes
if st.button("📤 Upload Updated DB to Google Drive"):
    with st.spinner("Uploading to Google Drive..."):
        uploaded_id = upload_db_to_drive(DB_FILE_NAME, DRIVE_FOLDER_ID)
        st.success(f"Uploaded. File ID: {uploaded_id}")
