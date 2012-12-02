#!/usr/bin/python

import sys, datetime
import doneit


def main():
    users = doneit.get_users_by_digest_request()
    # send message to email service with list of users
    for user in users:
        doneit.log("Wake to initiate digest request for %s at %s" % (user['name'], user['email']))


if __name__ == "__main__":
    main()
