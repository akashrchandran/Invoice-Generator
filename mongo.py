import os

import pymongo

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client.invoice_generator
invoice = db.invoice

def add_invoice(data):
    invoice.insert_one(data)

def get_invoice(invoice_id):
    return invoice.find_one({'invoice_id': invoice_id})