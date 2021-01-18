xcopy /I ..\sharedLib .\sharedLib
docker build -t quiz:latest .
rmdir /S /Q sharedLib
::pause