from django.test import TestCase

import os
import shutil

from django.core.management import call_command
from django.test import TestCase
from flow_files.models import D0010File, FlowMeterReading


# Create your tests here.

class MeterReadingsTest(TestCase):
    def test_import_meter_readings(self):
        shutil.copy('./meter_readings/D0010_test_files/DTC5259515123502080915D0010_test.uff',
        './meter_readings/D0010_files/DTC5259515123502080915D0010_test.uff')
        call_command('import_meter_readings', 'DTC5259515123502080915D0010_test.uff')
        imported_file = D0010File.objects.get(pk='DTC5259515123502080915D0010_test.uff')
        self.assertEqual(imported_file.file_name, 'DTC5259515123502080915D0010_test.uff')

        import_readings_count = FlowMeterReading.objects.count()
        self.assertEqual(import_readings_count, 12)


    def tearDown(self):
        D0010File.objects.filter(pk='DTC5259515123502080915D0010_test.uff').delete()
        FlowMeterReading.objects.filter(file_name='DTC5259515123502080915D0010_test.uff').delete()
        os.remove('./meter_readings/D0010_files_imported/DTC5259515123502080915D0010_test.uff')



