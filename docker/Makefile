all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build image"
	@echo "   2. make pull             - pull image"
	@echo "   3. make clean            - remove image"
	@echo "   3. make run              - run images"
	@echo ""

build:
	@docker build --tag=ruffsl/dds-recon:latest	.

pull:
	@docker pull ruffsl/dds-recon:latest

clean:
	@docker rmi -f ruffsl/dds-recon:latest

run:
	@docker run -it --rm -v ${HOME}/.imandra:/home/opam/.imandra -p 8000:8000 ruffsl/dds-recon:latest

bash:
	@docker run -it --rm -v ${HOME}/.imandra:/home/opam/.imandra -p 8000:8000 ruffsl/dds-recon:latest bash
