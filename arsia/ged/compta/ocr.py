#!/usr/bin/python

from arsia.ged.compta.logger import logger
import subprocess
import os

class Ocr(object):
    bin_path = None
    content = ""
    input_image = None

    def __repr__(self):
        return("%s : %s" % (self.bin_path, self.input_image))

    def parse(self):
       args = [self.bin_path, self.input_image, self.input_image]
       proc = subprocess.Popen(args)
       retcode = proc.wait()
       if retcode != 0:
           logger.error("Error durin OCR")
       else:
           output_file = open("%s.txt" % self.input_image, "r")
           self.content = output_file.read()
           output_file.close()
           os.unlink("%s.txt" % self.input_image)

