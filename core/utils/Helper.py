import requests
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status
from documents.models import Document


class Helper:
    def get_third_party_data(self, url: str):
        '''This methods make a request to an external site and fetch the required data'''
        try:
            response = requests.get(url, verify=False)
            return response
        except Exception as e:
            return JsonResponse({'error': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            Document.objects.create(
                renewal_date=renewal_date,
                expiry_date=expiry_date,
                renewal_status=renewal_status,
                vehicle=vehicle,
                document_type=document_type,
                insurance_company_name=insurance_company_name
            )

            return JsonResponse({'sucess': 'sucess'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
