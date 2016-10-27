from .dynamics import Dynamics

class Accounts(Dynamics):

    def base_uri(self):
        return '/accounts'

    def get_from_dynamics(self,without_date=False):
        if without_date:
            response = self.query()
        else:
#TODO
        client = boto3.client('dynamodb')
        client.get_item(
        TableName='dynamics_settings',
        Key={ 'bbug_company_id': { 'S':  bbug_company_id }
            }
      )
            response = self.query({'$filter','modifiedon gt ' + modifiedon})
