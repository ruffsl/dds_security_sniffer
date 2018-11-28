FROM ocaml/opam2:ubuntu-18.04

# install imandra
RUN sudo apt-get update && sudo apt-get install -y \
        iputils-ping \
        wget \
    && wget https://storage.googleapis.com/imandra-installer/install.sh -O install.sh \
    && echo "/usr/local/bin\n" | sh install.sh -n \
    && sudo rm -rf /var/lib/apt/lists/*

# install ocaml moduals
RUN opam install \
        ISO8601 \
        xml-light

# install package managers
RUN sudo apt-get update && sudo apt-get install -y \
        python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY python_requirements.txt .
RUN sudo pip3 install -r python_requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["imandra-repl"]

# docker run -it --rm -v ${HOME}/.imandra:/home/opam/.imandra -p 8000:8000 this_image 