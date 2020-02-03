import os.path
import os
print("Welcome in file manager")
def Menu():
    print("""
    1-work with file
    2-work with directory
    0-exit/quit""")

def FileOperations():
    print("""
    1 - Show all files
    2 - Create new file 
    3 - Delete a file 
    4 - Rename file 
    5 - Add content 
    6 - Rewwrite file
    0 - Return to MainMenu""")
    number=int(input())
    if number==0:
        return 0
    elif number == 1:
        from os import listdir
        from os.path import isfile, join
        files = [f for f in listdir(r"C:\Users\Erik\Desktop\pp1\ss") if isfile(join(r"C:\Users\Erik\Desktop\pp1\ss", f))]
        print(files)
    elif number == 2:
        nameoffile=input("New file name:")+".txt"
        r=open(nameoffile,"tw")
        r.close()
    elif number == 3:
        nameoffile=input("File name:")+".txt"
        try:
            os.remove()
        except FileNotFoundError:
            print("File was NOT find")
        else:
            print("File was deleted")
    elif number == 4:
        nameoffile = input("File name:")+".txt"
        newfile= input("new name which you want:")+".txt"
        try:
            os.rename(nameoffile,newfile)
        except FileNotFoundError:
            print("This file doesn't exist")
        else:
            print("This operation was successful")
    elif number == 5:
        nameoffile = input("Open file : ")+".txt"
        t=open(nameoffile,"at")
        Newcontent=input()
        t.write(Newcontent)
        t.close()
    elif number == 6:
        nameoffile = input("open this file :")+".txt"
        t=open(nameoffile,"wt")
        Newname=input()
        t.write(Newname)
        t.close()
def directorymanager():
    print("""
    1-rename directory
    2-print number of files in it
    3-print number of directories in it
    4-list content of the directory 
    5-add file to this directory
    6-add new directory to this directory
    7-create new directory
    0-exit/quit""")
    choose=int(input())
    if choose==0:
        return 0
    elif choose==1:
       Directoryname1=input("Old name:")+".txt"
       Directoryname2=input("New name:")+".txt"
       os.rename(Directoryname1,Directoryname2)
       print("This operation was succesfull")
    elif choose==2:
        num=0
        for f in os.listdir():
            File=os.path.join(f)
            if os.path.isdir(File):
                num=num+1
        print("number of dir is: ",num) 
    elif choose==3:
        num=0
        for f in os.listdir():
            Dir=os.path.join(f)
            if os.path.isdir(Dir):
                num=num+1
        print("number of dir is: ",num)
    elif choose==4:
        print(os.listdir())
    elif choose==5:
        file = open(r"C:\Users\Erik\Desktop\pp1\ss\newdir\test.txt", "w")
        file.close()
    elif choose==6:
        os.mkdir(r"C:\Users\Erik\Desktop\pp1\ss\newdir")
    elif choose==7:
        DirName = input("New dir's name: ")
        os.mkdir(DirName)
        print("Dir created ")
Work = True
while Work:
    Menu()
    add = int(input())
    if add == 0:
        print("program will out")
        Work=False 
    elif add == 1:
        print("you in file manager")
        FileOperations()
    elif add == 2:
        print("you in current location")
        directorymanager()