import simplejson as json


class SemEvalDataSet:

    def __init__(self, action_kb_file):
        self.action_kb = dict()

        with open(action_kb_file) as f:
            original_kb = json.load(f)

        for action in original_kb:
            provider = action['more'].get('provider') if 'more' in action else None
            provider = provider.lower().replace(' ', '_') if provider is not None else None
            name = action['name'].lower().replace(' ', '_')
            id = action['id']

            if provider is not None:
                if provider not in self.action_kb:
                    self.action_kb[provider] = dict()

                self.action_kb[provider][name] = id

    def get_action_id(self, provider, name):
        return self.action_kb[provider.lower()].get(name.lower()) if provider.lower() in self.action_kb else None