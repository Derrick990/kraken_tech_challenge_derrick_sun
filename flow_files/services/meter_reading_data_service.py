import logging

from flow_files.models import FlowMeterReading, D0010File

logger = logging.getLogger(__name__)

def delete_meter_readings(file_name_arg):
    """
      Delete D0010 file. When it is deleted this will cascade to all readings that are associated with this file.

      Args:
          file_name_arg (string): Original name of the file
      """
    if file_name_arg == 'all':
        D0010File.objects.all().delete()
        logger.info("Deleted all FlowMeterReadingFile entries.")
        return

    queryset = D0010File.objects.filter(file_name=file_name_arg)

    if queryset.exists():
        queryset.delete()
        logger.info(f"The file '{file_name_arg}' has been deleted.")
    else:
        logger.info(f"The file '{file_name_arg}' does not exist.")

def d0010_file_exists(file_name):
    return D0010File.objects.filter(file_name=file_name).exists()

def save_d0100_file(file_name, header, footer):
    D0010File.objects.create(
        file_name=file_name,
        header=header,
        footer=footer
    )


def create_meter_readings(file_data):
    return [FlowMeterReading(**data) for data in file_data]

def save_meter_readings(meter_readings):
    FlowMeterReading.objects.bulk_create(meter_readings)

