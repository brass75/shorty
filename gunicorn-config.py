import logging
import os

logger = logging.getLogger('config')

if os.path.exists('certs/certs.py'):
    # Since we don't want to have secrets in Git we'll import them from a separate directory.
    import certs.certs as certs
else:
    logger.warning('No certs config found')
    certs = None

bind = '0.0.0.0:8000'  # The IP:port to bind to. Using '0.0.0.0' says to accept from any IP.
workers = 2  # The number of worker processes to run
certfile = getattr(certs, 'certfile', None)  #
keyfile = getattr(certs, 'keyfile', None)
logger.info(f'Using {certfile=} {keyfile=}')
