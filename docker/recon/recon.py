#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

import docker

from construct import graph_construct

from extract import extract

from query import check_route

from recon_agent import ReconAgent


    
def detach_container(docker_client, targets_dict, network_id):
    docker_network = docker_client.networks.get(network_id)
    container_dict = {}
    for container in docker_network.containers:
        ip_address = container.attrs['NetworkSettings']['Networks'][network_id]['IPAddress']
        container_dict[ip_address] = container
    for target_name, target_ip in targets_dict.items():
        if target_ip in container_dict:
            target_container = container_dict[target_ip]
            print(f'Disconnecting {target_name}@{target_ip} from {network_id}')
            docker_network.disconnect(target_container)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True)
    parser.add_argument('--target')
    parser.add_argument('--source')
    args, argv = parser.parse_known_args(argv)
    if not args.target and not args.source:
        parser.error("Either source or target or both must be provided.")
    data_dir = Path(args.data_dir)

    docker_client =  docker.from_env()
    network_id = os.environ['PARTICIPANT_NETWORK']

    recon_agent = ReconAgent(os.environ['IMANDIRA_URL'])

    trial_data_dirs = [f for f in sorted(data_dir.iterdir()) if f.is_dir()]
    latest_trial_data_dir = trial_data_dirs[-1]
    latest_trial_data_file = list(latest_trial_data_dir.glob('*.pcapng'))[0]
    extract(fn=str(latest_trial_data_file), path=latest_trial_data_dir)
    graph_construct(path=latest_trial_data_dir)
    targets_dict = check_route(
        path=latest_trial_data_dir,
        source=args.source,
        target=args.target,
        check_func=recon_agent.instance_reachabile)
    
    targets_dict.pop(args.target, None)    
    detach_container(docker_client, targets_dict, network_id)

    #
    # is_sat = recon_agent.instance_reachabile(
    #     perms_x='/tmp/data/talker.xml',
    #     perms_y='/tmp/data/listener.xml')
    # if is_sat:
    #     print('woot!')
    # else:
    #     print('nope!')
    #
    # result = recon_agent.instance_reachabile(
    #     perms_x='/tmp/data/talker.xml',
    #     perms_y='/tmp/data/listener.xml',
    #     as_bool=False)
    # rj = result.json()
    # print(rj)
    # print(base64_str_to_str(rj['sat_example']['model']['src_base64']))


if __name__ == "__main__":
    main()
