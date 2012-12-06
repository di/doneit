#!/usr/bin/python

import sys, email, re, datetime, requests
import doneit

# this script reads an email from stdin.
# to test, use:
# $ cat email.sample | ./incoming.py

def get_user(message):
    # extract email address from From field
    sender = message['From']

    m = re.search('<([\w@\.]+)>', sender)
    sender_address = m.group(1)
    user = doneit.get_user_by_email(sender_address)
    return user

def get_project(message):
    # lookup from user id
    user = get_user(message)
    project = doneit.get_by_id('projects', user['project_id'])
    return project

def get_tasks(message):
    # parse tasks out of the payload
    tasks = []

    for part in message.walk():
        # find the first text portion of the email
        if part.get_content_maintype() != 'text':
            continue
        payload = part.get_payload(decode=True)
        break

    task_type = 'UNSPECIFIED'
    for line in payload.splitlines():
        m = re.search('TODO|DOING|DONE|BLOCK', line, re.IGNORECASE)
        if(m):
            task_type = m.group(0).lower()

        if(task_type != 'UNSPECIFIED'):
            m = re.search('\*(.+)', line)
            if(m):
                comment = m.group(1).strip()
                tasks.append({"type":task_type, "comment":comment})
    return tasks

def send_error_reply(message):
    to = message['From']
    subject = "Re: %s" % message['Subject']
    body = "The following message was rejected by the doneit system.\n\n%s" % message.get_payload()
    doneit.send_email(to, subject, body)


def main():
    message = email.message_from_string(sys.stdin.read())
    doneit.log("Got email from %s" % message['From'])

    user = get_user(message)
    project = get_project(message)
    tasks = get_tasks(message)

    if (user == None) or (project == None) or (tasks == None):
        send_error_reply(message)
        return

    for task in tasks:
        entity = dict()
        entity['date'] = datetime.datetime.utcnow()
        entity['user_id'] = user['_id']
        entity['project_id'] = project["_id"]
        for field in ['type', 'comment']:
            entity[field] = task[field]

        doneit.log("Submit Task: %s, %s, %s, %s" % (user['email'], project['name'], task['type'], task['comment']))
        r = requests.post(doneit.entry_input_service_url + "/task", entity)
        if r.json['status'] != "success":
            send_error_reply(message)
            return

if __name__ == "__main__":
    main()
