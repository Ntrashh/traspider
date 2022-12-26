import os
import re
import sys

from traspider.core.engine import Engine
from traspider.core.request import Request
from traspider.core.spider import Spider
from traspider.util import exception, Encrypt
from traspider.util.node_vm.node import Node




sys.path.insert(0, re.sub(r"([\\/]items)|([\\/]spiders)", "", os.getcwd()))

__all__ = [
	"Node",
	"Spider",
	"Request",
	"Engine",
	"exception",
	"Node",
	"Encrypt"
]

__version__ = "0.0.03"
