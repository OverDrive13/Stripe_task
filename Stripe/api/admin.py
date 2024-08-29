from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Кастомизация админ панели."""
    list_display = ('name', 'price', 'currency')
    search_fields = ('name', 'description')
    list_filter = ('currency',)
