
import os.path, os
from ftplib import FTP
from  lib2 import copyFilesToArc,Remove1File,copyFilesFromList

import time, ftplib
import pysftp as sftp
import paramiko
#from lib3 import sendFolderFiles, CreateArcFolders, CopyAllFolders, NewPrepareTempFolders, RemoveEmptyFolders

# functions exported to main2: sendFolderFiles,CreateArcFolders,CopyAllFolders,NewPrepareTempFolders
#  sendFolderFiles
#
#=========================================================================

def sendFolderFiles(session):
    protocol= str(session.protocol)
    protocol= protocol.lower()
    isSFTP = protocol.__contains__("sftp")
    isFtp = protocol.__contains__("ftp") and not (protocol.__contains__("sftp"))
    isSmb = protocol.__contains__("smb") or protocol.__contains__("shar")
    tempFolderPath = session.sourcefolder   # may be a mistake in name
   # upFolderPath = upfolder[i]
    #     print("prepare list for ftp, path :", tempFolderPath)
    numsent = 0
    for name in os.listdir(tempFolderPath):
        fileLocalpath = os.path.join(tempFolderPath, name)
        if os.path.isfile(fileLocalpath):
            try:
                if (isFtp) : push_file_FTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSFTP ) : push_file_SFTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSmb): print ("smb protocol is not impemented")
                numsent = numsent + 1

                time.sleep(0.03)

                Remove1File(fileLocalpath)
            except ftplib.all_errors as e:
                numsent=-0.1
                break
            except sftp.exceptions.ConnectionException  as es:
               numsent = -0.2
               break
            except paramiko.ssh_exception.SSHException as es2:
                numsent = -0.2
                break
            except paramiko.ssh_exception.AuthenticationException as es3:
                numsent = -0.2
                break
        else:
            print("main, 208.1,source content error")

    return numsent
#=======================================================================


def push_file_FTP(ip,port,user, psw,filePath):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    fileNameStrArr=str(filePath).split("\\")
    lastIndx= len(fileNameStrArr)-1
    fileName= fileNameStrArr[lastIndx]

    ftp.storbinary('STOR ' + fileName, open(filePath, 'rb'))
    ftp.close()
#=============     push_file_SFTP      =================================================


def push_file_SFTP(ip,port,user, psw,file):
    # ip user psw file - strings
   # file="C:\\Users\\wn10\\PycharmProjects\\multisender1.0\\initConfig.json"
    # port is string
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=ip, username= user, password=psw,
                        port = int(port),cnopts=cnopts)

  #  local_path ="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
#    remote_path = "REMOTE FILE PATH"

#   s.put(local_path, remote_path)
    s.put(file)
    s.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from paramiko.client import SSHClient
from paramiko import AutoAddPolicy
def push_file_SFTP_V2(ip,port,user, psw,file):
  client = SSHClient()
  client.set_missing_host_key_policy(AutoAddPolicy())

  client.connect(hostname=ip,
               port=port,
               username=user,
               password=psw,banner_timeout=200)

  sftp_handle = client.open_sftp()
  sftp_handle.put(file)
  sftp_handle.close()
  client.close()
#################################################################
def new_directory(directory):
  # Before creating a new directory, check to see if it already exists

  if os.path.isdir(directory) == False:
    os.makedirs(directory)
#################################################################

#=========================================
def CreateArcFolders(config,arcroot):
    arcfolder=[]
    users= config.users
    destinationHOST= config.hosts
    port= config.ports
    upfolder= config.sourcefolders
    for i in range(len(upfolder)):

        arcfolderStr= arcroot+"\\Arc"+  "-" + users[i]+"-"+destinationHOST[i]+"-"+port[i]
        new_directory(arcfolderStr)
        arcfolder.append(arcfolderStr)
     #   source = upfolder[i]
    #    dest = tempfolder[i]
  #      copyFilesToArc(source, dest) #we do an arc for every user-destination
    return arcfolder

#############################################

#=========================================
def CopyAllFolders(sourceArr,destArr):

    for i in range(len(sourceArr)):
      copyFilesToArc(sourceArr[i], destArr[i])
     # print("Copying files to Arc ")
         #we do an arc for every user-destination
    return


#=========================================
def RemoveFromUpfolder(upfolderDict):
    for key,val in upfolderDict.items():
       fileList= upfolderDict[key]
       for localpath in fileList:
         try:
            with open(localpath, encoding='utf-8') as f:
                xxxx = 1  ## no op to close localpath
            if os.path.isfile(localpath):
                open
                os.remove(localpath)

            else:
                print("RemoveFromUpfolder: source content error")
         except PermissionError as es:
            print("RemoveFromUpfolder : Pemission error")
    return


#===================================

#====================================


def NewPrepareTempFolders(config,temproot):
    tempfolder = []
    print ("making upfolder dictionary")
    upfolder = config.sourcefolders
    upFolderDict=MakeUpfolderDictionary(upfolder)

    for i in range(len(upfolder)):
        tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
        new_directory(tempfolderStr) #if doesnot exist
        tempfolder.append(tempfolderStr) #??? do we need it?
        print('copying to tempfolder[%d%%]\r' % i, end="")
     #   print("copying to tempfolder ",tempfolderStr)
        key= config.sourcefolders[i]  #key="c:\z\zz\zzz"
        fileList = upFolderDict[key] #["1.txt,111.txt]
        copyFilesFromList(fileList, tempfolderStr) ###########copy all the files to folder
    RemoveFromUpfolder(upFolderDict) # remove only files registered in dictionary
    return tempfolder
#=========================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def MakeUpfolderDictionary(upfolder):

    upFolderDict = {}
    emptyArr=[]
    for i in range (len(upfolder)):
        upFolderDict[upfolder[i]]=emptyArr  # {"c:\z\zz\zzz",[]}
    for key,val in upFolderDict.items():
        upFolderDict[key] = GetFileList(key)  # {c:\z\zz\zzz",[1.txt,111.txt]}

    return  upFolderDict


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def GetFileList(path):
    fileList = []
    for name in os.listdir(path):
        localpath = os.path.join(path, name)

        if os.path.isfile(localpath):
            fileList.append(localpath)
        else:
            print("source content error")
    return fileList
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def RemoveEmptyFolders(path_abs):
    root = path_abs
    folders = list(os.walk(root))[1:]

    for folder in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        if not folder[2]:
            print (">  removing empty temporary folder : ",folder[0] )
            os.rmdir(folder[0])
            time.sleep(0.01)
