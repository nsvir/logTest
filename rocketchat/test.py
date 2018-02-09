import sys
from datetime import datetime, timedelta

import SpiralsLogTest
from LogAgent import LogAgent
from tools.fancy import Log


class StatusAgent(LogAgent):
    def __init__(self):
        self.is_online = None

    def get_expected_list(self):
        return ["userpresence"]

    def notify_match_expected(self, timestamp, log):
        if "UserPresence:away" in log:
            self.is_online = False
        elif "UserPresence:online" in log:
            self.is_online = True
        else:
            print("Not Handled")

    def notify_not_match(self, timestamp):
        pass


class MessageAgent(LogAgent):
    def __init__(self, agent):
        self.notification_agent = agent

    def get_expected_list(self):
        return ["sendMessage"]

    def notify_match_expected(self, timestamp, log):
        self.notification_agent.sent_message(timestamp)

    def notify_not_match(self, timestamp):
        pass


def to_datetime(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")


class NotificationAgent(LogAgent):
    def __init__(self, agent):
        self.waiting_time = None
        self.status_agent = agent
        self.timeout = timedelta(seconds=5)
        self.waiting_push = False

    def get_expected_list(self):
        return ["send message"]

    def sent_message(self, timestamp):
        if not self.status_agent.is_online:
            self.waiting_push = True
            self.waiting_time = to_datetime(timestamp) + self.timeout

    def notify_match_expected(self, timestamp, log):
        if self.waiting_push is False:
            raise SpiralsLogTest.AssertFailedException("Notification was sent but not expected")
        self.waiting_push = False

    def notify_not_match(self, timestamp):
        if self.waiting_push is True and to_datetime(timestamp) > self.waiting_time:
            raise SpiralsLogTest.AssertFailedException("Notification was not sent but expected")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        SpiralsLogTest.LogSuccess = Log.Success
        SpiralsLogTest.LogInfo = Log.Info
        SpiralsLogTest.LogFailure = Log.Failure
    rocketChat = SpiralsLogTest.SpiralsCore()
    status_agent = StatusAgent()
    notification_agent = NotificationAgent(status_agent)
    message_agent = MessageAgent(notification_agent)
    rocketChat.register(status_agent)
    rocketChat.register(notification_agent)
    rocketChat.register(message_agent)
    rocketChat.run()
