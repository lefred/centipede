#!/usr/bin/python
import re
import os.path
from datetime import datetime
from arsia.ged.compta.config import readConfig, parseCmdLineOpt
from arsia.ged.compta.connection import create_connection, produce_msg
from arsia.ged.compta.convert import convert_file, merge_files
from arsia.ged.compta.document import Document
from arsia.ged.compta.logger import logger
from arsia.ged.compta.ocr import Ocr
from arsia.ged.compta.scanner import init_scanner, start_scanning

def main():
    document = None
    page_num = 0
    options, args = parseCmdLineOpt()
    config_file = options.configFile
    config = readConfig(config_file)
    channel = create_connection(config)
    documents = []
    scanner = init_scanner(config) 
    for output, image_bar in start_scanning(scanner):
        for symbol in image_bar:
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            for clef, valeur in config.items("compta"):
                if re.match(("^%s.*" % valeur), symbol.data):
                    page_num = 0
                    logger.debug("new document detected")
                    document = Document()
                    logger.debug(document)
                    document.name = symbol.data
                    document.genre = clef
                    #documents.append(document)
                    break
            if re.match(("^%s.*" % config.get("workflow", "key")), symbol.data):
                document.workflows.append(symbol.data)
        page_num += 1
        if document is not None:
            filename = "%s_%s.tiff" % (document.name, str(page_num))
        else:
            document = Document()
            filename = "undefined_%s_%s.tiff" % (datetime.today().strftime("%Y%m%d-%H%M%S"), str(page_num))
            document.name = "undefined_%s" % datetime.today().strftime("%Y%m%d-%H%M%S")
        documents.append(document)
        filepath = os.path.join(config.get("output", "tmp_dir"), filename)
        output.save(filepath, 'TIFF')
        document.files.append(filepath)
        for symbol in image_bar:
            document.barcodes.append(symbol.data)
        print str(document)

        ocr = Ocr()
        ocr.bin_path = config.get("ocr","ocr_bin")
        ocr.input_image = filepath
        ocr.parse()
        document.ocr.append(ocr.content)
        if config.get("scanner", "interactive") == "True":
            input_cmd = raw_input("press enter to scan the next document or 'quit' to leave ")
            if input_cmd == "quit":
                break
    for document in documents:
        old_files = document.files
        document.files = []
        file_format = config.get("output", "file_format")
        for image in old_files:
            document.files.append(convert_file(image,file_format))
        if file_format == "PDF":
            new_file = merge_files(document.files,file_format)
            document.files = [new_file]
        produce_msg(channel, document)


