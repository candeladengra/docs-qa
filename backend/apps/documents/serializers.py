from rest_framework import serializers
from .models import Document, Chunk


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'file',
            'status',
            'error_message',
            'page_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'error_message',
            'page_count',
            'created_at',
            'updated_at'
        ]


class ChunkSerializer(serializers.ModelSerializer):
    """Serializer for Chunk model."""
    document_title = serializers.CharField(source='document.title', read_only=True)
    
    class Meta:
        model = Chunk
        fields = [
            'id',
            'document',
            'document_title',
            'content',
            'page_number',
            'chunk_index',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QueryRequestSerializer(serializers.Serializer):
    """Serializer for query requests."""
    question = serializers.CharField(required=True, min_length=1, max_length=1000)


class SourceSerializer(serializers.Serializer):
    """Serializer for source chunks in query responses."""
    content = serializers.CharField()
    document_name = serializers.CharField()
    page_number = serializers.IntegerField()
    document_id = serializers.IntegerField()


class QueryResponseSerializer(serializers.Serializer):
    """Serializer for query responses."""
    answer = serializers.CharField()
    sources = SourceSerializer(many=True)
