#!/usr/bin/python

import sys, time, bottle, pymongo, bson
from bottle import route, run, request, abort, template
from bson.objectid import ObjectId
from pymongo import Connection
from daemon import Daemon

bottle.TEMPLATE_PATH.insert(0,'/doneit/views/')
db = Connection('localhost', 27017).doneit

def get_by_id(collection, _id):
    return db[collection].find_one({"_id": ObjectId(_id)})

def get_tasks(task_type, project_id):
    return db['tasks'].find({"project_id": ObjectId(project_id), "type": task_type})

@route('/', method='GET')
def get_homepage():
    return 'Hello, world!'

@route('/projects', method='GET')
def get_projects():
    entity = db['projects'].find()
    return template('projects', projects=entity)

@route('/projects/:id', method='GET')
def get_project(id):
    entity = db['projects'].find_one({"_id": ObjectId(id)})
    entity['admin'] = get_by_id("users", entity['admin_id'])
    entity['done'] = get_tasks("done", entity['_id'])
    entity['todo'] = get_tasks("todo", entity['_id'])
    entity['block'] = get_tasks("block", entity['_id'])
    return template('project', project=entity)

class MyDaemon(Daemon):
    def run(self):
        db = Connection('localhost', 27017).mydatabase
        run(host='doneit.cs.drexel.edu', port=80, debug=True)

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
