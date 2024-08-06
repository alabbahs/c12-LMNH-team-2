import logging
<<<<<<< HEAD
import cProfile
import pstats
import os
from io import StringIO
from constants import Constants as ct

LOGS_DIR = ct.PATH_TO_LOGS

def setup_logging(log_name: str, logging_level=logging.DEBUG,
                  logs_dir=LOGS_DIR):
    """setup logging with two logs, one normal, one for errors,
    prints everything to terminal as well as saving it."""

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logger = logging.getLogger(logs_dir)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{logs_dir}/{log_name}.log')
    error_file_handler = logging.FileHandler(f'{logs_dir}/{log_name}_errors.log')

    console_handler.setLevel(logging_level)
    file_handler.setLevel(logging_level)
=======

def setup_logging(log_name: str, logging_level=logging.DEBUG):
    """setup logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{log_name}.log')
    error_file_handler = logging.FileHandler(f'{log_name}_errors.log')

    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
>>>>>>> b741806bbc3ccf26e2e4a4adae695c3629b03ebf
    error_file_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_file_handler)

    return logger

<<<<<<< HEAD
def setup_subtle_logging(log_name, logging_level=logging.DEBUG, logs_dir=LOGS_DIR):
    """setup logging with only one log file and without printing
    to the terminal - useful for perfomrance logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)

    file_handler = logging.FileHandler(f'{logs_dir}/{log_name}.log')
=======
def setup_subtle_logging(log_name, logging_level=logging.DEBUG):
    """setup logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)

    file_handler = logging.FileHandler(f'{log_name}.log')
>>>>>>> b741806bbc3ccf26e2e4a4adae695c3629b03ebf

    file_handler.setLevel(logging.DEBUG)
    logger.propagate = False


    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

def start_monitor() -> cProfile.Profile:
<<<<<<< HEAD
    """Launches cProfile so it can log performance"""
=======
    """"""
>>>>>>> b741806bbc3ccf26e2e4a4adae695c3629b03ebf
    profiler = cProfile.Profile()
    profiler.enable()

    return profiler

<<<<<<< HEAD
def stop_monitor(script_name: str, profiler: cProfile.Profile, logger,
                 logs_dir=LOGS_DIR) -> None:
    """Terminates performance tracking, saves both a .prof files and a
    human readable text file."""
    profiler.disable()

    binary_profile = f"{logs_dir}/{script_name}_performance.prof"
=======
def stop_monitor(script_name: str, profiler: cProfile.Profile, logger) -> None:

    profiler.disable()

    script_name = script_name.split('.')[0]
    binary_profile = f"{LOG_DIR}/{script_name}.prof"
>>>>>>> b741806bbc3ccf26e2e4a4adae695c3629b03ebf

    profiler.dump_stats(binary_profile)

    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats()
<<<<<<< HEAD

    human_readable_stats = s.getvalue()
    text_profile = os.path.join(logs_dir, f"{script_name}_performance.txt")
    with open(text_profile, 'w') as f:
        f.write(human_readable_stats)
=======
>>>>>>> b741806bbc3ccf26e2e4a4adae695c3629b03ebf
 
    logger.info(s.getvalue())