from collections import defaultdict
from vehicle.models import Vehicel  # Correct the typo
from documents.models import Document
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response  # Correct the import
# Ensure the correct path and spelling
from .serializers import GuestSerializer


class Guest(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        unique_id = kwargs.get('pk')

        # Use first() to get the object directly
        cur_vehicle = Vehicel.objects.filter(unique_id=unique_id).first()

        if not cur_vehicle:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

        all_docs = Document.objects.filter(
            vehicle=cur_vehicle).order_by('expiry_date')

        if not all_docs.exists():
            return Response({"error": "No documents found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a dictionary to store the earliest document of each type
        docs_by_type = defaultdict(list)
        for doc in all_docs:
            doc_type = doc.document_type
            if doc_type not in docs_by_type:
                docs_by_type[doc_type] = doc

        # Convert the dictionary values to a list
        prioritized_docs = list(docs_by_type.values())

        serializer = GuestSerializer(prioritized_docs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
