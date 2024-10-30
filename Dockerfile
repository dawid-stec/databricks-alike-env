FROM python:3.11.4-buster

ARG APP_HOME=/home/app

WORKDIR ${APP_HOME}

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

RUN pip install pipenv

COPY Pipfile Pipfile.lock
RUN pipenv sync

COPY . ./

EXPOSE 8888
CMD ["pipenv", "run", "jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--no-browser"]