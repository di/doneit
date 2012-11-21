#!/usr/bin/python

# Utility functions for the Doneit project

import logging
from pymongo import Connection
from bson.objectid import ObjectId

logger = logging.getLogger('doneit')
hdlr = logging.FileHandler('/var/log/doneit.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

db = Connection('localhost', 27017).doneit

def save(collection, entity):
    return db[collection].save(entity)

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
