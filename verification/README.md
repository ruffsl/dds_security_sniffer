## Parser
To use the parser. You need to install
1. opam
2. Xml-light
3. utop (for simplicity, otherwise need to use package manager dune)

```bash
sudo apt-get install opam
opam install xml-light
opam install utop
```

Utop is a better Ocaml toplevel which has beautified display for all the result (thus no need to implement to_string for our data type).    

```ocaml
# #use "parser.ml"
# parse_permission_file FILE_NAME
```
