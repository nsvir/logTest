from tools.fancy import printOk, printFail

LogFailure = lambda  *args : None
LogSuccess = lambda  *args : None
LogInfo = lambda *args : None

class AssertFailedException(Exception):
    pass

class Application:

    def __init__(self):
        self.logFiles = []

    def register(self, logFile):
        self.logFiles.append(logFile)

    def verify(self):
        successLogs = 0
        errors = []
        for logFile in self.logFiles:
            try:
                logFile.verify()
                successLogs += 1
            except AssertFailedException as e:
                errors.append({"file": logFile.fileName, "args": e.args})
        LogInfo("\nSummary:\n")
        myprint = printOk if (len(errors) == 0) else printFail
        myprint("Success: {0}\tFailed: {1}\t Total: {2}\n".format(
            successLogs,
            len(self.logFiles) - successLogs,
            len(self.logFiles)))
        for error in errors:
            myprint("{0}: Expected '{1}' from line n°{2} to the end of file\n".format(
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
        global LogSuccess
        global LogInfo
        LogInfo("Testing: {0}\n".format(self.fileName))
        fileStream = open(self.fileName, 'r')
        lineIndex = 0
        lastLine = 0
        for expectedLine in self.expectedList:
            for line in fileStream:
                lineIndex += 1
                if (line[:-1] == expectedLine):
                    LogSuccess("{0}:{1}".format(lineIndex, line))
                    lastLine = lineIndex
                    break # Go to next expected item
            else:
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

