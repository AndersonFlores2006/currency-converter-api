import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

def log_event(event, details=None):
    if details:
        logging.info(f'{event}: {details}')
    else:
        logging.info(event) 