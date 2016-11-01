from bbug_dynamics import token, get_settings, Accounts
import httplib, urllib, json
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
    accounts = init_accounts('test')
    accounts.update()
    total_test_accounts = len(accounts.data['value'])
    assert  total_test_accounts > 1
    accounts2 = init_accounts()
    accounts2.update()

    total_uk__21_accounts = len(accounts2.data['value'])
    assert total_test_accounts > total_uk__21_accounts

def test_accounts_get_from_dynamo():
    accounts = init_accounts()
    first_dynamo_account = accounts.get_from_dynamo(limit=1)
    assert len(first_dynamo_account) == 1

