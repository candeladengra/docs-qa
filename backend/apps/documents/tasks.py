import django_rq
from .services import PDFProcessingService


def process_document_task(document_id: int):
    """
    Background task to process a document.

    This is queued by django-rq and executed by a worker.
    """
    service = PDFProcessingService()
    service.process_document(document_id)


def enqueue_document_processing(document_id: int):
    """Enqueue a document for processing."""
    queue = django_rq.get_queue("default")
    queue.enqueue(process_document_task, document_id)
