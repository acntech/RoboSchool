# RoboSchool

from branch

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

## Get started

To get start with development, run ``` docker-compose up -d ``` to start the docker environment that supports the python packages needed. 

To access the environment with a terminal, run ``` bash attatch.sh ```

you can edit the code in the local repository on your machine and test the code immediately in the docker image.

## Tensorboard

You can log the training using a tensorboard object that logs the training result and logs by default in a folder called runs in files with names created from a timestamp. 

To start tensorboard:

``` tensorboard --logdir runs --host localhost ```

This will start tensorboard on localhost:6006 from the runs folder. Alternatively you can set a different port by adding the argument ```-p xxxx:xxxx```

## Docker

Docker has the purpose of creating an environment the different parts of the application can run on. See the docker docs

To enter a container that is running, type

``` docker exec -it [container-id] bash ```

### Known issues setting up Docker

Setting up a docker volume, i.e. a dynamic connection between a folder on the local host and the container, can be problematic on windows. If docker is unable to establish a volume connection due to shared drivers try the following fix:

https://github.com/Cyb3rWard0g/HELK/issues/79 


### Docker-compose

Docker-compose is used to start all the docker files for the appliaction and enables you to run a single command to start up everything. I short: it summarizes all the commands above into one file and executes them such that all you have to do is run the docker-compose file and you're good to go.

To run application with docker-compose:

``` docker-compose up -d ```

The running containers can now be viewed with 

``` docker ps ```

To enter the development environment, attach to the src container by copying its ID in the container list and type

``` docker exec -it [container-id] bash ```

To close the containers, i.e. the application, simply type

``` docker-compose down ```






