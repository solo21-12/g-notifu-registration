import secrets


class GeneratePin:
    def gen_pin(self) -> int:
        number = secrets.randbelow(1000000)
        return number
