from django.core.management.base import BaseCommand
from flow_files.services.meter_reading_data_service import delete_meter_readings
import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = ('Delete all flow meter readings from the database. Specify the file name to delete one file.'
            'Add \'all\' as an argument to delete all readings.')
    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, nargs='?', default=None, help='Name of the pipe-delimited file')

    def handle(self, *args, **kwargs):
        file_name_arg = kwargs.get('file_name')
        delete_meter_readings(file_name_arg)


