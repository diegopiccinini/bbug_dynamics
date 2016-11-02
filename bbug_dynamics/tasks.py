from .accounts import Accounts
from .bbug import Bbug

class Tasks():
    def __init__(self,bbug_company_id):
        self.settings = get_settings(bbug_company_id)

    def sync(self):

        table=self.dynamodb.Table('dynamics_accounts')

        for account in self.data['value']:
            account['bbug_company_id']=self.bbug_company_id
            for k in account.keys():
                if isinstance(account[k] , float):
                    account[k]=Decimal(str(account[k]))
            table.put_item(Item=account)
            if modifiedon < account['modifiedon']:
                modifiedon=account['modifiedon']
        table_modifiedon.put_item(Item={ 'bbug_company_id': self.bbug_company_id, 'modifiedon': modifiedon})
