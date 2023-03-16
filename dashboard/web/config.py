import json
### Manage config

DEFAULT = {"framesToDetector": 3, "token": "5282233910:AAG_mddkn8zdw_Iip-n1zQX_gSURiBLomC0", "historySize": 40, "historySizeToDetect": 10}

class AppConfig():
    
    def __init__(self) -> None:
        ### First load
        try:
            with open('web/config.json') as f:
                self.data = json.load(f)
        except:
            with open('web/config.json','w+') as f:
                json.dump(DEFAULT,f)
                self.data = DEFAULT.copy()
        
    
    def get_config(self,key):
        return self.data[key]

    def set_config(self,queryDict):
        with open('web/config.json','w') as f:
            print(queryDict)
            self.data['framesToDetector'] = int(queryDict['framesToDetector'])
            self.data['historySize'] = int(queryDict['historySize'])
            self.data['historySizeToDetect'] = int(queryDict['historySizeToDetect'])
            self.data['token'] = queryDict['token']
            json.dump(self.data,f)



global_config = AppConfig()