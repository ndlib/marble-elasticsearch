import json


class DeployConfig:
    def __init__(self):
        try:
            print('init')
            with open('../deploy.json') as json_file:
                self.config = json.load(json_file)
        except EnvironmentError:
            self.config = None
            print('Unable to load deploy config')

    def get_stackname(self):
        return self.config['stackname']
