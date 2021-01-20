cp -r ../sharedLib .
docker build -t add-new-word:latest .
rm -rf sharedLib
