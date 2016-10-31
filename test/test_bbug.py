from bbug_dynamics import get_settings, Bbug

def init_bbug(bbug_company_id = 'uk__21'):
    settings = get_settings(bbug_company_id)
    return Bbug(settings)

def test_init():
    bbug =init_bbug()
    assert(bbug.response.status_code == 201)
