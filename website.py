#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, json, bson, urllib
from bottle import route, run, request, response, abort, template, redirect
from bson.objectid import ObjectId
from daemon import Daemon

bottle.TEMPLATE_PATH.insert(0,'/doneit/views/')

@route('/', method='GET')
def get_homepage():
    if doneit.check_login(request):
        return template('home')
    else:
        redirect("/login?ret=/")

@route('/login', method='GET')
def login():
    return template('login')

@route('/login', method='POST')
def login():
    if doneit.login(request.forms.get('email'), request.forms.get('password')):
        user_id = doneit.get_id_by_email(request.forms.get('email'))
        response.set_cookie("_id", str(user_id))
        response.set_cookie("session", doneit.new_session(str(user_id)))
        redirect("//%s" % (request.query.ret))
    else:
        redirect("/login?failed=true")

@route('/users', method='GET')
def get_users():
    entity = doneit.get_all('users')
    return template('users', users=entity)

@route('/users/add', method='GET')
def add_users():
    entity = doneit.get_all('projects')
    return template('users_add', projects=entity)

@route('/users/add', method='POST')
def add_users():
    entity = dict()
    for field in ['name', 'email', 'password', 'daily-digest']:
        entity[field] = request.forms.get(field)
    entity['project_id'] = ObjectId(request.forms.get('project'))
    _id = doneit.save('users', entity)
    redirect("/users/%s" % (_id))

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
