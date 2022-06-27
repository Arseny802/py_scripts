import os
from datetime import datetime

from common.log import get_logger
from kns_shop_listener.record import Record, ComputerComponents

stat_file = "kns_shop_stat__computer.csv"
encoding = 'UTF-8'


def log():
    return get_logger('stat_file', 'kns_shop_listener')


def stat_file_backup():
    old_stat_file = stat_file + '.old_' + str(datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.rename(stat_file, old_stat_file)


def stat_file_create():
    header = str()
    for component in ComputerComponents:
        header += component.name + ';'
    header += 'summary;timestamp\n'

    if os.path.exists(stat_file):
        with open(stat_file, 'r', encoding=encoding) as current_file:
            first_line: str = current_file.readline()
        need_rewrite = first_line != header
        log().info(f"File '{stat_file}' exists, headers are {'not ' if need_rewrite else ''}equal.")
        if not need_rewrite:
            return False
        stat_file_backup()

    with open(stat_file, 'a', encoding=encoding) as new_file:
        new_file.write(header)
    return True


def stat_file_read_record():
    record = Record()
    with open(stat_file, 'rb') as current_file:
        try:  # catch OSError in case of a one line file
            current_file.seek(0, os.SEEK_END)
            while current_file.read(1) != b'\n':
                current_file.seek(-2, os.SEEK_CUR)
        except OSError as exception:
            log().error(exception)
            current_file.seek(0)
            return record
        last_line = current_file.readline().decode(encoding)

    index = 0
    prices = last_line.split(';')
    if len(prices) < len(ComputerComponents):
        return record

    for component in ComputerComponents:
        try:
            record.add(component, int(prices[index]))
        except Exception as ex:
            log().error(f"On adding {index} price in '{last_line}' "
                        f"of '{component}' occurred exception: {ex}")
        index += 1
    return record


def stat_file_write_record(record: Record):
    with open(stat_file, 'a', encoding=encoding) as current_file:
        current_file.write(record.to_string() + '\n')

