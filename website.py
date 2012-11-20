#!/usr/bin/python

import sys, time, json, bottle
from bottle import route, run, request, abort
from daemon import Daemon

@route('/', method='GET')
def get_homepage():
    return 'Hello, world!'

class MyDaemon(Daemon):
    def run(self):
        run(host='doneit.cs.drexel.edu', port=80)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/doneit.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
