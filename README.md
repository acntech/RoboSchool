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
The docker image is automatically pushed to and updated if the tests 
pass

> https://cloud.docker.com/repository/docker/fabiansd/uka19_sommerprosjekt_docker/builds

## Docker

### Omniboard

Omniboard and mongo DB must be run and also be able to talk with each other. This can be obtained by starting them on the same docker network. First, create a new docker network or use an existing network

> docker network create omniboard-network

We now have a network on which to run the docker containers. The mongodb and omniboard container should use the same docker network

> docker run --rm --name mongo-container --net omniboard-network -d mongo

Then run the omniboard network 

> docker run --rm -d -p 9090:9090 --name omniboard --net=omniboard-network vivekratnavel/omniboard -m MONGODB_CONTAINER:27017:sacred

### RL development environment

To start up the RL environment with a jupyter notebook running, write:

> docker run --rm -it -v pwd:/notebooks -p 8888:8888 justheuristic/practical_rl

Go to localhost:8888 and insert the token from the console to log in.



### Flask application

The flask application can be started up by running:

> docker run --rm -d -p 9000:9000 fabiansd/roboschool-app

Then go to localhost:9000 to see the frontend application

## Usage

To run the application on a local environment

> `python -m src`



