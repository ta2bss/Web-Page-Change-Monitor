import os

ControlFolder = r'Datas/Control'
#Folder_Control = os.listdir(ControlFolder)

# Check whether the specified path exists or not
isExist = os.path.exists(ControlFolder)

if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(ControlFolder)
    print("The new directory is created!")