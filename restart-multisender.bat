cd C:\multisender2.2
del stop.conf
echo stopFlag=1 >> stop.conf
cls
echo off
echo ==================================================       
echo =                                                                            
echo =           Multisender2.2  will be stoped                    
echo =                                                                            
echo ====================================================       

timeout 20



taskkill /IM py.exe /F
cd C:\multisender2.2
runpy.bat
