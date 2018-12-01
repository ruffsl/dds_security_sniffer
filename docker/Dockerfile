FROM imandra/imandra-client-switch:ubuntu

# install ocaml moduals
RUN opam install \
      ISO8601 \
      xml-light

# install package managers
RUN sudo apt-get update && sudo apt-get install -y \
        python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN sudo pip3 install \
        jupyter \
        networkx \
        pexpect

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["imandra-repl", "--skip-update", "--skip-network-check"]

# docker run -it --rm -v ${HOME}/.imandra:/home/opam/.imandra -p 8000:8000 this_image
