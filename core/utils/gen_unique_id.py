import uuid
import hashlib


def unique_string_from_two_strings(str1, str2, length=8):
    combined_str = str1 + str2 + str(uuid.uuid4())

    # Create a hash of the combined string
    unique_hash = hashlib.sha256(combined_str.encode()).hexdigest()

    # Truncate the hash to the desired length
    return unique_hash[:length]
