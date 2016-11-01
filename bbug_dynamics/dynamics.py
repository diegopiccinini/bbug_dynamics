import httplib, urllib, json, boto3
from io import StringIO

class Dynamics:
    def __init__(self,token, settings):
        self.bbug_company_id = settings['Item']['bbug_company_id']['S']
        settings = settings['Item']['dynamics']['M']
        self._token= token
        self._settings=settings
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    def query(self, params={}):
        params = urllib.urlencode(params)
        if params!='' :
            params = '?' + params

        headers = { 'Authorization': 'Bearer ' + self._token['accessToken'],
                   'Content-Type': 'application/json; charset=utf-8',
                   'Accept': 'application/json',
                   'OData-Version': 4.0
                  }
        conn= httplib.HTTPSConnection(self._settings['web_api_resource']['S'])
        request_uri = self._settings['canonical_api_uri']['S'] + self.base_uri() + params
        conn.request('GET',request_uri,'', headers )
        self.response= conn.getresponse()

    def base_uri(self):
        return '/'

    def process_response(self):
        if self.response.status == 200:
            d = self.response.read()
            data=json.loads(d)
            return data['value']
        else:
            raise "Cannot get dynamics entities"
