import os
import os.path

for root, dirs, files in os.walk("../Mono_Depth/output"):
    for name in files:
        #print(name.split('.')[1])
        if (name.split('.')[1]) == "pfm":
            print("Deleteing", name)
            os.remove("../Mono_Depth/output/" + str(name))

