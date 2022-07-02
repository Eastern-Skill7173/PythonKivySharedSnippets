#! /usr/bin/bash
# This script automates the process of setting up the application
# on a linux machine, after the source code has been cloned.
# The application will be set up in the same directory as the script

echo "Installing setuptools and virtualenv"
pip3 install setuptools virtualenv
echo "Creating virtual environment named venv"
python3 -m virtualenv venv
echo "Activating virtual environment"
source ./venv/bin/activate
echo "Installing requirements.txt"
pip3 install -r PythonKivySharedSnippets/requirements.txt
echo "Application is now successfully installed."
read -r -p "Would you like to launch the application? [Y/n]" LAUNCH_APP
if [ "$(echo "${LAUNCH_APP}" | tr '[:upper:]' '[:lower:]')" == "y" ]
then
  python3 PythonKivySharedSnippets/main.py
fi
echo "Exiting virtual environment"
deactivate
echo "Terminating script..."
