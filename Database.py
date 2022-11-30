import json
from pymongo import MongoClient
import csv
from collections import Counter 
import requests


class db_pipeline:
    def __init__(self, link, from_cluster, collection_name):
        self.db = self.connect_db(link, from_cluster, collection_name)
        
    def connect_db(self, link, from_cluster, collection_name):
        cluster = MongoClient(link)
        db = cluster[from_cluster]
        return db[collection_name]

    def push_csv(self, csv_file_path):
        with open(csv_file_path,encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.db.insert_one(row)
                print(row)

    def remove_all(self):
        self.db.delete_many({})
        
class plates_db_api:
    def __init__(self):
        self.url = "https://data.mongodb-api.com/app/data-eqwcz/endpoint/data/v1/action/findOne"
    def query(self, plate_number):
        payload = json.dumps({
            "collection": "plates",
            "database": "Test",
            "dataSource": "Cluster0",
            "filter": {"plate": {"$regex": f"{plate_number}", "$options": "$i"},
            }})
        headers = {
             'Content-Type': 'application/json',
             'Access-Control-Request-Headers': '*',
             'api-key': "Kq9DlhcEHxGY5GoKLMAhAkotJOoSeHnbVIsBpEcbsnsepxG5qrPikWrerjRpDG4a"
              }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response["document"]


