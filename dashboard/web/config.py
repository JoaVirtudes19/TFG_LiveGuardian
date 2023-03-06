import json
### Manage configs

class AppConfig():
    
    def __init__(self) -> None:
        ### First load
        with open('config.json') as f:
            self.data = json.load(f)
        
    
    def get_config(self,key):
        return self.data[key]

    def set_config(self,key,value):
        self.data[key] = value
        with open('config.json','w') as f:
            json.dump(self.data,f)


global_config = AppConfig()