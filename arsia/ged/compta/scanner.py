#!/usr/bin/python

from arsia.ged.compta.logger import logger
import sane
import zbar

def init_scanner(config):
    sane.init()
    logger.debug(sane.get_devices())
    scanners = [i[0] for i in sane.get_devices()  if i[2] == config.get("scanner", "model")]
    if not scanners:
        logger.error("Not able to find any scanner !")
        exit(1)
    scanner = sane.open(scanners[0])
    scanner.mode = config.get("scanner","mode")
    scanner.resolution = int(config.get("scanner", "resolution"))
    scanner.source = config.get("scanner", "source")
    scanner.swcrop = 1
    return scanner

def start_scanning(scanner):
    for output in scanner.multi_scan():
        bw = output.convert("1")
        xsize, ysize = bw.size
        xsize2 = xsize * .9
        bw = bw.crop((int(xsize * .05), 0, int(xsize2), ysize))
        colors = bw.getcolors()
        max_occurence, most_present = 0, 0
        total = 0
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
                total += max_occurence

        if (float(max_occurence) / total * 100) < 99.1:
            scanner = zbar.ImageScanner()
            scanner.parse_config('enable')
            # obtain image data
            pil = output.convert('L')
            width, height = pil.size
            raw = pil.tostring()

            # wrap image data
            image_bar = zbar.Image(width, height, 'Y800', raw)

            # scan the image for barcodes
            scanner.scan(image_bar)

            #output.save('fred'+str(a)+'.jpg','JPEG')
            yield output, image_bar

