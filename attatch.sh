#!/usr/bin/env bash
ID=$(docker ps -aqf "name=rl-env")
docker exec -it $ID bash