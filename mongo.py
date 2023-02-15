import pymongo
import os

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client.invoice_generator
invoice = db.invoice

def add_invoice(data):
    invoice.insert_one(data)