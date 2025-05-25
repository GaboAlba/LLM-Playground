import yaml
import os

class ApiKeysHandler:
    def __init__(self, api_keys_file = "api_keys.yaml"):
        self.api_keys_default = {
            "OpenAI": "",
            "GoogleAI": ""
        }
        self.api_keys_file = api_keys_file
        self.load_api_keys()
                                                                                                                                                                                                                                                                                                        
    def load_api_keys(self):
        # Create the file if it doesn't exist
        if not os.path.exists(self.api_keys_file):
          with open(self.api_keys_file, "w") as file:
              yaml.dump(self.api_keys_default, file)
      
        with open(self.api_keys_file, "r") as file:
            self.api_keys = yaml.safe_load(file)

    def get_api_key(self, service_name):
        key = self.api_keys.get(service_name, None)
        return key if key else ""

    def set_api_key(self, service_name, api_key):
        self.api_keys[service_name] = api_key
        with open(self.api_keys_file, "w") as file:
            yaml.dump(self.api_keys, file)
    
    def are_all_api_keys_set(self):
        if self.api_keys is None:
            return False
        
        for service_name in self.api_keys.keys():
            if not self.api_keys[service_name]:
                return False
        return True