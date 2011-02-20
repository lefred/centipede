class Document(object):

    def __init__(self):
        self.name = ""
        self.genre = ""
        self.files = []
        self.barcodes = []
        self.ocr = []
        self.user = []
        self.workflows = []
        self.scanning_date = None

    def __repr__(self):
        return("%s - %s : %s - %s" % (self.name, self.genre, self.files, self.barcodes))

