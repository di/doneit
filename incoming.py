#!/usr/bin/python

import sys, doneit, email

email = email.message_from_string(sys.stdin.read())
sender = email['From']
payload = email.get_payload()
doneit.log("Got email from %s" % sender)
