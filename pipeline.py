# Links the Extract, Transform, and Load script.

import sys
import os
import logging
import timeit

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

def import_module_from_path(module_name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(__file__)
extract_main = import_module_from_path('extract_main', os.path.join(current_dir, 'extract', 'extract.py')).main
transform_main = import_module_from_path('transform_main', os.path.join(current_dir, 'transform', 'transform.py')).main
load_main = import_module_from_path('load_main', os.path.join(current_dir, 'load', 'load.py')).main

logger = cg.setup_logging(SCRIPT_NAME, LOGGING_LEVEL)

def pipeline():
    logger.info("|===============")
    logger.info("==> Running Pipeline!")
    logger.info("=======================================")
    logger.info(" ")

    logger.info("===========")
    logger.info("==> Executing Extract Script..")
    logger.info("===========")
    extract_time = timeit.timeit(extract_main, number=1)
    logger.info("Extract script completed in %s seconds", extract_time)

    logger.info("===========")
    logger.info("==> Executing Transform Script..")
    logger.info("===========")
    transform_time = timeit.timeit(transform_main, number=1)
    logger.info("Transform script completed in %s seconds", transform_time)

    logger.info("===========")
    logger.info("==> Executing Load Script..")
    logger.info("===========")
    load_time = timeit.timeit(load_main, number=1)
    logger.info("Load script completed in %s seconds", load_time)

    logger.info("===============")
    logger.info("==> Pipeline Complete!")
    logger.info("=======================================|")

def main():
    pipeline_time = timeit.timeit(pipeline, number=1)
    logger.info("Pipeline completed in %s seconds", pipeline_time)

if __name__ == "__main__":
    main()