import os
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.conf import settings

RCLONE_USER = settings.RCLONE_USER
RCLONE_PASS = settings.RCLONE_PASS
RCLONE_ADDR = settings.RCLONE_ADDR


class RcloneUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        remote_path = request.data.get('remote_path', 'remote:path')
        remote_filename = request.data.get('remote_filename', file.name)

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file temporarily
        temp_file_path = f"/tmp/{file.name}"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Rclone API endpoint URL
        url = f"http://{RCLONE_ADDR}/operations/uploadfile"

        try:
            # Prepare the file for upload
            with open(temp_file_path, 'rb') as f:
                # Define parameters for the API call
                params = {
                    'fs': remote_path,
                    'remote': remote_filename
                }

                # Make the API call to Rclone
                response = requests.post(url, params=params, files={'file': f},
                                         auth=HTTPBasicAuth(RCLONE_USER, RCLONE_PASS))

            if response.status_code == 200:
                return Response({"message": "File upload successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Failed to upload file: {response.status_code}, {response.text}"},
                                status=response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


class ListRemoteView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        fs = request.query_params.get('fs')
        remote = request.query_params.get('remote')
        opt = request.query_params.get('opt', {})
        recurse = request.query_params.get('recurse', 'false') == 'true'
        no_mod_time = request.query_params.get('noModTime', 'false') == 'true'
        show_encrypted = request.query_params.get('showEncrypted', 'false') == 'true'
        show_orig_ids = request.query_params.get('showOrigIDs', 'false') == 'true'
        show_hash = request.query_params.get('showHash', 'false') == 'true'
        no_mime_type = request.query_params.get('noMimeType', 'false') == 'true'
        dirs_only = request.query_params.get('dirsOnly', 'false') == 'true'
        files_only = request.query_params.get('filesOnly', 'false') == 'true'
        metadata = request.query_params.get('metadata', 'false') == 'true'
        hash_types = request.query_params.getlist('hashTypes')

        # Build the query parameters
        params = {
            'fs': fs,
            'remote': remote,
            'opt': opt,
            'recurse': recurse,
            'noModTime': no_mod_time,
            'showEncrypted': show_encrypted,
            'showOrigIDs': show_orig_ids,
            'showHash': show_hash,
            'noMimeType': no_mime_type,
            'dirsOnly': dirs_only,
            'filesOnly': files_only,
            'metadata': metadata,
            'hashTypes': ','.join(hash_types) if hash_types else ''
        }

        # Remove empty parameters
        params = {key: value for key, value in params.items() if value not in [None, '', {}, 'false']}

        # Rclone API endpoint URL
        url = f"http://{RCLONE_ADDR}/operations/list"

        try:
            # Make the API call to Rclone
            response = requests.get(url, params=params, auth=HTTPBasicAuth(RCLONE_USER, RCLONE_PASS))

            # Return response as JSON
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Failed to list remote contents: {response.status_code}, {response.text}"}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)