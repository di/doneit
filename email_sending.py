#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, requests, json, bson, urllib, datetime, pytz
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson.objectid import ObjectId
from daemon import Daemon

@route('/', method='POST')
def email_digest():
    doneit.log("Sending digest for %s at %s" % (request.forms.get('name'), request.forms.get('email')))
    r = requests.get("%s/%s" % (doneit.digest_composition_service_url, request.forms.get('project_id')))

class MyDaemon(Daemon):
    def run(self):
        run(host=doneit.email_sending_service_host, port=doneit.email_sending_service_port, debug=True)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/email_sending.pid')
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
