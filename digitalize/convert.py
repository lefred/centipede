#!/usr/bin/python

import os
from PIL import Image
from pyPdf import PdfFileWriter, PdfFileReader
from logger import logger

def convert_file(infile, file_type):
    if file_type == "TIFF":
        return infile
    im = Image.open(infile)
    basename, ext = os.path.splitext(infile)
    outfile = "%s.%s" % (basename, file_type)
    im.save(outfile, file_type)
    os.unlink(infile)
    return outfile

def merge_files(infiles, file_type):
    output = PdfFileWriter()
    logger.debug("nbr of files = %s" % len(infiles))
    if len(infiles) < 2:
        return infiles[0]
    for im_file in infiles:
        logger.debug("im_file = %s" % im_file)
        input1 = PdfFileReader(file(im_file, "rb"))
        output.addPage(input1.getPage(0))
        os.unlink(im_file)
    basename, ext = os.path.splitext(infiles[0])
    outfile = "%s.%s" % (basename, file_type)
    logger.debug("outfile = %s" % outfile)
    outputStream = file(outfile, "wb")
    output.write(outputStream)
    outputStream.close()
    return outfile

