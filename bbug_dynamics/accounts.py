import json
from .dynamics import Dynamics
from .bbug import Bbug
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

class Accounts(Dynamics):

    def base_uri(self):
        return '/accounts'


    def get_from_dynamics(self, param_modifiedon=''):
        """Get all the accounts with modifiedon greather than the latest
        modifiedon updated account. To change the defuault filter can use the
        param_modfiedon.

        Args:
            self (Accounts): Instance of Accounts.
            param_modifiedon (str): By defualt is an empty str, only used to
            force a modifiedon date.
        """
        # get in dynamo the date of latest update
        table_modifiedon = self.dynamodb.Table('dynamics_accounts_greather_modifiedon')

        try:
            last_update=table_modifiedon.get_item( Key={ 'bbug_company_id':
                                                        self.bbug_company_id })
            modifiedon=last_update['Item']['modifiedon']
        except:
            modifiedon='2000-01-01'

        # update all accounts greather than a param_modifiedon
        if param_modifiedon!='':
            modifiedon=param_modifiedon

        # get all accounts modifiedon after the latest update
        self.query({'$filter': 'modifiedon gt ' + modifiedon })
        self.data=json.loads(self.response.read())


    def get_from_dynamo(self, limit = 100 ):
        table = self.dynamodb.Table('dynamics_accounts')
        response=table.query( KeyConditionExpression=
                             Key('bbug_company_id').eq(
                                 self.bbug_company_id), Limit=limit)
        return response['Items']
