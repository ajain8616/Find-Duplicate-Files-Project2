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
        if os.path.isdir(path + "/" + file):
            LoadFileList(path + "/" + file)
        else:
            if filesPath.get(file) == None:
                filesPath[file] = []
            filesPath[file].append(path)

def LoadPriorityList():
    global FolderPriorityMap
    df=pd.read_excel('files-priority.xlsx')
    foldersPriority=np.array(df)
    foldersPriorityList=foldersPriority.flatten()  
    my_list = foldersPriority.tolist()
   
    val=1;
    for i in my_list:
        FolderPriorityMap[i[0]] = val
        val = val + 1 


def DeleteFile(file, folderlist):
    global FolderPriorityMap 
    print("Deleting Duplicates of: " , file , " From ", folderlist);
    # I need to browse through the folderlist
    folder = folderlist[0]
    val = FolderPriorityMap[folder]
    # If the value of a flder is higher , than I will remove file from the folder
    for fld in folderlist:
        if FolderPriorityMap[fld] > val:
            print("Remove From ", fld)
        elif FolderPriorityMap[fld] < val:
            print("Remove From ", folder)
            folder = fld
            val = FolderPriorityMap[folder]
    

def DeleteDuplicateFiles( ):
    global FolderPriorityMap
    global filesPath
    for filename in filesPath.keys():
        DeleteFile(filename, filesPath[filename])

## Execution Strts Here
LoadFileList("./test")
LoadPriorityList()
DeleteDuplicateFiles()


