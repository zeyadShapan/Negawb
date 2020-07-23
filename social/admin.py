from django.contrib import admin
from .models import ChatBox, ChatRequest


@admin.register(ChatRequest)
class ChatRequestAdmin(admin.ModelAdmin):
    """ Admin View for ChatRequest"""
    readonly_fields = ('sent_date',)


@admin.register(ChatBox)
class ChatBoxAdmin(admin.ModelAdmin):
    '''Admin View for ChatBox'''
    readonly_fields = ('created_date',)
