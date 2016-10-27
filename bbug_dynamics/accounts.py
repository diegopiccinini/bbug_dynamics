from .dynamics import Dynamics

class Accounts(Dynamics):

    def base_uri(self):
        return '/accounts'

    def update(self):
        # get in dynamo the date of latest update
        client = boto3.client('dynamodb')
        last_update=client.get_item(TableName='dynamics_accounts_greather_modifiedon',
                                    Key={ 'bbug_company_id':  self.bbug_company_id }
                                   )
        if 'Item' in last_update:
            modifiedon=last_update['Item']['modifiedon']
        else:
            modifiedon='2000-01-01'

        # get all accounts modifiedon after the latest update
        response = self.query({'$filter','modifiedon gt ' + modifiedon})

