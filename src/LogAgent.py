from SpiralsLogTest import AssertFailedException
from tools.fancy import printFail, printOk


def _print_result(logs, printer):
    for log in logs:
        printer("- {}: [{}]{}".format(log["timestamp"], log.agent, log["message"]))


class LogAgent(object):

    def __init__(self, agent):
        self.agent = agent
        self.expectedList = []

    def expect(self, expected):
        self.expectedList.append(expected)

    def _verifyLogFile(self, search):
        timestamp_cursor = "2017.12.22-17.48.49.643"
        for expectedLine in self.expectedList:
            s = search
            if timestamp_cursor is not None:
                s = s.filter("range", timestamp={'gte': timestamp_cursor})
            s = s.sort("timestamp")
            debuging = s
            s = s.filter("match_phrase", agent=self.agent)
            s = s.filter("match_phrase", message=expectedLine)
            results = s.execute()
            if len(results) == 0:
                _print_result(debuging.execute(), printer=printFail)
                raise AssertFailedException
            log = results[0]
            timestamp_cursor = log["timestamp"]
            printOk("- {}: [{}]{}".format(log["timestamp"], log.agent, log["message"]))

    def verify(self, search):
        try:
            self._verifyLogFile(search)
        except FileNotFoundError as e:
            printFail(e)
            raise e
