from tools.fancy import printFail


class LogAgent(object):

    def __init__(self, agent):
        self.agent = agent
        self.expectedList = []

    def expect(self, expected):
        self.expectedList.append(expected)

    def _verifyLogFile(self):
        for expectedLine in self.expectedList:
            pass

    def verify(self):
        try:
            self._verifyLogFile()
        except FileNotFoundError as e:
            printFail(e)
            raise e
