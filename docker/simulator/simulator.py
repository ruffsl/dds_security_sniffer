#!/usr/bin/env python3
import argparse
import os
import signal
import sys
from pathlib import Path


import docker


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True)
    args, argv = parser.parse_known_args(argv)
    docker_client = docker.from_env()

    local_container_id = os.environ['HOSTNAME']
    local_container = docker_client.containers.get(local_container_id)
    local_config = local_container.attrs['Config']
    local_networks = local_container.attrs['NetworkSettings']['Networks']
    local_network = list(local_networks.values())[0]['NetworkID']
    local_volumes = local_container.attrs['HostConfig']['Binds']

    p = Path(args.dir)
    participant_containers = []
    for i in p.glob('**/*'):
        node_ns = i.relative_to(p)
        participant_command = './participant.py ' + \
            ' '.join(argv) + \
            ' __ns:=' + '/' + str(node_ns.parent).rstrip('.') + \
            ' __node:=' + str(node_ns.name)
        print('command: ', participant_command)
        participant_name = local_container.attrs['Name'].lstrip('/') + \
            str(i).replace('/', '_')
        participant_container = docker_client.containers.run(
            image=local_config['Image'],
            command=participant_command,
            environment=local_config['Env'],
            name=participant_name,
            network=local_network,
            remove=True,
            tty=False,
            detach=True,
            volumes=local_volumes,
            working_dir=local_config['WorkingDir'],
        )
        print(participant_container)
        participant_containers.append(participant_container)

    def signal_handler(sig, frame):
        for participant_container in participant_containers:
            print('Killing: {}'.format(
                participant_container.attrs['Name']))
            participant_container.kill()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()
    sys.exit(0)


if __name__ == "__main__":
    main()
