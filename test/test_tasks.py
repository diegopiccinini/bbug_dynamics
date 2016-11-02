from bbug_dynamics import Settings,Tasks

def test_sync():
    settings = Settings('localhost__37000').settings
    task = Tasks(settings)
