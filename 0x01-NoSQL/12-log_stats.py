#!/usr/bin/env python3
"""
A Python script that provides some stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
"""
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.logs
nginx = db.nginx


if __name__ == "__main__":
    # Count the total number of logs
    total_logs = nginx.count_documents({})
    print(f"{total_logs} logs")
    print(f"Methods:")

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count the number of logs wih method=GET and path=/status
    status_check_count = nginx.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
