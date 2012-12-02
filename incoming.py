#!/usr/bin/python

import sys, email, re, datetime
import doneit

# this script reads an email from stdin. 
# to test, use:
# $ cat email.sample | ./incoming.py

def get_user(email):
    # extract email address from From field
    sender = email['From']

    m = re.search('<([\w@\.]+)>', sender)
    sender_address = m.group(1)
    user = doneit.get_user_by_email(sender_address)
    return user

def get_project(email):
    # lookup from user id
    user = get_user(email)
    project = doneit.get_by_id('projects', user['project_id'])
    return project

def get_tasks(email):
    # parse tasks out of the payload
    payload = email.get_payload()
    tasks = []

    task_type = 'UNSPECIFIED'
    for line in payload.splitlines():
        m = re.search('TODO|DOING|DONE|BLOCK', line, re.IGNORECASE)
        if(m):
            task_type = m.group(0).lower()
        else:
            if(task_type != 'UNSPECIFIED'):
                m = re.search('\*(.+)', line)
                if(m):
                    comment = m.group(1).strip()
                    tasks.append({"type":task_type, "comment":comment})
    return tasks


def main():
    message = email.message_from_string(sys.stdin.read())

    user = get_user(message)
    project = get_project(message)
    tasks = get_tasks(message)

    doneit.log("Got email from %s" % user['name'])

    for task in tasks:
        entity = dict()
        entity['date'] = datetime.datetime.utcnow()
        entity['user_id'] = user['_id']
        entity['project_id'] = project["_id"]
        for field in ['type', 'comment']:
            entity[field] = task[field]

        doneit.log("Submit Task: %s, %s, %s, %s" % (user['email'], project['name'], task['type'], task['comment']))
        _id = doneit.add_task(entity)


if __name__ == "__main__":
    main()
