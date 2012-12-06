#!/usr/bin/python

# Utility functions for the Doneit project

import logging
import base64, OpenSSL
import smtplib
from email.mime.text import MIMEText
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import timedelta

logger = logging.getLogger('doneit')
hdlr = logging.FileHandler('/var/log/doneit.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

date_format_digest = '%B %d, %Y (%A)'
date_format_url = '%y-%m-%d'

email_sending_service_host = "localhost"
email_sending_service_port = 5001
email_sending_service_url = "http://%s:%d" % (email_sending_service_host, email_sending_service_port)

digest_composition_service_host = "localhost"
digest_composition_service_port = 5002
digest_composition_service_url = "http://%s:%d" % (digest_composition_service_host, digest_composition_service_port)

entry_input_service_host = "localhost"
entry_input_service_port = 5003
entry_input_service_url = "http://%s:%d" % (entry_input_service_host, entry_input_service_port)

db = Connection('localhost', 27017).doneit
sessions = dict()

def check(request):
    session = request.get_cookie("session")
    _id = request.get_cookie("_id")
    return session and _id and _id in sessions.keys() and sessions[_id] == session

def login(email, password):
    user = get_user_by_email(email)
    return user != None and user['password'] == password

def logout(request):
    if check(request):
        del sessions[request.get_cookie("_id")]

def new_session(user_id):
    session_id = base64.b64encode(OpenSSL.rand.bytes(16))
    sessions[user_id] = session_id
    return session_id

def add_task(new_task):
    return save('tasks', new_task)

def add_user(new_user):
    user = get_user_by_email(new_user['email'])
    if user == None:
        return save('users', new_user)
    return user['_id']

def add_project(new_project):
    return save('projects', new_project)

def save(collection, entity):
    return db[collection].save(entity)

def get_user_by_email(email):
    return db['users'].find_one({"email": email})

def get_users_by_digest_request(since_time):
    return db['users'].find({"daily-digest" : True})

def get_users_by_reminder_request(since_time):
    return db['users'].find({"daily-digest" : True})

def get_project_members(project_id):
    return db['users'].find({"project_id": ObjectId(project_id)})

def get_all(collection):
    return db[collection].find()

def get_by_id(collection, _id):
    return db[collection].find_one({"_id": ObjectId(_id)})

def get_tasks(task_type, project_id, date):
    return db['tasks'].find({"project_id": ObjectId(project_id), "type": task_type, "date": {"$gte": date, "$lte": date+timedelta(days=1)}})

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = "[doneit] %s" % (subject)
    msg['From'] = "doneit@doneit.cs.drexel.edu"
    msg['To'] = to
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [to], msg.as_string())
    s.quit()

# Log a message
def log(msg):
    logger.info(msg)
