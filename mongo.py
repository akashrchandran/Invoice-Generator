import os

import pymongo
import dotenv

dotenv.load_dotenv()
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client.invoice_generator
invoice = db.invoice
users = db.users

def add_invoice(data):
    invoice.insert_one(data)

def get_invoice(invoice_id):
    return invoice.find_one({'invoice_id': invoice_id})

def update_invoice(invoice_id, method):
    invoice.update_one({'invoice_id': f'{invoice_id}'}, {"$set": {'invoice_type': 'paid', 'paid_through': method.title()}}, upsert=True)

def get_user(username):
    return users.find_one({'email': username})

def add_user(data):
    users.insert_one(data)