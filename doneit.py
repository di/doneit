#!/usr/bin/python

# Utility functions for the Doneit project

import logging
import base64, OpenSSL
from pymongo import Connection
from bson.objectid import ObjectId

logger = logging.getLogger('doneit')
hdlr = logging.FileHandler('/var/log/doneit.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

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

def add_user(new_user):
    user = get_user_by_email(new_user['email'])
    if user == None:
        return save('users', new_user)
    return user['_id']

def save(collection, entity):
    return db[collection].save(entity)

def get_user_by_email(email):
    return db['users'].find_one({"email": email})

def get_project_members(project_id):
    return db['users'].find({"project_id": ObjectId(project_id)})

def get_all(collection):
    return db[collection].find()

def get_by_id(collection, _id):
    return db[collection].find_one({"_id": ObjectId(_id)})

def get_tasks(task_type, project_id):
    return db['tasks'].find({"project_id": ObjectId(project_id), "type": task_type})

# Log a message
def log(msg):
    logger.info(msg)
