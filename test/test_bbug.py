from bbug_dynamics import get_settings, Bbug
from test_accounts import init_accounts

def init_bbug(bbug_company_id = 'uk__21'):
    settings = get_settings(bbug_company_id)
    return Bbug(settings)

def test_init():
    bbug =init_bbug()
    assert(bbug.response.status_code == 201)

def test_save_client():
    accounts = init_accounts('uk__21')
    accounts_from_dynamo = accounts.get_from_dynamo()
    bbug =init_bbug()
    for x in accounts_from_dynamo:
        bbug.save_client(x)
        print "status " + `bbug.response.status_code` + " for accountid: " + x['accountid']
        assert(bbug.response.status_code in [200,404])
        assert(bbug.bbug_response.status_code in [200,404])


