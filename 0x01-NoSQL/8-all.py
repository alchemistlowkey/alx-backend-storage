#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection:

Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""


def list_all(mongo_collection):
    """
    List all documents in a collection

    Args:
        mongo_collection: pymongo collection object

    Returns:
        A list of documents in the collection
    """
    collect = mongo_collection.find()
    collectall = list(collect)
    return collectall
