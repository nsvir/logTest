import random, string, sys

def randomString(length):
    return "[ Noise ] " + ''.join(random.choice(string.ascii_letters) for i in range(length))

f = open(sys.argv[1], 'r')
for line in f:
    print('\n'.join(randomString(random.choice(range(80))) for i in range(random.choice(range(5)))))
    print(line, end='')
