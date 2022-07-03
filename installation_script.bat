@echo off
:: This script automates the process of setting up the application
:: on a windows machine, after the source code has been cloned.
:: The application will be set up in the same directory as the script

echo Installing setuptools and virtualenv
pip install setuptools virtualenv
echo Creating virtual environment named venv
python -m virtualenv venv
echo Activating virtual environment
.\venv\Scripts\activate
echo Installing requirements.txt
pip install -r requirements.txt
echo Application is now successfully installed.
set /p LAUNCH_APP=Would you like to launch the application? [Y/n]
if %LAUNCH_APP%==y python main.py
if %LAUNCH_APP%==Y python main.py
echo Exiting virtual environment
deactivate
echo Terminating script...
