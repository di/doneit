#!/usr/bin/python

import sys, doneit, email, re

# this script reads an email from stdin. 
# to test, use:
# $ cat email.sample | ./incoming.py

def parse_address_from_sender(sender):
    m = re.search('<([\w@\.]+)>', sender)
    return m.group(1)

def parse_tasks_from_payload(payload):
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
sender = email['From']
payload = email.get_payload()
doneit.log("Got email from %s" % sender)

sender_address = parse_address_from_sender(sender)
tasks = parse_tasks_from_payload(payload)

for task in tasks:
    doneit.log("Submit Task: %s, %s, %s" % (sender_address, task['type'], task['comment']))

