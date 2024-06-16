from vehicle.models import Vehicel
from reportlab.lib.pagesizes import letter
from django.contrib.auth import get_user_model
from datetime import datetime
from core.utils.document_type import DocumentType
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime
import os

User = get_user_model()


class GeneratePdf:

    def generate_road_fund_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        """
        This is a method to generate a road fund file.
        It accepts the following arguments:
        renewal_date (str): The date the road fund is renewed.
        expire_date (str): The date the road fund expires.
        chassis_number (str): The chassis number of the vehicle.
        document_id (str): The id of the document.
        filename (str): The name of the file to be generated.
        transaction_number (str, optional): The transaction number. Defaults to None.
        returns the file path if the file is generated successfully, otherwise None.
        """

        try:
            cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return None
        try:
            cur_user = User.objects.get(username=cur_vehicle.owner)
        except User.DoesNotExist:
            return None

        cur_user = User.objects.get(id=cur_user.id)

        # Save the file to a temporary directory
        filepath = os.path.join('pdfs', filename)
        first_name = cur_user.first_name
        middle_name = cur_user.middle_name
        last_name = cur_user.last_name
        plate_number = cur_vehicle.plate_number

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = colors.darkblue
        header_style = ParagraphStyle(
            name='Header', fontSize=14, textColor=colors.darkred, spaceAfter=10, leading=18)
        normal_style = styles['Normal']

        # Title and header
        elements.append(Paragraph("FDRE Ministry of Transport", title_style))
        elements.append(Paragraph("Road Fund Office", header_style))
        elements.append(Spacer(1, 12))

        # Document ID and dates
        elements.append(Paragraph(f"ID: {document_id}", normal_style))
        elements.append(
            Paragraph(f"Renewal Date: {renewal_date}", normal_style))
        elements.append(Paragraph(f"Expire Date: {expire_date}", normal_style))
        elements.append(Spacer(1, 12))

        # Owner Information
        elements.append(Paragraph("Owner Information:", header_style))
        owner_info = [
            ["First Name", first_name],
            ["Middle Name", middle_name],
            ["Last Name", last_name],
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

        # Vehicle Information
        elements.append(Paragraph("Vehicle Information:", header_style))
        vehicle_info = [
            ["Plate Number", plate_number],
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

        # Issued by
        if transaction_number:
            elements.append(
                Paragraph(f"Transaction Number: {transaction_number}", normal_style))
            issued_by = "Goma Notify"
        else:
            issued_by = "Road Fond Office"

        elements.append(Paragraph(f"Issued by: {issued_by}", normal_style))
        elements.append(Paragraph(
            f"Issued Date: {datetime.now().strftime('%Y%m%d%H%M%S')}", normal_style))

        # Build the PDF
        doc.build(elements)

        return filepath

    @staticmethod
    def generate_road_authority_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        """
        This is a method to generate a road authority file.
        It accepts the following arguments:
        renewal_date (str): The date the road fund is renewed.
        expire_date (str): The date the road fund expires.
        chassis_number (str): The chassis number of the vehicle.
        document_id (str): The id of the document.
        returns the file path if the file is generated successfully, otherwise None.
        """

        try:
            cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return None
        try:
            cur_user = User.objects.get(username=cur_vehicle.owner)
        except User.DoesNotExist:
            return None

        cur_user = User.objects.get(id=cur_user.id)

        # Save the file to a temporary directory
        filepath = os.path.join('pdfs', filename)
        first_name = cur_user.first_name
        middle_name = cur_user.middle_name
        last_name = cur_user.last_name
        plate_number = cur_vehicle.plate_number

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = colors.darkblue
        header_style = ParagraphStyle(
            name='Header', fontSize=14, textColor=colors.darkred, spaceAfter=10, leading=18)
        normal_style = styles['Normal']

        # Title and header
        elements.append(Paragraph("FDRE Ministry of Transport", title_style))
        elements.append(Paragraph("Road Authority Office", header_style))
        elements.append(Spacer(1, 12))

        # Document ID and dates
        elements.append(Paragraph(f"ID: {document_id}", normal_style))
        elements.append(
            Paragraph(f"Renewal Date: {renewal_date}", normal_style))
        elements.append(Paragraph(f"Expire Date: {expire_date}", normal_style))
        elements.append(Spacer(1, 12))

        # Owner Information
        elements.append(Paragraph("Owner Information:", header_style))
        owner_info = [
            ["First Name", first_name],
            ["Middle Name", middle_name],
            ["Last Name", last_name],
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

        # Vehicle Information
        elements.append(Paragraph("Vehicle Information:", header_style))
        vehicle_info = [
            ["Plate Number", plate_number],
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

        # Issued by
        elements.append(Paragraph("Issued by: Goma Notify", normal_style))
        elements.append(Paragraph(
            f"Issued Date: {datetime.now().strftime('%Y%m%d%H%M%S')}", normal_style))

        # Build the PDF
        doc.build(elements)

        return filepath

    @staticmethod
    def generate_insurance_file(renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=None):
        """
        This is a method to generate a road fund file.
        It accepts the following arguments:
        renewal_date (str): The date the road fund is renewed.
        expire_date (str): The date the road fund expires.
        chassis_number (str): The chassis number of the vehicle.
        document_id (str): The id of the document.
        returns the file path if the file is generated successfully, otherwise None.
        """

        try:
            cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return None
        try:
            cur_user = User.objects.get(username=cur_vehicle.owner)
        except User.DoesNotExist:
            return None

        cur_user = User.objects.get(id=cur_user.id)

        # Save the file to a temporary directory
        filepath = os.path.join('pdfs', filename)
        first_name = cur_user.first_name
        middle_name = cur_user.middle_name
        last_name = cur_user.last_name
        plate_number = cur_vehicle.plate_number

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = colors.darkblue
        header_style = ParagraphStyle(
            name='Header', fontSize=14, textColor=colors.darkred, spaceAfter=10, leading=18)
        normal_style = styles['Normal']

        # Title and header
        elements.append(Paragraph("FDRE Ministry of Transport", title_style))
        elements.append(Paragraph("Insurance Office", header_style))
        elements.append(Spacer(1, 12))

        # Document ID and dates
        elements.append(Paragraph(f"ID: {document_id}", normal_style))
        elements.append(
            Paragraph(f"Renewal Date: {renewal_date}", normal_style))
        elements.append(Paragraph(f"Expire Date: {expire_date}", normal_style))
        elements.append(Spacer(1, 12))

        # Owner Information
        elements.append(Paragraph("Owner Information:", header_style))
        owner_info = [
            ["First Name", first_name],
            ["Middle Name", middle_name],
            ["Last Name", last_name],
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

        # Vehicle Information
        elements.append(Paragraph("Vehicle Information:", header_style))
        vehicle_info = [
            ["Plate Number", plate_number],
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

        # Issued by
        elements.append(Paragraph("Issued by: Goma Notify", normal_style))
        elements.append(Paragraph(
            f"Issued Date: {datetime.now().strftime('%Y%m%d%H%M%S')}", normal_style))

        # Build the PDF
        doc.build(elements)

        return filepath

    @staticmethod
    def generate_file(renewal_date, expire_date, chassis_number, document_id, filename, document_type, transaction_number=None):
        if document_type == DocumentType.ROAD_FUND:
            return GeneratePdf.generate_road_fund_file(
                renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=transaction_number)
        elif document_type == DocumentType.ROAD_AUTHORITY:
            return GeneratePdf.generate_road_authority_file(
                renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=transaction_number)
        else:
            return GeneratePdf.generate_insurance_file(
                renewal_date, expire_date, chassis_number, document_id, filename, transaction_number=transaction_number)
