#!/usr/bin/python

import sys, doneit, email

email = email.message_from_string(sys.stdin.read())
doneit.log("Got email from %s" % email['From'])
payload = email.get_payload()
