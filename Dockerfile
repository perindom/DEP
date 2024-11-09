FROM python:3.10-slim

RUN apt-get install debian-archive-keyring
RUN apt-get update

# Install dependencies.
# rm -rf /var/lib/apt/lists/* cleans up apt cache. See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
     python3-pip \
     locales \
     && rm -rf /var/lib/apt/lists/*


# Configure UTF-8 encoding.
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 


# Make python3 default
RUN rm -f /usr/bin/python \
     && ln -s /usr/bin/python3 /usr/bin/python

RUN apt-get update
RUN apt-get install -y vim git tmux

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /main
RUN chmod -R a+w .
