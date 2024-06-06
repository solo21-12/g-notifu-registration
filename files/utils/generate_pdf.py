from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth import get_user_model
from datetime import datetime
from vehicle.models import Vehicel
User = get_user_model()


class GeneratePdf:

    @staticmethod
    def generate_road_fund_file(renewal_date, expire_date, chassis_number, document_id):
        '''
        This is a method to generate a road fund file.
        It accepts the following arguments:
        renewal_date (str): The date the road fund is renewed.
        expire_date (str): The date the road fund expires.
        chassis_number (str): The chassis number of the vehicle.
        document_id (str): The id of the document.
        returns True if the file is generated successfully, otherwise None.
        '''

        try:
            cur_vehicle = Vehicel.objects.get(chassis_number=chassis_number)
        except Vehicel.DoesNotExist:
            return None

        cur_user = User.objects.get(id=cur_vehicle.owner)

        filename = f"{cur_user.get_username()}_road_fund_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        first_name = cur_user.first_name
        middle_name = cur_user.middle_name
        last_name = cur_user.last_name
        plate_number = cur_vehicle.plate_number

        c = canvas.Canvas(filename, pagesize=letter)

        # Define the width and height of the page
        width, height = letter

        # Set the title of the document
        c.setTitle("Vehicle Information Document")

        # Draw the header
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 50,
                            "FDRE Ministry of Transport")
        c.drawCentredString(width / 2, height - 70, "Road Fund Office")

        # Set the font for the content
        c.setFont("Helvetica", 12)

        # Dynamic information
        c.drawString(50, height - 100, f"ID: {document_id}")
        c.drawString(50, height - 120, f"Renewal Date: {renewal_date}")
        c.drawString(50, height - 140, f"Expire Date: {expire_date}")

        # Owner information
        c.drawString(50, height - 180, "Owner Information:")
        c.drawString(70, height - 200, f"First Name: {first_name}")
        c.drawString(70, height - 220, f"Middle Name: {middle_name}")
        c.drawString(70, height - 240, f"Last Name: {last_name}")
        c.drawString(70, height - 260, "City: Addis Abeba")
        c.drawString(70, height - 280, "Country: Ethiopia")

        # Vehicle information
        c.drawString(50, height - 320, "Vehicle Information:")
        c.drawString(70, height - 340, f"Plate Number: {plate_number}")
        c.drawString(70, height - 380, f"Chassis Number: {chassis_number}")

        # Issued by
        c.drawString(50, height - 420, "Issued by: Goma Notify")
        c.drawString(50, height - 420,
                     f"Issued Date: {datetime.now().strftime('%Y%m%d%H%M%S')}")

        # Save the document
        c.save()

        return True
