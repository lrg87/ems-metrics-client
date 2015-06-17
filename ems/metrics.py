# coding=utf-8
import urllib
import socket
import datetime
import functools

__author__ = 'xuemingli'


class MetricsClient(object):

    """Metrics client object
    """
    def __init__(self, appid=None, host='127.0.0.1', port=1800):

        """initialization metric client

        :param appid: app id, if you not set, when you send metrics, you mus be give it
        :param host: ems-collector host, default is '127.0.0.1',
        :param port: ems-collector port, default is 1800
        :return: Nothing
        """
        self.appid = appid
        self.host = host
        self.port = port

    def _build(self, name, tp, val, tags):
        if tp not in ("t", "c"):
            raise ValueError("type must be c or t")
        if tp == 'c':
            if not isinstance(val, int):
                raise ValueError("count must be int")
        if tp == 't':
            if not (isinstance(val, int) or isinstance(val, float)):
                raise ValueError("timing must be number")
        return "{0}?{1}:{2}|{3}".format(name, urllib.urlencode(tags), val, tp)

    def _send(self, name, tp, val, tags):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = self._build(name, tp, val, tags)
        sock.sendto(message, (self.host, self.port))

    def _set_app_id(self, tags=None):
        if tags is None:
            if self.appid is None:
                raise ValueError("appid is require")
            return {'appid': self.appid}
        elif 'appid' not in tags.keys():
            if self.appid is None:
                raise ValueError("appid is require")
            tags['appid'] = self.appid
            return tags
        return tags

    def set(self, name, count=0, tags=None):

        """send a count metrics with name

        :param name: metrics name
        :param count: metrics value
        :param tags: additional information, if you not define app_id at initialization, you must define at here
        :return: Nothing
        """
        tags = self._set_app_id(tags)
        self._send(name, 'c', count, tags)

    def timing(self, name, val=0.0, tags=None):

        """send a timing metrics with name
        :param name: metrics name
        :param val: metrics value
        :param tags: additional information, if you not define app_id at initialization, you must define at here
        :return: Nothing
        """
        tags = self._set_app_id(tags)
        self._send(name, 't', val, tags)


class Timer(object):

    """timing metrics helper
    example:

        @Timer(client)
        def fn():
            ...
            ...

    or like this

        with Timer(client, name='xxxx'):
            ....
            ....
    """
    def __init__(self, client, name=None, tags=None):
        
        """initialization Timer

        :param client: instance of MetricsClient
        :param name: metrics name, as decorator, name can be None, it where use full name of function
        :param tags: additional information
        :return: Nothing
        """
        self.client = client
        self.name = name
        self.tags = tags

    def __enter__(self):
        self.start = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        t = (datetime.datetime.now() - self.start).total_seconds()
        if self.name is None:
            raise ValueError("name is require")
        self.client.timing(self.name, t, self.tags)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            if self.name is None:
                self.name = "{0}.{1}".format(func.__module__, func.__name__)
            start = datetime.datetime.now()
            try:
                ret_val = func(*args, **kwargs)
            finally:
                t = (datetime.datetime.now() - start).total_seconds()
                self.client.timing(self.name, t, self.tags)
            return ret_val
        return _wrapped

if __name__ == '__main__':
    import time
    client = MetricsClient(appid='test')
    client.set("count_test", 5)
    client.timing("timing_test", 35.6)

    @Timer(client)
    def slow():
        time.sleep(1)

    slow()

    with Timer(client, name="with_timing_test"):
        time.sleep(2)


