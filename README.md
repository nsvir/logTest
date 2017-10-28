# SpiralsLogTest

SpiralsLogTest.py is a framework used to test an application using log file analysis

## QuickStart

`python test.py`

`python test.py -v` to enable verbose mode

`cat test.py`

## How does it works

### Log file generation

1. We have recorded the logs of the java application called "chat"
```
cd chat
cat README.md
...
java Client > ../logs/client.log
```

2. We have injected some noise to the log file `python ./tools/generateNoise.py ./logs/client.log >> ./log/clientFull.log`

3. We have removed an expected line in ./logs/serverError.log

### Creating test.py with SpiralsLogTest framework

`cat test.py`

