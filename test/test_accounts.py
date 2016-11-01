from bbug_dynamics import token, get_settings, Accounts
import httplib, urllib, json, boto3
from datetime import datetime
from dateutil.relativedelta import relativedelta

def init_accounts(bbug_company_id = 'uk__21'):
    t = token(bbug_company_id)
    settings = get_settings(bbug_company_id)
    return Accounts(t,settings)

def test_all_accounts_status():
    accounts = init_accounts()
    accounts.query()
    assert accounts.response.status == 200

def test_accounts_data():
    accounts = init_accounts()
    accounts.query()
    assert len(accounts.process_response()) > 1

def test_accounts_query():
    accounts = init_accounts()
    date_after_month = datetime.today() + relativedelta(months=1)
    accounts.query({ '$filter': 'modifiedon gt ' +
                        date_after_month.strftime('%Y-%m-%d') })
    assert len(accounts.process_response()) == 0

def test_acounts_update():
    # reset date in test account
    table_modifiedon=boto3.resource('dynamodb').Table('dynamics_accounts_greather_modifiedon')
    table_modifiedon.put_item(Item={ 'bbug_company_id': 'test', 'modifiedon':
                                    '2010-01-01'})

    accounts = init_accounts('test')
    accounts.update()
    total_test = len(accounts.data['value'])
    assert  total_test > 1
    accounts2 = init_accounts('localhost__37000')
    accounts2.update()

    total_local = len(accounts2.data['value'])
    assert total_test > total_local

def test_accounts_get_from_dynamo():
    accounts = init_accounts()
    first_dynamo_account = accounts.get_from_dynamo(limit=1)
    assert len(first_dynamo_account) == 1

