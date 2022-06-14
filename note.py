
from pathlib import Path
import datetime 
import os
import sys , getopt
from colors import Colors
import argparse
from commands import Command

#Global variables 
HOMEDIR = str(Path.home())
APPDIR = f'{HOMEDIR}/.todo-cli/'
TODAY = datetime.datetime.now().strftime('%x')
COMMAND = ['add' , 'list' , 'done' , 'alldone']
TODAYNOTE = f'{APPDIR}today'
TODAYDONE = f'{APPDIR}done'
NOTECOUNTER = f'{APPDIR}note_counter'
DONE = []

def parseCommand(cmds):
    command = Command(None)
    
    check_list_name = getCheckListName(cmds)
    if check_list_name == '':
        check_list_name = 'today'
    
    command = getCommandFrom(cmds)

    return check_list_name ,command ; 

def getCheckListName(cmds):
    checklist = ''
    for c in cmds : 
        if Command.recognizeCommand(c) is not None:
            break
        checklist += c + ' '
    return checklist.strip()

def getCommandFrom(cmds):
    cm = None
    value = ''
    for c in range(len(cmds)): 
        if cm is None: 
            cm = Command.recognizeCommand(cmds[c])
        else: 
            value += cmds[c] + ' '
        c+=1
    if cm is None: 
        cm = Command.SHW
    return cm , value.strip()
        


def runCommands(checklist , command ):
    output_message = ''
    cmd = command[0]
    value = command[1]

    if cmd == Command.SHW: 
        showList(checklist)
    elif cmd == Command.NEW: 
        newCheckList(checklist)
    elif cmd == Command.ADD: 
        addNewItem(checklist, value)
    elif cmd == Command.DEL: 
        delCheckList(checklist)
    elif cmd == Command.REM:
        removeItem(checklist , value)
    elif cmd == Command.DON: 
        doneItem(checklist , value)
    else: 
        raise ValueError()
    
    return 
def showList(name):
    lines  = read_file(name)
    print(colorizeForMe(lines))
def colorizeForMe(text):
    output = ''
    output += f'\n{Colors.YELLOW}------ {text[0].strip()} ------\n'
    for line in text[1:]:
        if line[0] == '*':
            output += f'{Colors.GREEN}   ■   {Colors.CROSSED}{line[1:]}{Colors.END}'
        else: 
            output += f'   □   {line}'
    return output
def newCheckList(name):
    createFile(name)
def addNewItem(name , item):
    write_file(name, item)
def delCheckList(name):
    if name == 'today':
        print('today checklist can not be removed')
        return 
    delFile(f'{APPDIR}{name}')
def doneItem(name , item):
    item = int(item)
    lines = read_file(name) 
    lines[item] = '*' + lines[item]
    write_file(name, lines , mode='w')
def removeItem(name , item):
    pass
def createFile(name):
    try:
        file = open(f'{APPDIR}{name}' , 'w')
        file.write(name+'\n')
        file.close()
    except Exception():
        tb = sys.exc_info()[2]
        # raise OtherException(...).with_traceback(tb)
def delFile(name):
    if os.path.exists(name):
        os.remove(name)
    else:
        raise FileExistsError()
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

def write_file(name , text ,  mode='a'):
    file = open(f'{APPDIR}{name}' , mode)
    if mode == 'w':
        file.writelines(text)
    else: 
        file.write(text+"\n")
    file.close()
    print("OK")

def read_file(name):
    if not os.path.exists(f'{APPDIR}{name}'):
        print("There is nothing to show.")
        return 
    file = open(f'{APPDIR}{name}' , 'r')
    data = file.readlines()
    file.close()
    return data

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
    parser = argparse.ArgumentParser(description='Create to-do and shopping list (the today checklist is by default ) ' , usage='''note [LISTNAME] [COMMAND]... [OPTION]...''')
    parser.add_argument('commands' , help='<listname> <new-add-del-rem-don>' ,default='today' ,nargs='+')
    parser.add_argument('-n' , help='create new item in today check list' , nargs='+')
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
    commands = args.commands
    new_arg = args.n 
    list_arg = args.l 
    done_arg = args.d 
    undone_arg = args.x
    remove_arg = args.r

    #
    # each argument instructions 
    #
    parsed_commands = parseCommand(commands)
    # print(parsed_commands)
    runCommands(parsed_commands[0] , parsed_commands[1])
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