import os
import sys
from scipy import sparse
from src.logger import logging
from src.exception import CustomException

def save_object(filepath, data):
    try:
        logging.info("Saving sparse data")
        dirpath = os.path.dirname(filepath)

        os.makedirs(dirpath, exist_ok=True)

        sparse.save_npz(filepath, data)
    except Exception as e:
        logging.error("Failed to save sparse data")
        raise CustomException(e,sys)