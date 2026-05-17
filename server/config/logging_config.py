import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
def init_logging():
    #level defines the lowest level it will handle.
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_file = log_dir / "app.log"
    print(log_file)
    log_dir.mkdir(parents=True, exist_ok=True)
    fmt = '%(asctime)s - %(module)s - %(levelname)s - [%(name)s] - %(message)s'
    handler = RotatingFileHandler(log_file ,maxBytes=1_000_000, backupCount=3)
    logging.basicConfig(format=fmt, 
                        handlers=[handler],
                        level=logging.DEBUG)
    logging.info(f'Init logging, handler - {log_file} from {base_dir}')
