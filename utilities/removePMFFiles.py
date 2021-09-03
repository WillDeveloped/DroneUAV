import os
import os.path

for root, dirs, files in os.walk("frames/Video/"):
    for name in files:
        #print(name.split('.')[1])
        if (name.split('.')[1]) == "pfm":
            print("Deleteing", name)
            os.remove("frames/Video/" + str(name))

