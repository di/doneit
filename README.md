# doneit
Daily Task Management &amp; Daily Digest System

# Required libraries
## bottle
Bottle is a micro-framework for Python:

    $ sudo easy_install bottle

## requests
Requests is an HTTP library for Python:

    $ sudo easy_install requests

## pytz
Pytz brings the Olson tz database to Python:

    $ sudo easy_install pytz

## pymongo
Pymongo is the MongoDB driver for Python:

    $ sudo easy_install pymongo

## MongoDB
MongoDB is the database for Doneit:

    $ sudo apt-get install mongodb

## Postfix
Postfix is the email server used by Doneit:

    $ sudo apt-get install postfix

# Getting Started
## Checking out the repo
To get the source, run the following:

    $ cd /
    $ sudo git clone git://github.com/di/doneit.git

We now have a directory at `/doneit` where the application resides.

## Importing the database
To build the database, from the `/doneit/` directory, run:

    $ mongorestore

To dump the database (to commit to git), run:

    $ mongodump

## Starting the Daemon
The daemon allows the web service to run indefinitely. To start it, in the
application directory, run:

    $ sudo ./website.py start

To restart:

    $ sudo ./website.py restart

To stop:

    $ sudo ./website.py stop

## Accepting incoming mail:
To process incoming mail, we need to set an alias for the user (here, `doneit`)
that pipes the email to the stdin of a file instead of to `mail`.

In `/etc/aliases`, add the line

    doneit: "|/usr/bin/doneit_incoming"

Then, we need to symlink the `incoming.py` file to this location:

    $ sudo ln -s /doneit/incoming.py /usr/bin/doneit_incoming

And then update Postfix's aliases:

    $ sudo postalias /etc/aliases

## Setup waker cronjob
The waker process is initiated by a cronjob periodically. 

To edit the root crontab:

    $ sudo crontab -e

Then setup the cron with the following line:

    0 * * * * /doneit/waker.py 2>&1

This triggers the waker every hour on the hour. The 2>&1 is used to suppress emails from the cron.

## Logging
Logs are logged at `/var/log/doneit.log`
