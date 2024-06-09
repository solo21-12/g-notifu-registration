from typing import Any

import requests
from datetime import datetime
from rest_framework import status
from rest_framework.routers import Response
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from documents.models import Document
from files.utils.generate_pdf import GeneratePdf
from vehicle.models import Vehicel
from files.utils.create_file import ManageFile
import logging

logger = logging.getLogger(__name__)


class Helper:
    @staticmethod
    def make_api_call(url: str) -> Response:
        """These methods make a request to an external site and fetch the required data"""
        try:
            response = requests.get(url, verify=False)
            return response
        except Exception as e:
            return Response({'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_document(vehicle: Vehicel, document_type: str, renewal_date, expiry_date, owner_username: str, insurance_company_name='') -> Any | None:
        """This method generate the required type of document

        Args:
            vehicle (str): The vehicle for which the document is being generated.
            document_type (str): The type of document to generate.
            renewal_date (datetime): The date when the document renewed.
            expiry_date (datetime): The date when the document expires.
            owner_username: The username of the owner of the vehicle.
            insurance_company_name (str): The name of the insurance company.

        Returns:
        Document: The generated document object.
        """

        renewal_status = True
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

        if expiry_date < datetime.now():
            renewal_status = False
        try:
            create_file = ManageFile.create_file(owner_username, document_type)
            if create_file:

                created_doc = Document.objects.create(
                    renewal_date=renewal_date,
                    expiry_date=expiry_date,
                    renewal_status=renewal_status,
                    vehicle=vehicle,
                    document_type=document_type,
                    insurance_company_name=insurance_company_name,
                )

                created_doc.files.add(create_file)
                created_doc.save()

                GeneratePdf.generate_road_fund_file(
                    renewal_date, created_doc.expiry_date, vehicle.chassis_number, created_doc.id, create_file.file_name)

                return created_doc

            return None

        except Exception as e:
            logging.debug(e)
            return None

    @staticmethod
    def update_document(vehicle: Vehicel, document_type: str, transaction_code: str,  owner_username: str, insurance_company_name=None):
        """
            Update the required type of document.

            This method accepts the following arguments:

            Args:
                vehicle (str): The vehicle for which the document is being generated.
                document_type (str): The type of document to generate (e.g., 'registration', 'insurance').
                renewal_date (datetime): The date when the document should be renewed.
                insurance_company_name (str): The name of the insurance company.

            Returns:
                Document: The generated document object.
            """
        renewal_status = True
        renewal_date = timezone.now().date()
        create_file = ManageFile.create_file(owner_username, document_type)

        try:
            cur_document = Document.objects.create(
                renewal_date=renewal_date,
                renewal_status=renewal_status,
                vehicle=vehicle,
                document_type=document_type,
                renewed_tansaction_code=transaction_code,
                insurance_company_name=insurance_company_name
            )

            cur_document.files.add(create_file)
            cur_document.save()

            GeneratePdf.generate_road_fund_file(
                renewal_date, cur_document.expiry_date, vehicle.chassis_number, cur_document.id, create_file.file_name)

            return cur_document
        except Exception as e:
            logging.debug(e)
            return None

    @staticmethod
    def outdate_document(id):
        """
            This is a function to outdate a document when renewing a new document.

            Args:
                id (int): The ID of the document to be outdated.

            Returns:
                tuple: (bool, str) A tuple where the first value indicates success (True/False)
                    and the second value is a message."""
        try:
            cur_document = Document.objects.get(id=id)
            cur_document.renewal_status = False
            cur_document.save()
            return cur_document

        except ObjectDoesNotExist as e:
            logging.debug(e)
            return None
