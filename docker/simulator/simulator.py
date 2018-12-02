#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
import docker


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True)
    args = parser.parse_args(argv)
    docker_client = docker.from_env()
    local_container_id = os.environ['HOSTNAME']
    local_container = docker_client.containers.get(local_container_id)
    local_config = local_container.attrs['Config']

    p = Path(args.dir)
    for i in p.glob('**/*'):
        print(i.name)


if __name__ == "__main__":
    main()
