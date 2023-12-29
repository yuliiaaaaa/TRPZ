import logging


class ConsoleLogger:
    def __init__(self, log_file='../file_log_errors.txt',level=logging.ERROR):
        self.log_file = log_file
        self.level = level

    def log_error(self, error_message):
        try:
            logging.basicConfig(filename=self.log_file, level=self.level, flush=True)
            logging.error(error_message)
        except Exception as e:
            print(f"Error occurred while logging: {e}")