FROM centos:8

ENV DOCKER_USER=bitcoin
ENV DOCKER_DOWNLOAD_URL=https://bitcoin.org/bin/bitcoin-core-0.21.1/bitcoin-0.21.1-x86_64-linux-gnu.tar.gz
ENV DOCKER_VERSION=0.21.1

RUN yum install wget -y
RUN wget ${DOCKER_DOWNLOAD_URL}
RUN tar xzf bitcoin-${DOCKER_VERSION}-x86_64-linux-gnu.tar.gz
RUN install -m 0755 -o root -g root -t /usr/local/bin bitcoin-${DOCKER_VERSION}/bin/*

RUN useradd -ms /bin/bash ${DOCKER_USER}
USER ${DOCKER_USER}
WORKDIR /home/${DOCKER_USER}
