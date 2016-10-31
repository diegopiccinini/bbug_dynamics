import urlparse, requests

class Bbug():
    def __init__(self, settings):

        bbug_company_id = settings['Item']['bbug_company_id']['S']
        bbug_ids = bbug_company_id.split('__')
        settings=settings['Item']['bbug_app']['M']

        url = settings['admin_endpoint']['S'] +  '/login/admin/'+ bbug_ids[1]


        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n" +  settings['email']['S'] + "\r\n-----011000010111000001101001\r\n Content-Disposition: form-data; name=\"password\"\r\n\r\n" + settings['password']['S'] + "\r\n-----011000010111000001101001--"

        headers = {
                   'content-type': "multipart/form-data; boundary=---011000010111000001101001",
                    'app-id': settings['app_id']['S'],
                    'cache-control': "no-cache"
                    }

        response = requests.request("POST", url, data=payload,
                                            headers=headers)

        self.response= response


