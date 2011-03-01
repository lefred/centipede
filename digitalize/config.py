#!/usr/bin/python
import os
import sys
from ConfigParser import ConfigParser


def readConfig(filePath):
    config = ConfigParser()
    if not os.path.exists(filePath):
        print "Error: configuration file is missing !"
        sys.exit(1)
    config.read(filePath)
    return config


def parseCmdLineOpt():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--configFile", type="string", dest="configFile",
                      default=None, help="The path to the config file")
    return parser.parse_args()
