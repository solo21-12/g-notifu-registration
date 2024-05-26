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


class VehicleManagementViewUser(viewsets.ViewSet):
    '''This is the route to return the list of documents with the given user '''
    def retrieve(self, request, pk=None):
        users_document = Document.objects.filter(vehicle__owner=pk)
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
