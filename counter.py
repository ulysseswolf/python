#ps -ef | python3 couter.py 

import sys

counter = 0
while 1:
    line = sys.stdin.readline()
    if not line:
        break
    counter += 1
    print("{0}: {1}".format(counter, line))


for i, line in enumerate(sys.stdin):
    print("{0}: {1}".format(i, line))
