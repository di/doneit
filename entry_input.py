#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, requests, json, bson, urllib, datetime, pytz
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson.objectid import ObjectId
from daemon import Daemon

@route('/task', method='POST')
def task_input():
    request.forms['user_id'] = ObjectId(request.forms['user_id'])
    request.forms['project_id'] = ObjectId(request.forms['project_id'])
    request.forms['date'] = datetime.datetime.utcnow()
    _id = doneit.add_task(dict(request.forms))
    return {'status':'success', '_id':str(_id)}

class MyDaemon(Daemon):
    def run(self):
        run(host=doneit.entry_input_service_host, port=doneit.entry_input_service_port, debug=True)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/entry_input.pid', stderr='/var/log/entry_input.log')
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
