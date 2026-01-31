import Instance

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

