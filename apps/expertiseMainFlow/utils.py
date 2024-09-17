import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from rest_framework import serializers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# def get_upload_to(instance, filename):
#     return f"{instance.owner.id}/uploads/{instance.folder.uuid}/{instance.uuid}_{filename.replace(' ', '_')}"


def get_upload_to(instance, filename):
    return f"attachments/{instance.subtask.uuid}/{filename.replace(' ', '_')}"


def validate_response(response, response_serializer):
    if response.status_code == 200:
        # Deserialize the response JSON using the response serializer
        response_data = response.json()
        logger.info(f"returned data: {response_data}")
        response_serializer = response_serializer(data=response_data)

        # Validate the response data
        if response_serializer.is_valid():
            logger.info("Successfully received remote contents")
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(f"Invalid response data: {response_serializer.errors}")
            return Response(
                {"error": "Invalid response data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        logger.error(f"Failed to list remote contents: {response.status_code}, {response.text}")
        return Response(
            {"error": f"Failed to list remote contents: {response.status_code}, {response.text}"},
            status=response.status_code
        )