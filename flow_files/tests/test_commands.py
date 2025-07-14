import os
import shutil
from pathlib import Path

import django
from django.core.management import call_command
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kraken_tech_challenge_derrick_sun.settings")
django.setup()


from flow_files.models import D0010File, FlowMeterReading
from kraken_tech_challenge_derrick_sun import settings

# Set the settings module

files_dir = settings.BASE_DIR / 'flow_files\\tests\\test_files'
used_files_dir = settings.BASE_DIR / 'flow_files\\imported_d0010_files'
file_name = 'DTC5259515123502080915D0010.uff'

class MeterReadingsTest(TestCase):
    def test_import_meter_readings(self):
        call_command('import_meter_readings', files_dir)
        imported_file = D0010File.objects.get(pk=file_name)
        self.assertEqual(imported_file.file_name, file_name)

        import_readings_count = FlowMeterReading.objects.count()
        self.assertEqual(import_readings_count, 13)
        D0010File.objects.filter(file_name=file_name).exists()



    def tearDown(self):
        D0010File.objects.filter(pk=file_name).delete()
        FlowMeterReading.objects.filter(file_name=file_name).delete()
        shutil.move(used_files_dir / file_name, Path(files_dir) / file_name)


