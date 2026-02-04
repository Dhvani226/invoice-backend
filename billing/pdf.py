from django.template.loader import render_to_string
from weasyprint import HTML # type: ignore
from django.http import HttpResponse
from .models import Invoice

def generate_invoice_pdf(request,id):
    invoice=Invoice.objects.get(id=id)
    html=render_to_string("invoice.html",{"invoice":invoice})
    pdf=HTML(string=html).write_pdf()
    response=HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition']='filename="invoice.pdf"'
    return response
