
from pathlib import Path
import datetime 
import os
import sys , getopt
from colors import Colors
import argparse

#Global variables 
HOMEDIR = str(Path.home())
APPDIR = f'{HOMEDIR}/.todo-cli/'
TODAY = datetime.datetime.now().strftime('%x')
COMMAND = ['add' , 'list' , 'done' , 'alldone']
TODAYNOTE = f'{APPDIR}today'
TODAYDONE = f'{APPDIR}done'
NOTECOUNTER = f'{APPDIR}note_counter'
DONE = []

def check_dir():
    if os.path.exists(APPDIR) == False:
        try : 
            os.makedirs(APPDIR)
            return True
        except OSError : 
            print("Couldn't create directory : "+APPDIR)
            return False 
    else :
        return True

def file_validation() : 

    status = int(read_date())
    if status == 1 :
        create_today()

    global COUNTER 
    COUNTER = counter()

def counter(inc=True):

    if os.path.exists(NOTECOUNTER) :
        f = open(NOTECOUNTER , 'r')
        t = f.readline()
        f.close()
        if inc : 
            c = int(str.rstrip(t)) + 1
            f = open(NOTECOUNTER , 'w')
            f.write(str(c))
            f.close()
            return  c 
        else :
            return int(str.rstrip(t))
    else :
        f = open(NOTECOUNTER , 'w')
        f.write(str(1))
        f.close()
        return 1 

def done_items(): 
    file = open(TODAYDONE , 'r')
    while True : 
        num = file.readline()
        if num == '':
            break 
        DONE.append(int(num))
    file.close()

def create_today():
    file = open(TODAYNOTE , 'w')
    file.write(TODAY+"\n")
    file.close()

    file = open(TODAYDONE , 'w')
    file.writelines([])
    file.close()

    if os.path.exists(NOTECOUNTER):
        os.remove(NOTECOUNTER)

def write_file(text):
    file = open(TODAYNOTE , 'a')
    file.write(str(COUNTER)+" "+text+"\n")
    file.close()
    print("OK")

def read_file(all=True , complete = False , undone = False):
    if not os.path.exists(TODAYNOTE):
        print("There is nothing to show . Use -n to add new item")
        return 
    done_items()
    file = open(TODAYNOTE , 'r')
    today_header = f'\n——— {TODAY} ———\n'
    print(today_header)
    total = 0 
    counter = 0
    file.seek(9)
    while(1):
        line = file.readline()
        num = line.split(" ")[0]
        if( line == ''):
            break;
        counter +=1 
        if int(num) in DONE and (complete == True or all == True )  : 
            print(Colors.CROSSED+" "+line + Colors.END , end="")
        elif all == True or undone == True and counter not in DONE: 
            print(" "+line,end="")
        total +=1 
    today_footer = f'\n——— total {total} ———\n'
    print(today_footer)
    file.close()

def done(nums):
    print(f'{nums} marked as done.')
    file = open(TODAYDONE , 'a')
    for num in nums:
        file.writelines(num+"\n")
    file.close()

def undone(nums):
    file = open(TODAYDONE , 'r')
    lines = file.readlines()
    file.close()
    for num in nums :
        try:
            index = lines.index(nums[0]+'\n')
        except ValueError : 
            print("selected item is not marked as completed")
        del(lines[index])
        print(f'{num} is undone now')

    file = open(TODAYDONE , 'w')
    file.writelines(lines)
    file.close()

def read_date():
    try:
        file = open(TODAYNOTE , 'r')
    except FileNotFoundError :
        return 1 

    line = file.readline()
    file.close()

    if TODAY in  line : 
        return 0 
    else :
        return 1

def remove_items(nums):
    file = open(TODAYNOTE , 'r')
    lines = file.readlines()
    file.close()

    for num in nums : 
        num = int(num)
        item = lines[num].split(" ")
        if num == int(item[0]):
            del(lines[num])
            print("selected item {num} deleted")
        else :
            print("selected item {num} dosen't exist")
    file = open(TODAYNOTE , 'w')
    file.writelines(lines)
    file.close()
    
def main(argv):

    if check_dir() == False :
        sys.exit(2)

    #
    # command line arguments 
    #
    parser = argparse.ArgumentParser(description='Create to-do and shopping list' , usage='''note <command> [<args>]''')
    parser.add_argument('-n' , help='create new item in today list' , nargs='+')
    parser.add_argument('-l' , help='list all the items in today list' , nargs='?' , default='0' ,  const='1')
    parser.add_argument('-d' , help='mark selected items as done ' , nargs='+')
    parser.add_argument('-a' , help='using with -l make the list to present all the items of todo list . Default mode for -l option' , action='store_true' , default=True)
    parser.add_argument('-c' , help="using with -l make the list to present only completed items " , action='store_true')
    parser.add_argument('-u' , help='using with -l make the list to present only uncompleted items' , action='store_true')
    parser.add_argument('-r' , help='removes the items form todo list' , nargs='+')
    parser.add_argument('-x' , help='make selected items mark as undone if its make done ' , nargs='+' )

    #
    # parsing arguments 
    #
    args = parser.parse_args()
    new_arg = args.n 
    list_arg = args.l 
    done_arg = args.d 
    undone_arg = args.x
    remove_arg = args.r

    #
    # each argument instructions 
    #
    if new_arg is not None : 
        message = ' '.join(new_arg)
        file_validation()
        write_file(message)
    
    if '1' in list_arg : 
        if args.c is True or args.u is True : 
            args.a = False 
        read_file(all=args.a , complete=args.c , undone=args.u)

    elif 'u' in list_arg or 'a' in list_arg or 'c' in list_arg :
        list_arg = split(list_arg)
        a = False 
        c = False 
        u = False 
        if 'a' in list_arg: 
            a = True 
        elif 'c' in list_arg:
            c = True 
        elif 'u' in list_arg:
            u = True

        read_file(all=a , complete=c , undone=u)
   
    if done_arg is not None : 
        done(done_arg)
    
    if undone_arg is not None : 
        undone(undone_arg)
        read_file()

    if remove_arg is not None : 
        remove_items(remove_arg)

def split(word):
    return [char for char in word]