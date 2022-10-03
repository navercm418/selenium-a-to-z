from myutils import zvFileUtil
from subprocess import Popen, PIPE, STDOUT


zvFileName = 'names_list2.txt'
zvTown = 'bedford'
zvName = ''

zvNameLst = zvFileUtil(zvFileName, 'r')
zvNameLst = zvNameLst.splitlines()

for n in zvNameLst:

    zvName = n

    # python3 AtoZ.py tabayoyong randolph Massachusetts --headless log-level=3
    cmd = r'C:\Users\amcc4\AppData\Local\Programs\Python\Python39\python.exe AtoZ.py '+ zvName +' '+ zvTown +' Massachusetts --headless log-level=3'
    print(cmd)
    prc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    prc.wait()