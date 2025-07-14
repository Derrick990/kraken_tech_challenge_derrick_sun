# Kraken Distribution Technical Challenge - Derrick Sun
This project implements the Technical challenge from Kraken Technology. It ingests D0010 .uff files, parses through them and saves the electricty meter data contained into an sqlite database.

# ADD DESCRIPTION
## How to set up the Project locally
The project can only run in a python virtual environment.
1. Go to command line in a folder where you want to create a virtual environment and enter: 
   - python -m venv <environmentname>
2. Unzip the project folder and copy/paste the project folder into the venv folder.
3. In the command line of the venv folder enter: 
   - Scripts\activate.bat
4. Go into the project folder
   - cd src\kraken_tech_challenge_derrick_sun
5. Run the project and update it with the below 3 commands. (NOTE: Before running the server it's best to create an admin user first):
   - python manage.py runserver
   - python manage.py make migrations 
   - python manage.py migrate

## Create an admin user and login
1. Go to the project folder in the terminal, run the venv again and enter:
   - python manage.py createsuperuser
2. Enter username, password and email. Email can be left blank.

## Process file while the server is running
1. Go to project folder in command line
2. Run the management command and specify the absolute path of the D0010 file. The server can inject files from any folder in the local machine. e.g. C:\Users\Derrick\Django Project\VENV\src\kraken_test_derrick_sun\meter_readings\D0010_files
   - python manage.py import_meter_readings <folder path\file name>
3. To import all files in a folder leave the filename blank. The command only accepts .uff files. Incorrectly formatted files will be skipped.
4. Add more .uff files to the desired folder to import them.

## View meter Readings
1. With the server running go to http://127.0.0.1:8000/admin in your web browser.
2. Enter admin credentials

## To run unit tests
1. With the venv and server already running enter below in the command line:
   - python manage.py test meter_readings

## To delete the DB data.
1. You can delete entries via the browser UI or run the below command in the command line:
   - python manage.py delete_readings <file name>
   OR to delete all entries at once:
   - python manage.py delete_readings all

## Assumptions
- The specification mentions that a full path should be used when running the script and not a single folder.
- Some of the fields in the D0010 are left blank. Assume its enough to import the existing readings data for now while leaving the code extensible for other fields.


## Areas of improvement
- Add a CRUD functionality to the command line for the files and individual readings. Especially deletion of 
  potentially invalid data.
- Add a view so that the data can be viewed in a more user-friendly way.
- The D0010_test_files folders is a bit messy. Could edit the management command so that it can also pull files from
an absolute path/
- Some naming conventions are perhaps unclear.
- Needs exception handling for invalid/incorrectly formatted data.
- Add validation to the file and readings parameters.

TODO
- Injest 13 readings
- Look at documentation for is required.
