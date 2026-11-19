from django.contrib import admin
from .models import Document, Chunk


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "page_count", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ["document", "page_number", "chunk_index", "created_at"]
    list_filter = ["document", "page_number"]
    search_fields = ["content", "document__title"]
    readonly_fields = ["created_at"]
