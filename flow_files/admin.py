from django.contrib import admin

from flow_files.models import FlowMeterReading, FlowMeterReadingFile

@admin.register(FlowMeterReading)
class FlowMeterReadingAdmin(admin.ModelAdmin):
    search_fields = ['mpan_core', 'meter_id']
    list_display = ('mpan_core', 'meter_id', 'file_name')


@admin.register(FlowMeterReadingFile)
class FlowMeterReadingFileAdmin(admin.ModelAdmin):
    search_fields = ['file_name']
    list_display = ['file_name']

