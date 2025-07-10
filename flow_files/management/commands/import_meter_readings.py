import logging
import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand

from kraken_tech_challenge_derrick_sun import settings
from flow_files.models import FlowMeterReadingFile
from flow_files.services.d0010_file_service import import_d0010_file, parse_d0010_lines
from flow_files.services.meter_reading_service import d0010_file_exists, create_meter_readings, save_meter_readings

logger = logging.getLogger(__name__)
used_files_dir = settings.BASE_DIR / 'flow_files\\imported_files'

class Command(BaseCommand):
    help = 'Import flow meter readings and save to database'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path of the folder while contains the '
        'pipe-delimited file(s)')

    def handle(self, *args, **kwargs):
        files_dir = kwargs.get('path')
        files = os.listdir(files_dir)

        # Get the list of .uff files for importing and returns a list of file data.
        uff_files = [file for file in files if file.endswith('.uff')]
        # Check if the directory is empty.
        if not uff_files:
            logger.error(f"Directory contains no valid files for ingestion: {files_dir}. Please check the directory.")
            return

        meter_readings = []
        for file_name in uff_files:
            try:
                if not d0010_file_exists(file_name):
                    lines = import_d0010_file(files_dir + '\\' + file_name)
                    print(lines)
                    FlowMeterReadingFile.objects.create(
                        file_name=file_name,
                        header=lines[0],
                        footer=lines[-1]
                    )
                    file_data = parse_d0010_lines(lines, file_name)
                    reading_objects = create_meter_readings(file_data)
                    meter_readings.extend(reading_objects)
                    shutil.move(Path(files_dir) / file_name, used_files_dir / file_name)
                else:
                    logger.info("File %s already exists and imported." % file_name)
            except Exception as e:
                logger.error("Exception occurred while importing readings from file {}: {e}", file_name)
                continue
        # Bulk create all imported readings.
        save_meter_readings(meter_readings)
        logger.info("Successfully imported {} meter_readings".format(len(meter_readings)))


















