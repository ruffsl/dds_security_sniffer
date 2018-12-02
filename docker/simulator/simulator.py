#!/usr/bin/env python3
import argparse
import datetime
import os
import pwd
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path


import docker


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True)
    parser.add_argument('--recon', required=True, type=int)
    args, argv = parser.parse_known_args(argv)
    dir = Path(args.dir)
    docker_client = docker.from_env()

    local_container_id = subprocess.check_output(
        'head -1 /proc/self/cgroup | cut -d/ -f3',
        shell=True).decode('utf8')[:12]
    local_container = docker_client.containers.get(local_container_id)
    local_config = local_container.attrs['Config']
    local_networks = local_container.attrs['NetworkSettings']['Networks']
    local_network = list(local_networks.values())[0]['NetworkID']
    local_volumes = local_container.attrs['HostConfig']['Binds']

    # tshark_interface = 'br-' + local_network[:12]
    # tshark_interface = 'br-' + '3a7606234e45'
    # tshark_outfile = Path('/root').joinpath(datetime.datetime.utcnow().isoformat() + '.pcapng')
    # tshark_command = 'tshark -a duration:{duration} -i {interface} -w {outfile} -F pcapng'.format(
    #     duration=args.recon,
    #     interface=tshark_interface,
    #     outfile=str(tshark_outfile))
    # tshark_child = subprocess.Popen(shlex.split(tshark_command))
    # time.sleep(5)

    participant_containers = []
    for root, dirs, files in os.walk(str(dir)):
        for i in dirs:
            node_ns = Path(root, i).relative_to(dir)
            participant_command = './participant.py ' + \
                ' '.join(argv) + \
                ' __ns:=' + '/' + str(node_ns.parent).rstrip('.') + \
                ' __node:=' + str(node_ns.name)
            print('command: ', participant_command)
            participant_name = local_container.attrs['Name'].lstrip('/') + \
                str(node_ns).replace('/', '.')
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
                working_dir=local_config['WorkingDir'])
            participant_containers.append(participant_container)

        def signal_handler(sig, frame):
            for participant_container in participant_containers:
                # tshark_child.terminate()
                # shutil.copyfile(tshark_outfile, str(dir.joinpath(tshark_outfile.name)))
                print('Killing: {}'.format(
                    participant_container.attrs['Name']))
                participant_container.kill()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGALRM, signal_handler)
        print('Press Ctrl+C')
        signal.alarm(args.recon)
        signal.pause()
        sys.exit(0)


if __name__ == "__main__":
    main()
