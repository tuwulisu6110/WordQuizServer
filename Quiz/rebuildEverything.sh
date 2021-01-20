./killContainer.sh
./buildImage.sh
docker image prune -f
./startContainer.sh
docker logs -f Quiz
