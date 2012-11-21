#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, bson
from bottle import route, run, request, abort, template
from bson.objectid import ObjectId
from daemon import Daemon

bottle.TEMPLATE_PATH.insert(0,'/doneit/views/')

@route('/', method='GET')
def get_homepage():
    return template('home')

@route('/users', method='GET')
def get_users():
    entity = doneit.db['users'].find()
    return template('users', users=entity)

@route('/users/:id', method='GET')
def get_user(id):
    entity = doneit.db['users'].find_one({"_id": ObjectId(id)})
    return template('user', user=entity)

@route('/projects', method='GET')
def get_projects():
    entity = doneit.db['projects'].find()
    return template('projects', projects=entity)

@route('/projects/:id', method='GET')
def get_project(id):
    entity = doneit.db['projects'].find_one({"_id": ObjectId(id)})
    entity['admin'] = doneit.get_by_id("users", entity['admin_id'])
    entity['done'] = doneit.get_tasks("done", entity['_id'])
    entity['todo'] = doneit.get_tasks("todo", entity['_id'])
    entity['block'] = doneit.get_tasks("block", entity['_id'])
    return template('project', project=entity)

class MyDaemon(Daemon):
    def run(self):
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
