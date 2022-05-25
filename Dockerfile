# Basic Dockerfile to be used to create an image for a PyCharm Docker interpreter, that can be used for the
# generation of the _Sphinx_ documentation as well as for the unit tests.

FROM ubuntu:20.04
# Any base image you need

WORKDIR /home
# For installing all the python packages which are required for the project
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --upgrade pip setuptools &&\
    pip install --no-cache-dir -r requirements.txt

COPY . .
