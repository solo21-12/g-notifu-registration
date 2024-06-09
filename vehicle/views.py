import requests
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.routers import Response
from core.utils.Helper import Helper
from documents.models import Document
from .serializers import VehicleSerializer, AddVehicleSerlizer
from .models import Vehicel
from core.utils.document_type import DocumentType

import logging


logger = logging.getLogger(__name__)
User = get_user_model()
Doc = DocumentType()


class AddVehicleViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = Vehicel.objects.all()
    serializer_class = AddVehicleSerlizer

    def create(self, request):
        url = 'http://localhost:8001'
        serlizer = AddVehicleSerlizer(data=request.data)
        serlizer.is_valid(raise_exception=True)
        chassis_number = serlizer.validated_data['chassis_number']
        plate_number = serlizer.validated_data['plate_number']

        insurance_name = serlizer.validated_data['insurance_company_name']
        url_road_auth = f'{url}/roadauthrity/{chassis_number}'
        url_road_fund = f'{url}/roadfund/{chassis_number}'
        url_insurance = f'{url}/insurance/{chassis_number}'

        road_auth_data = Helper.make_api_call(url_road_auth)
        road_fund_data = Helper.make_api_call(url_road_fund)
        insurance_data = Helper.make_api_call(url_insurance)

        if road_auth_data and road_auth_data.status_code == 200 and insurance_data and insurance_data.status_code == 200:
            if road_fund_data and road_fund_data.status_code == 200:
                if insurance_data and insurance_data.json().get('insurance_name') != insurance_name:
                    return JsonResponse({'status': 'failed', 'message': 'Invalid insurance company'}, status=status.HTTP_400_BAD_REQUEST)
                elif road_auth_data.json().get('plate_number') != plate_number:
                    return JsonResponse({"status": "error", "message": "plate number didn't match"}, status=status.HTTP_400_BAD_REQUEST)

                road_fund = road_fund_data.json()
                road_auth = road_auth_data.json()
                insurance = insurance_data.json()

                user_id = request.user.id
                owner = User.objects.get(id=user_id)
                owner_email_road_fund = road_fund.get(
                    'owner').get('contact').get('email')
                owner_email_road_auth = road_auth.get(
                    'owner').get('contact').get('email')
                owner_email_insurance = insurance.get(
                    'owner').get('contact').get('email')

                renewal_date_road_fund = road_fund.get('renewal_date')
                expiry_date_road_fund = road_fund.get('expiry_date')

                renewal_date_road_auth = road_auth.get('renewal_date')
                expiry_date_road_auth = road_auth.get('expiry_date')

                renewal_date_insurance = insurance.get('renewal_date')
                expiry_date_insurance = insurance.get('expiry_date')
                if owner and owner.get_username() == owner_email_road_fund and owner_email_road_auth == owner_email_road_fund and owner.get_username() == owner_email_insurance:
                    try:
                        vehicle = Vehicel.objects.get(
                            chassis_number=chassis_number)

                        return JsonResponse({'status': 'failed', 'message': 'Vehicle already exists'}, status=status.HTTP_400_BAD_REQUEST)

                    except Vehicel.DoesNotExist:

                        vehicle = Vehicel.objects.create(
                            owner=owner,
                            chassis_number=chassis_number,
                            plate_number=plate_number)

                        create_road_fund = Helper.create_document(
                            vehicle,
                            Doc.ROAD_FUND,
                            renewal_date_road_fund,
                            expiry_date_road_fund,
                            owner.get_username()

                        )

                        create_road_auth = Helper.create_document(
                            vehicle,
                            Doc.ROAD_AUTHORITY,
                            renewal_date_road_fund,
                            expiry_date_road_fund,
                            owner.get_username()

                        )

                        create_insurance = Helper.create_document(
                            vehicle,
                            Doc.THIRD_PARTY_INSURANCE,
                            renewal_date_road_fund,
                            expiry_date_road_fund,
                            owner.get_username(),
                            insurance_name,
                        )

                        if not create_road_auth or not create_road_fund or not create_insurance:
                            return JsonResponse({'status': 'failed', 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return JsonResponse({'status': 'failed', 'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Invalid chassis number'}, status=status.HTTP_400_BAD_REQUEST)
        elif road_auth_data and road_auth_data.status_code == 500:
            return JsonResponse({"status": "error", "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid chassis number'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):

        try:
            vehicle = Vehicel.objects.get(id=id)
        except Vehicel.DoesNotExist:
            return JsonResponse({'message': "No vehicel found with the given information"}, status=status.HTTP_404_NOT_FOUND)

        vehicle.delete()

        return JsonResponse({'message': "sucess"}, status=status.HTTP_204_NO_CONTENT)


class ManageVehicleViewSet(mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):

    queryset = Vehicel.objects.all()
    serializer_class = VehicleSerializer


class VehicleListView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Vehicel.objects.all()
    serializer_class = AddVehicleSerlizer

    def retrieve(self, request, pk=None):
        try:
            cur_user = request.user
        except User.DoesNotExist:
            return Response({'message': "No user found with the given information"}, status=status.HTTP_404_NOT_FOUND)

        vehicles = Vehicel.objects.filter(owner=cur_user)
        if not vehicles.exists():
            return Response({'message': "No vehicles found with the given information"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
