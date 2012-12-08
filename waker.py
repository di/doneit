#!/usr/bin/python

import sys, datetime
import requests, json
import doneit

def main():

    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    doneit.log("Waker triggered at %s H. " % hour)

    users = doneit.get_user_list_by_reminder_request(hour)
    for user in users:
        if user['reminder-email']:
            doneit.log("Waker to initiate reminder request for %s" % user['name'])
            r = requests.post(doneit.email_sending_service_url + "/reminder", user)

    users = doneit.get_user_list_by_digest_request(hour)
    for user in users:
        doneit.log("Waker to initiate digest request for %s" % user['name'])
        r = requests.post(doneit.email_sending_service_url + "/digest", user)

if __name__ == "__main__":
    main()
