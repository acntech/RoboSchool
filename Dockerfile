FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apt-utils \
       build-essential \
       curl \
       xvfb \
       ffmpeg \
       xorg-dev \
       libsdl2-dev \
       swig \
       cmake \
       python-opengl \
       tmux \
       vim


RUN pip3 install --upgrade pip && \
    pip3 install --upgrade numpy scipy && \
    pip3 install --upgrade sklearn \
                           pytest \
                           jupyter \
                           tqdm \
                           graphviz \
                           gym gym[box2d] gym[atari] \
                           matplotlib \
                           seaborn && \
    pip3 install --upgrade torch \
                           torchvision \
                           tensorflow \
                           tensorboard \
                           keras && \
    python3 -m ipykernel.kernelspec


# Install from requirements
#RUN pip3 install --upgrade pip
#RUN pip3 install pytest

RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/
RUN pip3 install --trusted-host pypi.python.org -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt


# Expose ports for various applications
EXPOSE 8888
EXPOSE 6006

# Copy the folder structure and content
#COPY . /RoboSchool
#
#WORKDIR /RoboSchool

# Download the display hotfix
RUN wget https://raw.githubusercontent.com/yandexdataschool/Practical_RL/master/xvfb
#RUN ./xvfb start

ENTRYPOINT ["tail", "-f", "/dev/null"]
