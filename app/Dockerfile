# In the repo root, run
# docker build -f Dockerfile -t docker_image_name .
# to build this image

# After successful build, it can be started with
# docker run --rm --detach docker_image_name

# You can also check the image by
# docker run --rm -it --entrypoint /bin/bash docker_image_name
# to enter the container and observe

# start from base
FROM ubuntu:14.04

# Intall apt dependencies
RUN apt-get -yqq update
RUN apt-get -yqq upgrade
RUN apt-get -yqq install python3
RUN apt-get -yqq install python3-pip
RUN apt-get -yqq install curl

# copy our application code
COPY ./app/requirements.txt /RoboSchool/app/requirements.txt

WORKDIR /RoboSchool

RUN pip3 install -r /RoboSchool/app/requirements.txt

COPY ./app /RoboSchool/app

# expose port
EXPOSE 9999

# start app
CMD [ "python3", "-m", "app" ]

