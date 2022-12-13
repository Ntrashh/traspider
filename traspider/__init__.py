import os
import re
import sys

from traspider.core.request import Request
from traspider.core.spider import Spider
from traspider.util.log import Logging
from traspider.util.node_vm.node import Node

print(
	"""

											   __                            _     __         
											  / /___  ________ __________  (_)___/ /__  _____
											 / __/  / ___/ __ `/ ___/ __ \/ / __  / _ \/ ___/
											/ /_/  / /  / /_/ (__  ) /_/ / / /_/ /  __/ /    
											\__/  /_/   \__,_/____/ .___/_/\__,_/\___/_/     
															  /_/                         
"""

)


sys.path.insert(0, re.sub(r"([\\/]items)|([\\/]spiders)", "", os.getcwd()))

__all__ = [
	"Logging",
	"Node",
	"Spider",
	"Request"
]

__version__ = "0.0.01"
