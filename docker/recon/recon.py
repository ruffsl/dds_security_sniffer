#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

from construct import graph_construct

from extract import extract

from query import check_route

from recon_agent import ReconAgent


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--source', required=True)
    args, argv = parser.parse_known_args(argv)
    data_dir = Path(args.data_dir)

    recon_agent = ReconAgent(os.environ['IMANDIRA_URL'])

    trial_data_dirs = [f for f in sorted(data_dir.iterdir()) if f.is_dir()]
    latest_trial_data_dir = trial_data_dirs[-1]
    latest_trial_data_file = list(latest_trial_data_dir.glob('*.pcapng'))[0]
    extract(fn=str(latest_trial_data_file), path=latest_trial_data_dir)
    graph_construct(path=latest_trial_data_dir)
    check_route(
        path=latest_trial_data_dir,
        source=args.source,
        target=args.target,
        check_func=recon_agent.instance_reachabile)

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
