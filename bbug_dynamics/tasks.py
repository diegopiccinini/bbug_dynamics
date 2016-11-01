from .accounts import Accounts
from .bbug import Bbug

class Tasks():
    def __init__(self,bbug_company_id):
        self.settings = get_settings(bbug_company_id)

