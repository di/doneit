#!/usr/bin/python

import sys, datetime
import requests, json
import doneit

def main():
    if len(sys.argv) <= 1:
        print "Usage: %s <minutes_since_last_wake>" % sys.argv[0]
        return

    time_since_last_wake_min = int(sys.argv[1])
    doneit.log("Waker triggered at %s. %d minutes since last wake" % 
               (datetime.datetime.utcnow().strftime("%H:%M %p UTC"), time_since_last_wake_min))

    since_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_since_last_wake_min)

    users = doneit.get_users_by_reminder_request(since_time)
    for user in users:
        doneit.log("Waker to initiate reminder request for %s" % user['name'])
        r = requests.post(doneit.email_sending_service_url + "/reminder", user)
        print r

    users = doneit.get_users_by_digest_request(since_time)
    for user in users:
        doneit.log("Waker to initiate digest request for %s" % user['name'])
        r = requests.post(doneit.email_sending_service_url + "/digest", user)
        print r


if __name__ == "__main__":
    main()
