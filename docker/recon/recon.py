#!/usr/bin/env python3
import argparse
import base64
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


class ImandraClient:
    def __init__(self, base_url):
        self._base_url = base_url

    def _init(self, timout=10, cooldown=1):
        def handler(signum, frame):
            raise Exception("init timeout")

        # signal.signal(signal.SIGALRM, handler)
        # signal.alarm(timout)
        while True:
            result = self._send_request('/status')
            if result.status_code == 200:
                break
            time.sleep(cooldown)

    def _eval(self, input, type='src'):
        if type == 'src':
            data = {'src_base64': str_to_base64_str(input)}
        elif type == 'name':
            data = {'name': input}
        result = self._send_request(
            suffix='/eval/by-' + type,
            data=data)
        rj = result.json()
        return rj

    def _verify(self, input, type='src'):
        if type == 'src':
            data = {'src_base64': str_to_base64_str(input)}
        elif type == 'name':
            data = {'name': input}
        result = self._send_request(
            suffix='/verify/by-' + type,
            data=data)
        rj = result.json()
        # return rj
        if rj['result'] == 'proved':
            return True
        elif rj['result'] == 'refuted':
            return False

    def _instance(self, input, type='src'):
        if type == 'src':
            data = {'src_base64': str_to_base64_str(input)}
        elif type == 'name':
            data = {'name': input}
        result = self._send_request(
            suffix='/instance/by-' + type,
            data=data)
        return result
        rj = result.json()
        return rj
        if rj['result'] == 'sat':
            return True
        elif rj['result'] == 'unsat':
            return False

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
        super()._init(self)
        self._eval(input='#redef true;;', type='src')
        self._eval(input='#use "reachability.ml";;', type='src')

    def instance_reachabile(self, perms_x, perms_y):
        self._eval(input='#program;;', type='src')
        self._eval(
            input='let perms_x = parse_permission_file "{}";;'.format(perms_x),
            type='src')
        self._eval(
            input='let perms_y = parse_permission_file {}'.format(perms_y),
            type='src')
        self._eval(input='#logic;;', type='src')
        return self._instance(input='reachable', type='name')


def main(argv=sys.argv[1:]):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--dir', required=True)
    # parser.add_argument('--target', required=True)
    # args, argv = parser.parse_known_args(argv)

    recon_agent = ReconAgent(os.environ['IMANDIRA_URL'])
    result = recon_agent.instance_reachabile(
        perms_x='/tmp/data/talker.xml',
        perms_y='/tmp/data/listener.xml')
    rj = result.json()
    print(base64_str_to_str(rj['sat_example']['model']['src_base64']))


if __name__ == "__main__":
    main()
