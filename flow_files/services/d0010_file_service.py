import logging
from datetime import datetime
from django.utils import timezone
from django.conf import settings

from flow_files.models import FlowMeterReadingFile

logger = logging.getLogger(__name__)

def import_d0010_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = list(file)
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return

    return lines

def parse_d0010_lines(file_data, file_name):
    mpan_cores = []
    meter_reading_type = []
    register_readings = []
    meter_readings = []
    prev_record = '000'

    # Remove header and footer
    file_data = file_data[1:-1]

    for line in file_data:
        line = line.strip()
        if not line:
            continue
        split_line = line.split('|')[:-1]
        if split_line[0] <= prev_record or split_line[0] > '999':
            meter_reading_data = clean_meter_reading_data(mpan_cores + meter_reading_type + register_readings,
                                                             file_name)
            meter_readings.append(meter_reading_data)

        if split_line[0] == '026':
            mpan_cores = split_line[1:]

        if split_line[0] == '028':
            meter_reading_type = split_line[1:]

        if split_line[0] == '030':
            register_readings = split_line[1:]

        prev_record = split_line[0]

    return meter_readings

def clean_meter_reading_data(raw_data, file_name):
    return {
        "mpan_core": raw_data[0],
        "bsc_validation_status": raw_data[1],
        "meter_id": raw_data[2],
        "reading_type": raw_data[3],
        "meter_register_id": raw_data[4],
        "reading_date_time": timezone.make_aware(datetime.strptime(raw_data[5], "%Y%m%d%H%M%S")),
        "register_reading": raw_data[6],
        "reset_date_time": None if raw_data[7]=='' else raw_data[7],
        "number_of_md_resets": None if raw_data[8]=='' else raw_data[8],
        "meter_reading_flag": True if raw_data[9] == 'T' else raw_data[9],
        "reading_method": raw_data[10],
        "file_name": FlowMeterReadingFile.objects.get(file_name=file_name)
    }

