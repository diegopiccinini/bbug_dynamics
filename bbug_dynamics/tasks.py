from .settings import Settings
from boto3.dynamodb.conditions import Key, Attr
import datetime
import pytz

class Tasks():
    def __init__(self,settings):
        self.bbug_company_id=settings['Item']['bbug_company_id']
        self.settings = settings

    def sync(self):
        accounts=Acconts(self.bbug_company_id)
        messages= accounts.get_from_dynamics()

        accounts_for_update = accounts.for_update()
        if accounts_for_update.count > 0:
            messages.append('There are ' + `accounts_for_update.count` + ' for update')

            my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
            modifiedon='2010-01-01'
            bbug = Bbug(self.settings)
            for account in accounts_for_update():
                messages+=bbug.save_client(account)
                if modifiedon < account['modifiedon']:
                    modifiedon=account['modifiedon']

            table_modifiedon = self.dynamodb.Table('dynamics_accounts_greather_modifiedon')
            table_modifiedon.put_item(Item={ 'bbug_company_id': self.bbug_company_id, 'modifiedon': modifiedon})
