"""
File containing functions to be executed by background workers
(like celery, etc)
"""

import time


def get_stats():
    """test"""
    print('executing task...')
    time.sleep(10)

