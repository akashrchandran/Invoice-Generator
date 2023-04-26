import base64
import bcrypt
import os
import random
from datetime import date, datetime

import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.datastructures import MultiDict

from mongo import add_invoice, get_invoice, update_invoice, get_user, add_user
import razorpay
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

client = razorpay.Client(auth=("rzp_test_L9OIPDvaiZydu8", os.environ.get('RAZORPAY_Secret')))
client.set_app_details({"title" : "Invoice Generator", "version" : "v0.0.1"})

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
    share_link = f'{request.url_root}share?id={base64.b64encode(data["invoice_id"].encode("utf-8")).decode("utf-8")}'
    return render_template('invoice.html', image=img_url, data=data, invoice_date=invoice_date, invoice_due_date=invoice_due_date, items=items, sub_total=sub_total, tax=tax, total=total, share_link=share_link)

@app.route('/create/order', methods=['POST'])
def pay():
    data=request.get_json()
    amount = float(data['amount'])
    invoice_id = data['invoice_id']
    order = client.order.create({
        'amount': amount * 100, 
        'currency': 'INR', 
        'receipt': invoice_id,
    })
    return jsonify({
        'success': True,
        'order': order,
    }), 201

@app.route('/share', methods=['GET'])
def share():
    share_id = request.args.get('id')
    invoice_id = base64.b64decode(share_id).decode('utf-8')
    data = get_invoice(invoice_id)
    return render_template('invoice.html', image=data['image'], data=data, invoice_date=data['invoice_date'], invoice_due_date=data['invoice_due_date'], items=data['items'], sub_total=data['sub_total'], tax=data['tax'], total=data['total'])

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


@app.route('/success', methods=['POST'])
def success():
    payment_id = request.form['razorpay_payment_id']
    pay_details = client.payment.fetch(payment_id)
    invoice_id = pay_details['notes']['invoice_id']
    update_invoice(invoice_id, pay_details['method'])
    return render_template('success.html', invoice_id=invoice_id)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        if login_user := get_user(request.form['email']):
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['email'] = request.form['email']
                return redirect(url_for('index'))
        return 'Invalid email/password combination'
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method != 'POST':
        return render_template('signup.html')
    existing_user = get_user(request.form['email'])
    if existing_user is None:
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        add_user({'email' : request.form['email'], 'password' : hashpass})
        session['email'] = request.form['email']
        return redirect(url_for('index'))
    return 'That email already exists!'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

