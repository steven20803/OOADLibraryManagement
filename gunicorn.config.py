import multiprocessing
import logging
import logging.config
from config import config as conf # naming it config may overwrite gunicorn's config

logging.config.fileConfig("log.ini")

bind = f"{conf.host}:{conf.port}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "log/access.log"
errorlog = "log/error.log"
timeout = 20
loglevel = "info"
