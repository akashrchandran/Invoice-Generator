import base64
import os
import random
from datetime import date, datetime
from mongo import add_invoice
import requests
from werkzeug.datastructures import MultiDict

from flask import Flask, render_template, request

import dotenv as dotenv

dotenv.load_dotenv()


app = Flask(__name__)

@app.route('/')
def index():
    invoice_id = ''.join(random.sample('0123456789', 6))
    return render_template('index.html', invoice_id=invoice_id, date = date.today())

@app.route('/invoice', methods=['POST'])
def invoice():
    data=request.form
    image = request.files['sp_logo'].read()
    img_url = upload_image(image)
    invoice_date = datetime.strptime(data['invoice_date'], '%Y-%m-%d').date().strftime("%B %d, %Y")
    invoice_due_date = datetime.strptime(data['invoice_due_date'], '%Y-%m-%d').date().strftime("%B %d, %Y")
    item_name = data.getlist('item_name[]')
    item_qty = data.getlist('item_unit[]')
    item_unitprice = data.getlist('item_unitprice[]')
    items = []
    sub_total = 0
    for x, _ in enumerate(item_name):
        amount = int(item_qty[x]) * int(item_unitprice[x])
        sub_total += amount
        items.append({'item_name': item_name[x], 'item_qty': item_qty[x], 'item_unitprice': item_unitprice[x], 'amount': amount})
    tax = int(data['tax_percentage']) * sub_total / 100
    total = sub_total + tax
    form = MultiDict(request.form)
    form['image'] = img_url
    form['invoice_date'] = invoice_date
    form['invoice_due_date'] = invoice_due_date
    form['items'] = items
    form['sub_total'] = sub_total
    form['tax'] = tax
    form['total'] = total
    add_invoice(form.to_dict())
    return render_template('invoice.html', image=img_url, data=data, invoice_date=invoice_date, invoice_due_date=invoice_due_date, items=items, sub_total=sub_total, tax=tax, total=total)

@app.route('/share', methods=['GET'])
def share(encoded_id):
    return render_template('invoice.html', image=img_url, data=data, invoice_date=invoice_date, invoice_due_date=invoice_due_date, items=items, sub_total=sub_total, tax=tax, total=total)

def upload_image(image_data):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": os.environ.get('ImgBB_API_KEY'),
    }
    files = {
        "image": image_data
    }
    response = requests.post(url, data=payload, files=files)
    return response.json()['data']['url']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)