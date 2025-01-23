#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

def fetch_nginx_logs():
    """Fetch and provide some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Count total logs
    total_logs = nginx_collection.count_documents({})
    print(f'{total_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    # Count status check requests
    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check_count} status check')

if __name__ == "__main__":
    fetch_nginx_logs()

