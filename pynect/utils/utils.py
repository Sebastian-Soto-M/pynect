import numpy as np
import functools
import time

import logging
import math
import re
from datetime import datetime, timedelta
from os.path import join
from typing import Dict, Generator

import pandas as pd

from .file_management import create_logs_folder

FORMAT = '%-20s\t=>\t%-50s[%.4f]'


def configure_logger(project_name: str, logging_mode: int) -> None:  # pragma: no cover
    """ Configures the logging format: time:levelname[module]name:message"""
    name = join(create_logs_folder(project_name),
                f'{datetime.now().strftime("%Y-%m-%d")}.log')
    logging.basicConfig(filename=name, encoding='utf-8', level=logging_mode,
                        format='%(asctime)s:%(levelname)s[%(module)s|%(funcName)s]%(name)s:\t%(message)s')


def is_date_older_than_delta(date: datetime, delta: timedelta) -> bool:
    elapsed = datetime.now() - date
    return elapsed > delta


def calc_iterations(total_records: int, page_size: int) -> int:
    return math.ceil(total_records / page_size)


def split_list(data: list, size: int) -> Generator[list, None, None]:
    """Generator able to split a list of data into chunks of the desired size.

    Args:
        data (list): list to split
        size (int): batch size

    Yields:
        Generator[list, None, None]: chunk of list split
    """
    for i in range(0, len(data), size):
        yield data[i: i+size]


def camel_to_snake(name) -> str:
    pattern1 = re.compile(r'(\s+)')
    pattern2 = re.compile(r'([^_])([A-Z][a-z]+)')
    pattern3 = re.compile(r'([a-z0-9])([A-Z])')
    name = pattern1.sub('_', name.strip())
    name = pattern2.sub(r'\1_\2', name)
    return pattern3.sub(r'\1_\2', name).lower()


def map_dataframe_columns(df: pd.DataFrame,  mappings: Dict[str, str]) -> pd.DataFrame:
    return df.rename(columns=mappings)


def is_valid_email(email: str) -> bool:
    regex = re.compile(
        r'([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)


def is_valid_email_list(email_list: str) -> bool:
    for email in email_list.split(';'):
        email = email.strip()
        if email and not is_valid_email(email):
            return False
    return True


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer


def str_to_date(dt: str) -> datetime:
    return datetime.strptime(dt, '%Y-%m-%d')


def solr_format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def output_format_date(dt: datetime) -> str:
    return dt.strftime("%m/%d/%Y")


def add_lists(*lists):
    """
    This function adds an arbitrary number of lists element-wise, padding the shorter lists with zeros if necessary.

    Parameters:
    *lists (List[int]): The lists to add.

    Returns:
    List[int]: The element-wise sum of the input lists.

    Example:
    >>> add_lists([1, 2, 3, 4], [3, 2, 2], [0, 0, 1, 1])
    [4, 4, 6, 5]
    """
    if len(lists) != 0:
        length = max(len(l) for l in lists)
        padded_lists = [l + [0] * (length - len(l)) for l in lists]
        result = np.sum(padded_lists, axis=0).tolist()
        return result
    return list()
