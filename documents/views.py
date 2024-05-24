from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render

from core.utils.Helper import Helper
from .serializers import DocumentSerializer
from .models import Document
from rest_framework import viewsets, status


class DocuemntViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class VehicleManagementView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        users_document = Document.objects.filter(vehicle__owner=pk)
        if not users_document:
            return JsonResponse({'error': 'No document found for the given user'}, status=status.HTTP_404_NOT_FOUND)

        serlizer = DocumentSerializer(users_document, many=True)
        return JsonResponse(serlizer.data, status=status.HTTP_200_OK, safe=False)


class VehicleWithUser(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        user_id = request.user.id

        # Filter documents based on both user_id and vehicle_id
        user_documents = Document.objects.filter(
            vehicle__owner=user_id, vehicle_id=pk)
        if not user_documents:
            return JsonResponse({'error': 'No document found for the given user and vehicle'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentSerializer(user_documents, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class UpdateInsurance(viewsets.ViewSet):
    # This needs some workthrough
    def update(self, request, pk=None):
        user_id = request.user.id
        chassis_number = request.query_params.get('chassis_number')
        insurance_name = request.query_params.get('insurance_name')

        try:
            document = Document.objects.get(
                vehicle__owner=user_id, vehicle_id=pk)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'No document found for the given user and vehicle'}, status=status.HTTP_404_NOT_FOUND)

        insurnance_check = Helper().get_third_party_data(
            f'https://g-notify-third-parties-ceb6d907d4de.herokuapp.com/insurance/check?chassis_number={chassis_number}&insurance_name={insurance_name}')
        if insurnance_check.status_code == 200:
            pass
