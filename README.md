# RoboSchool

[![Build Status](https://travis-ci.org/acntech/RoboSchool.svg?branch=master)](https://travis-ci.org/acntech/RoboSchool.svg)
[![codecov](https://codecov.io/gh/acntech/RoboSchool/branch/master/graph/badge.svg)](https://codecov.io/gh/acntech/RoboSchool)
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

> This is a Reinforcement Learning framework with the purpose of experimenting with RL and building and training different agents.

The status of the automatic tests can be viewed here

> https://travis-ci.org/acntech/RoboSchool

Test progress and coverage is visualized here

> https://codecov.io/gh/acntech/RoboSchool

Docker images used for development can be found here

> https://hub.docker.com/u/fabiansd

## Docker

Docker has the purpose of creating an environment the different parts of the application can run on. See the docker docs

To enter a container that is running, type

> docker exec -it [container-id] bash

### Issues

Setting up a docker volume, i.e. a dynamic connection between a folder on the local host and the container, can be problematic on windows. If docker is unable to establish a volume connection due to shared drivers try the following fix:

https://github.com/Cyb3rWard0g/HELK/issues/79 

### Omniboard and mongoDB

Omniboard and mongo DB must be run and also be able to talk with each other. This can be obtained by starting them on the same docker network. First, create a new docker network or use an existing network

> docker network create omniboard-network

We now have a network on which to run the docker containers. The mongodb and omniboard container should use the same docker network

> docker run --rm --name mongo-container --net omniboard-network -d mongo

Then run the omniboard network 

> docker run --rm -d -p 9000:9000 --name omniboard --net=omniboard-network vivekratnavel/omniboard -m MONGODB_CONTAINER:27017:sacred


### RL development environment

To start up the RL environment with a jupyter notebook running, write:

> docker run --rm -it -v pwd:/notebooks -p 8888:8888 justheuristic/practical_rl

Go to localhost:8888 and insert the token from the console to log in. A RL environment image has been made for this projects and can be run by 

> docker run --rm -it -p 8888:8888 fabiansd/rl-env bash

You will then start up a linux container with all the necessary libraries installed. Here you can run python scripts and linux commands, and also start jupyter by typing

> sh /RoboSchool/src/run_jyputer.sh


### Flask application

The frontend application is implemented with a Flask app and docker image built from /Roboschool with

> docker build -f app/Dockerfile -t fabiansd/roboschool-app .

The application can be started up by running:

> docker run --rm -d -p 9999:9999 fabiansd/roboschool-app

Then go to localhost:9090 to see the frontend application

### Docker-compose

Docker-compose is used to start all the docker files for the appliaction and enables you to run a single command to start up everything. I short: it summarizes all the commands above into one file and executes them such that all you have to do is run the docker-compose file and you're good to go.

To run application with docker-compose:

> docker-compose up -d

The running containers can now be viewed with 

> docker ps

To enter the development environment, attach to the src container by copying its ID in the container list and type

> docker exec -it [container-id] bash

To close the containers, i.e. the application, simply type

> docker-compose down


## Usage

To run the application on a local environment

> `python -m src`





