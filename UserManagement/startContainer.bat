docker run -d -v db:/Database -p 5001:5000 --name UserManagement user-management:latest
docker logs -f UserManagement