from flow_files.models import FlowMeterReading, FlowMeterReadingFile
import logging

logger = logging.getLogger(__name__)


def delete_meter_readings(file_name_arg):
    if not file_name_arg:
        logger.info("Please provide a file name argument or specify 'all'")
        return

    if file_name_arg == 'all':
        FlowMeterReadingFile.objects.all().delete()
        logger.info("Deleted all FlowMeterReadingFile entries.")
        return

    queryset = FlowMeterReadingFile.objects.filter(file_name=file_name_arg)

    if queryset.exists():
        queryset.delete()
        logger.info(f"The file '{file_name_arg}' has been deleted.")
    else:
        logger.info(f"The file '{file_name_arg}' does not exist.")

def d0010_file_exists(file_name):
    return FlowMeterReadingFile.objects.filter(file_name=file_name).exists()

def create_meter_readings(file_data):
    return [FlowMeterReading(**data) for data in file_data]

def save_meter_readings(meter_readings):
    FlowMeterReading.objects.bulk_create(meter_readings)

