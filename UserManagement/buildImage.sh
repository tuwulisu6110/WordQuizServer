cp -r ../sharedLib .
docker build -t user-management:latest .
rm -rf ./sharedLib
