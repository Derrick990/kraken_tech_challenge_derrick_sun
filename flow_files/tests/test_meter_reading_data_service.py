import os

import django
from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from flow_files.tests.test_commands import file_name

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kraken_tech_challenge_derrick_sun.settings")
django.setup()

from flow_files.models import D0010File, FlowMeterReading
from flow_files.services.meter_reading_data_service import d0010_file_exists, create_meter_readings, \
    save_meter_readings, delete_meter_readings
from kraken_tech_challenge_derrick_sun import settings




files_dir = settings.BASE_DIR / 'flow_files/tests/test_files/DTC5259515123502080915D0010_test.uff'

class MeterDataServiceTest(TestCase):
    def setUp(self):
        self.file_path = files_dir
        self.file_name = 'DTC5259515123502080915D0010_test.uff'
        D0010File(self.file_name, "header", "footer").save()
        D0010File('DTC5259515123502080915D0011.uff', "header", "footer").save()

    def test_delete_meter_readings(self):
        self.assertTrue(D0010File.objects.filter(file_name=file_name).exists())
        delete_meter_readings(self.file_name)
        self.assertFalse(D0010File.objects.filter(file_name=file_name).exists())

    def test_d0010_file_exists(self):
        d0010_files = d0010_file_exists(self.file_name)
        self.assertTrue(d0010_files)

    def test_d0010_file_exists_false(self):
        D0010File.objects.filter(file_name=file_name).delete()
        d0010_files = d0010_file_exists(self.file_name)
        self.assertFalse(d0010_files)

    def test_create_meter_readings(self):
        data = [{
            "mpan_core": "1200023305967",
            "bsc_validation_status": "V",
            "meter_id": "F75A 00802",
            "reading_type": "D",
            "meter_register_id": "S",
            "reading_date_time": timezone.make_aware(datetime.strptime("20160222000000", "%Y%m%d%H%M%S")),
            "register_reading": "56311.0",
            "reset_date_time": None,
            "number_of_md_resets": None,
            "meter_reading_flag": True,
            "reading_method": "N",
            "file_name": D0010File.objects.get(file_name='DTC5259515123502080915D0010_test.uff')
        },
        {
            "mpan_core": "1200023305968",
            "bsc_validation_status": "V",
            "meter_id": "G75A 00802",
            "reading_type": "D",
            "meter_register_id": "S",
            "reading_date_time": timezone.make_aware(datetime.strptime("20160222000000", "%Y%m%d%H%M%S")),
            "register_reading": "56311.0",
            "reset_date_time": None,
            "number_of_md_resets": None,
            "meter_reading_flag": True,
            "reading_method": "N",
            "file_name": D0010File.objects.get(file_name='DTC5259515123502080915D0011.uff')
        }
        ]
        readings = create_meter_readings(data)
        self.assertEqual(len(readings), 2)
        self.assertEqual(readings[0].mpan_core, "1200023305967")
        self.assertEqual(readings[1].mpan_core, "1200023305968")

    def test_save_meter_reading(self):
        data = [{
            "mpan_core": "1200023305967",
            "bsc_validation_status": "V",
            "meter_id": "F75A 00802",
            "reading_type": "D",
            "meter_register_id": "S",
            "reading_date_time": timezone.make_aware(datetime.strptime("20160222000000", "%Y%m%d%H%M%S")),
            "register_reading": "56311.0",
            "reset_date_time": None,
            "number_of_md_resets": None,
            "meter_reading_flag": True,
            "reading_method": "N",
            "file_name": D0010File.objects.get(file_name='DTC5259515123502080915D0010_test.uff')
        },
            {
                "mpan_core": "1200023305968",
                "bsc_validation_status": "V",
                "meter_id": "G75A 00802",
                "reading_type": "D",
                "meter_register_id": "S",
                "reading_date_time": timezone.make_aware(datetime.strptime("20160222000000", "%Y%m%d%H%M%S")),
                "register_reading": "56311.0",
                "reset_date_time": None,
                "number_of_md_resets": None,
                "meter_reading_flag": True,
                "reading_method": "N",
                "file_name": D0010File.objects.get(file_name='DTC5259515123502080915D0011.uff')
            }
        ]
        readings = create_meter_readings(data)
        save_meter_readings(readings)
        self.assertEqual(FlowMeterReading.objects.count(), 2)
        self.assertTrue(FlowMeterReading.objects.filter(file_name='DTC5259515123502080915D0010_test.uff').exists())
        self.assertTrue(FlowMeterReading.objects.filter(file_name='DTC5259515123502080915D0011.uff').exists())




