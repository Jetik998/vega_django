from django.contrib import admin
from .models import Repair, StatusHistory

class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ('changed_at', 'status', 'completed_works')
    can_delete = False

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_phone', 'device_model', 'status', 'cost', 'accepted_at')
    list_filter = ('status', 'accepted_at')
    search_fields = ('id', 'client_name', 'client_phone', 'device_model')
    inlines = [StatusHistoryInline]

@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('repair', 'status', 'changed_at', 'completed_works')
    list_filter = ('status', 'changed_at')
