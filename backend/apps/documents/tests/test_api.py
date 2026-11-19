import json
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from apps.documents.models import Document, Chunk
from unittest.mock import patch


class TestDocumentAPI(TestCase):
    """Test document API endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_list_documents_empty(self):
        response = self.client.get("/api/documents/")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 0

    def test_list_documents_with_data(self):
        Document.objects.create(title="Test Document", file="test.pdf", status="ready")

        response = self.client.get("/api/documents/")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Test Document"
        assert data["results"][0]["status"] == "ready"

    @patch("apps.documents.views.enqueue_document_processing")
    def test_upload_document(self, mock_enqueue):
        pdf_content = b"%PDF-1.4 fake pdf content"
        pdf_file = SimpleUploadedFile(
            "test.pdf", pdf_content, content_type="application/pdf"
        )

        response = self.client.post(
            "/api/documents/",
            {"title": "Test Upload", "file": pdf_file},
            format="multipart",
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Upload"
        assert data["status"] == "processing"
        assert mock_enqueue.called

        assert Document.objects.count() == 1

    def test_delete_document(self):
        doc = Document.objects.create(
            title="Test Document", file="test.pdf", status="ready"
        )

        response = self.client.delete(f"/api/documents/{doc.id}/")
        assert response.status_code == 204
        assert Document.objects.count() == 0

    @patch("apps.documents.views.QueryService.query")
    def test_query_endpoint(self, mock_query):
        mock_query.return_value = {"answer": "Test answer", "sources": []}

        response = self.client.post(
            "/api/documents/query/",
            json.dumps({"question": "What is this?"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Test answer"
        assert "sources" in data

    def test_query_endpoint_missing_question(self):
        response = self.client.post(
            "/api/documents/query/",
            json.dumps({}),
            content_type="application/json",
        )

        assert response.status_code == 400


class TestDocumentModel(TestCase):
    """Test Document model."""

    def test_create_document(self):
        doc = Document.objects.create(
            title="Test", file="test.pdf", status="processing"
        )

        assert doc.id is not None
        assert doc.title == "Test"
        assert doc.status == "processing"
        assert doc.page_count is None

    def test_document_ordering(self):
        doc1 = Document.objects.create(title="First", file="1.pdf")
        doc2 = Document.objects.create(title="Second", file="2.pdf")

        docs = list(Document.objects.all())
        assert docs[0].id == doc2.id
        assert docs[1].id == doc1.id


class TestChunkModel(TestCase):
    """Test Chunk model."""

    def test_create_chunk(self):
        doc = Document.objects.create(title="Test", file="test.pdf")

        chunk = Chunk.objects.create(
            document=doc,
            content="Test content",
            page_number=1,
            chunk_index=0,
            embedding=[0.1] * 768,
        )

        assert chunk.id is not None
        assert chunk.document == doc
        assert chunk.content == "Test content"
        assert len(chunk.embedding) == 768
