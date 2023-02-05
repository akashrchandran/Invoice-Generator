from flask import Flask, after_this_request, render_template, request, send_file
from invoice_generator import generate_invoice
import random
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    invoice_id = "invoice_"+''.join(random.sample('0123456789', 5))
    c_id = "customer_"+''.join(random.sample('0123456789', 5))
    return render_template('index.html', invoice_id=invoice_id, c_id=c_id, date = date.today())

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        details = request.form
        file_name = details.get("invoice_id")+'.pdf'
        if generate_invoice(details):
            return send_file('invoice.pdf', as_attachment=True, download_name=file_name)
        else:
            return "Error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)