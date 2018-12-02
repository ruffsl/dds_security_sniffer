FROM imandra/imandra-client-switch:ubuntu

# install ocaml moduals
RUN opam install \
      ISO8601 \
      xml-light

# CMD ["imandra-repl", "--skip-update", "--skip-network-check"]

# docker run -it --rm -v ${HOME}/.imandra:/home/opam/.imandra -p 8000:8000 this_image
