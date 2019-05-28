# RoboSchool

[![Build Status](https://travis-ci.com/acntech/UKA19-sommerprosjekt.svg?branch=master)](https://travis-ci.com/acntech/UKA19-sommerprosjekt.svg)
[![codecov](https://codecov.io/gh/fabiansd/UKA19-sommerprosjekt/branch/master/graph/badge.svg?token=vHIWuOEtHF)](https://codecov.io/gh/fabiansd/UKA19-sommerprosjekt)
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

> This is a Reinforcement Learning framework with the purpose of experimenting with RL and building and training different agents.

The status of the automatic tests can be viewed here

> https://travis-ci.com/fabiansd/UKA19-sommerprosjekt

Test progress and coverage is visualized here

> https://codecov.io/gh/fabiansd/UKA19-sommerprosjekt

The docker image is automatically pushed to and updated if the tests 
pass

> https://cloud.docker.com/repository/docker/fabiansd/uka19_sommerprosjekt_docker/builds

## Usage

For å kjøre applikasjonen på lokalt miljø: 

> `python -m project_code`

For å kjøre applikasjonen på konfigurert Docker miljø må du først, med mindre du allerede har gjorte, nedlaste docker bildet fra Docker hub:

> `docker pull fabiansd/uka19_sommerprosjekt_docker`

Deretter kan applikasjonen kjøres på dette utviklingsmiljøet:

> `docker run --rm --detach fabiansd/uka19_sommerprosjekt_docker`

For å få innsyn i kjøreprosessen:

> `docker run --rm -it fabiansd/uka19_sommerprosjekt_docker`

