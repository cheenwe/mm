# encoding=utf-8

import logging
import os
import config
import traceback
import datetime




# 自定义的日志输出
def log(msg, level = logging.DEBUG):
    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/run.log',
        format = '%(asctime)s: %(message)s',
        level = logging.DEBUG
    )
    logging.log(level, msg)
    print('%s [%s], msg:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, msg))

    if level == logging.WARNING or level == logging.ERROR:
        for line in traceback.format_stack():
            print(line.strip())

        for line in traceback.format_stack():
            logging.log(level, line.strip())


def make_dir(dir):
    log('make dir:%s' % dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
