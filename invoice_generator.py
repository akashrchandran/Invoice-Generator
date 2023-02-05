from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice

def generate_invoice(details):
    doc = SimpleInvoice('invoice.pdf')
    doc.is_paid = False
    doc.invoice_info = InvoiceInfo(details.get("invoice_id"), details.get("invoice_date"), details.get("invoice_due_date"))
    doc.service_provider_info = ServiceProviderInfo(
        name=details.get("sp_fname") + " " + details.get("sp_lname"),
        street=details.get("sp_street"),
        city=details.get("sp_city"),
        state=details.get("sp_state"),
        country=details.get("sp_country"),
        post_code=details.get("sp_post_code"),
        vat_tax_number=details.get("sp_gst")
    )
    doc.client_info = ClientInfo(
        client_id=details.get("c_id"),
        email=details.get("c_email"),
        name=details.get("c_fname") + " " + details.get("c_lname"),
        street=details.get("c_street"),
        city=details.get("c_city"),
        state=details.get("c_state"),
        country=details.get("c_country"),
        post_code=details.get("c_post_code"),
        )
    item_name = details.getlist('item_name[]')
    item_desc = details.getlist('item_desc[]')
    item_qty = details.getlist('item_unit[]')
    item_price = details.getlist('item_unitprice[]')
    for x in range(int(details.get("item_nos"))):
        doc.add_item(Item(item_name[x], item_desc[x], item_qty[x], item_price[x]))
    doc.set_item_tax_rate(details.get("tax_percentage"))  
    doc.set_bottom_tip(details.get("footer"))

    doc.finish()
    return True