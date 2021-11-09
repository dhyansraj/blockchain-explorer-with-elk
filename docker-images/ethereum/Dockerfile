FROM oraclelinux:7-slim

ENV DOCKER_USER=ethereum
ENV DOCKER_DOWNLOAD_URL=https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.10.11-7231b3ef.tar.gz
ENV DOCKER_VERSION=1.10.11

RUN yum install tar gzip wget -y
RUN wget ${DOCKER_DOWNLOAD_URL}
RUN tar xzf geth-linux-amd64-${DOCKER_VERSION}-7231b3ef.tar.gz
RUN install -m 0755 -o root -g root -t /usr/local/bin geth-linux-amd64-${DOCKER_VERSION}-7231b3ef/*

RUN useradd -ms /bin/bash ${DOCKER_USER}
USER ${DOCKER_USER}
WORKDIR /home/${DOCKER_USER}
