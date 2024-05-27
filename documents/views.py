from rest_framework import status
from rest_framework import viewsets, status, mixins
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.routers import Response
from .serializers import DocumentSerializer, DocumentRenewalInitalizer
from .models import Document
from core.utils.Helper import Helper
from vehicle.models import Vehicel


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


class RoadFundDocumentRenew(viewsets.ViewSet):

    '''This is the route handelr for renewing road fund document'''
    serializer_class = DocumentRenewalInitalizer

    def retrieve(self, request, pk=None):
        User = get_user_model()
        user_id = request.user.id
        chassis_number = pk

        cur_user = User.objects.get(id=user_id)
        cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)

        if cur_vehicle.owner != cur_user:
            return Response({"Message": "The current users doesn't own the vehicle"})

        url = 'http://localhost:8001'
        helper = Helper()

        result = helper.make_api_call(
            f'{url}/roadfund/get_payment_info/{chassis_number}/')

        if result.status_code == 200:
            return Response(result.json())

        return Response({"Message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        print(request.data)
        return Response({})
