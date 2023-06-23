@echo off
echo Installing required dependencies for Python
python -m pip install selenium

echo Downloading ChromeDriver
powershell -command "Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE' -OutFile 'chromedriver_version.txt'"
set /p chromedriver_version=<chromedriver_version.txt
del chromedriver_version.txt
powershell -command "Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/%chromedriver_version%/chromedriver_win32.zip' -OutFile 'chromedriver.zip'"
powershell -command "Expand-Archive -Path 'chromedriver.zip' -DestinationPath 'chromedriver'"
del chromedriver.zip

echo Installation completed.
