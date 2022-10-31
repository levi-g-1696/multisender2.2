# alrgoritm
# common: to send a file on time array by internet unix time sec or every 100 sec.
#
# protokol FTP pas. users/psw destination ( ip of multisender) csv file using read csv tool
#
# we can use mutisender for it but it will be difficult to synchronize it on various comp
#  so we will use code without while loop. and a loop on unix time will be done
#
# make files on folders by conf file
# loop on unixtime
#  { multisender session
#    make files on folders by config file}



from urllib.request import urlopen
import time
from datetime import datetime
def getOnlineGMTTime(mode):
    webpage = urlopen("http://just-the-time.appspot.com/")
    internettime = webpage.read().strip()

    strt = str(internettime)
    datestr = strt.split("'")[1]
    dateYMD = datestr.split(" ")[0]
    time = datestr.split(" ")[1]
    datearr = dateYMD.split("-")
    Y = int(datearr[0])
    M =int(datearr[1])
    D = int(datearr[2])
    timearr = time.split(":")
    hh = int(timearr[0])
    mm = int(timearr[1])
    sec = int(timearr[2])
    if (mode == "datetime") or mode == "":
      return  datetime(Y, M, D, hh, mm, sec)
    elif mode == "unixtimesec":
       t= datetime(Y, M, D, hh, mm, sec)
       return t.timestamp()
    else: return "mode is not defined"
 #   OnlineUTCTime = datetime.strptime(internettime.strip())
 #   return OnlineUTCTime


if __name__ == "__main__":
 #   foldersStat = namedtuple("foldersStat", "tempFolder num")  # a tuple (tempfoldr-path,
 #   tempfolders= ["C:\\Users\\wn10\\Downloads","C:\\Users\\wn10\\Downloads\\ENVR TAM 160221","C:\\Users\\wn10\\Downloads\\HMH1_20211123_1805"]
 #   status= MakeStatusArray(tempfolders)

 ##  loop on unix-time
   sendingTimeBase = 15 # send every 60s

   t2= getOnlineGMTTime("unixtimesec")
   print("---------  TESTING SENDER IS RUNING    ----------")
   for i in range(350):
       t= getOnlineGMTTime("unixtimesec") # takes about 0.22sec
       if t%sendingTimeBase==0 :
             print ( "tick15",t,i)
            # time.sleep(1)
       else:  time.sleep(0.1)