from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    """Represents an uploaded PDF document."""
    
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    error_message = models.TextField(blank=True, null=True)
    page_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Chunk(models.Model):
    """Represents a text chunk from a document with its embedding."""
    
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks'
    )
    content = models.TextField()
    page_number = models.IntegerField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=768, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['document', 'chunk_index']
        indexes = [
            models.Index(fields=['document', 'chunk_index']),
        ]
    
    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"
