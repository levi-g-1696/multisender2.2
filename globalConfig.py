from collections import namedtuple

configFile = ".\\transferConfig22_2.csv"
log = ".\\Log\\transferLog.csv"
temproot = ".\\Temp"
#arcroot=  ".\\Arc"
arcroot= "D:\multisender ARC"
logoldpath = ".\\LogOld\\"

stopfile = "\\stop.conf"
alertFile= ".\\Alert.txt"
alertHistory =".\\AlertHistory.txt"

config = namedtuple("config", "isSendEnable isAlertEnable hosts ports protocol users passwords sourcefolders")