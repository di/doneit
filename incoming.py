#!/usr/bin/python

import sys, email, re, datetime
import doneit

# this script reads an email from stdin. 
# to test, use:
# $ cat email.sample | ./incoming.py

def get_user(email):
    # extract email address from From field
    sender = email['From']
    doneit.log("Got email from %s" % sender)

    m = re.search('<([\w@\.]+)>', sender)
    sender_address = m.group(1)
    user_id = doneit.get_user_by_email(sender_address)['_id']
    return user_id

def get_project(email):
    # lookup from user id
    user_id = get_user(email)
    project_id = doneit.get_by_id('users', user_id)["project_id"]
    return project_id

def get_tasks(email):
    # parse tasks out of the payload
    payload = email.get_payload()
    tasks = []

    task_type = 'UNSPECIFIED'
    for line in payload.splitlines():
        m = re.search('TODO|DOING|DONE|BLOCK', line)
        if(m):
            task_type = m.group(0)
        else:
            if(task_type != 'UNSPECIFIED'):
                m = re.search('\*(.+)', line)
                if(m):
                    comment = m.group(1).strip()
                    tasks.append({"type":task_type, "comment":comment})
    return tasks



email = email.message_from_string(sys.stdin.read())

entity = dict()
entity['date'] = datetime.datetime.utcnow()
entity['user_id'] = get_user(email)
entity['project_id'] = get_project(email)

tasks = get_tasks(email)
for task in tasks:
    for field in ['type', 'comment']:
        entity[field] = task[field]
    doneit.log("Submit Task: %d, %d, %s, %s" % (entity['user_id'], entity['project_id'], entity['type'], entity['comment']))
    _id = doneit.add_task(entity)

