from django.db import models

class D0010File(models.Model):
    file_name = models.CharField(max_length=100, primary_key=True)
    header = models.CharField(max_length=100)
    footer = models.CharField(max_length=100)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "D0010 Flow Meter Readings File"
        verbose_name_plural = "D00010 Flow Meter Readings Files"
        app_label = "flow_files"


class FlowMeterReading(models.Model):
    mpan_core = models.IntegerField(null=False, blank=False)
    bsc_validation_status = models.CharField(max_length=1, null=False, blank=False)
    meter_id = models.CharField(max_length=10, null=False, blank=False)
    reading_type = models.CharField(max_length=1, default='', null=False, blank=False)
    meter_register_id = models.CharField(max_length=2, null=False, blank=False)
    reading_date_time = models.DateTimeField(null=False, blank=False)
    register_reading = models.DecimalField(max_digits=10, decimal_places=1, null=False, blank=False)
    reset_date_time = models.DateTimeField(null=True, blank=True)
    number_of_md_resets = models.IntegerField(null=True, blank=True)
    meter_reading_flag = models.BooleanField(null=True, blank=True)
    reading_method = models.CharField(max_length=1, null=False, blank=False)
    file_name = models.ForeignKey(
        'D0010File',
        on_delete=models.CASCADE)

    def __str__(self):
        return f"MPAN Core: {self.mpan_core} Meter Id: {self.meter_id} @ {self.reading_date_time.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        # unique_together = ('mpan_core', 'meter_id', 'reading_date_time')
        verbose_name = "Flow Meter Reading"
        verbose_name_plural = "Flow Meter Readings"
        app_label = "flow_files"
