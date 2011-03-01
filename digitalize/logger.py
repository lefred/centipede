#!/usr/bin/python
import sys
import logging

logger = logging.getLogger('centipede.digitalize')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - \
%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
