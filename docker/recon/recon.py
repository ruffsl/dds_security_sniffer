#!/usr/bin/env python3
import argparse
import os
import sys

from construct import graph_construct
from extract import extract

from query import check_route

from recon_agent import ReconAgent


def main(argv=sys.argv[1:]):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--dir', required=True)
    # parser.add_argument('--target', required=True)
    # args, argv = parser.parse_known_args(argv)

    recon_agent = ReconAgent(os.environ['IMANDIRA_URL'])
    is_sat = recon_agent._instance(
        data='fun x -> ((x = 3) && (x = 1))',
        data_type='src')
    if is_sat:
        print('woot!')
    else:
        print('nope!')

    is_sat = recon_agent.instance_reachabile(
        perms_x='/tmp/data/talker.xml',
        perms_y='/tmp/data/listener.xml')
    if is_sat:
        print('woot!')
    else:
        print('nope!')

    result = recon_agent.instance_reachabile(
        perms_x='/tmp/data/talker.xml',
        perms_y='/tmp/data/listener.xml',
        as_bool=False)
    rj = result.json()
    print(rj)
    print(base64_str_to_str(rj['sat_example']['model']['src_base64']))


if __name__ == "__main__":
    main()
