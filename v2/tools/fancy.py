class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printOk(message):
    print("{1}{0}{2}\n".format(
          message,
          bcolors.OKGREEN,
          bcolors.ENDC), end="")

def printFail(message):
    print("{1}{0}{2}\n".format(
          message,
          bcolors.FAIL,
          bcolors.ENDC), end="")

class Log:
    Info = lambda *args : print(args[0], end="")
    Success = lambda *args: printOk(args[0])
    Failure = lambda *args: printFail(args[0])

