#!/usr/bin/python

import web, sys, time
from daemon import Daemon

class hello:
    def GET(self):
        return 'Hello, world!'

class MyDaemon(Daemon):
    def run(self):
        sys.argv[1] = '80'
        urls = ("/.*", "hello")
        app = web.application(urls, globals())
        app.run()

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
