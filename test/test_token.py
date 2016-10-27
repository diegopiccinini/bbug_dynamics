from bbug_dynamics import token

def test_token():
    t = token('uk__21')
    assert('accessToken' in t)

