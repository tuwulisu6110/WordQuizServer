xcopy /I ..\sharedLib .\sharedLib
docker build -t add-new-word:latest .
rmdir /S /Q sharedLib
::pause