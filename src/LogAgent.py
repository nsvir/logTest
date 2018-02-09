
class LogAgent(object):

    def get_expected_list(self):
        raise NotImplementedError

    def notify_match_expected(self, timestamp, log):
        raise NotImplementedError

    def notify_not_match(self, timestamp):
        raise NotImplementedError
