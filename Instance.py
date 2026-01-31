import os
import sys
import shutil
import json

class Instance:
    numInstances = 0
    def __init__(self, given_path, given_name, game_version):
        Instance.numInstances += 1 
        self.version = game_version

        self.index = self.numInstances
        if os.path.exists(given_path):
            self.path = given_path
        else:
            print('That path does not in fact exist.')
            sys.exit()
        self.name = given_name


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
        
        print(f'Successfully moved contents from {current} to {new}')

    def delete_instance(self, instancePath):
        sure = input(f"Are you sure you'd like to delete the instance at path {instancePath}? (y/n): ")
        if sure == "y":
            shutil.rmtree(instancePath)
            print(f"Removed the intance at path {instancePath}")
        else: 
            print("Operation Cancelled")

    def save_to_json(self):
        jason = {
            'name': self.name,
            'version': self.version,
            'path': self.path,
            'index': self.getIndex()
        }
        with open ("instances.json","w") as file:
            json.dump(jason, file, indent = 4)

if __name__ == "__main__":
    print("Built by a human: RalphieDawg")
    print("Who's Jason?")
    print("Does he own the JSTOR??")


