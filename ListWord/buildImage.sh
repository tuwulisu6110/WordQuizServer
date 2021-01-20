cp -r ../sharedLib .
docker build -t list-word:latest .
rm -rf sharedLib

