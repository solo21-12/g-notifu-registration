from django.shortcuts import render
from .serializers import DocumentSerializer
from .models import Document
from rest_framework import viewsets

class DocuemntViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
