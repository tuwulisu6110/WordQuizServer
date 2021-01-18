docker run -d -v db:/Database -p 5002:5000 --name AddNewWord add-new-word:latest
docker logs -f AddNewWord