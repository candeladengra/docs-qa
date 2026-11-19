from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction

from .models import Document
from .serializers import (
    DocumentSerializer,
    QueryRequestSerializer,
    QueryResponseSerializer,
)
from .tasks import enqueue_document_processing
from .services import QueryService


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document CRUD operations."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        """
        Upload and process a new document.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            document = serializer.save()
            enqueue_document_processing(document.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def query(self, request):
        """
        Query documents with a natural language question.

        POST /api/documents/query/
        {
            "question": "What is the main topic?"
        }
        """
        request_serializer = QueryRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        question = request_serializer.validated_data["question"]

        try:
            query_service = QueryService()
            result = query_service.query(question)

            response_serializer = QueryResponseSerializer(result)
            return Response(response_serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
