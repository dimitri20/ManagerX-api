import os

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from google.oauth2 import service_account
from googleapiclient.discovery import build

import io
import os

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

User = get_user_model()

def create_folder(folder_name, parent_folder_id=None):
    """Create a folder in Google Drive and return its ID."""
    folder_metadata = {
        'name': folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        'parents': [parent_folder_id] if parent_folder_id else []
    }

    created_folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()

    print(f'Created Folder ID: {created_folder["id"]}')
    return created_folder["id"]

def share_folder(folder_id, user_email, role='writer'):
    """Share a folder with a specified user."""
    permission = {
        'type': 'user',
        'role': role,
        'emailAddress': user_email
    }

    try:
        drive_service.permissions().create(
            fileId=folder_id,
            body=permission,
            fields='id'
        ).execute()
        print(f'Folder {folder_id} shared with {user_email} as {role}.')
    except Exception as e:
        print(f'An error occurred: {e}')

def list_folder(parent_folder_id=None, delete=False):
    """List folders and files in Google Drive."""
    results = drive_service.files().list(
        q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("No folders or files found in Google Drive.")
    else:
        print("Folders and files in Google Drive:")
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
            if delete:
                delete_files(item['id'])


def get_file_by_id(file_id):
    """Retrieve a single file from Google Drive by its ID."""
    try:
        # Get the file metadata and content
        file = drive_service.files().get(fileId=file_id,
                                         fields="id, name, mimeType, webContentLink, webViewLink").execute()

        return file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_folder_by_id(folder_id):
    """Retrieve a single folder from Google Drive by its ID."""
    # Get the folder metadata
    try:

        folder = drive_service.files().get(fileId=folder_id, fields="id, name, mimeType, webViewLink").execute()

        # Check if the retrieved item is a folder
        if folder['mimeType'] != 'application/vnd.google-apps.folder':
            print(f"The item with ID {folder_id} is not a folder.")
            return None

        return folder
    except Exception as e:
        print("Folder doesn't exist.")
        return None


#TODO -
def get_folder_by_name(folder_name, parent_folder_id=None):
    try:
        """Check if a folder exists by name and return its ID."""
        # Start the query with the folder name and mimeType
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"

        # If a parent folder ID is specified, add it to the query
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        # Execute the query and get the results
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        # Retrieve the files list from the results
        files = results.get('files', [])

        # Return the first file if found, otherwise None
        return files[0] if files else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def delete_files(file_or_folder_id):
    """Delete a file or folder in Google Drive by ID."""
    try:
        drive_service.files().delete(fileId=file_or_folder_id).execute()
        print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
    except Exception as e:
        print(f"Error deleting file/folder with ID: {file_or_folder_id}")
        print(f"Error details: {str(e)}")

def download_file(file_id, destination_path):
    """Download a file from Google Drive by its ID."""
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, mode='wb')

    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

def create_shared_folder_for_user(user: User):
    folder_name = user.username
    user_email = user.email

    if not check_if_folder_exists_on_drive(folder_name=folder_name):
        # Create a new folder if it doesn't exist
        folder_id = create_folder(folder_name)

        # Share the folder with the user
        share_folder(folder_id, user_email)

        # Add the folder information to the list
        shared_folder_info = {
            'user': user.id,
            'drive_folder_name': folder_name,
            'drive_folder_id': folder_id
        }
        print(f'Successfully created and shared folder for {user_email}', shared_folder_info)
        return shared_folder_info

    return None

def create_shared_folder_for_each_user():
    email_adresses = EmailAddress.objects.all()
    shared_folders = []

    for email in email_adresses:
        user = User.objects.get(email=email)
        create_shared_folder_for_user(user)
        created_folder = create_shared_folder_for_user(user)
        shared_folders.append(created_folder)

    return shared_folders

def check_if_folder_exists_on_drive(folder_id=None, folder_name=None):

    if folder_id:
        return get_folder_by_id(folder_id)
    elif folder_name:
        return get_folder_by_id(get_folder_by_name(folder_name))

    return False

def upload_file(title, path, folder_id=None):
    """
    Upload a file to Google Drive.

    Args:
        title (str): File title,
        path (str): File path,
        folder_id (str, optional): The ID of the Google Drive folder to upload the file to.
                                   If None, the file will be uploaded to the root.

    Returns:
        str: The ID of the uploaded file in Google Drive.
    """
    try:
        # Define the file metadata
        file_metadata = {
            'name': title,
            'parents': [folder_id] if folder_id else []  # Ensure parents is a list
        }

        # Create a media upload object using the file path
        media = MediaFileUpload(path, resumable=True)

        # Upload the file to Google Drive
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        print(f"File '{title}' uploaded successfully with ID: {uploaded_file['id']}")
        return uploaded_file

    except Exception as e:
        print(f'An error occurred while uploading the file: {e}')
        return None

def delete_all_files_from_drive():
    """Deletes all files from Google Drive using the service account."""

    # Query to retrieve all files
    query = "trashed=false"

    # List all files in the Drive
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        print("No files found.")
        return

    # Iterate over all files and delete them
    for file in files:
        try:
            drive_service.files().delete(fileId=file['id']).execute()
            print(f"Deleted file with ID: {file['id']}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    list_folder()