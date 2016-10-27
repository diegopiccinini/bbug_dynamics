import adal
from accounts import Accounts
from dynamics import Dynamics
import boto3

def adal_token(settings):
    settings = settings['Item']['dynamics']['M']
    authority_url = ('https://login.microsoftonline.com/' +
                     settings['tenant']['S'])

    RESOURCE = 'https://' + settings['web_api_resource']['S']

    context = adal.AuthenticationContext(authority_url)

    token = context.acquire_token_with_username_password(
        RESOURCE,
        settings['user']['S'],
        settings['password']['S'],
        settings['client_id']['S'])
    return token


def get_settings(bbug_company_id):
    client = boto3.client('dynamodb')
    return client.get_item(
        TableName='dynamics_settings',
        Key={ 'bbug_company_id': { 'S':  bbug_company_id }
            }
      )

def token(bbug_company_id):
    # Your code goes here!
    settings = get_settings(bbug_company_id)
    token = adal_token(settings)
    return token

