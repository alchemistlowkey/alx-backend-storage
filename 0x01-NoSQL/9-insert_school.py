#!/usr/bin/env python3
"""
A Python function that inserts a new document in a collection based on kwargs:

Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a collection based on kwargs

    Args:
        mongo_collection: pymongo collection object
        **kwargs: keyword arguments representing the fields of the document

    Returns:
        The new _id of the inserted document
    """
    ins = mongo_collection.insert_one(kwargs)
    return ins.inserted_id
