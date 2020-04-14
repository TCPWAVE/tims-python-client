import requests
import json
from requests.auth import HTTPBasicAuth
from requests import Session
from _collections import defaultdict
from client import (APICallFailedException, UnsupportedMethodException)


class Connector(object):
    """
        Class to handle connection to Tcpwave's IPAM
    """
    def __init__(self, cert=None, key=None, user=None, password=None, verify=False):
        """
        creates connector object either with client certificates or with client credentials
        :param cert:
        :param key:
        :param user:
        :param password:
        :param verify:
        """
        self.session = Session()
        if cert is not None or key is not None:
            self.session.cert = (cert, key)
        elif user is not None and password is not None:
            self.session.auth = HTTPBasicAuth(user, password)
        else:
            raise Exception("Missing certificates or user credentials")

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.verify = verify
        self.url = "https://%s:7443/tims/rest%s"

    def __construct_url(self, server, rel_url):
        self.url = str(self.url) % (server, rel_url)

    def get_object(self, payload):
        """
        Make GET call
        :param payload:
        :return:
        """
        if '%s' in self.url:
            self.__construct_url(payload['provider']['host'], payload['rel_url'])
        rsp = self.session.get(url=self.url, headers=payload.get('headers'), params=payload.get('params'))
        status_code = rsp.status_code
        if status_code == 200:
            if len(rsp.content):
                try:
                    data = rsp.json()
                except Exception:
                    data = rsp.content
                return data
        else:
            raise APICallFailedException("API call failed. Msg :: "+str(rsp.content.decode("utf-8")))

    def create_object(self, payload):
        """
        Make PUT/POST call to create/update object
        :param payload:
        :return:
        """
        method = payload['method']
        if method not in ["PUT", "POST"]:
            raise UnsupportedMethodException("method %s not supported" % method)

        if '%s' in self.url:
            self.__construct_url(payload['provider']['host'], payload['rel_url'])

        if method == "POST":
            rsp = self.session.post(url=self.url, headers=payload.get('headers'), params=payload.get('params'),
                                    data=json.dumps(payload.get('body')))
        else:
            rsp = self.session.put(url=self.url, headers=payload.get('headers'), params=payload.get('params'),
                                   data=json.dumps(payload.get('body')))

        status_code = rsp.status_code
        if status_code == 200 or status_code == 201:
            if len(rsp.content):
                return rsp.json()
            else:
                return '{"msg": "Successful"}'
        else:
            raise APICallFailedException("API call failed. Msg :: "+str(rsp.content.decode("utf-8")))

    def delete_object(self, payload):
        """
        Make DELETE call to remove object.
        :param payload:
        :return:
        """
        if '%s' in self.url:
            self.__construct_url(payload['provider']['host'], payload['rel_url'])

        method = payload['method']
        if method not in ["POST", "DELETE"]:
            raise UnsupportedMethodException("method %s not supported" % method)

        if method == "POST":
            rsp = self.session.post(url=self.url, headers=payload.get('headers'), params=payload.get('params'),
                                    data=json.dumps(payload.get('body')))
        else:
            rsp = self.session.delete(url=self.url, headers=payload.get('headers'), params=payload.get('params'),
                                      data=json.dumps(payload.get('body')))

        status_code = rsp.status_code
        if status_code == 200:
            if len(rsp.content):
                return rsp.json()
            else:
                return '{"msg": "Successful"}'
        else:
            raise APICallFailedException("API call failed. Msg :: "+str(rsp.content.decode("utf-8")))
