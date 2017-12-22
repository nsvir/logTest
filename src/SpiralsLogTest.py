from tools.fancy import printOk, printFail

LogFailure = lambda  *args : None
LogSuccess = lambda  *args : None
LogInfo = lambda *args : None

class AssertFailedException(Exception):
    pass

class Application:

    def __init__(self):
        self.logFiles = []
        self.errors = []

    def register(self, logFile):
        self.logFiles.append(logFile)

    def verify(self):
        for logFile in self.logFiles:
            try:
                logFile.verify()
            except AssertFailedException as e:
                self.errors.append({"file": logFile.fileName, "args": e.args})
        self._printResult()

    def _printResult(self):
        LogInfo("\nSummary:\n")
        total = len(self.logFiles)
        failure = len(self.errors)
        success = total - failure
        myprint = printOk if failure == 0 else printFail
        myprint("Success: {0}\tFailed: {1}\t Total: {2}\n".format(
            success,
            failure,
            total))
        for error in self.errors:
            myprint("{0}: Expected '{1}' from line n{2} to the end of file\n".format(
                error["file"],
                error["args"][0],
                error["args"][1]))
        LogInfo("\n")

class LogFile(object):

    def __init__(self, fileName):
        self.fileName = fileName
        self.expectedList = []

    def expect(self, expected):
        self.expectedList.append(expected)

    def _verifyLogFile(self):
        fileStream = open(self.fileName, 'r')
        lineIndex = lastLine = 1
        LogInfo("Testing: {0}\n".format(self.fileName))
        for expectedLine in self.expectedList:
            for line in fileStream:
                lineIndex += 1
                if (line[:-1] == expectedLine):
                    LogSuccess("{0}:{1}".format(lineIndex, line))
                    lastLine = lineIndex
                    break # Go to next expected item
            else: # End of file reached but expected line not find
                LogFailure("{0}\n".format(expectedLine))
                fileStream.close()
                raise AssertFailedException(expectedLine, lastLine)
        fileStream.close()

    def verify(self):
        try:
            self._verifyLogFile()
        except FileNotFoundError as e:
            printFail(e)
            raise e
