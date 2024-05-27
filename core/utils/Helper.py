import requests
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status
from rest_framework.routers import Response
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from documents.models import Document
from vehicle.models import Vehicel


class Helper:
    def make_api_call(self, url: str) -> Response:
        '''This methods make a request to an external site and fetch the required data'''
        try:
            response = requests.get(url, verify=False)
            return response
        except Exception as e:
            return Response({'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_document(self, **kwargs):
        '''This method genenerate the required type of document'''
        vehicle = kwargs.get('vehicle')
        document_type = kwargs.get('document_type')
        renewal_date = kwargs.get('renewal_date')
        expiry_date = kwargs.get('expiry_date')
        insurance_company_name = kwargs.get('insurance_company_name') or ""
        renewal_status = True
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

        if expiry_date < datetime.now():
            renewal_status = False
        try:
            created_doc = Document.objects.create(
                renewal_date=renewal_date,
                expiry_date=expiry_date,
                renewal_status=renewal_status,
                vehicle=vehicle,
                document_type=document_type,
                insurance_company_name=insurance_company_name
            )

            return created_doc
        except Exception as e:
            return None

    def update_document(self, vehicle: Vehicel, document_type: str, transaction_code: str, insurance_company_name=None):
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

        try:
            cur_document = Document.objects.create(
                renewal_date=renewal_date,
                renewal_status=renewal_status,
                vehicle=vehicle,
                document_type=document_type,
                renewed_tansaction_code=transaction_code,
                insurance_company_name=insurance_company_name
            )

            return cur_document
        except Exception as e:
            return None

    def outdate_document(self, id):
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
            return None
