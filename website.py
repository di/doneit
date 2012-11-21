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
    entity = doneit.get_all('users')
    return template('users', users=entity)

@route('/users/:id', method='GET')
def get_user(id):
    entity = doneit.get_by_id('users', id)
    return template('user', user=entity)

@route('/projects', method='GET')
def get_projects():
    entity = doneit.get_all('projects')
    return template('projects', projects=entity)

@route('/projects/:id', method='GET')
def get_project(id):
    entity = doneit.get_by_id('projects', id)
    entity['admin'] = doneit.get_by_id("users", entity['admin_id'])
    for task_type in ['done', 'todo', 'block', 'doing']:
        entity[task_type] = doneit.get_tasks(task_type, entity['_id'])
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
