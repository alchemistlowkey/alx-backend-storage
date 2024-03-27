#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs:

The IPs top must be sorted (like the example below)
"""
from pymongo import MongoClient

# Connect to MpngoDB
client = MongoClient("localhost", 27017)
db = client.logs
nginx = db.nginx


if __name__ == "__main__":
    # Total number of logs
    total_logs = nginx.count_documents({})
    print(f"{total_logs} logs")
    print(f"Methods:")

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of logs wih method=GET and path=/status
    status_check_count = nginx.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
    print("IPs:")

    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 10}, {"$project": {
            "_id": 0, "ip": "$_id", "count": 1}}
    ]

    IPs = list(nginx.aggregate(pipeline))
    for top_ip in IPs:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print(f"\t{ip_address}: {count}")
