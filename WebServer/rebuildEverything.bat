call killContainer.bat
call buildImage.bat
docker image prune -f
call startContainer.bat
docker logs -f WebServer