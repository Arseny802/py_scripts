from kns_loader import download_record
from stat_file import stat_file_create, stat_file_read_record, stat_file_write_record
import common


def setup_loggers():
    common.log.all_loggers['kns_loader'] = common.log.DailyLogger(
        'kns_loader', 'kns_shop_listener.log', backup_count=90)
    common.log.all_loggers['main'] = common.log.DailyLogger(
        'main', 'kns_shop_listener.log', backup_count=90)
    common.log.all_loggers['record'] = common.log.DailyLogger(
        'record', 'kns_shop_listener.log', backup_count=90)
    common.log.all_loggers['stat_file'] = common.log.DailyLogger(
        'stat_file', 'kns_shop_listener.log', backup_count=90)


def log():
    return common.log.get_logger('main', 'kns_shop_listener')


def main():
    setup_loggers()
    log().info('Application started')
    stat_file_create()

    record_last = stat_file_read_record()
    log().debug(f"Last record: {record_last.to_string()}")

    record_new = download_record()
    log().debug(f"New record:  {record_new.to_string()}")

    if not record_last.equal(record_new):
        log().info("Last record and downloaded are not equal. Writing new data...")
        stat_file_write_record(record_new)
    else:
        log().info("Last record and downloaded are equal. No changes to write.")
    log().info("Application finished")


if __name__ == "__main__":
    main()
