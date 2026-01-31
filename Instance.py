import os
import sys
import shutil
import json

class Instance:
    numInstances = 0
    
    @classmethod
    def _load_instance_count(cls):
        if os.path.exists("instances.json"):
            with open("instances.json", "r") as file:
                data = json.load(file)
                cls.numInstances = max((info.get('index', 0) for info in data.values()), default=0)
    
    @classmethod
    def load_from_json(cls):
        instances = {}
        if os.path.exists("instances.json"):
            with open("instances.json", "r") as file:
                data = json.load(file)
            
            for name, info in data.items():
                instance = cls.__new__(cls)
                instance.name = name
                instance.version = info['version']
                instance.path = info['path']
                instance.index = info['index']
                cls.numInstances = max(cls.numInstances, instance.index)
                instances[name] = instance
        
        return instances
    
    def __init__(self, given_path, given_name, game_version):
        Instance._load_instance_count()
        Instance.numInstances += 1 
        self.version = game_version

        self.index = self.numInstances
        if os.path.exists(given_path):
            self.path = given_path
        else:
            print('That path does not in fact exist.')
            sys.exit()
        self.name = given_name
        self.save_to_json()


    def totalInstances(self):
        return self.numInstances

    def getIndex(self):
        return self.index

    def move(self, newLoc):
        current = self.path
        new = newLoc

        if not os.path.exists(new):
            os.makedirs(new)

        for item in os.listdir(current):
            src = os.path.join(current, item)
            dst = os.path.join(new, item)
            shutil.move(src, dst)
        
        self.path = new
        self.save_to_json()
        print(f'Successfully moved contents from {current} to {new}')

    def delete_instance(self, instancePath):
        sure = input(f"Are you sure you'd like to delete the instance at path {instancePath}? (y/n): ")
        if sure == "y":
            shutil.rmtree(instancePath)
            
            # Remove from JSON
            if os.path.exists("instances.json"):
                with open("instances.json", "r") as file:
                    data = json.load(file)
                
                for name, info in list(data.items()):
                    if info['path'] == instancePath:
                        del data[name]
                        break
                
                with open("instances.json", "w") as file:
                    json.dump(data, file, indent=4)
            
            print(f"Removed the instance at path {instancePath}")
        else: 
            print("Operation Cancelled")

    def save_to_json(self, mods_folder=None):
        jason = {}
        if os.path.exists("instances.json"):
            with open("instances.json", "r") as file:
                jason = json.load(file)
        jason[self.name] = {
            'version': self.version,
            'path': self.path,
            'index':self.index,
        }
        if mods_folder:
            jason['mods_folder'] = mods_folder
        with open("instances.json", "w") as file:
            json.dump(jason, file, indent=4)


if __name__ == "__main__":
    print("Built by a human: RalphieDawg")
    print("Who's Jason?")
    print("Does he own the JSTOR??")


