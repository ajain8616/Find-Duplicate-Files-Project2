import pandas as pd
import numpy as np
import os

## Initialization Section
filesPath = {}
FolderPriorityMap = {}

## Function Definition
def LoadFileList(path):
    global filesPath
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            LoadFileList(file_path)
        else:
            if filesPath.get(file) is None:
                filesPath[file] = []
            filesPath[file].append(path)

def LoadPriorityList():
    global FolderPriorityMap
    df = pd.read_excel('files-priority.xlsx')
    foldersPriority = np.array(df)
    foldersPriorityList = foldersPriority.flatten()  
    my_list = foldersPriority.tolist()
   
    val = 1
    for i in my_list:
        folder_name = i[0]
        FolderPriorityMap[folder_name] = val
        val += 1 

def DeleteFile(file, folderlist):
    global FolderPriorityMap 
    print("Deleting Duplicates of:", file, "From", folderlist)    
    folder = os.path.dirname(folderlist[0])  # Extract folder name
    val = FolderPriorityMap.get(folder, 0)
    deleted = False
    
    for fld in folderlist:
        current_folder = os.path.dirname(fld)  # Extract folder name
        current_folder = current_folder if current_folder != '' else '.'  # Handle current_folder being ''
        if FolderPriorityMap.get(current_folder, 0) > val:
            print("Deleting from", fld)
            os.remove(os.path.join(fld, file))  # Remove file
            deleted = True
        elif FolderPriorityMap.get(current_folder, 0) < val:
            print("Deleting from", folder)
            os.remove(os.path.join(folder, file))  # Remove file
            folder = current_folder
            val = FolderPriorityMap.get(folder, 0)
            deleted = True
    
    if deleted:
        print("Deleted:", file)

def DeleteDuplicateFiles():
    global FolderPriorityMap
    global filesPath
    for filename in filesPath.keys():
        DeleteFile(filename, filesPath[filename])

def ShowDuplicateFiles():
    for filename, folderlist in filesPath.items():
        if len(folderlist) > 1:
            print("Duplicate file:", filename)
            print("Found in folders:")
            for folder in folderlist:
                print("-", folder)
            print()

def checkDuplicateFolderFiles():
    has_duplicates = False
    for filename, folderlist in filesPath.items():
        if len(folderlist) > 1:
            has_duplicates = True
            break
    
    if has_duplicates:
        DeleteDuplicateFiles()
    else:
        ShowDuplicateFiles()

## Execution Starts Here
LoadFileList("./test")
LoadPriorityList()
checkDuplicateFolderFiles()
