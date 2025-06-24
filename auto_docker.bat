@echo off
echo [Stop] All containers
FOR /F "tokens=*" %%i IN ('docker ps -q') DO docker stop %%i

echo [Removing] All Containers
FOR /F "tokens=*" %%i IN ('docker ps -aq') DO docker rm %%i

echo [Removing] All images...
FOR /F "tokens=*" %%i IN ('docker images -q') DO docker rmi -f %%i

echo [Cleaning] Not used volumes
docker volume prune -fC:\GitHub\fastApi\garantiasIA\config\response_format.json

echo [Cleaning] Not used networks
docker network prune -f

echo [Composing Up]

docker compose up

pause