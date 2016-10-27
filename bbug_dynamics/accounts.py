import boto3, json
from .dynamics import Dynamics

class Accounts(Dynamics):

    def base_uri(self):
        return '/accounts'

    def update(self):
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

        # get all accounts modifiedon after the latest update
        self.query({'$filter': 'modifiedon gt ' + modifiedon })
        self.data=json.loads(self.response.read())
