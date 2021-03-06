#!/usr/bin/python

import doneit
import sys, time, requests, bottle, pymongo, json, bson, urllib, datetime
import random
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson.objectid import ObjectId
from daemon import Daemon
from datetime import timedelta

bottle.TEMPLATE_PATH.insert(0,'/doneit/views/')

@route('/', method='GET')
def get_homepage():
    return template('home', loggedin=check(request))

@route('/login', method='GET')
def login():
    failed = request.query.failed == "true"
    return template('login', loggedin=check(request), failed=failed)

@route('/login', method='POST')
def login():
    if check(request):
        redirect(request.query.ret or "/")
    if doneit.login(request.forms.get('email'), request.forms.get('password')):
        user_id = doneit.get_user_by_email(request.forms.get('email'))['_id']
        response.set_cookie("_id", str(user_id))
        response.set_cookie("session", doneit.new_session(str(user_id)))
        redirect(request.query.ret or "/")
    redirect("/login?failed=true&ret=%s" % (request.query.ret))

@route('/logout', method='GET')
def logout():
    doneit.logout(request)
    redirect("/")

@route('/tasks', method='GET')
def get_tasks():
    if check(request):
        return template('tasks', loggedin=check(request))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/tasks', method='POST')
def post_tasks():
    if check(request):
        entity = dict()
        user_id = request.get_cookie("_id")
        project_id = doneit.get_by_id('users', user_id)["project_id"]
        for field in ['type', 'comment']:
            entity[field] = request.forms.get(field)
        entity['user_id'] = user_id
        entity['project_id'] = project_id
        r = requests.post(doneit.entry_input_service_url + "/task", entity)
        if r.json['status'] == "success":
            redirect("/projects/%s" % (project_id))
        else:
            redirect("/tasks")
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/users', method='GET')
def get_users():
    users = doneit.get_all('users')
    projects = doneit.get_all('projects')
    return template('users', loggedin=check(request), users=users, projects=projects)

@route('/users', method='POST')
def post_users():
    if check(request):
        entity = dict()
        for field in ['name', 'email', 'password', 'reminder-hour', 'alternate-email']:
            entity[field] = request.forms.get(field)
        for field in ['daily-digest', 'reminder-email']:
            entity[field] = (request.forms.get(field) == 'true')
        entity['project_id'] = ObjectId(request.forms.get('project'))
        _id = doneit.add_user(entity)
        redirect("/users/%s" % (_id))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/users/:id', method='GET')
def get_user(id):
    entity = doneit.get_by_id('users', id)
    return template('user', loggedin=check(request), user=entity)

@route('/projects', method='GET')
def get_projects():
    entity = doneit.get_all('projects')
    return template('projects', loggedin=check(request), projects=entity)

@route('/projects', method='POST')
def post_projects():
    if check(request):
        entity = dict()
        for field in ['name', 'description', 'digest-hour']:
            entity[field] = request.forms.get(field)
        entity['admin_id'] = request.get_cookie("_id")
        entity['secret-key'] = "%032x" % random.getrandbits(128)
        _id = doneit.add_project(entity)
        redirect("/projects/%s" % (_id))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/projects/:id', method='GET')
def get_project(id):
    entity = doneit.get_by_id('projects', id)
    entity['admin'] = doneit.get_by_id("users", entity['admin_id'])
    if request.query.date:
        entity['date'] = doneit.timezone.localize(datetime.datetime.fromtimestamp(time.mktime(time.strptime(request.query.date, "%y-%m-%d"))))
    else:
        entity['date'] = doneit.timezone.localize(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)) # midnight today
        if (doneit.timezone.localize(datetime.datetime.now()).hour > int(entity['digest-hour'])):
            # Cutoff has already passed for today
            entity['date'] = entity['date'] + timedelta(days=1)

    # Offset date based on when digest is sent (plus a magic number)
    entity['date'] = entity['date'] + timedelta(hours=int(entity['digest-hour']))

    for task_type in ['done', 'todo', 'block', 'doing']:
        entity[task_type] = doneit.get_tasks(task_type, entity['_id'], entity['date'])
    return template('project', loggedin=check(request), project=entity)

class MyDaemon(Daemon):
    def run(self):
        run(host='doneit.cs.drexel.edu', port=80, debug=True)
#        run(host='localhost', port=5000, debug=True)

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
