import httplib, urllib, json

class Dynamics:
    def __init__(self,token, settings):
        self.bbug_company_id = settings['Item']['bbug_company_id']['S']
        settings = settings['Item']['dynamics']['M']
        self._token= token
        self._settings=settings

    def query(self, params={}):
        params = urllib.urlencode(params)
        if params!='' :
            params = '?' + params
        headers = { "Authorization": 'Bearer ' + self._token['accessToken'] }
        conn= httplib.HTTPSConnection(self._settings['web_api_resource']['S'])
        request_uri = self._settings['canonical_api_uri']['S'] + self.base_uri() + params
        conn.request('GET',request_uri,'', headers )
        return conn.getresponse()

    def base_uri(self):
        return '/'

    def process_response(self, response):
        if response.status == 200:
            data = response.read()
            data=json.loads(data)
            return data['value']
        else:
            raise "Cannot get dynamics entities"
