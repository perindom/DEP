FROM python:3.10-slim

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

RUN pip3 install jupyter
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install kaleido
RUN pip3 install pandas
RUN pip3 install plotly
RUN pip3 install pyyaml
RUN pip3 install requests
RUN pip3 install seaborn
RUN pip3 install scikit-learn
RUN pip3 install pandas-datareader
RUN pip3 install yfinance --upgrade
RUN pip3 install s3fs
RUN pip3 install apache-airflow
RUN pip3 install kafka-python

WORKDIR /main
RUN chmod -R a+w .
