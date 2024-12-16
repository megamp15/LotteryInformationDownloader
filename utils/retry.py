import time
from functools import wraps
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import logging

logger = logging.getLogger(__name__)

def retry_on_exception(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (StaleElementReferenceException, TimeoutException) as e:
                    if attempt == retries - 1:
                        logger.error(f"Failed after {retries} attempts: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator 