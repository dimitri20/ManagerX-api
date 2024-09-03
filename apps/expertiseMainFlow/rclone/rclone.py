import logging
from typing import TypeVar, Optional, Type

import requests
from requests.auth import HTTPBasicAuth
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from django.conf import settings
from apps.expertiseMainFlow.rclone.endpoints import RcloneOperations
from apps.expertiseMainFlow.utils import validate_response

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Rclone configuration from settings
RCLONE_USER = settings.RCLONE_USER
RCLONE_PASS = settings.RCLONE_PASS
RCLONE_ADDR = settings.RCLONE_ADDR

# Type variable for method chaining in RcloneAbstract
T = TypeVar('T', bound='RcloneAbstract')

class RcloneAbstract:
    """
    Base class for Rclone operations. Provides methods for setting headers, request and response serializers,
    and operation type.
    """

    def __init__(self):
        self._request_serializer: Optional[Type[serializers.Serializer]] = None
        self._response_serializer: Optional[Type[serializers.Serializer]] = None
        self._headers: dict = {}
        self._operation: Optional[RcloneOperations] = None
        self._full_url: str = ""

    def set_headers(self, headers: dict) -> T:
        self._headers = headers
        return self

    def set_request_serializer(self, request_serializer: Type[serializers.Serializer]) -> T:
        self._request_serializer = request_serializer
        return self

    def set_response_serializer(self, response_serializer: Type[serializers.Serializer]) -> T:
        self._response_serializer = response_serializer
        return self

    def set_operation(self, operation: RcloneOperations) -> T:
        self._operation = operation
        return self


class Rclone(RcloneAbstract):
    """
    Class for executing Rclone operations using provided serializers and configurations.
    """

    def execute(self, data: dict) -> Response:
        """
        Executes the Rclone operation based on the set operation type and serializers.

        :param data: Data to be sent in the request.
        :return: Response from the Rclone server.
        """
        if not self._operation:
            logger.error("Operation not set")
            return Response({"error": "Operation not set"}, status=status.HTTP_400_BAD_REQUEST)

        if not self._request_serializer:
            logger.error("Request serializer not set")
            return Response({"error": "Request serializer not set"}, status=status.HTTP_400_BAD_REQUEST)

        self._full_url = f'{RCLONE_ADDR}/{self._operation.value}'
        self._headers = {
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }

        serializer = self._request_serializer(data=data)
        if not serializer.is_valid():
            logger.error(f"Invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        logger.info(f"Sending request to {self._full_url} with data: {validated_data}")

        try:
            response = requests.post(
                self._full_url,
                headers=self._headers,
                json=validated_data,
                auth=HTTPBasicAuth(RCLONE_USER, RCLONE_PASS)
            )

            return self._validate_response(response)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_response(self, response: requests.Response) -> Response:
        """
        Validates the response from the Rclone server using the response serializer.

        :param response: Response from the Rclone server.
        :return: Formatted Response object.
        """
        if not self._response_serializer:
            logger.error("Response serializer not set")
            return Response({"error": "Response serializer not set"}, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"Received data: {response_data}")
            serializer = self._response_serializer(data=response_data)

            if serializer.is_valid():
                logger.info("Successfully received and validated remote contents")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f"Invalid response data: {serializer.errors}")
                return Response({"error": "Invalid response data", "details": serializer.errors},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Failed to retrieve remote contents: {response.status_code}, {response.text}")
            return Response(
                {"error": f"Failed to retrieve remote contents: {response.status_code}, {response.text}"},
                status=response.status_code
            )
