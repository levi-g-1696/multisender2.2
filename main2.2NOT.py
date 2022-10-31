import collections
import json
import os.path, os, sys
from ftplib import FTP, error_perm
from shutil import copy2
import csv
import gc
from collections import namedtuple

from FoldersCheckLib import CheckTempFolderStatus, CheckSourcefolderStatus, PrintLastFileAlert
from lib2 import confreader, copyFilesToArc, Remove1File, RemoveFilesFrom, removeOld, copyFilesFromList
import logging
import time, ftplib, glob, globalConfig, datetime
from lib3 import sendFolderFiles, CreateArcFolders, CopyAllFolders, NewPrepareTempFolders, RemoveEmptyFolders
import subprocess

ftpExceptIParr = []
ftpExceptUserList = []

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def AddToExceptIParr(n, value):
    l = list(ftpExceptIParr)  # WHAT?

    num = n - l.count(value)
    for i in range(1, num):
        ftpExceptIParr.append(value)
    return


# ++++++++++++++++++++++++++++++++++++++++++++++
def RemoveAllIPfromExeptArr(empty_arg):
    del ftpExceptIParr[:]
    return


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def makeSessionDict(destinationHOST, users, port, passw, tempfolder):
        sessionDict= {}
        for i in range(len(users)):
          key = session(destinationHOST[i], port[i], protocol[i], users[i], passw[i], tempfolder[i])
          sessionDict[key] = 1
        return sessionDict
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def GetFileNumOnTempFolders(configProps):
    resarr = []
    res = resarr.append(foldersStat("c:\\ccc\\cccc", 57))
    res = resarr.append(foldersStat("c:\\cc\\bbbb", 157))
    res = resarr.append(foldersStat("c:\\ccc\\dddd", 0))
    return (res)


# ---------------------------------------------------------------------
def PrintBannerAndWarnings():
    print()
    print()
    print("        *******************************************")
    print("        *        ENVIRO MULTISENDER 7.3           *")
    print("        *   file transfer     is running          *")
    print("        *        DO NOT CLOSE THIS WINDOW         *")
    print("        *******************************************")
    print("       ")
    print("\n               L A S T   W A R N I N G S :")
    PrintLastFileAlert(alertFile, 16)


################################## ###########################3
# def PrepareTempFolders(config):
#     tempfolder=[]
#     for i in range(len(config.sourcefolders)):
#
#         tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
#         new_directory(tempfolderStr)
#         tempfolder.append(tempfolderStr)
#         source = config.sourcefolders[i]
#         dest = tempfolder[i]
#         copyFilesToArc(source, dest)
#     return tempfolder


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def ReadInitCofiguration(initJsonFile):
    with open(initJsonFile) as f:
        return json.load(f)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def doEveryXmin1Arg(lastRunTime, minNum, function, arg1):
    dt = datetime.datetime.now()
    newts = lastRunTime
    if dt.timestamp() >= lastRunTime + minNum * 60:
        function(arg1)
        newts = dt.timestamp()

    return newts
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def returnSorted(dict):
    sortedlist = sorted(dict.items(), key=lambda x: x[1])
    sortedDict = collections.OrderedDict(sortedlist)
    return sortedDict


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def doEveryXmin2Arg(lastRunTime, minNum, function, arg1, arg2):
    dt = datetime.datetime.now()
    newts = lastRunTime
    if dt.timestamp() >= lastRunTime + minNum * 60:
        newts = dt.timestamp()
        d1 = datetime.datetime.now
        function(arg1, arg2)
        d2 = datetime.datetime.now
    #      logging.info("," + "before function " + str(function) + "," + str(d1) + "," + "after:" + "," + str(d2))
    return newts


# ======================================================

if __name__ == "__main__":
    ## stoping option  ##
    # looking for init json file
    if len(sys.argv) < 2:
        print("You must set argument initconfig file directory as c:\\\z\\\zzz \n prefer use batch file for run")
        time.sleep(4)
        sys.exit()
    #    initConfigDirectoty="C:\\Users\\wn10\\PycharmProjects\\multisender1.0"
    initConfigDirectoty = str(sys.argv[1])
    initConfigFile = initConfigDirectoty + "\\initConfig.json"
    configDict = ReadInitCofiguration(initConfigFile)

    # ------------------------------------------
    # set init configuration data
    workingDirectory = configDict["workDirectory"]
    ftpExceptEscapecount = int(configDict["ftpExceptEscapecount"])
    fileNumberLimitforAlert = int(configDict["fileNumberLimitforAlert"])
    mailAlertPeriod = 8  # int(configDict["mailAlertPeriod"])
    receiveFilesAlertTime = 120
    # ------------------------------------------

    os.chdir(workingDirectory)
    configFile = globalConfig.configFile
    log = globalConfig.log
    temproot = globalConfig.temproot
    arcroot = globalConfig.arcroot
    logoldpath = globalConfig.logoldpath
    ftpExceptIParr = []
    st = workingDirectory + globalConfig.stopfile
    alertFile = globalConfig.alertFile
    dt = datetime.datetime.now()
    lastRunTime0 = dt.timestamp()
    lastRunTime1 = dt.timestamp()
    lastRunTime2 = dt.timestamp()
    lastRunTime3 = dt.timestamp()

    continueFlag = True
    session = namedtuple("session", "ip port protocol user psw sourcefolder")

    foldersStat = namedtuple("foldersStat", "tempFolder num")  # a tuple (tempfoldr-path, files-number-in-it)

    # --------------------------------
    try:
        os.remove(st)
    except FileNotFoundError as e:
        print("Cannot find stop.conf")
    try:
        os.remove(globalConfig.alertFile)
    except FileNotFoundError as e:
        print("Cannot find " + globalConfig.alertFile)

    f1 = open(st, 'w')
    f1.write('stopFlag=0\n')  # python will convert \n to os.linesep
    f1.close()  # you can omit in most cases as the destructor will call it
    continueFlag = True
    ######################
    f1 = open(log, "r")
    logfileid = f1.fileno
    f1.close
    ###################
    f1 = open(globalConfig.alertFile, 'w')
    f1.write(' \n')  # python will convert \n to os.linesep
    f1.close()
    print()
    print("    ftp transfer is started\r\n")
    count1m = 0
    count3m = 0
    countXXm = 0

    # -----------

    # =====================================
    ## confreader is filtering the lines that isEnable= 0 not the best solution. but works. So will not be session on this lines
    # res= confreader()
    # isEnable,isAlertEnable, users, passw, upfolder,  destinationHOST, port = confreader()
    #    configProps= config()

    configProps = confreader()
    destinationHOST = configProps.hosts
    users = configProps.users
    passw = configProps.passwords
    port = configProps.ports
    upfolders = configProps.sourcefolders
    isEnable = configProps.isSendEnable
    isAlertEnable = configProps.isAlertEnable
    protocol = configProps.protocol
        # ===== prepare temporary folders from upfolders  =====

    tempfolder = NewPrepareTempFolders(configProps, temproot)  # make and fill tempfoders() and remove upfolders
    arcfolder = CreateArcFolders(configProps, arcroot)  # make arcfolder if not exist
    CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination

    sessionsDict = makeSessionDict(destinationHOST, users, port, passw, tempfolder)
    maxSesDictPriority= 1
    #    RemoveFromUpfolder(filedict) is in NewPrepareTempFolders
    while (continueFlag):

        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

        # ===========================================================
        thereWasAnException=False
        for elem in sessionsDict.keys() :
                currentSession =elem
               # currentSession = session(destinationHOST[i], port[i], protocol[i], users[i], passw[i], tempfolder[i])
                ftpExceptIP = currentSession.ip + "-" + currentSession.port

                if (ftpExceptIP in ftpExceptIParr):
                    ## if host was not reachable then do not send it
                    logging.info("," + currentSession.ip + "," + currentSession.user  + "," + currentSession.sourcefolder + "," + "skiped")

                #  ftpExceptIParr.remove(ftpExceptIP)

                else:
                    # if host was ok - send
                    #    sendtempfoderFiles()
                    numsent = sendFolderFiles(currentSession)
                    if numsent >= 0:
                      logging.info("," + currentSession.ip + "," + currentSession.user  + "," + currentSession.sourcefolder + "," + str(numsent))
                      print("  ", numsent, " files were sent to ", currentSession.ip, currentSession.user )

                    else:  #if there was an exception on   sendFolderFiles(currentSession)
                      exceptionType= "FTP exception - "
                      if numsent < -0.1 : exceptionType= "SFTP exception - "
                      print(" \n> > >   " + exceptionType , currentSession.ip , currentSession.user, "\n")
                      logging.info("," + currentSession.ip + "," + currentSession.user  + "," + currentSession.sourcefolder + "," + exceptionType)

                      ftpExceptIParr.append(ftpExceptIP)
                      maxSesDictPriority +=1
                      sessionsDict[elem]  =maxSesDictPriority
                      thereWasAnException= True

                #  time.sleep(0.1)

                #  AddToExceptIParr( 10, ftpExceptIP) #10 ip numbers to array if destination is not reachable

                #  ftpExceptEscapecount = 10
                #logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolders[i] + "," + "Error " + str(e))
        PrintBannerAndWarnings()
        if not thereWasAnException :
          print("sleep10")
          time.sleep(10)
        sessionsDict = returnSorted(sessionsDict)
        time.sleep(0.05)
        lastRunTime0 = doEveryXmin1Arg(lastRunTime0, 3, function=RemoveAllIPfromExeptArr,
                                       arg1="")  # lastRunTime0 will be used as arg on next iteration
        lastRunTime1 = doEveryXmin1Arg(lastRunTime1, 1, function=RemoveEmptyFolders, arg1=temproot)
        lastRunTime2 = doEveryXmin2Arg(lastRunTime2, mailAlertPeriod, function=CheckTempFolderStatus, arg1=tempfolder,
                                       arg2=fileNumberLimitforAlert)
        lastRunTime3 = doEveryXmin2Arg(lastRunTime3, mailAlertPeriod, function=CheckSourcefolderStatus, arg1=upfolders,
                                       arg2=receiveFilesAlertTime)
        # if count1m % 6 == 0:
        #  removeOld()  # every 1 min
        #        RemoveEmptyFolders(temproot)
        #  log= makeNewLogFile(log)

        #   count1m = 0
        # if countXXm % mailAlertPeriod ==0 : #every <mailAlertPeriod> min
        # statusArr = MakeStatusArray(tempfolder)
        # if num in tempfolder >120 alert by mail

        #     CheckTempFolderStatus(tempfolder, fileNumberLimitforAlert) # big folder is a sign of
        # connection to destination problem
        # must Check
        #    CheckSourcefolderStatus(upfolders, receiveFilesAlertTime)
        #  countXXm= 0

        ##  check stop   ##
        lines = tuple(open(st, 'r'))
        arr = lines[0].split("=")
        if "1" in arr[1]:
            continueFlag = False  # end loop and exit programm
        configProps = confreader()
        tempfolder = NewPrepareTempFolders(configProps, temproot)  # make and fill tempfoders() and remove upfolders
        arcfolder = CreateArcFolders(configProps, arcroot)  # make arcfolder if not exist
        CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination





