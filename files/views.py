from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from documents.utils.check_owner import OwnerCheck
from django.contrib.auth import get_user_model
from core.utils.document_type import DocumentType
from django.http import FileResponse
import os

User = get_user_model()


class FilesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        chassis_number = pk
        user_id = request.user.id
        doc_type = request.query_params.get('doc_type')

        # Checking ownership
        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)
        if error_response:
            return error_response

        # Retrieving document based on vehicle and document type
        error_response, cur_doc = OwnerCheck.get_document(
            current_vehicle, DocumentType.ROAD_FUND)
        if error_response:
            return error_response

        # Getting the file associated with the document
        error_response, cur_file = OwnerCheck.get_file(cur_doc)
        if error_response:
            return error_response

        if not cur_file:
            return Response({'detail': 'Failed to generate PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Extract the filename from cur_file if it's an object, assuming it has a 'name' attribute
        if hasattr(cur_file, 'name'):
            file_name = cur_file.name
        else:
            file_name = str(cur_file)

        # Constructing file path
        pdf_file_path = os.path.join("pdfs", file_name)

        try:
            # Open the file without closing it manually
            pdf_file = open(pdf_file_path, 'rb')
            response = FileResponse(
                pdf_file, as_attachment=True, filename=os.path.basename(pdf_file_path))
            return response
        except FileNotFoundError:
            return Response({'detail': 'PDF file not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
