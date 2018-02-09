from typing import List

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from tools.fancy import printOk, printFail

LogFailure = lambda *args: None
LogSuccess = lambda *args: None
LogInfo = lambda *args: None


class AssertFailedException(Exception):
    pass


def get_expected_list(log_agents):
    result = []
    for agent in log_agents:
        for expected in agent.get_expected_list():
            element = {"agent": agent, "expected": expected}
            result.append(element)
    return result


class SpiralsCore:

    def __init__(self, elastic=None):
        self.timestamp_cursor = None
        self.logAgents = []  # type List[LogAgent]
        self.errors = []
        self.elastic = elastic
        if self.elastic is None:
            self.elastic = {
                'host': 'localhost',
                'port': '9200',
                'index': "logstash-*"
            }
        self.client = Elasticsearch([self.elastic])
        self.search = Search(using=self.client, index=self.elastic["index"])

    def register(self, log_agents):
        self.logAgents.append(log_agents)

    def run(self):
        try:
            while True:
                element_list = get_expected_list(self.logAgents)
                s = self.build_query(element_list)
                results = s.execute()
                if len(results) == 0:
                    timestamp = self.get_oldest_timestamp()
                    for element in element_list:
                        element["agent"].notify_not_match(timestamp)
                    break
                result = results[0]
                log = result["log"]
                timestamp = result["@timestamp"]
                for element in element_list:
                    if element["expected"].lower() in log.lower():
                        element["agent"].notify_match_expected(timestamp, log)
                        print("time: %s, log: %s" % (timestamp, log))
                    else:
                        element["agent"].notify_not_match(timestamp)
                self.timestamp_cursor = result["@timestamp"]
        except AssertFailedException as e:
            print("assert failed", e)
        print("end of run")

    def build_query(self, element_list):
        s = self.search
        s = s.sort("@timestamp")
        expected_match = []
        for element in element_list:
            query_string = Q("query_string",
                             query="log:*%s*" % element["expected"],
                             split_on_whitespace=False,
                             analyze_wildcard=True)
            expected_match.append(query_string)
        #    {"wildcard": {"log": "*%s*" % element["expected"]}})
        s.query = Q('bool', should=expected_match)
        if self.timestamp_cursor is not None:
            s = s.filter("range", **{"@timestamp": {'gt': self.timestamp_cursor}})
        return s

    def _print_result(self):
        LogInfo("\nSummary:\n")
        total = len(self.logAgents)
        failure = len(self.errors)
        success = total - failure
        myprint = printOk if failure == 0 else printFail
        myprint("Success: {0}\tFailed: {1}\t Total: {2}\n".format(
            success,
            failure,
            total))
        for error in self.errors:
            myprint("Agent: {0}\n".format(error["agent"]))
        LogInfo("\n")

    def get_oldest_timestamp(self):
        s = self.search
        s = s.sort("-@timestamp")
        timestamp = s.execute()[0]["@timestamp"]
        return timestamp


def _print_result_log(logs, printer):
    for log in logs:
        printer("- {}: [{}]{}".format(log["timestamp"], log.agent, log["message"]))
