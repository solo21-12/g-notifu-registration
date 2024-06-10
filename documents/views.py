from rest_framework import status
from rest_framework import viewsets, status
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.routers import Response
from .serializers import DocumentSerializer, DocumentRenewalInitalizer
from .models import Document
from .serializers import DocumentSerializer
from core.utils.Helper import Helper
from core.utils.document_type import DocumentType
from files.utils.create_file import ManageFile
from .utils.check_owner import OwnerCheck
import logging

User = get_user_model()
Doc = DocumentType()
logger = logging.getLogger(__name__)


class DocuemntViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class VehicleManagementViewUser(viewsets.ViewSet):
    '''This is the route to return the list of documents with the given user '''

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        users_document = Document.objects.filter(vehicle__owner=user.id)
        if not users_document:
            return JsonResponse({'error': 'No document found for the given user'}, status=status.HTTP_404_NOT_FOUND)

        serlizer = DocumentSerializer(users_document, many=True)
        return JsonResponse(serlizer.data, status=status.HTTP_200_OK, safe=False)


class VehicleWithUser(viewsets.ViewSet):
    '''This is the route to return the list of documents given a user and a vehicle '''

    def retrieve(self, request, pk=None):
        user_id = request.user.id

        # Filter documents based on both user_id and vehicle_id
        user_documents = Document.objects.filter(
            vehicle__owner=user_id, vehicle_id=pk)
        if not user_documents:
            return JsonResponse({'error': 'No document found for the given user and vehicle'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentSerializer(user_documents, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class RoadFundDocumentRenew(viewsets.ViewSet):

    '''This is the route handelr for renewing road fund document'''
    serializer_class = DocumentRenewalInitalizer

    def retrieve(self, request, pk=None):
        user_id = request.user.id
        chassis_number = pk

        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        url = 'http://localhost:8001'

        result = Helper.make_api_call(
            f'{url}/roadfund/get_payment_info/{chassis_number}/')

        if result.status_code == 200:
            return Response(result.json())

        return Response({"Message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update the document for a vehicle owned by the current user.

        Args:
            request (Request): The HTTP request object containing data and user information.
            pk (str): The primary key (chassis number) of the vehicle.

        Returns:
            Response: A Response object with the result of the update operation.
        """
        chassis_number = pk
        transaction_code = request.data.get("transaction_code")
        user_id = request.user.id

        # Check if the user owns the vehicle
        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        # Get the current active document
        error_response_getting_doc, cur_doc = OwnerCheck.get_document(
            current_vehicle, Doc.ROAD_FUND)
        if error_response_getting_doc:
            return error_response_getting_doc

        # Outdate the current active document
        outdated_success = Helper.outdate_document(id=cur_doc.id)
        if not outdated_success:
            return Response({"Message": "Error occurred while outdating the document"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current file
        error_response_getting_file, cur_file = OwnerCheck.get_file(cur_doc)
        if error_response_getting_file:
            return error_response_getting_file

        # Outdate the current file
        outdate_file = ManageFile.out_date_file(cur_file.id)
        if not outdate_file:
            return Response({"Message": "Error occurred while outdating the file"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the vehicle road fund document and create a new document
        updated_doc = Helper.update_document(
            current_vehicle, Doc.ROAD_FUND, transaction_code, current_user.get_username())
        if not updated_doc:
            return Response({"Message": "Error occurred while updating the document"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the updated document
        serializer = DocumentSerializer(updated_doc)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InsuranceDocumentRenew(viewsets.ViewSet):
    '''This is a route to handle the renewal of third party insurance document'''

    def retrieve(self, request, pk=None):
        user_id = request.user.id
        chassis_number = pk

        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        url = 'http://localhost:8001'

        result = Helper.make_api_call(
            f'{url}/insurance/get_payment_info/{chassis_number}/')

        if result.status_code == 200:
            return Response(result.json())

        return Response({"Message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update the document for a vehicle owned by the current user.

        Args:
            request (Request): The HTTP request object containing data and user information.
            pk (str): The primary key (chassis number) of the vehicle.

        Returns:
            Response: A Response object with the result of the update operation.
        """
        chassis_number = pk
        transaction_code = request.data.get("transaction_code")
        user_id = request.user.id

        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        error_response_getting_doc, cur_doc = OwnerCheck.get_document(
            current_vehicle, Doc.THIRD_PARTY_INSURANCE)

        if error_response_getting_doc:
            return error_response_getting_doc

        # Outdate the current active document
        outdated_success = Helper.outdate_document(cur_doc.id)

        if not outdated_success:
            return Response({"Message": "Error occured"}, status=status.HTTP_400_BAD_REQUEST)

        error_response_getting_file, cur_file = OwnerCheck.get_file(cur_doc)

        if error_response_getting_file:
            return error_response_getting_file

        # Outdate the current file
        outdate_file = ManageFile.out_date_file(cur_file.id)
        if not outdate_file:
            return Response({"Message": "Error occurred while outdating the file"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the vehicle road fund document and create a new document
        updated_doc = Helper.update_document(
            current_vehicle, Doc.THIRD_PARTY_INSURANCE, transaction_code, current_user.get_username(), insurance_company_name=cur_doc.insurance_company_name)

        if not updated_doc:
            return Response({"Message": "Error occured"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DocumentSerializer(updated_doc)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoadAuthorityDocumentRenew(viewsets.ViewSet):
    '''This is a route to handle the renewal of third party insurance document'''

    def retrieve(self, request, pk=None):

        user_id = request.user.id
        chassis_number = pk

        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        url = 'http://localhost:8001'

        result = Helper.make_api_call(
            f'{url}/roadauthrity/get_payment_info/{chassis_number}/')

        if result.status_code == 200:
            return Response(result.json())

        return Response({"Message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update the document for a vehicle owned by the current user.

        Args:
            request (Request): The HTTP request object containing data and user information.
            pk (str): The primary key (chassis number) of the vehicle.

        Returns:
            Response: A Response object with the result of the update operation.
        """
        chassis_number = pk
        transaction_code = request.data.get("transaction_code")
        user_id = request.user.id

        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response

        url = 'http://localhost:8001'

        result = Helper.make_api_call(
            f'{url}/roadauthrity/get_payment_info/{chassis_number}/')

        if result.status_code == 400:
            return Response({"Message": "Please update the bolo document before updating this!"}, status=status.HTTP_400_BAD_REQUEST)

        error_response_getting_doc, cur_doc = OwnerCheck.get_document(
            current_vehicle, Doc.ROAD_AUTHORITY)

        if error_response_getting_doc:
            return error_response_getting_doc

        # Outdate the current active document
        outdated_success = Helper.outdate_document(cur_doc.id)

        if not outdated_success:
            return Response({"Message": "Error occured"}, status=status.HTTP_400_BAD_REQUEST)

        error_response_getting_file, cur_file = OwnerCheck.get_file(cur_doc)

        if error_response_getting_file:
            return error_response_getting_file

        # Update the vehicle road fund document and create a new document
        updated_doc = Helper.update_document(
            current_vehicle, Doc.ROAD_AUTHORITY, transaction_code, current_user.get_username())

        if not updated_doc:
            return Response({"Message": "Error occured"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DocumentSerializer(updated_doc)
        return Response(serializer.data, status=status.HTTP_200_OK)
