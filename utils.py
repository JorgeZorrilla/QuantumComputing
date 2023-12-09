
from enum import Enum

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

def print_correct(str):
    print(Colors.GREEN + str + Colors.RESET)

def print_warning(str):
    print(Colors.YELLOW + str + Colors.RESET)

def print_error(str):
    print(Colors.RED + str + Colors.RESET)

def print_section(str):
    print(Colors.BLUE + str + Colors.RESET)

def print_title(str):
    print(Colors.MAGENTA + str + Colors.RESET)

class Log_Level(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3

class Log:
    def __init__(self, log_level) -> None:
        self.log_level = log_level

    def print(self, log_level, str):
        if log_level.value <= self.log_level:
            print(str)

