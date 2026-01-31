import Instance
import os
import json

try: 
    import cfonts
    cfonts_bool = True
except ImportError: 
    print("Cfonts not detected, falling back to basic output")
    cfonts_bool = False

def out(message):
    if cfonts_bool:
        print(cfonts.render(message))
    else:
        print(message)

out("MCINSTA")
print("a simple modded minecraft instance manager")

instances = Instance.Instance.load_from_json()
selected_instance = None
mods_folder = None

if os.path.exists("instances.json"):
    with open("instances.json", "r") as file:
        data = json.load(file)
        if 'mods_folder' in data:
            mods_folder = data['mods_folder']
        if 'selected_instance' in data:
            selected_instance = data['selected_instance']

if not mods_folder:
    mods_folder = input("Enter the path to your mods folder: ")

def save_config(instance_name=None):
    if os.path.exists("instances.json"):
        with open("instances.json", "r") as file:
            data = json.load(file)
        data['mods_folder'] = mods_folder
        if instance_name:
            data['selected_instance'] = instance_name
        with open("instances.json", "w") as file:
            json.dump(data, file, indent=4)

save_config()

while True:
    selected_text = selected_instance if selected_instance else "None"
    print(f"\nThe currently selected instance is: {selected_text}")
    
    print("\nSelect an Action")
    print("(1) List instances")
    print("(2) Create a new instance")
    print("(3) Move an instance")
    print("(4) Delete an instance")
    print("(5) Select instance")
    print("(any other key) exit the program")
    
    action = input("Your selection: ")
    
    if action == "1":
        if instances:
            print("\nInstances:")
            for name, inst in instances.items():
                print(f"  - {name} (v{inst.version}) at {inst.path}")
        else:
            print("No instances found.")
    
    elif action == "2":
        name = input("Instance name: ")
        path = input("Instance path: ")
        version = input("Game version: ")
        inst = Instance.Instance(path, name, version)
        instances[name] = inst
        save_config()
        print(f"Created instance '{name}'")
    
    elif action == "3":
        if instances:
            name = input("Instance name to move: ")
            if name in instances:
                new_path = input("New path: ")
                instances[name].move(new_path)
            else:
                print("Instance not found.")
        else:
            print("No instances to move.")
    
    elif action == "4":
        if instances:
            name = input("Instance name to delete: ")
            if name in instances:
                instances[name].delete_instance(instances[name].path)
                del instances[name]
            else:
                print("Instance not found.")
        else:
            print("No instances to delete.")
    
    elif action == "5":
        if instances:
            if selected_instance:
                old_inst = instances[selected_instance]
                old_inst.move(old_inst.path)
                print(f"Moved mods back to '{selected_instance}'")
            
            print("\nInstances:")
            for i, name in enumerate(instances.keys(), 1):
                print(f"  ({i}) {name} (v{instances[name].version})")
            choice = input("Select instance number: ")
            try:
                instance_list = list(instances.keys())
                idx = int(choice) - 1
                if 0 <= idx < len(instance_list):
                    selected_instance = instance_list[idx]
                    selected_inst = instances[selected_instance]
                    selected_inst.move(mods_folder)
                    save_config(selected_instance)
                    print(f"Selected and moved mods to '{selected_instance}'")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")
        else:
            print("No instances to select.")
    
    else:
        print("Exiting...")
        break
