from loguru import logger
from .core import spider
import sys

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <level>{message}</level>")
logger.info(
    """
    
								   __                        _     __         
								  / /__________ __________  (_)___/ /__  _____
								 / __/ ___/ __ `/ ___/ __ \/ / __  / _ \/ ___/
								/ /_/ /  / /_/ (__  ) /_/ / / /_/ /  __/ /    
								\__/_/   \__,_/____/ .___/_/\__,_/\___/_/     
												  /_/                         
"""

)
