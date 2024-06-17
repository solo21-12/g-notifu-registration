from vehicle.models import Vehicel
from reportlab.lib.pagesizes import letter
from django.contrib.auth import get_user_model
from datetime import datetime
from core.utils.document_type import DocumentType
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

User = get_user_model()


class GeneratePdf:
    @staticmethod
    def generate_road_fund_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        return GeneratePdf._generate_file(renewal_date, expire_date, chassis_number, document_id, filename, "Road Fund Office", transaction_number)

    @staticmethod
    def generate_road_authority_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        return GeneratePdf._generate_file(renewal_date, expire_date, chassis_number, document_id, filename, "Road Authority Office", transaction_number)

    @staticmethod
    def generate_insurance_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        return GeneratePdf._generate_file(renewal_date, expire_date, chassis_number, document_id, filename, "Insurance Office", transaction_number)

    @staticmethod
    def _generate_file(renewal_date, expire_date, chassis_number, document_id, filename, office_name, transaction_number=None):
        try:
            cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return None
        try:
            cur_user = User.objects.get(username=cur_vehicle.owner)
        except User.DoesNotExist:
            return None

        # Ensure the user object is properly retrieved
        cur_user = User.objects.get(id=cur_user.id)

        # Define file path for PDF
        filepath = os.path.join('pdfs', filename)

        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = colors.darkblue
        header_style = ParagraphStyle(
            name='Header', fontSize=14, textColor=colors.darkred, spaceAfter=10, leading=18)
        normal_style = styles['Normal']

        # Add content to PDF
        elements.append(Paragraph("FDRE Ministry of Transport", title_style))
        elements.append(Paragraph(office_name, header_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"ID: {document_id}", normal_style))
        elements.append(
            Paragraph(f"Renewal Date: {renewal_date}", normal_style))
        elements.append(Paragraph(f"Expire Date: {expire_date}", normal_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(
            f"Unique ID: {cur_vehicle.unique_id}", normal_style))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Owner Information:", header_style))
        owner_info = [
            ["First Name", cur_user.first_name],
            ["Middle Name", cur_user.middle_name],
            ["Last Name", cur_user.last_name],
            ["City", "Addis Abeba"],
            ["Country", "Ethiopia"]
        ]
        table = Table(owner_info, hAlign='LEFT', colWidths=[100, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Vehicle Information:", header_style))
        vehicle_info = [
            ["Plate Number", cur_vehicle.plate_number],
            ["Chassis Number", chassis_number]
        ]
        table = Table(vehicle_info, hAlign='LEFT', colWidths=[100, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        if transaction_number:
            elements.append(
                Paragraph(f"Transaction Number: {transaction_number}", normal_style))
            issued_by = "Goma Notify"
        else:
            issued_by = office_name

        elements.append(Paragraph(f"Issued by: {issued_by}", normal_style))
        elements.append(
            Paragraph(f"Issued Date: {datetime.now().strftime('%Y%m%d')}", normal_style))

        # Add unique ID to top right corner

        # Build the PDF
        doc.build(elements, onFirstPage=GeneratePdf.add_watermark,
                  onLaterPages=GeneratePdf.add_watermark)

        return filepath

    @staticmethod
    def add_watermark(canvas, doc):
        # Add watermark
        canvas.saveState()
        canvas.setFont('Helvetica', 40)
        canvas.setFillColor(colors.lightgrey)
        canvas.translate(300, 500)
        canvas.rotate(45)
        canvas.drawString(0, 0, "Goma Notify")
        canvas.restoreState()

    @staticmethod
    def generate_file(renewal_date, expire_date, chassis_number, document_id, filename, document_type, transaction_number=None):
        if document_type == DocumentType.ROAD_FUND:
            return GeneratePdf.generate_road_fund_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number)
        elif document_type == DocumentType.ROAD_AUTHORITY:
            return GeneratePdf.generate_road_authority_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number)
        else:
            return GeneratePdf.generate_insurance_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number)
