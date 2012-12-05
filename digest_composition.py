#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, json, bson, urllib, datetime, pytz
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson import json_util
from bson.objectid import ObjectId
from daemon import Daemon

@route('/:project_id', method='GET')
def digest_composition(project_id):
    project = doneit.get_by_id('projects', project_id)

    timezone = pytz.timezone('US/Eastern')
    if request.query.date:
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(request.query.date, doneit.date_format_url)))
    else:
        date = datetime.datetime.now(timezone).replace(hour=0,minute=0,second=0,microsecond=0).astimezone(pytz.utc) # midnight today

    doneit.log("Digest requested for %s as of %s" % (project['name'], date))

    response = {'status':'success', 'tasks':{'done':[], 'todo':[], 'block':[], 'doing':[]}}
    for task_type in response['tasks']:
        task_list = doneit.get_tasks(task_type, project['_id'], date)
        response['tasks'][task_type] = json_util.dumps(task_list)

    return response

class MyDaemon(Daemon):
    def run(self):
        run(host=doneit.digest_composition_service_host, port=doneit.digest_composition_service_port, debug=True)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/digest_composition.pid', stderr='/var/log/digest_composition.log')
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
