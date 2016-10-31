import urlparse, requests, json

class Bbug():
    def __init__(self, settings):

        bbug_ids = settings['Item']['bbug_company_id']['S'].split('__')
        self.company_id=bbug_ids[1]
        settings=settings['Item']['bbug_app']['M']

        url = settings['admin_endpoint']['S'] +  '/login/admin/'+ self.company_id
        self.url = settings['admin_endpoint']['S'] +  '/admin/'+ self.company_id


        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n" +  settings['email']['S'] + "\r\n-----011000010111000001101001\r\n Content-Disposition: form-data; name=\"password\"\r\n\r\n" + settings['password']['S'] + "\r\n-----011000010111000001101001--"

        headers = {
                   'content-type': "multipart/form-data; boundary=---011000010111000001101001",
                    'App-Id': settings['app_id']['S'],
                    'cache-control': "no-cache"
                    }

        self.response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(self.response.text)
        headers['auth-token']= data['auth_token']
        self.headers = headers


    def update_client(self,account):
        headers=self.headers
        headers['content-type']='application/json; charset=utf-8'
        self.response = requests.request("GET",self.url + '/client/find_by_ref/' + account['accountid'],
                             headers=headers )



