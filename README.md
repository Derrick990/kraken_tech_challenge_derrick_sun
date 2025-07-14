# Kraken Distribution Technical Challenge - Derrick Sun
This project implements the Technical challenge from Kraken Technology. It ingests D0010 .uff files, parses through them to extract the relevant data and saves the electricity meter data contained into a sqlite database.
Django models are used represent the D00010 files and the meter readings contained. File and Readings have a one-to-many relationship. The file object is a primary foreign key of each reading.
The 3-digit code at the beginning of each line tells the program what type of data is recorded in the line.
The management command provided can ingest files from any local directory (DO NOT use the file in the test directory as this will break the tests). In addition, there are two helper services for modularity.
1. d0010_file_service.py handles logic related to importing and parsing the files to prepare them for saving.
2. meter_reading_data_service handles logic related to creating and saving FlowMeterReading objects and D00010File objects.

FOR BELOW COMMANDS: If using Mac use python3 in command line, if using Windows use python

## How to set up the Project locally
The project can only run in a python virtual environment. I'm assuming python is installed on your local machine.
1. Unzip the project folder to the desired location.
2. Go to command line in the project folder where you want to create a virtual environment and enter: 

   For MAC
   - python3 -m venv `<environmentname>` 
   
   For Windows
   - py -m venv `<environmentname>` 

3. In the command line of the venv folder enter:
   
   Mac
   - bin/activate.bat

   Windows
   - Scripts\activate.bat
4. If Django is not installed, run the below:
   
   Mac
   - python3 -m pip install django
   
   Windows
   - pip install django
5. Run the project and update it with the below 3 commands.
   - python3 manage.py make migrations 
   - python3 manage.py migrate
   - python3 manage.py runserver

## Process file 
1. Go to project folder in command line with the venv already running.
2. Run the management command and specify the absolute path of the D0010 file. Make sure the path is double-quoted. The server can inject files from any folder in the local machine. e.g. C:\Users\Derrick\Django Project\VENV\src\kraken_test_derrick_sun\flow_files\D0010_files
   - python3 manage.py import_meter_readings "`<folder path>`"
   - The command only accepts .uff files. Incorrectly formatted files will be skipped.
3. Add more .uff files to the desired folder to import them.


## Create an admin user and login
1. Go to the project folder in the terminal, run the venv again and enter:
   - python3 manage.py createsuperuser
2. Enter username, password and email. Email can be left blank.

## View meter Readings
1. With the server running go to http://127.0.0.1:8000/admin in your web browser.
2. Enter admin credentials

## To run unit tests
1. With the venv and server already running enter below in the command line:
   - python3 manage.py test

## To delete the DB data.
1. You can delete entries via the browser UI or run the below command in the command line:
   - python3 manage.py delete_readings <file name>
   OR to delete all entries at once:
   - python3 manage.py delete_readings all

## Assumptions
- The specification mentions that a full folder path should be used when running the command. All files inside that folder will be imported.
- Some of the fields in the D0010 are left blank. Couldn't find another example D0010 file. Assume it's enough to import the existing readings data for now while leaving the code extensible for other fields.
- Multiple readings 030 can exist for the same meter and meter point in the same file.


## Areas of improvement
- Add a CRUD functionality to the command line for the files and individual readings. Especially deletion of 
  potentially invalid data.
- Add a Django view so that the data can be viewed in a more user-friendly way.
- Needs more exception handling for invalid/incorrectly formatted data.
- Add validation to the file and readings parameters.
- The footer appears to have meta-data about the file e.g. how many lines and how many meter points were read. Could record this metadata explicitly and use it for validation.
- What if two readings from the same MPAN but different meters are in the file (multiple 028 lines), need to handle for this case.
- Separate data services for files and readings.
- Add unique constraint to flow meter readings to avoid duplicates.