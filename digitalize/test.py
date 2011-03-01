#!/usr/bin/python

from connection import create_connection, consume_msg, produce_msg
from config import readConfig, parseCmdLineOpt

def main():
    options, args = parseCmdLineOpt()
    config_file = options.configFile
    config = readConfig(config_file)
    channel = create_connection(config)
    #produce_msg(channel, "FRED")
    consume_msg(channel)

main()
