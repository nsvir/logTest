from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from tools.fancy import printOk, printFail

LogFailure = lambda  *args : None
LogSuccess = lambda  *args : None
LogInfo = lambda *args : None

class AssertFailedException(Exception):
    pass

class Application:

    def __init__(self, elastic=None):
        self.logAgent = []
        self.errors = []
        self.elastic = elastic
        if self.elastic is None:
            self.elastic = {
                'host': 'spirana.lille.inria.fr',
                'port': '80',
                'index': "chat"
            }
        self.client = Elasticsearch([self.elastic])
        self.search = Search(using=self.client, index=self.elastic["index"])

    def register(self, logAgent):
        self.logAgent.append(logAgent)

    def verify(self):
        for logAgent in self.logAgent:
            try:
                logAgent.verify(self.search)
            except AssertFailedException as e:
                self.errors.append({"agent": logAgent.agent})
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
            myprint("Agent: {0}\n".format(error["agent"]))
        LogInfo("\n")

