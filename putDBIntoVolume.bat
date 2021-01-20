docker run -d --name putData -v db:/Database centos:7 tail -f /dev/null
docker cp wordQuizData.db putData:/Database
docker exec -it putData chmod -R 777 /Database
docker kill putData
docker rm putData