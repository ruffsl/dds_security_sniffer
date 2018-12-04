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
