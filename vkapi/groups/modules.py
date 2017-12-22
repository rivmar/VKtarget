import requests
from django.conf import settings

class VK:
    def __init__(self):
        self.url = settings.VK_BASE_URL
        self.params = {
            'access_token':settings.VK_ACCOUNT_ID,
            'account_id': settings.VK_ACCOUNT_ID
        }

    def get_target_groups(self):
        method = 'ads.getTargetGroups'
        group = requests.get(self.url.format(method), params=self.params)
        return group

    def create_target_group(self, name, file):
        method = 'ads.createTargetGroup'
        self.params['name'] = name
        group = requests.get(self.url.format(method), params = self.params)
        return group

    def import_target_contacts(self, group_id, contacts):
        method = 'ads.importTargetContacts'
        self.params['target_group_id'] = group_id
        self.params['contects'] = contacts
        group = requests.get(self.url.format(method), params=self.params)
        return group