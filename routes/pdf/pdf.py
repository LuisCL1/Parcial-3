
#pip install reportlab
from flask import Blueprint,make_response,render_template
from models import User
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
apppdf = Blueprint('apppdf',__name__,template_folder="templates")


@apppdf.route('/generatePdf')
def generate_pdf():
   
    doc = SimpleDocTemplate("users.pdf", pagesize=letter)
    usuarios = User.query.all()
    listaUsuarios=[["ID","EMAIL","REGISTRADO","ADMIN"]]
    for usuario in usuarios:
        listaUsuarios.append(
            [usuario.id,usuario.email,usuario.registered_on,usuario.admin]
        )
    table = Table(listaUsuarios)

    style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 16),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table.setStyle(style)
    # Add the table to the PDF document

    text = "This is a paragraph of text that will be added to the PDF."

    # Create a paragraph object
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_CENTER 
    paragraph = Paragraph(text, style)
    elements = [paragraph,table]
    
    doc.build(elements)

    # Create a response with the PDF file
    response = make_response(open("users.pdf", "rb").read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=users.pdf'
    return response



@apppdf.route('/mainPdf')
def index():
    return render_template('indexPdf.html')