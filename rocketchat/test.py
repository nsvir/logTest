import sys
from SpiralsLogTest import Application
from LogAgent import LogAgent
from tools.fancy import Log

# Application
#     \/
#  Behaviors
#     \/
#   Action
#     \/
#    Log

# This class defines the expected Logs from Actions
class ChatLogFile(LogAgent):

    def received(self, message):
        self.expect("[ Received ] " + message)

    def sent(self, message):
        self.expect("[ Sent ] " + message)

    def log(self, message):
        self.expect("[ " + message + " ]")


# Application defines the expected Actions from Behaviors
class Chat(Application):

    def __init__(self):
        super().__init__()
        self.client = ChatLogFile("Client")
        self.server = ChatLogFile("Server")
        self.register(self.client)
        self.register(self.server)

    def _send(self, n1, message, n2):
        n1.sent(message);
        n2.received(message);

    def _sendData(self, n1, data, n2):
        self._send(n1, data, n2)
        self._send(n2, "ACK", n1)

    def connectClient(self):
        self._send(self.client, "Hello", self.server)
        self._send(self.server, "Hello", self.client)
        self._send(self.client, "ACK", self.server)

    def disconnectClient(self):
        self._send(self.client, "Disconnecting", self.server)
        self._send(self.server, "ACK", self.client)
        self.server.log("Disconnected")
        self.client.log("Disconnected")

    def sendToClient(self, data):
        self._sendData(self.server, data, self.client)

    def sendToServer(self, data):
        self._sendData(self.client, data, self.server)

# Testing application sequence of behaviors
def testSuccess():
    chat = Chat()

    chat.connectClient()
    chat.sendToClient("DATA1")
    chat.sendToServer("DATA2")
    chat.disconnectClient()
    chat.verify()

def testFailure():
    chat = Chat()

    chat.connectClient()
    chat.sendToClient("DATA1")
    chat.sendToServer("DATA2")
    chat.disconnectClient()
    chat.verify()


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == "-v"):
        SpiralsLogTest.LogSuccess = Log.Success
        SpiralsLogTest.LogInfo = Log.Info
        SpiralsLogTest.LogFailure = Log.Failure
    print("--- Test n1 ---")
    testSuccess()
    print("--- Test n2 ---")
    testFailure()
