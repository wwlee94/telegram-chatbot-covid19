import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime

def info(string):
    return f'[{datetime.now()}] {string}'