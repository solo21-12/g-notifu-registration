from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from vehicle.models import Vehicel
from documents.models import Document
from files.models import Files

User = get_user_model()


class OwnerCheck:
    @staticmethod
    def check_owner(user_id, chassis_number) -> tuple:
        '''This method checks if the user owns the vehicle
        Args:
            user_id (int): The id of the user.
            chassis_number (str): The chassis number of the vehicle.
        returns:
            tuple: A tuple containing the response (if error) and the user and vehicle objects.
        '''

        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"Message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST), None, None

        try:
            current_vehicle = Vehicel.objects.get(
                chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return Response({"Message": "Vehicle does not exist"}, status=status.HTTP_400_BAD_REQUEST), None, None

        if current_vehicle.owner != current_user:
            return Response({"Message": "The current user doesn't own the vehicle"}, status=status.HTTP_400_BAD_REQUEST), None, None

        return None, current_user, current_vehicle

    @staticmethod
    def get_document(current_vehicle: Vehicel, doc_type: str) -> tuple:
        '''
        This method gets the document of the current vehicle.
        Args:
            current_vehicle (Vehicel): The current vehicle.
            doc_type (str): The type of the document.
        returns:
            tuple: A tuple containing the response (if error) and the document object.
        '''
        try:
            cur_doc = Document.objects.get(
                vehicle=current_vehicle, renewal_status=True, document_type=doc_type)
        except Document.DoesNotExist:
            return Response({"Message": "Current vehicle doesn't have an active document"}, status=status.HTTP_400_BAD_REQUEST), None

        return None, cur_doc

    @staticmethod
    def get_file(cur_doc: Document) -> tuple:
        '''
        This method gets the file of the current document.
        Args:
            cur_doc (Document): The current document.
        returns:
            tuple: A tuple containing the response (if error) and the file object.
        '''
        try:
            cur_file = cur_doc.files.get(current=True)
        except Files.DoesNotExist:
            return Response({"Message": "Current document doesn't have a file"}, status=status.HTTP_400_BAD_REQUEST), None

        return None, cur_file
    

