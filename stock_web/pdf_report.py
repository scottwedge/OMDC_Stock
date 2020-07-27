import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import  BaseDocTemplate, Paragraph, Table, TableStyle, Frame, PageTemplate
from .version import __version__

def report_gen(body, title, httpresponse, user):
    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleHeading = styles['Heading1']
    styleHeading.alignment = 1
    total_pages=1
    def head_footer(canvas, doc):
        canvas.saveState()
        P = Paragraph("Report Generated: {}    By: {} - Stock Database V{}".format(datetime.datetime.today().strftime("%d/%m/%Y"), user, __version__),
                      styleNormal)
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.leftMargin, h)
        P = Paragraph("Page {} of {}".format(canvas.getPageNumber(), total_pages),
                      styleNormal)
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.width+doc.leftMargin, h)

        P = Paragraph("{}".format(title),styleHeading)
        w, h = P.wrap(doc.width, doc.topMargin)
        #P.drawOn(canvas, ((doc.width-stringWidth(title, "Times-Roman", 20))/2.0), doc.height + doc.topMargin)
        canvas.drawCentredString((doc.width+canvas.stringWidth(title))/2.0, doc.height+doc.topMargin, title)
        #pdb.set_trace()
        canvas.restoreState()
    TABLE=Table(data=body, repeatRows=1)
    TABLE.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('ALIGN', (0, 0), (-1, -1), "CENTER")]))
    table=[]
    table.append(TABLE)
    doc = BaseDocTemplate(httpresponse, topMargin=12, bottomMargin=20, pagesize=landscape(A4))

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
           id='normal')
    template = PageTemplate(id='table', frames=frame, onPage=head_footer)
    doc.addPageTemplates([template])

    doc.build(table)
    ######COMPELTE HACK TO PAGE NUMBERS######
    #Builds the entire document (above), then counts the number of pages
    #Then rebuilds the entire document but with the new value for total pages to include in footer
    total_pages=doc.page

    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleHeading = styles['Heading1']
    styleHeading.alignment = 1

    TABLE=Table(data=body, repeatRows=1)
    TABLE.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('ALIGN', (0, 0), (-1, -1), "CENTER")]))
    table=[]
    table.append(TABLE)
    doc = BaseDocTemplate(httpresponse, topMargin=12, bottomMargin=20, pagesize=landscape(A4))

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
           id='normal')
    template = PageTemplate(id='table', frames=frame, onPage=head_footer)
    doc.addPageTemplates([template])

    doc.build(table)
