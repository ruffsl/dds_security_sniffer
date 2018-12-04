FROM ubuntu:18.04

# install package managers
RUN apt-get update && apt-get install -y \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip3 install \
        jupyter \
        networkx \
        pexpect
