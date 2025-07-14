# Kraken Distribution Technical Challenge - Derrick Sun
This project implements the Technical challenge from Kraken Technology. It ingests D0010 .uff files, parses through them and saves the electricty meter data contained into an sqlite database.
It imports the .uff file separates the lines and elements using the pipes | and parses them to a JSON structure. Then creates and saves each meter reading.

# ADD DESCRIPTION
## How to set up the Project locally
The project can only run in a python virtual environment.
1. Unzip the project folder to desired location.
2. Go to command line in the project folder where you want to create a virtual environment and enter: 
   - python -m venv <environmentname>
3. In the command line of the venv folder enter: 
   - Scripts\activate.bat
   NOTE: if this doesn't work you may need to install django by running:
   - pip install django
5. Run the project and update it with the below 3 commands. (NOTE: Before running the server it's best to create an admin user first):
   - python manage.py runserver
   - python manage.py make migrations 
   - python manage.py migrate

## Create an admin user and login
1. Go to the project folder in the terminal, run the venv again and enter:
   - python manage.py createsuperuser
2. Enter username, password and email. Email can be left blank.

## Process file 
1. Go to project folder in command line with the venv already running.
2. Run the management command and specify the absolute path of the D0010 file. The server can inject files from any folder in the local machine. e.g. C:\Users\Derrick\Django Project\VENV\src\kraken_test_derrick_sun\meter_readings\D0010_files
   - python manage.py import_meter_readings <folder path>
   The command only accepts .uff files. Incorrectly formatted files will be skipped.
4. Add more .uff files to the desired folder to import them.

## View meter Readings
1. With the server running go to http://127.0.0.1:8000/admin in your web browser.
2. Enter admin credentials

## To run unit tests
1. With the venv and server already running enter below in the command line:
   - python manage.py test

## To delete the DB data.
1. You can delete entries via the browser UI or run the below command in the command line:
   - python manage.py delete_readings <file name>
   OR to delete all entries at once:
   - python manage.py delete_readings all

## Assumptions
- The specification mentions that a full folder path should be used when running the script and not a single file.
- Some of the fields in the D0010 are left blank. Couldn't find another example D0010 file. Assume its enough to import the existing readings data for now while leaving the code extensible for other fields.
- Multiple readings 030 can exist for the same meter and meter point in the same file.


## Areas of improvement
- Add a CRUD functionality to the command line for the files and individual readings. Especially deletion of 
  potentially invalid data.
- Add a view so that the data can be viewed in a more user-friendly way.
- Needs more exception handling for invalid/incorrectly formatted data.
- Add validation to the file and readings parameters.
- The footer appears to have meta data about the file e.g. how many lines and how many meter points were read. Could record this meta data explicitly and use it for validation.
