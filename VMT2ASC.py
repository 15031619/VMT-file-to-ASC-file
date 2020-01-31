# coding: utf-8

"""

author:Wang.Shilong  

March 10th 2019 in Changchun
it can convert the VMT file (the ODIS trace file) to ASC file(it can be used by CANOE).
VER 1.0 
March 12th 2019 in Changchun change the date format

VER 2.0
read VMT file automatic

VER 2.0
change time to BeiJing  time

"""
import time
import os

def timestamp_datetime(value):
    format = "date %a %b %d %I:%M:%S %p %Y"    
    value = time.localtime(value-28800)
    dt = time.strftime(format, value)
    return dt


def readAndTranform(fullpathname):	
    x = []
    x1 = []
    y =[]
    trace =[]
    

    #the fisrt line to read and analysis#
    f = open(fullpathname, 'r')
    line= f.readline() 
    x1 = line.split()

    #read the linux time and transform the tpye to asc standard#
    logtime = timestamp_datetime(int(x1[0])/1000000)
    y.append(int(x1[0]))        
    x1[0]="0.000000"
    x1[1]="1"

    #for the ID transform#
    if x1[2][1] is "0":
        x1[2]=x1[2].lstrip('0')
    else:
        x1[2]=x1[2]+"x"

    x1[3]="RX D"
    x1.remove("|")
    trace.append(x1)
    #print(trace)

    #analyze all the file#
    line = f.readline()

    while line: 
        x = line.split()
        y.append(int(x[0]))
        #print(y[-1])
        x[0]=str((int(x[0])-y[-2])/1000000)
        x[1]="1"
        if x[2][1] is "0":
            x[2]=x[2].lstrip('0')
        else:
            x[2]=x[2]+"x"
        x[3]="RX D"
        x.remove("|")
        trace.append(x)
        line = f.readline() 
  
    f.close()
    return logtime,trace

def saveAscFile(logtime,trace,fullpathname):  
    #print(s)
  
    outputFileName = fullpathname[0:-4] + ".asc"
    fileObject = open(outputFileName, 'w')   #creat write files
    fileObject.write(logtime) 
    fileObject.write("\nbase hex timestamps relative\nNO internal events logged \n \n" ) 

    for ip in trace:
        for data in ip:
            fileObject.write(data)  
            fileObject.write(' ')
        fileObject.write('\n')  
    fileObject.close()  

if __name__ == "__main__":
    cwd=os.getcwd()
    files = os.listdir(cwd)
    vmtFiles = [f for f in files if f.endswith((".vmt"))]
    #print(vmtFiles)
    for vmtFile in vmtFiles:
        
        #fullpathname=os.path.join(cwd, vmtFile)
        fullpathname=vmtFile
        print(fullpathname)
        logtime,trace=readAndTranform(fullpathname)
        saveAscFile(logtime,trace,fullpathname)

