#!/usr/bin/python

from arsia.ged.compta.connection import create_connection, consume_msg
from arsia.ged.compta.config import readConfig, parseCmdLineOpt

def main():
    options, args = parseCmdLineOpt()
    config_file = options.configFile
    config = readConfig(config_file)
    channel = create_connection(config)
    consume_msg(channel)

