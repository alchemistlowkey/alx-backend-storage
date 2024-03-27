#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score

    Args:
        mongo_collection: the pymongo collection object

    Returns:
        A list of dictionaries containing students sorted by average score.
    """
    pipeline = [
        {
            "$project": {
                "id": 1,
                "name":  1,
                "averageScore": {
                    "$avg": "$topics.score"
                 },
            }
        },
        {
           "$sort": {"averageScore": -1}
        }
    ]
    average = list(mongo_collection.aggregate(pipeline))
    return average
