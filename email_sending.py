#!/usr/bin/python

import doneit
import sys, time, bottle, pymongo, requests, json, bson, urllib, datetime, pytz
from doneit import check
from bottle import route, run, request, response, abort, template, redirect
from bson import json_util
from bson.objectid import ObjectId
from daemon import Daemon

@route('/digest', method='POST')
def email_digest():
    timezone = pytz.timezone('US/Eastern')
    date = doneit.timezone.localize(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)) # midnight today

    doneit.log("Sending digest for %s at %s" % (request.forms.get('name'), request.forms.get('email')))
    r = requests.get("%s/%s?date=%s" % (doneit.digest_composition_service_url,
                                        request.forms.get('project_id'),
                                        date.strftime(doneit.date_format_url)))
    tasks = r.json['tasks']
    to = request.forms.get('email')
    subject = "Daily digest for %s" % doneit.get_by_id('projects', request.forms.get('project_id'))['name']
    body = []
    body.append("Project status as of %s\n\n" % datetime.datetime.now().strftime(doneit.date_format_digest))
    for task_type in tasks:
        body.append("%s:\n" % task_type.title())
        task_list = json_util.loads(r.json['tasks'][task_type])
        if len(task_list) > 0:
            for task in task_list:
                user = doneit.get_by_id('users', task['user_id'])
                body.append("* %s - %s\n" % (task['comment'], user['name']))
        else:
            body.append("* None\n")
        body.append('\n')

    body.append('\nView your project here:\n')
    body.append('http://doneit.cs.drexel.edu/projects/%s\n' % (request.forms.get('project_id')))

    sign(body)
    body = ''.join(body)

    doneit.send_email(to, subject, body)

@route('/reminder', method='POST')
def email_reminder():
    doneit.log("Sending reminder for %s at %s" % (request.forms.get('name'), request.forms.get('email')))

    project = doneit.get_by_id('projects', request.forms.get('project_id'))

    to = request.forms.get('email')
    subject = "Daily reminder for %s" % project['name']
    body = []
    body.append("Please remember to provide your status for %s.\n" % project['name'])
    sign(body)
    body = ''.join(body)

    doneit.send_email(to, subject, body)

def sign(body):
    body.append("\n\n")
    body.append("From,\n")
    body.append("  Your friends at doneit!\n")
    body.append("\n\n")
    body.append("--- You may reply to this email. ---\n")

class MyDaemon(Daemon):
    def run(self):
        run(host=doneit.email_sending_service_host, port=doneit.email_sending_service_port, debug=True)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/email_sending.pid', stderr='/var/log/email_sending.log')
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
