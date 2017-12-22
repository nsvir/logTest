from tools.fancy import printOk, printFail

LogFailure = lambda  *args : None
LogSuccess = lambda  *args : None
LogInfo = lambda *args : None

class AssertFailedException(Exception):
    pass

class Application:

    def __init__(self):
        self.logAgent = []
        self.errors = []

    def register(self, logAgent):
        self.logAgent.append(logAgent)

    def verify(self):
        for logAgent in self.logAgent:
            try:
                logAgent.verify()
            except AssertFailedException as e:
                self.errors.append({"Agent": logAgent.agent})
        self._printResult()

    def _printResult(self):
        LogInfo("\nSummary:\n")
        total = len(self.logAgent)
        failure = len(self.errors)
        success = total - failure
        myprint = printOk if failure == 0 else printFail
        myprint("Success: {0}\tFailed: {1}\t Total: {2}\n".format(
            success,
            failure,
            total))
        for error in self.errors:
            myprint("Agent: {0}\n".format(error["file"]))
        LogInfo("\n")

