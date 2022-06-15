from enum import Enum
class Command(Enum):
    SHW = 0 
    NEW = 1 
    ADD = 2 
    DEL = 3  
    REM = 4 
    DON = 5 
    LIS = 6 

    def recognizeCommand(c):
        if c == 'new':
            return Command.NEW
        elif c == 'add':
            return Command.ADD
        elif c == 'del':
            return Command.DEL 
        elif c == 'rem':
            return Command.REM
        elif c == 'don':
            return Command.DON
        elif c == 'ls':
            return Command.LIS
        else: 
            return None

    @classmethod
    def _missing_(cls , value):
        return cls.SHW

