import logging

def setup_logging(log_name: str, logging_level=logging.DEBUG):
    """setup logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{log_name}.log')
    error_file_handler = logging.FileHandler(f'{log_name}_errors.log')

    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
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

def setup_subtle_logging(log_name, logging_level=logging.DEBUG):
    """setup logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)

    file_handler = logging.FileHandler(f'{log_name}.log')

    file_handler.setLevel(logging.DEBUG)
    logger.propagate = False


    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

def start_monitor() -> cProfile.Profile:

    profiler = cProfile.Profile()
    profiler.enable()

    return profiler

def stop_monitor(script_name: str, profiler: cProfile.Profile, logger) -> None:

    profiler.disable()

    script_name = script_name.split('.')[0]
    binary_profile = f"{LOG_DIR}/{script_name}.prof"

    profiler.dump_stats(binary_profile)

    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats()
 
    logger.info(s.getvalue())