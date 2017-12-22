import requests
from django.conf import settings
import pprint

pp = pprint.PrettyPrinter(indent=4)

class VKads:
    def __init__(self):
        self.url = settings.VK_BASE_URL
        self.params = {
            'access_token':settings.VK_ACCESS_TOKEN,
            'account_id': settings.VK_ACCOUNT_ID
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
        print(group_id)
        method = 'ads.importTargetContacts'
        self.params['target_group_id'] = group_id
        self.params['contacts'] = contacts
        group = requests.get(self.url.format(method), params=self.params)
        pp.pprint(group.json())
        return group.json()