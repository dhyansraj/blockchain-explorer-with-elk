FROM centos:8

ENV DOCKER_USER=ethereum

RUN yum -y install make golang-1.15.14 gmp-devel git-2.27.0
RUN git clone https://github.com/ethereum/go-ethereum
WORKDIR go-ethereum
RUN make geth

RUN install -m 0755 -o root -g root -t /usr/local/bin build/bin/*

RUN useradd -ms /bin/bash ${DOCKER_USER}
USER ${DOCKER_USER}
WORKDIR /home/${DOCKER_USER}
