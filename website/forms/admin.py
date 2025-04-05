from django.contrib import admin
from .models import ContactForm

# Register your models here.

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('proposed_title', 'request_type', 'requested_by', 'created_at')
    list_filter = ('request_type', 'created_at')
    search_fields = ('proposed_title', 'requested_by__username')
