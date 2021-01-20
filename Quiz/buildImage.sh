cp -r ../sharedLib .
docker build -t quiz:latest .
rm -rf sharedLib

