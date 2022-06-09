
import argparse as ap
import sys

argparser = ap.ArgumentParser(description="adjksdns")
argparser.add_argument("-kmar", action="store",
                           dest="kmar", required=True, type=int,
                           help="the arguments")

kmars = ap.kmar

path = '/students/2021-2022/master/Rients_DSLS/output/'
    
with open(path + kmars +'/Log') as file:
#with open('Assignment4/directory/Log') as file:
    for row in file:
        if 'n50' in row:
            row_use = row


row_use = row_use.split()
nr = row_use[8]
nr = nr.replace(',','')
sys.stdout.write(f"{kmars}, {nr}\n")

#final_max = max(n50, key=n50.get)

