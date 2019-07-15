mkdir -p ./ppe-release
tar zxvf ppe-release-$date.tar.gz -C ./ppe-release
cd ./ppe-release
docker load -i ppe-backend.tar
docker load -i ppe-frontend.tar
docker-compose up -d
