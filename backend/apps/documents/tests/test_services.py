import pytest
from apps.documents.services import PDFProcessingService


class TestPDFProcessingService:
    """Test PDF processing service."""

    def test_chunk_text_small(self):
        service = PDFProcessingService()
        text = "This is a small text."
        chunks = service.chunk_text(text, page_number=1)

        assert len(chunks) == 1
        assert chunks[0]["content"] == text
        assert chunks[0]["page_number"] == 1

    def test_chunk_text_large(self):
        service = PDFProcessingService()
        text = "A " * 1500
        chunks = service.chunk_text(text, page_number=1)

        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk["content"]) <= service.chunk_size + service.chunk_overlap
            assert chunk["page_number"] == 1

    def test_clean_text(self):
        service = PDFProcessingService()

        text = "Hello   world\n\n  with   spaces  "
        cleaned = service._clean_text(text)
        assert cleaned == "Hello world with spaces"

    def test_clean_text_tabs(self):
        service = PDFProcessingService()

        text = "Hello\t\tworld"
        cleaned = service._clean_text(text)
        assert "  " not in cleaned

    def test_find_sentence_boundary(self):
        service = PDFProcessingService()

        text = "First sentence. Second sentence. Third sentence."
        position = 10
        boundary = service._find_sentence_boundary(text, position)

        assert boundary > position
        assert text[boundary - 1] == "."

    def test_chunk_overlap(self):
        service = PDFProcessingService()
        service.chunk_size = 100
        service.chunk_overlap = 20

        text = "A " * 200
        chunks = service.chunk_text(text, page_number=1)

        assert len(chunks) >= 2
