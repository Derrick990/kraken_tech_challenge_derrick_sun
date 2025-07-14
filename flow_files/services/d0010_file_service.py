import logging
from datetime import datetime
from django.utils import timezone

from flow_files.models import D0010File

logger = logging.getLogger(__name__)

def import_d0010_file(file_path):
    """
         Import D0010 file from a folder location and split the contents into lines

         Args:
             file_path (string): path of file to be imported

         Returns:
             list of strings: List of each line of the file
         """
    try:
        with open(file_path, 'r') as file:
            lines = list(file)
    except FileNotFoundError as e:
        logger.error(f"File not found in {file_path}: {e}")
        return None

    return lines

def parse_d0010_lines(file_data, file_name):
    """
      Parse the lines of a D0010 file.

      Args:
          file_data (list of strings): Data from file
          file_name (string): Original name of the file

      Returns:
          list of JSON: Processed meter reading data.
      """

    meter_readings = []
    prev_record = '000'

    # Remove header and footer
    file_data = file_data[1:-1]
    current_record = {
        "026": None,
        "028": None,
        "030": None,
    }

    for line in file_data:
        line = line.strip()
        if not line:
            continue
        split_line = line.split('|')[:-1]
        line_code = split_line[0]
        # Assumming the 3-digit line code always increases for a single reading, if the current line code is less than or
        # equal the previous, we can assume that the previous lines constitute a single meter reading.

        if line_code <= prev_record:
            raw_data = current_record["026"] + current_record["028"] + current_record["030"]
            cleaned = clean_meter_reading_data(raw_data, file_name)
            meter_readings.append(cleaned)

        # This is not functionally necessary, but I cleared the current_record every time the loop moves to a new MPAN
        # This is so that there is never mismatched data in current_record (For debugging).
        if line_code == '026':
            current_record = current_record = {
                "026": None,
                "028": None,
                "030": None,
            }

        if line_code in current_record:
            current_record[line_code] = split_line[1:]

        prev_record = split_line[0]

    # This picks up the last record not recorded in the loop.
    if all(current_record.values()):
        raw_data = current_record["026"] + current_record["028"] + current_record["030"]
        cleaned = clean_meter_reading_data(raw_data, file_name)
        meter_readings.append(cleaned)

    return meter_readings

def clean_meter_reading_data(raw_data, file_name):
    """
    Separate the elements of single meter readings into a JSON-like structure.
    """
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
        "file_name": D0010File.objects.get(file_name=file_name)
    }

