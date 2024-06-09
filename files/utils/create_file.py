from files.models import Files
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ManageFile:
    @staticmethod
    def create_file(owner_username: str, file_type: str) -> Files:
        '''
        This is a method to create a file object. it accepts the following arguments:
        owner_username (str): The username of the owner of the file.
        file_type (str): The type of the file to be created.
        returns the created file.

        '''
        filename = f"{owner_username}_{file_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        file_address = f"pdfs/{filename}"
        new_file = Files.objects.create(
            file_name=filename,
            file_address=file_address,
            file_type=file_type,
            current=True
        )

        return new_file

    @staticmethod
    def out_date_file(file_id) -> Files:
        '''
        This is a method to out date an already created file.
        It accepts the following arguments:
        file_id (str): The id of the file to be outdated.
        returns the outdated file.

        '''
        try:
            file = Files.objects.get(id=file_id)
        except Files.DoesNotExist as e:
            logging.error(f"File with id {file_id} does not exist.")
            return None

        file.current = False
        file.save()

        return file
