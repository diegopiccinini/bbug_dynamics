import boto3, json
from .dynamics import Dynamics
from boto3.dynamodb.conditions import Key, Attr

class Accounts(Dynamics):

    def base_uri(self):
        return '/accounts'


    def update(self, param_modifiedon=''):
        """Update all the accounts with modifiedon greather than the latest
        modifiedon updated account. To change the defuault filter can use the
        param_modfiedon.

        Args:
            self (Accounts): Instance of Accounts.
            param_modifiedon (str): By defualt is an empty str, only used to
            force a modifiedon date.
        """
        # get in dynamo the date of latest update
        client = boto3.client('dynamodb')
        last_update=client.get_item(TableName='dynamics_accounts_greather_modifiedon',
                                    Key={ 'bbug_company_id':  { 'S': self.bbug_company_id }
                                        }
                                   )
        if 'Item' in last_update:
            modifiedon=last_update['Item']['modifiedon']['S']
        else:
            modifiedon='2000-01-01'

        # update all accounts greather than a param_modifiedon
        if param_modifiedon!='':
            modifiedon=param_modifiedon

        # get all accounts modifiedon after the latest update
        self.query({'$filter': 'modifiedon gt ' + modifiedon })
        self.data=json.loads(self.response.read())

    def get_from_dynamo(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('dynamics_accounts')
        response=table.query( KeyConditionExpression= Key('bbug_company_id').eq( self.bbug_company_id))
        return response['Items']
