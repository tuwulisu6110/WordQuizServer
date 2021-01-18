xcopy /I ..\sharedLib .\sharedLib
docker build -t user-management:latest .
rmdir /S /Q sharedLib
pause