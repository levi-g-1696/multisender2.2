import json
import os.path, os, sys
import random
from ftplib import FTP, error_perm
from shutil import copy2
import csv
import gc
from collections import namedtuple

from FoldersCheckLib import CheckTempFolderStatus, CheckSourcefolderStatus, PrintLastFileAlert
from lib2 import confreader, copyFilesToArc, Remove1File, RemoveFilesFrom, removeOld, copyFilesFromList
import logging, asyncio
import time, ftplib, glob, globalConfig, datetime
from lib3 import sendFolderFiles, CreateArcFolders, CopyAllFolders, NewPrepareTempFolders, RemoveEmptyFolders
import subprocess

ftpExceptIParr = []


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
    print("        *        ENVIRO MULTISENDER 8.1A          *")
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
#
# async def sendingLoop():
#     # for i in range(len(users)):
#
#     #  currentSession = session(destinationHOST[i], port[i], protocol[i], users[i], passw[i], tempfolder[i])
#     newTask = asyncio.create_task(sendingAndLogging())
#     taskList.append(newTask)
#     PrintBannerAndWarnings()
#     print("sleep 10")
#     await asyncio.sleep(10)
#
#     for t in taskList:  # cancel all the tasks that not ended
#         t.cancel()
#
#
# =================================================================


async def sendingAndLogging():
    print("debug1626 sendingAndLoggin")
    taskDict={}
    for i in range(len(users)):

        print (i," trying to send to ",destinationHOST[i] + "," + users[i])

        currentSession = session(destinationHOST[i], port[i], protocol[i], users[i], passw[i], tempfolder[i])
        newTask = asyncio.create_task(sendFolderFiles(currentSession))
        taskList.append(newTask)
        taskDict[newTask]  = currentSession


        # except ftplib.all_errors as e:
        #     print(" \n","sig=",sig,"  > >   F T P exception  - ", destinationHOST[i], users[i], str(e), "\n")
        #     logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolders[i] + "," + "FTP-exception")



    print("sleep 10")
    print ("debug 1915 tasdict=",taskDict  )
    await asyncio.sleep(9) #  task is removed only after hole lloop
    for t in taskList:
            print ("debug 1810 Ntasklist=",len( taskList)  )
            destination= taskDict[t].ip
            user=    taskDict[t].user
            upfolder= taskDict[t].sourcefolder
            if t.done():
                numsent= t.result()
                logging.info("," + destination + "," + user + "," + upfolder + "," + str(numsent))
                #      print( "  ", numsent , " files were sent to " ,destinationHOST[i], users[i])
                print("  ", numsent, " files were sent to ", destination, user)

            else:
              logging.info("," + destination + "," + user + "," + upfolder+ "," + "connection error for 10s")
            #      print( "  ", numsent , " files were sent to " ,destinationHOST[i], users[i])
              print(">>>>   connection error for 10s to ", destination, user)
              t.cancel()
    PrintBannerAndWarnings()
    await asyncio.sleep(1)
# ================================

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
    taskList = []

    #    RemoveFromUpfolder(filedict) is in NewPrepareTempFolders
    while (continueFlag):
        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

        # **************************
        asyncio.run(sendingAndLogging())
        taskList=[]
        ftpExceptIParr = []

        # ****************************

        time.sleep(0.15)
        lastRunTime0 = doEveryXmin1Arg(lastRunTime0, 1, function=RemoveAllIPfromExeptArr,
                                       arg1="")  # lastRunTime0 will be used as arg on next iteration
        lastRunTime1 = doEveryXmin1Arg(lastRunTime1, 1, function=RemoveEmptyFolders, arg1=temproot)
        lastRunTime2 = doEveryXmin2Arg(lastRunTime2, mailAlertPeriod, function=CheckTempFolderStatus, arg1=tempfolder,
                                       arg2=fileNumberLimitforAlert)
        lastRunTime3 = doEveryXmin2Arg(lastRunTime3, mailAlertPeriod, function=CheckSourcefolderStatus, arg1=upfolders,
                                       arg2=receiveFilesAlertTime)

        ##  check stop   ##
        lines = tuple(open(st, 'r'))
        arr = lines[0].split("=")
        if "1" in arr[1]:
            continueFlag = False  # end loop and exit programm
        configProps = confreader()
        tempfolder = NewPrepareTempFolders(configProps, temproot)  # make and fill tempfoders() and remove upfolders
        arcfolder = CreateArcFolders(configProps, arcroot)  # make arcfolder if not exist
        CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination
