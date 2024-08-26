from allauth.socialaccount.models import SocialAccount, SocialToken
from google.cloud import storage
from google.oauth2 import service_account
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

import os

CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'managerx-test-d56b2dbaa330.json')
DESTINATION_FOLDER = 'backup/'
BUCKET_NAME = 'managerxstoragetest'



def upload_file_to_gcs(source_file_name, destination_blob_name, bucket_name=BUCKET_NAME, credentials_path=CREDENTIALS_PATH):
    # Load credentials from the specified path
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # Initialize a client using the loaded credentials
    storage_client = storage.Client(credentials=credentials)

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def upload_file_to_drive(user, file_path):
    access_token = get_google_access_token(user)

    if not access_token:
        return {'error': 'Google token not available'}

    creds = Credentials(token=access_token)

    try:
        service = build('drive', 'v3', credentials=creds)
        media = MediaFileUpload(file_path, resumable=True)
        file_metadata = {'name': os.path.basename(file_path)}
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return {'message': 'File uploaded successfully', 'file_id': file.get('id')}
    except Exception as e:
        return {'error': str(e)}

def get_google_access_token(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        social_token = SocialToken.objects.get(account=social_account)
        return social_token.token
    except SocialToken.DoesNotExist:
        return None


# Example usage:

# if __name__ == "__main__":
#
#     # Example usage:
#     upload_file_to_gcs('/Users/guluadim/Desktop/managerx-test-d56b2dbaa330.json', 'backup-folder/filename')
