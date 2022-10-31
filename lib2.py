# lib2 has repository pattern functions

##########  function send folder files by ftp  ############
#from  lib2 import copyFilesToArc,Remove1File,copyFilesFromList. from lib2 import confreader

import os.path, os, globalConfig

from shutil import copy2
import csv
import pysftp as sftp

import time, glob
import subprocess


def copyFilesToArc(path, archiv):

    # ftp- FTP() object . path-upload folder path name. archive- folder to move upladed files from path
    # must a tool to clean archive from old files
  #  print("is coping from ", path, " to ", archiv)
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        try:
            if os.path.isfile(localpath):
                copy2(localpath, archiv)
            else:
                print("copyFileToArc: source content error")
        except PermissionError as es:
            print("CopytoArc : Pemission error")
    return

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def copyFilesFromList(fileList, dest):
    for localpath in fileList:
        try:
            if os.path.isfile(localpath):
                copy2(localpath, dest)
            else:
                print("copyFilesFromList: source content error")
        except PermissionError as es:
            print("copyFilesFromList : Pemission error")
    return

#########################
def Remove1File(localpath):
    print("Sending OK.system is removing :", localpath)

    try:
        with open(localpath, encoding='utf-8') as f:
            xxxx = 1  ## no op to close localpath
        if os.path.isfile(localpath):
            # open
            delstr= '"del ' +localpath +'"'
            os.system('cmd /c ' + delstr)

        else:
            print("copyFileToArc: source content error")
    except PermissionError as es:
        print("exception point 102030")
    return
########++++++++++++++++++++++++++++++++++
# def BatchRemoveOlderThan_15min():
#     print("run C:\FtpTransfer\remove-older-15min.bat")
#     subprocess.call([r'C:\FtpTransfer\remove-old-15.bat'])

#################     CONFREADER    ####################################
####     function read config file ####

def confreader():
    file= globalConfig.configFile
    isEnable=[]


    users = []
    passw = []
    upfolders = []
    arcfolders = []
    host = []
    port = []

    isAlertEnable=[]
    protocol = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            isEnable= row[0]
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif isEnable=="0" :
                line_count += 1
            else:
                isEnable=row[0]
                isAlertEnable.append(row[1])
                users.append(row[2])
                passw.append(row[3])
                upfolders.append(row[4])
            #    arcfolders.append(row[5])
                host.append(row[6])
                port.append(row[7])
                protocol.append(row[8])
                line_count += 1

    res = globalConfig.config(isEnable,isAlertEnable, host,port,protocol,users, passw, upfolders )
    return res
# --------------------------------------------------



def makeNewLogFile(log):
    if os.stat(log).st_size > 1024 * 1024 * 50:
        now = int(time.time())
        ar = log.split(".")
        log = ar[0] + str(now) + ".csv"
        fLog = open(log, "x")
    return log

