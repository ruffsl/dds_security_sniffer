#!/usr/bin/env python3
import argparse
import datetime
import os
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
    parser.add_argument('--data_dir', required=True)
    parser.add_argument('--recon', required=True, type=int)
    args, argv = parser.parse_known_args(argv)
    credentials_dir = Path(os.environ['ROS_SECURITY_ROOT_DIRECTORY'])
    data_dir = Path(args.data_dir)
    docker_client = docker.from_env()

    local_container_id = subprocess.check_output(
        'head -1 /proc/self/cgroup | cut -d/ -f3',
        shell=True).decode('utf8')[:12]
    local_container = docker_client.containers.get(local_container_id)
    local_config = local_container.attrs['Config']
    # local_networks = local_container.attrs['NetworkSettings']['Networks']
    # local_network = list(local_networks.values())[0]['NetworkID']
    participant_volumes = local_container.attrs['HostConfig']['Binds']
    participant_network = docker_client.networks.list(os.environ['PARTICIPANT_NETWORK'])[0]

    tshark_interface = 'br-' + participant_network.id[:12]
    # tshark_interface = 'br-' + '3a7606234e45'
    # tshark_interface = 'eth0'
   
    tshark_outfile = Path('/root').joinpath(datetime.datetime.utcnow().isoformat() + '.pcapng')
    tshark_command = 'tshark -a duration:{duration} -i {interface} -w {outfile} -F pcapng'.format(
        duration=args.recon,
        interface=tshark_interface,
        outfile=str(tshark_outfile))
    tshark_child = subprocess.Popen(shlex.split(tshark_command))
    time.sleep(5)
  

    participant_containers = []
    for root, dirs, files in os.walk(str(credentials_dir)):
        for i in dirs:
            node_ns = Path(root, i).relative_to(credentials_dir)
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
                network=participant_network.name,
                remove=True,
                tty=False,
                detach=True,
                volumes=participant_volumes,
                working_dir=local_config['WorkingDir'],
                labels={'simulation': 'participant'})
            participant_containers.append(participant_container)

        def signal_handler(sig, frame):
            tshark_child.terminate()
            trial_data_dir = data_dir.joinpath(tshark_outfile.stem)
            trial_data_file = trial_data_dir.joinpath(tshark_outfile.name)
            trial_data_dir.mkdir()
            shutil.copyfile(tshark_outfile, trial_data_file)
            data_dir_uid = os.stat(data_dir).st_uid
            data_dir_gid = os.stat(data_dir).st_gid
            os.chown(trial_data_dir, data_dir_uid, data_dir_gid)
            os.chown(trial_data_file, data_dir_uid, data_dir_gid)
            for participant_container in participant_containers:
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
