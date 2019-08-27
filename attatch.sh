#!/usr/bin/env bash
ID=$(docker ps -aqf "name=roboschool_devenv")
docker exec -it $ID bash