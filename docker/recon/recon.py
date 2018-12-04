#!/usr/bin/env python3
import argparse
import os
import sys

from imandra_client import ImandraClient
from imandra_client import base64_str_to_str


class ReconAgent(ImandraClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self._config()

    def _config(self):
        super()._init()
        self._eval(data='#redef true')
        self._eval(data='#use "reachability.ml"')
        self._eval(data='Genpp.eval()')
        self._eval(data='''
let reflect_permission_into_logic name value = Pconfig.(with_mode_assigned ~to_:State.Logic
   Imandra.eval_string (Printf.sprintf "let %s = %s" name @@ Pp.pp_permissions value)) [@@program] 
''')

    def instance_reachabile(self, perms_x, perms_y, as_bool=True):
        self._eval(
            data='let perms_x = parse_permission_file "{}" [@@program]'.format(perms_x))
        self._eval(
            data='let perms_y = parse_permission_file "{}" [@@program]'.format(perms_y))
        self._eval(
            data='reflect_permission_into_logic "perms_x" perms_x [@@program]')
        self._eval(
            data='reflect_permission_into_logic "perms_y" perms_y [@@program]')
        return self._instance(
            data='fun x y -> reachable x perms_x y perms_y',
            data_type='src',
            as_bool=as_bool)


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
