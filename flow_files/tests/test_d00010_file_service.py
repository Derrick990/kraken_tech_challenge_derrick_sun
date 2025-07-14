import os

import django
from django.test import TestCase
from django.utils import timezone
from datetime import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kraken_tech_challenge_derrick_sun.settings")
django.setup()

from flow_files.models import D0010File
from flow_files.services.d0010_file_service import import_d0010_file, parse_d0010_lines, clean_meter_reading_data
from kraken_tech_challenge_derrick_sun import settings




files_dir = settings.BASE_DIR / 'flow_files\\tests\\test_files\\DTC5259515123502080915D0010.uff'

class FileServiceTest(TestCase):
    def setUp(self):
        self.file_path = files_dir
        self.file_name = 'DTC5259515123502080915D0010.uff'
        self.lines = import_d0010_file(self.file_path)
        D0010File(self.file_name, "header", "footer").save()


    def test_import_d0010_file(self):
        result = import_d0010_file(self.file_path)
        self.assertEqual(len(result), 37)

    def test_parse_d0010_file(self):
        result = parse_d0010_lines(self.lines, 'DTC5259515123502080915D0010.uff')
        self.assertEqual(len(result), 13)

    def test_clean_meter_reading_date(self):
        result = parse_d0010_lines(self.lines, 'DTC5259515123502080915D0010.uff')
        result = result[0]
        D0010File('DTC5259515123502080915D0010.uff', "header", "footer").save()
        expected = {
            "mpan_core": "1200023305967",
            "bsc_validation_status": "V",
            "meter_id": "F75A 00802",
            "reading_type": "D",
            "meter_register_id": "S",
            "reading_date_time": timezone.make_aware(datetime.strptime("20160222000000", "%Y%m%d%H%M%S")),
            "register_reading": "56311.0",
            "reset_date_time": None,
            "number_of_md_resets": None,
            "meter_reading_flag":  True,
            "reading_method": "N",
            "file_name": D0010File.objects.get(file_name='DTC5259515123502080915D0010.uff')
        }
        self.assertEqual(result, expected)



