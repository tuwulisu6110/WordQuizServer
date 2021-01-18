xcopy /I ..\sharedLib .\sharedLib
docker build -t list-word:latest .
rmdir /S /Q sharedLib
::pause