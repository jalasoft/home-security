import yaml

class AppConfig:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r") as config_file:
             self.data = yaml.load(config_file)
    
    def __contains__(self, key):
        return key in self.data	

    def __getitem__(self, key):
        if self.data is None:
            raise ValueError("Configuration not loaded.")
        
        return self.data[key]
