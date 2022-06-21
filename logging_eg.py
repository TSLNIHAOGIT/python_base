import logging
from logging.handlers import RotatingFileHandler
import os
logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s]'
           '[%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
def my_logger():
    extra = {'app_name':'1234567'}

    logger = logging.getLogger('app')
    # syslog = logging.StreamHandler()
    syslog = RotatingFileHandler('app.log', maxBytes=500000, backupCount=2)
    formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)

    logger = logging.LoggerAdapter(logger, extra)
    return logger

# def get_logger(name='app',log_path='log/app.log',log_ids = None):
#     logging.basicConfig(
#         format='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s]'
#                '[%(name)s][%(app_name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#     extra = {'app_name': 'Super 1234 App'}
#
#     logger = logging.getLogger('app')
#
#     # if name in logger_initialized:
#     #     return logger
#     # logger.setLevel(logging.DEBUG)
#     logger.setLevel(logging.INFO)
#
#     log_path = os.path.join(os.path.dirname(__file__), './log/app.log')
#     """ 输出日志到日志文件 """
#     rotatingFileHandler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=2)
#     # formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
#     formatter = logging.Formatter(
#         fmt='{%(asctime)s.%(msecs)03d} [%(thread)d] %(levelname)s -%(app_name)s : %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S')
#
#     rotatingFileHandler.setFormatter(formatter)
#     # 设置级别如果低于设置的级别则无效
#     rotatingFileHandler.setLevel(logging.INFO)
#     logger.addHandler(rotatingFileHandler)
#
#     # logger_initialized[name] = True
#     logger = logging.LoggerAdapter(logger, extra)
#
#
#     return logger
#
# if __name__ =='__main__':
#     logger= get_logger(name='schedule',log_ids={'my_log_id':'1234567'})
#     logger.info('你好')

# logger_initialized = {}


def get_logger(name='app',log_path='log/app.log',log_ids = None):
    logging.basicConfig(
        format='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s]'
               '[%(name)s][%(app_name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    extra = {'app_name': 'Super App'}
    extra ={'app_name':''}

    logger = logging.getLogger('app')

    # if name in logger_initialized:
    #     return logger
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    log_path = os.path.join(os.path.dirname(__file__), './log/app.log')
    """ 输出日志到日志文件 """
    rotatingFileHandler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=2)
    formatter = logging.Formatter('%(asctime)s  : %(message)s')
    # formatter = logging.Formatter(
    #     fmt='{%(asctime)s.%(msecs)03d} [%(thread)d] %(levelname)s -%(app_name)s : %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S')

    rotatingFileHandler.setFormatter(formatter)
    # 设置级别如果低于设置的级别则无效
    rotatingFileHandler.setLevel(logging.INFO)
    logger.addHandler(rotatingFileHandler)

    # logger_initialized[name] = True
    logger = logging.LoggerAdapter(logger, extra)


    return logger

if __name__ =='__main__':
    logger= get_logger(name='schedule',log_ids={'my_log_id':'1234567'})
    logger.info('你好')


# if __name__ == '__main__':
#     logger=my_logger()
#     logger.info('The sky is so blue')