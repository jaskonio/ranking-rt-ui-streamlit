import requests

class RequestServices():

    def send_request(self, method, url, headers=None, data=None, json=None, timeout=60):
        return requests.request(method, url, headers=headers, data=data, json= json, timeout=timeout)

    def get(self, url, headers=None, data=None, json=None, timeout=60):
        return self.send_request('GET', url, headers, data, json, timeout)

    def post(self, url, headers=None, data=None, json=None, timeout=60):
        return self.send_request('POST', url, headers, data, json, timeout)

    def put(self, url, headers=None, data=None, json=None, timeout=60):
        return self.send_request('PUT', url, headers, data, json, timeout)

    def delete(self, url, headers=None, data=None, json=None, timeout=60):
        return self.send_request('DELETE', url, headers, data, json, timeout)
