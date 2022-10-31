import collections
import json
import os, sys
from ftplib import FTP
from collections import namedtuple
from FoldersCheckLib import CheckTempFolderStatus, CheckSourcefolderStatus, PrintLastFileAlert
from lib2 import confreader
import logging
import time, globalConfig, datetime
from lib3 import sendFolderFiles, CreateArcFolders, CopyAllFolders, NewPrepareTempFolders, RemoveEmptyFolders

ftpExceptIParr = []
ftpExceptUserList = []
maxSesDictPriority= 1
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def AddToExceptIParr(n, value):
    l = list(ftpExceptIParr)  # WHAT?

    num = n - l.count(value)
    for i in range(1, num):
        ftpExceptIParr.append(value)
    return


# ++++++++++++++++++++++++++++++++++++++++++++++
def RemoveAllIPfromExeptArr(empty_arg):
    global maxSesDictPriority
    del ftpExceptIParr[:]
    maxSesDictPriority = 1
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
    print("        *        ENVIRO MULTISENDER 2.2 (7.4)     *")
    print("        *   file transfer     is running          *")
    print("        *        DO NOT CLOSE THIS WINDOW         *")
    print("        *******************************************")
    print("       ")
    print("\n               L A S T   W A R N I N G S :")
    PrintLastFileAlert(alertFile, 16)


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

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def conditionalSleep(sec,startTime):


    dt= datetime.datetime.now()
    nowTime= dt.timestamp()
    delta= nowTime-startTime
    if  delta< sec:
        print ("sleep ", sec-delta)
        time.sleep(sec-delta)

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

#///////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////

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
    mailAlertPeriod =  int(configDict["mailAlertPeriod"])
    receiveFilesAlertTime = 120
    # ------------------------------------------

    os.chdir(workingDirectory)
    configFile = globalConfig.configFile
    log = globalConfig.log
    temproot = globalConfig.temproot
    arcroot = globalConfig.arcroot
    logoldpath = globalConfig.logoldpath
    ftpExceptIParr = []
    stp = workingDirectory + globalConfig.stopfile
    print ("stpfile ",stp)
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
        print ("stopfile ",stp)
        os.remove(stp)
    except FileNotFoundError as e:
        print("Cannot find stop.conf")
    try:
        os.remove(globalConfig.alertFile)
    except FileNotFoundError as e:
        print("Cannot find " + globalConfig.alertFile)

    f1 = open(stp, 'w')
    f1.write('stopFlag=0\n')  # python will convert \n to os.linesep
    print ("write 0 to stopfile")
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
    # =====================================
    ## confreader is filtering the lines that isEnable= 0 not the best solution. but works. So will not be session on this lines
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
    print("Copying files from Tempfolders to ArcFolders")
    CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination

    sessionsDict = makeSessionDict(destinationHOST, users, port, passw, tempfolder)
    #maxSesDictPriority= 1

    while (continueFlag):

        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')
        dt2 = datetime.datetime.now()
        lastRunTime4 = dt2.timestamp()
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

        PrintBannerAndWarnings()

        conditionalSleep(10,lastRunTime4)
        sessionsDict = returnSorted(sessionsDict)
        time.sleep(0.05)
        lastRunTime0 = doEveryXmin1Arg(lastRunTime0, 3, function=RemoveAllIPfromExeptArr,
                                       arg1="")  # lastRunTime0 will be used as arg on next iteration
        lastRunTime1 = doEveryXmin1Arg(lastRunTime1, 1, function=RemoveEmptyFolders, arg1=temproot)
        lastRunTime2 = doEveryXmin2Arg(lastRunTime2, mailAlertPeriod, function=CheckTempFolderStatus, arg1=tempfolder,
                                       arg2=fileNumberLimitforAlert)
        lastRunTime3 = doEveryXmin2Arg(lastRunTime3, mailAlertPeriod, function=CheckSourcefolderStatus, arg1=upfolders,
                                       arg2=receiveFilesAlertTime)
        # if countXXm % mailAlertPeriod ==0 : #every <mailAlertPeriod> min
        # statusArr = MakeStatusArray(tempfolder)
        # if num in tempfolder >120 alert by mail

        #     CheckTempFolderStatus(tempfolder, fileNumberLimitforAlert) # big folder is a sign of
        # connection to destination problem
        # must Check
        #    CheckSourcefolderStatus(upfolders, receiveFilesAlertTime)
        #  countXXm= 0

        ##  check stop   ##
        lines = tuple(open(stp, 'r'))
        arr = lines[0].split("=")
        if "1" in arr[1]:
            continueFlag = False  # end loop and exit programm
        configProps = confreader()
        print ("Moving  the new files from ftp/sftp folders to TempFolders")
        time.sleep(0.3)
        tempfolder = NewPrepareTempFolders(configProps, temproot)  # make and fill tempfoders() and remove upfolders
        arcfolder = CreateArcFolders(configProps, arcroot)  # make arcfolder if not exist
        print("Copying files from Tempfolders to ArcFolders")
        time.sleep(0.3)
        CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination
# end of while loop