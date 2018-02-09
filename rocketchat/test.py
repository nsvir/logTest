import sys

import SpiralsLogTest
from LogAgent import LogAgent
from tools.fancy import Log


class StatusAgent(LogAgent):
    def get_expected_list(self):
        return ["away", "online"]

    def notify_match_expected(self, timestamp, log):
        print("timestamp: %s matched: %s" % (timestamp, log))

    def notify_not_match(self, timestamp):
        print("not matched: %s" % timestamp)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        SpiralsLogTest.LogSuccess = Log.Success
        SpiralsLogTest.LogInfo = Log.Info
        SpiralsLogTest.LogFailure = Log.Failure
    rocketChat = SpiralsLogTest.SpiralsCore()
    status_agent = StatusAgent()
    rocketChat.register(status_agent)
    rocketChat.run()
