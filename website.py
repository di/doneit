#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, json, bson, urllib, datetime, pytz
#from dateutil.tz import tzlocal
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson.objectid import ObjectId
from daemon import Daemon

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

@route('/tasks/add', method='GET')
def add_tasks():
    if check(request):
        return template('tasks_add', loggedin=check(request))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/tasks/add', method='POST')
def add_tasks():
    if check(request):
        entity = dict()
        user_id = request.get_cookie("_id")
        project_id = doneit.get_by_id('users', user_id)["project_id"]
        for field in ['type', 'comment']:
            entity[field] = request.forms.get(field)
        entity['user_id'] = user_id
        entity['project_id'] = project_id
        entity['date'] = datetime.datetime.utcnow()
        _id = doneit.add_task(entity)
        redirect("/projects/%s" % (project_id))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/users', method='GET')
def get_users():
    entity = doneit.get_all('users')
    return template('users', loggedin=check(request), users=entity)

@route('/users/add', method='GET')
def add_users():
    if check(request):
        entity = doneit.get_all('projects')
        return template('users_add', loggedin=check(request), projects=entity)
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/users/add', method='POST')
def add_users():
    if check(request):
        entity = dict()
        for field in ['name', 'email', 'password', 'daily-digest']:
            entity[field] = request.forms.get(field)
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

@route('/projects/add', method='GET')
def add_projects():
    if check(request):
        return template('projects_add', loggedin=check(request))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/projects/add', method='POST')
def add_projects():
    if check(request):
        entity = dict()
        for field in ['name', 'description']:
            entity[field] = request.forms.get(field)
        entity['admin_id'] = request.get_cookie("_id")
        _id = doneit.add_project(entity)
        redirect("/projects/%s" % (_id))
    else:
        redirect("/login?ret=%s" % (request.path))

@route('/projects/:id', method='GET')
def get_project(id):
    entity = doneit.get_by_id('projects', id)
    entity['admin'] = doneit.get_by_id("users", entity['admin_id'])
    timezone = pytz.timezone('US/Eastern')
#    timezone = tzlocal()
    if request.query.date:
        entity['date'] = datetime.datetime.fromtimestamp(time.mktime(time.strptime(request.query.date, "%y-%m-%d")))
    else:
        entity['date'] = datetime.datetime.now(timezone).replace(hour=0,minute=0,second=0,microsecond=0).astimezone(pytz.utc) # midnight today
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
