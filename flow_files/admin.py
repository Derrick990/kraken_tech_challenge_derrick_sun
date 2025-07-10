from django.contrib import admin

from flow_files.models import FlowMeterReading, D0010File

@admin.register(FlowMeterReading)
class FlowMeterReadingAdmin(admin.ModelAdmin):
    search_fields = ['mpan_core', 'meter_id']
    list_display = ('mpan_core', 'meter_id', 'file_name')


@admin.register(D0010File)
class FlowMeterReadingFileAdmin(admin.ModelAdmin):
    search_fields = ['file_name']
    list_display = ['file_name']

