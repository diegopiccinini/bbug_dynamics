from bbug_dynamics import token, get_settings, Accounts
import httplib, urllib, json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def init_accounts():
    t = token('uk__21')
    settings = get_settings('uk__21')
    return Accounts(t,settings)

def test_all_accounts_status():
    accounts = init_accounts()
    r = accounts.query()
    assert r.status == 200

def test_accounts_data():
    accounts = init_accounts()
    r = accounts.query()
    assert len(accounts.process_response(r)) > 1

def test_accounts_query():
    accounts = init_accounts()
    date_after_month = datetime.today() + relativedelta(months=1)
    r = accounts.query({ '$filter': 'modifiedon gt ' +
                        date_after_month.strftime('%Y-%m-%d') })
    assert len(accounts.process_response(r)) == 0
