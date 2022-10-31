##########  function send folder files by ftp  ############


import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
import pysftp as sftp
import logging
import time, ftplib, glob
import subprocess
def placeFilesFTP(ftp, path, archiv):
    # print ("placefile point5")
    #  print (ftp, path, archiv)
    # print ("placefile point6  ")
    #  print ( os.listdir(path))
    # ftp- FTP() object . path-upload folder path name. archive- folder to move upladed files from path
    # must a tool to clean archive from old files
    print("prepare list for ftp, path :", path)
    for name in os.listdir(path):

        localpath = os.path.join(path, name)
        print("placefile FTP  ", localpath)

        if os.path.isfile(localpath):
            print("placefile point10")
            #   print("is coping from ", localpath," to ",archiv)
            #  copy2(localpath, archiv)
            ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
            # print ("From placeFilesFTP: stor ", name, localpath)
            os.remove(localpath)
        else:
            print("source content error")
    return
# ==================   push_file_SFTP   ================================================
def pushFileSFTP(ip,port,user, psw,file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=ip, username= user, password=psw,
                        port =port,cnopts=cnopts)
  #  local_path ="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
#    remote_path = "REMOTE FILE PATH"

#   s.put(local_path, remote_path)
    s.put(file)
    s.close()
#==========================================================================================
def copyFilesToArc(path, archiv):
    # print ("placefile point5")
    # print (ftp, path, archiv)
    # print ("placefile point6  ")

    # ftp- FTP() object . path-upload folder path name. archive- folder to move upladed files from path
    # must a tool to clean archive from old files
    print("is coping from ", path, " to ", archiv)
    for name in os.listdir(path):
        #  print ("placefile point7  ",name)

        localpath = os.path.join(path, name)
        try:
            if os.path.isfile(localpath):
                #   print ("placefile point10")
                #  print("is coping from ", localpath," to ",archiv)
                copy2(localpath, archiv)
            #    print(" from copyFilesToArc: copying to ",localpath, archiv)
            #   ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
            #  time.sleep(0.15)
            #    os.remove(localpath)

            else:
                print("copyFileToArc: source content error")
        except PermissionError as es:
            print("CopytoArc : Pemission error")
    return


###++++++++++++++++++++++++++++++++++++
def RemoveFilesFrom(path):
    print("is removing from", path)
    for name in os.listdir(path):
        #  print ("placefile point7  ",name)

        localpath = os.path.join(path, name)
        try:
            with open(localpath, encoding='utf-8') as f:
                xxxx = 1  ## no op to close localpath
            if os.path.isfile(localpath):
                open
                os.remove(localpath)

            else:
                print("copyFileToArc: source content error")
        except PermissionError as es:
            print("CopytoArc : Pemission error")
    return


#########################
def Remove1File(localpath):
    print("system is removing :", localpath)

    try:
        with open(localpath, encoding='utf-8') as f:
            xxxx = 1  ## no op to close localpath
        if os.path.isfile(localpath):
            # open
            os.remove(localpath)

        else:
            print("copyFileToArc: source content error")
    except PermissionError as es:
        print("exception point 102030")
    return


########++++++++++++++++++++++++++++++++++
def BatchRemoveOlderThan_15min():
    print("run C:\FtpTransfer\remove-older-15min.bat")
    subprocess.call([r'C:\FtpTransfer\remove-old-15.bat'])


#### function read config file ####
def confreader(file):
    isEnable=False
    users = []
    passw = []
    upfolders = []
    arcfolders = []
    host = []
    port = []

    isLastDest=[]
    tempfolders = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            isInable= row[0]
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif isInable=="0" :
                line_count += 1
            else:
                isEnable=row[0]
                isLastDest.append(row[1])
                users.append(row[2])
                passw.append(row[3])
                upfolders.append(row[4])
                arcfolders.append(row[5])
                host.append(row[6])
                port.append(row[7])
                tempfolders.append(row[8])
                line_count += 1

    return (isEnable,isLastDest, users, passw, upfolders, arcfolders, host, port, tempfolders)


# -----------------------------------------------
def cleanTemporaryFolders():
    tempfolders = ['F:\\TEMP\\arc1\\*',
                   'F:\\TEMP\\arc2\\*',
                   'F:\\TEMP\\arc3\\*',
                   'F:\\TEMP\\arc4\\*',
                   'F:\\TEMP\\arc5\\*',
                   'F:\\TEMP\\arc6\\*'
                   'F:\\TEMP\\forDEL\\*']
    for i in range(len(tempfolders)):
        files = glob.glob(tempfolders[i])
        for f in files:
            os.remove(f)
    return


# --------------------------------------------------
def removeOld():
    arcfolders = ["F:\\ARC\\Arc1\\*",
                  "F:\\ARC\\Arc2\\*",
                  "F:\\ARC\\Arc3\\*",
                  "F:\\ARC\\Arc3\\*",
                  "F:\\ARC\\Arc4\\*",
                  "F:\\ARC\\Arc6\\*",
                  "F:\\ARC\\hydArc1\\*",
                  "F:\\ARC\\hydArc2\\*",
                  "F:\\ARC\\hydArc3sportek\\*",
                  "F:\\ARC\\hydArc4wiseman\\*",
                  "F:\\ARC\\hydArc5Kane\\*"
                  ]
    daysNotDelete = 20
    now = time.time()  # time in sec
    s = 0
    print("deleting old arc files")
    for i in range(len(arcfolders)):
        files = glob.glob(arcfolders[i])

        for f in files:

            if os.stat(f).st_mtime < now - daysNotDelete * 86400:
                s = s + 1
                if os.path.isfile(f):
                    os.remove(f)
    print("deleted ", s)
    return


# ----------------------------------------------------------------------


def makeNewLogFile(log):
    if os.stat(log).st_size > 1024 * 1024 * 50:
        now = int(time.time())
        ar = log.split(".")
        log = ar[0] + str(now) + ".csv"
        fLog = open(log, "x")
    return log

