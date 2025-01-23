#!/usr/bin/env python3
""" Operations with Python """


def update_topics(mongo_collection, name, topics):
    """ Changes based on name """
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, new_values)
