import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import configparser

def parse_rclone_conf(file_path):
    """
    Parse the rclone.conf file to extract the Google Drive access token.

    Args:
    file_path: The path to the rclone.conf file.

    Returns:
    A dictionary containing access token and other token information.
    """
    config = configparser.ConfigParser()
    config.read(file_path)

    return config['GoogleDrive']


def get_folder_id_from_path(service, folder_path, parent_id='root'):
    """
    Resolve a Google Drive folder path to its corresponding folder ID.

    Args:
    service: Google Drive API service instance.
    folder_path: The full path to the folder.
    parent_id: The parent folder ID (default is 'root' for the root directory).

    Returns:
    The Google Drive folder ID corresponding to the folder_path.
    """
    folder_names = folder_path.split('/')

    # Start from the root or provided parent ID and traverse the folder structure
    for folder_name in folder_names:
        query = f"'{parent_id}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        response = service.files().list(q=query, fields="files(id, name)").execute()
        files = response.get('files', [])

        if not files:
            raise Exception(f"Folder '{folder_name}' not found in path '{folder_path}'")

        # Update parent_id to the found folder ID for the next iteration
        parent_id = files[0]['id']

    return parent_id


def move_folder(src_folder_path, dst_folder_path):
    """
    Move a folder from one directory to another in Google Drive.

    Args:
    src_folder_path: The path of the folder to be moved.
    dst_folder_path: The destination path.
    """
    try:

        # Path to the rclone.conf file
        rclone_conf_path = 'rclone/config/rclone.conf'

        # Parse rclone.conf to get the token
        drive_data = parse_rclone_conf(rclone_conf_path)
        token = json.loads(drive_data['token'])

        print("TOKEN_DATA", drive_data)

        # Use the token to build Google API credentials
        creds = Credentials(
            token['access_token'],
            refresh_token=token['refresh_token'],
            token_uri='https://oauth2.googleapis.com/token',
            client_id=drive_data['client_id'],
            client_secret=drive_data['client_secret'],
            scopes=['https://www.googleapis.com/auth/drive']
        )

        # Build the Drive API service
        service = build('drive', 'v3', credentials=creds)

        # Resolve folder paths to IDs
        src_folder_id = get_folder_id_from_path(service, src_folder_path)
        dst_folder_id = get_folder_id_from_path(service, dst_folder_path)

        # Retrieve the source folder's current parent(s)
        folder = service.files().get(fileId=src_folder_id, fields='parents').execute()
        previous_parents = ",".join(folder.get('parents'))

        # Move the folder by removing it from the old parent and adding it to the new one
        updated_file = service.files().update(
            fileId=src_folder_id,
            addParents=dst_folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

        return f"Folder moved successfully to new parent ID: {updated_file.get('parents')}"
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    move_folder("სამუშაო გარემო/ჯი არ ქი", "საბოლოო დასკვნები")
