import logging
import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand

from kraken_tech_challenge_derrick_sun import settings
from flow_files.models import D0010File
from flow_files.services.d0010_file_service import import_d0010_file, parse_d0010_lines
from flow_files.services.meter_reading_data_service import d0010_file_exists, create_meter_readings, \
    save_meter_readings, save_d0100_file

logger = logging.getLogger(__name__)
used_files_dir = settings.BASE_DIR / 'flow_files\\imported_d0010_files'

class Command(BaseCommand):
    help = ('Import D0010 file, parse for flow meter readings and save to database. Takes a folder path in the local'
            'machine as an argument')

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path of the folder which contains the '
        'pipe-delimited .uff file(s)')

    def handle(self, *args, **kwargs):
        files_dir = kwargs.get('path')
        files = os.listdir(files_dir)

        # Get the list of .uff files from the path argument.
        uff_files = [file for file in files if file.endswith('.uff')]

        # Check if the directory is empty. If it is empty, no exception is thrown. The program exits.
        if not uff_files:
            logger.error(f"Directory contains no valid files for ingestion: {files_dir}. Please check the directory.")
            return
        meter_readings = []

        # Loop through uff files. Once the file is processed it is moved to a separate folder.
        # If there is a problem with a specific file the program skips it.
        for file_name in uff_files:
            try:
                if not d0010_file_exists(file_name):
                    lines = import_d0010_file(files_dir + '\\' + file_name)
                    save_d0100_file(file_name, lines[0], lines[1])
                    file_data = parse_d0010_lines(lines, file_name)
                    reading_objects = create_meter_readings(file_data)
                    meter_readings.extend(reading_objects)
                    shutil.move(Path(files_dir) / file_name, used_files_dir / file_name)
                else:
                    logger.info("File %s already exists and imported." % file_name)
                    shutil.move(Path(files_dir) / file_name, used_files_dir / file_name)
            except Exception as e:
                logger.error("Exception occurred while importing readings from file {}: {e}", file_name)
                D0010File.objects.filter(file_name=file_name).delete()
                continue

        # Bulk create all imported readings.
        try:
            save_meter_readings(meter_readings)
            logger.info("Successfully imported {} meter_readings".format(len(meter_readings)))
        except Exception as e:
            logger.error("Exception occurred while saving readings.")



















