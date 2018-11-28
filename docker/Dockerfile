FROM ocaml/opam2:ubuntu-18.04

# install package managers
RUN sudo apt-get update && sudo apt-get install -y \
        libgmp-dev \
        libssl-dev \
        m4 \
        pkg-config \
        python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

# install imandra
COPY --from=imandra/imandra-client:latest /usr/local/var/imandra /usr/local/var/imandra
ENV OPAMSWITCH '/usr/local/var/imandra'
ENV OPAM_SWITCH_PREFIX '/usr/local/var/imandra/_opam'
ENV LD_LIBRARY_PATH /usr/local/var/imandra/_opam/lib/stublibs:${LD_LIBRARY_PATH}
ENV PATH=/usr/local/var/imandra/_opam/bin:${PATH}

# install ocaml dependencies
RUN opam install \
        ISO8601 \
        xml-light

# install python dependencies
COPY python_requirements.txt .
RUN sudo pip3 install -r python_requirements.txt

ENTRYPOINT ["imandra_client" "-server" "imandra_network_client"]
# CMD ["imandra-repl"]

# COPY ./entrypoint.sh /
# ENTRYPOINT ["/entrypoint.sh"]
# CMD ["bash"]

# docker run -it --rm -v ${HOME}/.imandra:/opam/.imandra -p 8000:8000 this_image