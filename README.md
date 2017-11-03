# SpiTest

SpiTest is a framework to perform testing using log file analysis.
Using our framework you can dynamically and semantically parse your log using a simple API.
## Quick Start

live  test examples :
  - Java chat example (below).
  - [Restaurant mobile App](https://github.com/nsvir/logTest/wiki/Testing-a-mobile-App).

## Getting Started
### Example

We will get you through this [chat application example](https://repl.it/Ndgo/2)

To simplify our example we will strip the log of the timestamps.

Client log  |  Server log
--|--
`Connecting to localhost on port 7520...`|`Server Listening on port : 7520`
`Connected to localhost/127.0.0.1:7520`|`Connected to /127.0.0.1:60174`
`[ Sent ] Hello`|`[ Received ] Hello`
`[ Received ] Hello`|`[ noise log ]`
`[ Sent ] ACK`|`[ noise log ]`
`[ Received ] DATA1`|`[ noise log ]`
`[ Sent ] ACK`|`[ noise log ]`
`[ Sent ] DATA2`|`[ Sent ] Hello`
`[ Received ] ACK`|`[ Received ] ACK`
`[ Sent ] Disconnecting`|`[ Sent ] DATA1`
`[ Received ] ACK`|`[ Received ] ACK`
`[ Disconnected ]`|  `[ Received ] DATA2`
  `[ noise log ]` |`[ Sent ] ACK`
  `[ noise log ]` |`[ Received ] Disconnecting`
  `[ noise log ]` |`[ Sent ] ACK`
  `[ noise log ]` |`[ Disconnected ]`

1. Testing a simple scenario :
```python
def testSimpleChatScenario():
    scenario("Testing Simple chat application")
    client = Agent("Client", "client.log")
    server = Agent("Server" ,"server.log")

    connect(client, server)#Start connection session (semantic operation)
    _send(server, "DATA1", client)
    _send(client, "DATA2", server)
    disconnect()#End the connection session
    #verify() unnecessary, I prefer to omit this, and do it as a hooker after each scenario
```
2. Defining the connect method (semantic method):
```python
def connect(client, server):#override
    _send(client, "Hello", server)
    _send(server, "Hello", client)
    _send(client, "ACK", server)
```
2. Defining the disconnect method (semantic method):
```python
def disconnect(client, server):#override
    _send(client, "Disconnecting", server)
    _send(server, "ACK", client)
    server.expect("Disconnected")
    client.expect("Disconnected")
```
3. If you are wondering what are the main bricks the developer has to use, well they are `send` and `receive` :
```python
def _send(a1, message, a2):
    behavior("Message: %s, is sent" % message)#define a semantic to the added behavior
    a1.send(message, a2);#if error: message from n1 to n2 failed to be sent
    a2.receive(message, a1, 2000);
```
4. To parse the log, The developer must define `send` as an action:
```python
def send(message):#override: define a semantic send
    expect("[ Sent ] " + message)#if error, show: Message $message was not sent between $self.source and $self.target.
```
4. The developer must define `receive` as an event :
```python
def receive(message, timeout):#override: define a semantic receive
    wait("[ Received ] " + message, timeout)#if error, show: Message: $message  between $self.source and $self.target, was not received after $timeout ms.
```

### How does it work
Following are the bricks you need to build upon our framework.

You need ?  |  Syntax |  Meaning
--|---|--
Information  | expect/extract  |  expect a `string` or parse one. An action with a `timestamp`
Event  |  wait |  wait for an `Event` for some `timeouts`, the first raises a `warning` and the second raises an `error`
Message  | send/receive  |  send or receive a message between two `Agents`
Agent  |  Agent |  an agent that executes actions and send messages
Session  | connect/disconnect  |  a connection between two agents (semantic word)
Interactive  | ping/pong  |  a `ping` action that requires a `pong` after a `timeout` (same as wait).

### To Do
1.  Add `timestamp` handling to the framework, along with `timeout` syntax.
2. Add a single `Agent` example.
3. Respect the event/action order between the `Agents`
4. Pass the equals function : for example `grep`, instead of just `==`.
5. Add `extract` syntax to the framework, [examples](https://stackoverflow.com/questions/6260777/python-regex-to-parse-string-and-return-tuple):
    * Using `map(strip,split) => select`.
    * Using `regex => match => group`.
6. Pass the `extract` map/filter functions.
7. Add `Async` functions.
8. Add multiple `Agent` per `LogFile`.
9. Add **performance profiling** for each scenario.
10. Reconstruct the same function that had written the log, ex: `log.debug()`.
11. Build the test file from the code source, for each agent.
12. Propose a general log format, that can be parsed directly, ex:`apache`, or:
  * `timestamp` => `Agent` => `Action`/`Event`/`Async` => `Data[]`.
  * One log per function (for automatic code source parsing).
13. Define p2p specific operations to handle its semantic **As a plugin**. Check several properties for each Agent : `connect`, `disconnect`, `subscribe`, `publish`,`join` and `leave`.
14. Define Ui/User specific operations **As a plugin**, `press`, `see`,`lock`,`text`.
15. Report graphic interactions between agents.
16. Get a snapshot of the system at a given time/operation (Realtime state diagram).
