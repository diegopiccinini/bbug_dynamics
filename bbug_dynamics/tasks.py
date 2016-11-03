from .settings import Settings
from .accounts import Accounts
from .bbug import Bbug
from boto3.dynamodb.conditions import Key, Attr
import boto3, datetime, pytz

class Tasks():
    def __init__(self,settings):
        self.bbug_company_id=settings['Item']['bbug_company_id']
        self.settings = settings
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    def sync(self):
        messages = ['Synchronization started for: ' + self.bbug_company_id]
        accounts=Accounts(self.settings)
        messages+= accounts.get_from_dynamics()

        accounts_for_update = accounts.to_update()
        if len(accounts_for_update) > 0:
            messages.append('There are ' + `len(accounts_for_update)` + ' for update')

            modifiedon='2010-01-01'
            bbug = Bbug(self.settings)
            for account in accounts_for_update:
                try:
                    messages+=bbug.save_client(account)

                    # update the account in dynamo
                    my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
                    account['bbug_updated_at']=str(my_date)
                    accounts.save(account)
                except RuntimeError as err:
                    messages.append(err)

                if modifiedon < account['modifiedon']:
                    modifiedon=account['modifiedon']

            table_modifiedon = self.dynamodb.Table('dynamics_accounts_greather_modifiedon')
            table_modifiedon.put_item(Item={ 'bbug_company_id': self.bbug_company_id, 'modifiedon': modifiedon})
            messages.append('Updated the last mofied on ' + modifiedon )
        else:
            messages.append('There are no accounts to update')
        messages.append('Synchronization ended for: ' + self.bbug_company_id)
        return messages
