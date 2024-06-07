from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from documents.utils.check_owner import OwnerCheck
from django.contrib.auth import get_user_model
from core.utils.document_type import DocumentType
from django.http import FileResponse
from files.utils.generate_pdf import GeneratePdf
import os


User = get_user_model()


class FilesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        chassis_number = pk
        user_id = request.user.id
        doc_type = request.query_params.get('doc_type')
        error_response, current_user, current_vehicle = OwnerCheck.check_owner(
            user_id, chassis_number)

        if error_response:
            return error_response
        
       

        error_response, cur_doc = OwnerCheck.get_document(
            current_vehicle, DocumentType.ROAD_FUND)

        if error_response:
            return error_response

        error_response, cur_file = OwnerCheck.get_file(cur_doc)

        if error_response:
            return error_response

        # Generate PDF
        renewal_date = cur_file.renewal_date
        expire_date = cur_file.expire_date
        document_id = cur_doc.id
        pdf_path = GeneratePdf.generate_road_fund_file(
            renewal_date, expire_date, chassis_number, document_id)

        if not pdf_path:
            return Response({'detail': 'Failed to generate PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return PDF as response
        response = FileResponse(
            open(pdf_path, 'rb'), as_attachment=True, filename=os.path.basename(pdf_path))
        return response
