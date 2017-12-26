import requests
from django.conf import settings

class VKads:
    def __init__(self, user):
        self.url = settings.VK_BASE_URL
        self.params = {
            'access_token':user.credentials.token,
            'account_id': user.credentials.account_id
        }

    def get_target_groups(self):
        method = 'ads.getTargetGroups'
        group = requests.get(self.url.format(method), params=self.params)
        return group.json()["response"]

    def create_target_group(self, name):
        method = 'ads.createTargetGroup'
        self.params['name'] = name
        group = requests.get(self.url.format(method), params = self.params)
        return group.json()['response']['id']

    def import_target_contacts(self, group_id, contacts):
        method = 'ads.importTargetContacts'
        self.params['target_group_id'] = group_id
        self.params['contacts'] = contacts
        group = requests.get(self.url.format(method), params=self.params)
        return group.json()