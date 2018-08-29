"""Module to create a PDF file."""

try:
    from cStringIO import StringIO
except ImportError:
    # from io import StringIO BytesIO
    from io import BytesIO as StringIO

import logging

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.rl_config import defaultPageSize

pdfmetrics.registerFont(TTFont('OpenSans-Bold', 'fonts/OpenSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('OpenSans-Regular', 'fonts/OpenSans-Regular.ttf'))

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

LEFTMARGIN = cm
RIGHTMARGIN = cm
BOTTOMMARGIN = inch - cm

GREY_2 = colors.CMYKColor(0.0909, 0.0455, 0.0000, 0.5686)  # Grey 2:#64696e


def create_pdf(reportid, data):
    """Generate the Report PDF and return pdf."""
    buf = StringIO()
    pdftools = PdfTools(buffer=buf,
                        data=data,
                        reportid=reportid,
                        )
    filename = pdftools.filename
    if reportid != 'all':
        pdftools.go()
    else:
        pdftools.go_all()
    pdf = buf.getvalue()
    buf.close()
    logging.debug("Generating Report nb %s completed.", reportid)
    return pdf, filename


class PdfTools(object):
    """docstring for PdfPrint."""

    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    draw_height = 6 * cm
    draw_width = 19 * cm

    def __init__(self, buffer, reportid, data=None, filename=''):
        """Init."""
        self.buf = buffer
        self.data = data
        self.id = reportid
        self.organization = data['organization'] if 'organization' in data else 'No Data'
        self.reported_at = data['reported_at'] if 'organization' in data else 'No Data'
        self.created_at = data['created_at'] if 'organization' in data else 'No Data'
        self.inventory = data['inventory'] if 'organization' in data else []
        self.filename = 'Report - {0} - {1}.pdf'.format(self.id, self.organization) if reportid != 'all' else 'Full report.pdf'

    def firstpage(self, canvas, doc):
        """Write fixed elements of the page, e.g. the footer."""
        canvas.saveState()

        # Footer
        canvas.setFont('OpenSans-Regular', 13)
        canvas.setFillColor(GREY_2)
        canvas.restoreState()
        return

    def laterpages(self, canvas, doc):
        """Write fixed elements of the page, e.g. the footer."""
        canvas.saveState()
        # Footer
        canvas.setFillColor(GREY_2)
        self._page_number(canvas, doc)
        canvas.restoreState()
        return

    def _page_number(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawRightString(PAGE_WIDTH - RIGHTMARGIN, BOTTOMMARGIN, str(number))

    def _build_title(self, title):
        """Write The site name under the title of the Document."""
        style = ParagraphStyle(None,
                               fontName='OpenSans-Regular',
                               fontSize=20,
                               alignment=TA_CENTER,
                               textColor=GREY_2)
        content = "{}".format(title)
        p = Paragraph(content, style)
        return p

    def _build_document_content(self, data):
        """Write inventory in the Document."""
        style = ParagraphStyle(None,
                               fontName='OpenSans-Regular',
                               fontSize=12,
                               alignment=TA_CENTER,
                               textColor=GREY_2)
        content = "{}: {}".format(data['name'], data['price'])
        p = Paragraph(content, style)
        return p

    def _build_no_content(self):
        """Write No Data in the Document."""
        style = ParagraphStyle(None,
                               fontName='OpenSans-Regular',
                               fontSize=12,
                               alignment=TA_CENTER,
                               textColor=GREY_2)
        content = "No data or data corrupted"
        p = Paragraph(content, style)
        return p

    def _build_document_title(self, title, infos):
        """Write name and date under the title of the Document."""
        style = ParagraphStyle(None,
                               fontName='OpenSans-Regular',
                               fontSize=12,
                               alignment=TA_RIGHT,
                               textColor=GREY_2)
        content = "{}: {}".format(title, infos)
        p = Paragraph(content, style)
        return p

    def go(self):
        """Render the PDF foer individual item."""
        doc = SimpleDocTemplate(self.buf, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN)
        doc.title = self.filename
        doc.creator = "Romain Belia."
        doc.author = "Romain Belia."
        doc.subject = "Report created by Romain Belia."
        doc.keywords = ["report", "Romain Belia"]
        story = []
        # First Page

        story.append(self._build_title("The Report"))
        story.append(Spacer(1, 1 * cm))
        story.append(self._build_document_title("organization", self.organization))
        story.append(self._build_document_title("reported_at", self.reported_at))
        story.append(self._build_document_title("created_at", self.created_at))
        story.append(Spacer(1, 1 * cm))
        story.append(Spacer(1, 1 * cm))
        if not self.inventory:
                story.append(self._build_no_content())
        for x in self.inventory:
            story.append(self._build_document_content(x))
            story.append(Spacer(1, 1 * cm))
        story.append(PageBreak())

        doc.build(story, onFirstPage=self.firstpage, onLaterPages=self.laterpages)
        return

    def go_all(self):
        """Render the PDF for all items."""
        doc = SimpleDocTemplate(self.buf, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN)
        doc.title = self.filename
        doc.creator = "Romain Belia."
        doc.author = "Romain Belia."
        doc.subject = "Report created by Romain Belia."
        doc.keywords = ["report", "Romain Belia"]
        story = []
        # First Page

        story.append(self._build_title("Full Report"))
        story.append(Spacer(1, 1 * cm))
        for item in self.data:
            data = item['data']
            inventory = data['inventory'] if 'inventory' in data else []
            if 'id' in item:
                story.append(self._build_document_title("id", item['id']))
            if 'organization' in data:
                story.append(self._build_document_title("organization", data['organization']))
            if 'reported_at' in data:
                story.append(self._build_document_title("reported_at", data['reported_at']))
            if 'created_at' in data:
                story.append(self._build_document_title("created_at", data['created_at']))
            story.append(Spacer(1, 1 * cm))
            story.append(Spacer(1, 1 * cm))
            if not inventory:
                story.append(self._build_no_content())
            for x in inventory:
                story.append(self._build_document_content(x))
                story.append(Spacer(1, 1 * cm))
            story.append(PageBreak())

        doc.build(story, onFirstPage=self.firstpage, onLaterPages=self.laterpages)
        return
