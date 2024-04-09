from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import IndividualOwner, CompanyOwner
from .serializers import (CompanyOwnerCreateSeralizer,
                          CompanyOwnerUpdateSeralizer,
                          IndividualOwnerCreaterSerializer,
                          IndividualOwnerUpdateSerializer,
                          UserEmailVerificationSerializer,
                          UserPasswordResetRequestSerializer,
                          UserPasswordResetUpdateSerlizer,
                          UserPasswordSetUpSerlizer
                          )
from rest_framework.views import APIView
from rest_framework.response import Response


class IndvidualOwnerCreateView(mixins.CreateModelMixin,  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = IndividualOwner.objects.all()
    serializer_class = IndividualOwnerCreaterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class IndvidualOwnerUpdateDeleteView(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = IndividualOwner.objects.all()
    serializer_class = IndividualOwnerUpdateSerializer
    lookup_field='username'



class CompanyOwnerCreateView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CompanyOwner.objects.all()
    serializer_class = CompanyOwnerCreateSeralizer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class CompanyOwnerUpdateDeleteView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CompanyOwner.objects.all()
    serializer_class = CompanyOwnerUpdateSeralizer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class UserEmailVerificationView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [AllowAny()]
        return [IsAuthenticated()]

    def put(self, request):
        serializer = UserEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=serializer.instance,
                              validated_data=request.data)
            return Response('Email verified successfully', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetRequestView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [AllowAny()]
        return [IsAuthenticated()]

    def put(self, request):
        serlizer = UserPasswordResetRequestSerializer(data=request.data)

        serlizer.update(
            validated_data=request.data)
        return Response("Password request sent successfully", status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [AllowAny()]

        return [IsAuthenticated]

    def put(self, request):
        serlizer = UserPasswordResetUpdateSerlizer(data=request.data)
        # if serlizer.is_valid():
        serlizer.update(instance=serlizer.instance,
                        validated_data=request.data)

        return Response('Password succesfully changed', status=status.HTTP_204_NO_CONTENT)

        # return Response(serlizer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordSetView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [AllowAny()]

        return [IsAuthenticated]

    def put(self, request):
        serlizer = UserPasswordSetUpSerlizer(data=request.data)
        serlizer.update(serlizer.instance, request.data)

        return Response('Password succesfully changed', status=status.HTTP_204_NO_CONTENT)
