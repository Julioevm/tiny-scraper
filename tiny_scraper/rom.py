class Rom:
    def __init__(self, name, filename, crc = ""):
        self.name = name
        self.filename = filename
        self.crc = crc

    def set_crc(self, crc):
        self.crc = crc