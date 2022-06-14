from enum import Enum
class Command(Enum):
    NEW = 0  
    ADD = 1 
    DEL = 2  
    REM = 3 
    DON = 4 

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
        else: 
            return None

    @classmethod
    def _missing_(cls , value):
        return cls.NEW

