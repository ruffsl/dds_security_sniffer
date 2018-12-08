FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# install package managers
RUN apt-get update && apt-get install -y \
        libgraphviz-dev \
        python3-graphviz \
        python3-pip \
        tshark \
    && rm -rf /var/lib/apt/lists/*

# install M2Crypto dependencies
RUN apt-get update -qq && apt-get install -qq -y \
      build-essential \
      python3-dev \
      libssl-dev \
      swig \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip3 install \
        docker \
        jupyter \
        networkx \
        M2Crypto \
        pexpect \
        pygraphviz \
        pyshark \
        requests \
