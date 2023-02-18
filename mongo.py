import pymongo
import os

import dotenv as dotenv

dotenv.load_dotenv()

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client.invoice_generator
invoice = db.invoice

def add_invoice(data):
    print(data)
    invoice.insert_one(data)