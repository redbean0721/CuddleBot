from logging.handlers import TimedRotatingFileHandler
import datetime
import logging
import os


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    log_format = "\033[90m%(asctime)s\033[0m \033[94m%(levelname)-8s\033[0m %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # 創建 FileHandler 並設置格式
    if not os.path.exists("logs"):
        os.makedirs("logs")

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_number = 1
    while os.path.exists(f"logs/{today_date}-{log_number}.log"):
        log_number += 1
    log_filename = f"logs/{today_date}-{log_number}.log"
    log_handler = TimedRotatingFileHandler(filename=log_filename, when="midnight", interval=1, backupCount=7)
    log_handler.suffix = "%Y-%m-%d.log"  # 文件名後墜

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    # 獲取根logger
    root_logger = logging.getLogger()

    # 移除根logger上的所有現有處理程序(handlers)
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    # 添加新的 StreamHandler 和 FileHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
