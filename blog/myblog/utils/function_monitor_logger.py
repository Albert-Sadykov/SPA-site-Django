import logging
import traceback
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('function_logging.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log_operations(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, *kwargs)

            if hasattr(func, '__self__'):
                # Для методов класса (bound methods)
                class_name = func.__self__.__class__.__name__
                logger.info(f"Method {class_name}.{func.__name__} executed successfully.")
            elif hasattr(func, '__qualname__') and '.' in func.__qualname__:
                # Для статических методов и методов класса (unbound)
                class_name = func.__qualname__.split('.')[0]
                logger.info(f"Class method {class_name}.{func.__name__} executed successfully.")
            else:
                # Для обычных функций
                logger.info(f"Function {func.__name__} executed successfully.")
            return result
        except Exception as e:
            if hasattr(func, '__self__'):
                class_name = func.__self__.__class__.__name__
                logger.error('Error in method %s.%s: %s - %s', 
                            class_name, func.__name__, e.__class__.__name__, e)
            elif hasattr(func, '__qualname__') and '.' in func.__qualname__:
                class_name = func.__qualname__.split('.')[0]
                logger.error('Error in class method %s.%s: %s - %s',
                            class_name, func.__name__, e.__class__.__name__, e)
            else:
                logger.error('Error in function %s: %s - %s',
                            func.__name__, e.__class__.__name__, e)
            logger.error(traceback.format_exc())
            raise
    return wrapper