#!/usr/bin/env python3
import argparse
import base64
import functools
import os
import requests
import signal
import sys
import time
import urllib


def str_to_base64_str(string):
    return base64.urlsafe_b64encode(
        string.encode('utf8')
    ).decode('utf-8')


def base64_str_to_str(string):
    return base64.urlsafe_b64decode(
        string.encode('utf8')
    ).decode('utf-8')


def data_decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(self, data, data_type='src', **kwargs):
        if data_type == 'src':
            data = {'src_base64': str_to_base64_str(data)}
        elif data_type == 'name':
            data = {'name': data}
        return func(self, data, data_type, **kwargs)
    return wrapper_decorator


class ImandraClient:
    def __init__(self, base_url):
        self._base_url = base_url

    def _init(self, timout=10, cooldown=1):
        for i in range(timout):
            try:
                result = self._send_request('/status')
                if result.status_code == 200:
                    return True
            except Exception as err:
                time.sleep(cooldown)
        return False

    @data_decorator
    def _eval(self, data, data_type, as_bool=True):
        result = self._send_request(
            suffix='/eval/by-' + data_type,
            data=data)
        if as_bool:
            if result.status_code == 200:
                return True
            else:
                return False
        return result

    @data_decorator
    def _verify(self, data, data_type, as_bool=True):
        result = self._send_request(
            suffix='/verify/by-' + data_type,
            data=data)
        if as_bool:
            rj = result.json()
            if rj['result'] == 'proved':
                return True
            elif rj['result'] == 'refuted':
                return False
            else:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))
        return result

    @data_decorator
    def _instance(self, data, data_type, as_bool=True):
        result = self._send_request(
            suffix='/instance/by-' + data_type,
            data=data)
        if as_bool:
            rj = result.json()
            if rj['result'] == 'sat':
                return True
            elif rj['result'] == 'unsat':
                return False
            else:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))
        return result

    def _send_request(self, suffix, data=None):
        url = urllib.parse.urljoin(self._base_url, suffix)

        try:
            if data is not None:
                result = requests.post(url, json=data)
            else:
                result = requests.get(url)

            # if result.status_code != 200:
            #     raise Exception("Error {}: {}".format(
            #         result.status_code, result.reason))
            #
            # elif not result.ok:
            #     raise Exception("Error {}: {}".format(
            #         result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise Exception(err)

        return result


class ReconAgent(ImandraClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self._config()

    def _config(self):
        super()._init()
        self._eval(data='#redef true')
        self._eval(data='#use "reachability.ml"')

    def instance_reachabile(self, perms_x, perms_y, as_bool=True):
        self._eval(
            data=f'#program;; let perms_x = parse_permission_file "{perms_x}"')
        self._eval(
            data=f'#program;; let perms_y = parse_permission_file "{perms_y}"')
        return self._instance(
            data='reachable',
            data_type='name',
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
