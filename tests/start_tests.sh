# rm -r cache/
docker-compose down
docker-compose rm -f
docker-compose pull
docker-compose up --build -d
sleep 10
docker-compose exec database pytest tests/test_routes.py